"""
CLIP zero-shot classifier for crowd video clips.

Loads a pretrained CLIP checkpoint via open_clip (no fine-tuning), embeds
text prompts per class (src/config.CLASS_PROMPTS) and extracted video frames,
then classifies each clip by mean cosine similarity between its frame
embeddings and each class's (mean) text embedding.

Runs unmodified on CPU (local) or GPU (Colab) -- device is auto-detected.
"""

from dataclasses import dataclass, field

import numpy as np
import open_clip
import torch
import torch.nn.functional as F
from PIL import Image

from src.config import CLASS_PROMPTS, CLIP_MODEL_NAME, CLIP_PRETRAINED, NUM_FRAMES_PER_CLIP
from src.frame_extraction import extract_frames


@dataclass
class ClipPrediction:
    video_id: str
    video_path: str
    predicted_label: str
    confidence: float
    class_scores: dict = field(default_factory=dict)
    num_frames_used: int = 0
    error: str | None = None


class ZeroShotRiotClassifier:
    def __init__(
        self,
        class_prompts: dict[str, list[str]] = None,
        model_name: str = CLIP_MODEL_NAME,
        pretrained: str = CLIP_PRETRAINED,
        device: str | None = None,
    ):
        self.class_prompts = class_prompts or CLASS_PROMPTS
        self.class_names = list(self.class_prompts.keys())

        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"[clip] loading {model_name} ({pretrained}) on device={self.device}")

        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            model_name, pretrained=pretrained, force_quick_gelu=True
        )
        self.tokenizer = open_clip.get_tokenizer(model_name)
        self.model.to(self.device)
        self.model.eval()

        self.text_embeddings = self._embed_class_prompts()

    @torch.no_grad()
    def _embed_class_prompts(self) -> dict[str, torch.Tensor]:
        """Embed all prompts per class and mean-pool into one vector per class."""
        embeddings = {}
        for class_name, prompts in self.class_prompts.items():
            tokens = self.tokenizer(prompts).to(self.device)
            feats = self.model.encode_text(tokens)
            feats = F.normalize(feats, dim=-1)
            class_vec = feats.mean(dim=0)
            class_vec = F.normalize(class_vec, dim=0)
            embeddings[class_name] = class_vec
        return embeddings

    @torch.no_grad()
    def _embed_frames(self, frames: list[np.ndarray]) -> torch.Tensor:
        images = [self.preprocess(Image.fromarray(f)) for f in frames]
        batch = torch.stack(images).to(self.device)
        feats = self.model.encode_image(batch)
        feats = F.normalize(feats, dim=-1)
        return feats

    @torch.no_grad()
    def classify_clip(
        self, video_path: str, video_id: str | None = None, num_frames: int = NUM_FRAMES_PER_CLIP
    ) -> ClipPrediction:
        video_id = video_id or video_path
        try:
            frames = extract_frames(video_path, num_frames=num_frames)
        except Exception as exc:
            return ClipPrediction(
                video_id=video_id,
                video_path=video_path,
                predicted_label="ERROR",
                confidence=0.0,
                error=str(exc),
            )

        frame_embeds = self._embed_frames(frames)  # (num_frames, dim)

        class_scores = {}
        for class_name, text_vec in self.text_embeddings.items():
            sims = frame_embeds @ text_vec  # cosine sim per frame, (num_frames,)
            class_scores[class_name] = float(sims.mean().item())

        # Softmax over class mean-similarities gives an interpretable confidence.
        scores_tensor = torch.tensor([class_scores[c] for c in self.class_names])
        probs = F.softmax(scores_tensor / 0.01, dim=0)  # temperature-scaled like CLIP logit_scale
        pred_idx = int(torch.argmax(probs).item())

        return ClipPrediction(
            video_id=video_id,
            video_path=video_path,
            predicted_label=self.class_names[pred_idx],
            confidence=float(probs[pred_idx].item()),
            class_scores=class_scores,
            num_frames_used=len(frames),
        )

    def classify_clips(self, video_paths: list[str], video_ids: list[str] = None) -> list[ClipPrediction]:
        video_ids = video_ids or video_paths
        results = []
        for i, (path, vid) in enumerate(zip(video_paths, video_ids), 1):
            print(f"[classify] ({i}/{len(video_paths)}) {vid}")
            results.append(self.classify_clip(path, video_id=vid))
        return results
