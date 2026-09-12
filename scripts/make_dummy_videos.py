"""
Generate small synthetic dummy video clips + a matching manifest, so the
full pipeline (inspect -> classify -> evaluate) is actually runnable
end-to-end tonight, without the real XD-Violence files.

THESE ARE NOT REAL DATA. They are synthetic OpenCV-drawn clips that loosely
caricature each class (e.g. "riot" = many jittering random shapes simulating
a chaotic crowd; "normal" = one or two calmly moving shapes) purely so the
pipeline mechanics and CLIP inference path can be validated. Any accuracy
number produced against these dummy clips is meaningless as a research
result -- it only demonstrates the code runs. Real results require the real
XD-Violence subset (see scripts/select_subset.py + README.md).
"""

import csv
import sys
from pathlib import Path

import cv2
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.config import set_seed

VIDEOS_DIR = REPO_ROOT / "data" / "videos"
MANIFEST_PATH = REPO_ROOT / "data" / "manifest.csv"

FPS = 10
DURATION_SEC = 2
WIDTH, HEIGHT = 320, 240

DUMMY_CLIPS = [
    ("dummy_riot_01", "riot"),
    ("dummy_riot_02", "riot"),
    ("dummy_normal_01", "normal"),
    ("dummy_normal_02", "normal"),
    ("dummy_fighting_01", "fighting"),
    ("dummy_fighting_02", "fighting"),
]


def make_frame(label: str, frame_idx: int, rng: np.random.Generator) -> np.ndarray:
    frame = np.full((HEIGHT, WIDTH, 3), 30, dtype=np.uint8)  # dark background

    if label == "riot":
        num_shapes = 25
        for _ in range(num_shapes):
            x, y = rng.integers(0, WIDTH), rng.integers(0, HEIGHT)
            r = rng.integers(4, 10)
            color = tuple(int(c) for c in rng.integers(100, 255, size=3))
            cv2.circle(frame, (x, y), r, color, -1)
    elif label == "fighting":
        num_shapes = 4
        for i in range(num_shapes):
            cx = WIDTH // 2 + (i - num_shapes / 2) * 20
            cx += int(10 * np.sin(frame_idx * 0.8 + i))
            cy = HEIGHT // 2 + int(15 * np.cos(frame_idx * 0.8 + i))
            color = (0, 0, 220) if i % 2 == 0 else (220, 0, 0)
            cv2.circle(frame, (int(cx), int(cy)), 12, color, -1)
    else:  # normal
        cx = int(WIDTH * 0.2 + (WIDTH * 0.6) * (frame_idx / (FPS * DURATION_SEC)))
        cy = HEIGHT // 2
        cv2.circle(frame, (cx, cy), 10, (0, 200, 0), -1)

    return frame


def write_dummy_video(path: Path, label: str, seed: int):
    rng = np.random.default_rng(seed)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(path), fourcc, FPS, (WIDTH, HEIGHT))
    for frame_idx in range(FPS * DURATION_SEC):
        frame = make_frame(label, frame_idx, rng)
        writer.write(frame)
    writer.release()


def main():
    seed = set_seed()

    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

    rows = []
    for i, (video_id, label) in enumerate(DUMMY_CLIPS):
        path = VIDEOS_DIR / f"{video_id}.mp4"
        write_dummy_video(path, label, seed=seed + i)
        rows.append((video_id, label, str(path)))
        print(f"[make_dummy_videos] wrote {path} (label={label})")

    with open(MANIFEST_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "label", "filepath"])
        writer.writerows(rows)

    print(f"[make_dummy_videos] Wrote manifest -> {MANIFEST_PATH}")
    print("[make_dummy_videos] NOTE: these are synthetic placeholder clips, not real data.")


if __name__ == "__main__":
    main()
