"""
Deterministic, evenly-spaced frame extraction from a video file via OpenCV.

No randomness is involved in which frames are picked -- frame indices are a
fixed linspace over the clip's total frame count, so the same video always
yields the same frames regardless of machine or run.
"""

from pathlib import Path

import cv2
import numpy as np

from src.config import FRAME_SIZE, NUM_FRAMES_PER_CLIP


def get_video_metadata(video_path: str) -> dict:
    """Return basic metadata (fps, frame_count, duration_sec, width, height)."""
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise IOError(f"Could not open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 0.0
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration_sec = (frame_count / fps) if fps > 0 else 0.0
    cap.release()

    return {
        "fps": fps,
        "frame_count": frame_count,
        "duration_sec": duration_sec,
        "width": width,
        "height": height,
    }


def extract_frames(
    video_path: str,
    num_frames: int = NUM_FRAMES_PER_CLIP,
    resize: int = FRAME_SIZE,
) -> list[np.ndarray]:
    """
    Extract `num_frames` evenly-spaced frames from `video_path`.

    Returns a list of RGB numpy arrays of shape (resize, resize, 3).
    Sampling is deterministic: indices = round(linspace(0, frame_count-1, num_frames)).
    """
    video_path = str(video_path)
    if not Path(video_path).exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Could not open video: {video_path}")

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_count <= 0:
        cap.release()
        raise ValueError(f"Video has no readable frames: {video_path}")

    if num_frames > frame_count:
        num_frames = frame_count

    indices = np.linspace(0, frame_count - 1, num_frames)
    indices = np.round(indices).astype(int)
    indices = np.unique(indices)  # guard against duplicate rounding on very short clips

    frames = []
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(idx))
        ok, frame_bgr = cap.read()
        if not ok:
            continue
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.resize(frame_rgb, (resize, resize), interpolation=cv2.INTER_AREA)
        frames.append(frame_rgb)

    cap.release()

    if not frames:
        raise ValueError(f"Failed to extract any frames from: {video_path}")

    return frames
