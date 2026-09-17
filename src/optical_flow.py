"""
Sparse Lucas-Kanade optical flow over a deterministic sequence of frames.

Tracks a fixed set of "good features to track" (Shi-Tomasi corners) across
consecutive frames via cv2.calcOpticalFlowPyrLK, and derives simple scalar
motion features per frame pair (mean/max flow magnitude, mean flow angle,
tracked/lost point counts). This module only computes motion features -- it
does not classify anything; a future classifier (e.g. an LSTM over this
feature sequence, echoing the original stampede paper's approach) consumes
its output.

Sparse (Lucas-Kanade), not dense (Farneback) -- deliberately different from
the prior published paper's Farneback-based feature vector. See
docs/roadmap.md for why this is being tried as an alternative signal.
"""

from pathlib import Path

import cv2
import numpy as np

from src.config import (
    LK_CRITERIA_COUNT,
    LK_CRITERIA_EPS,
    LK_FEATURE_PARAMS,
    LK_MAX_LEVEL,
    LK_WIN_SIZE,
)


def _lk_params() -> dict:
    return dict(
        winSize=LK_WIN_SIZE,
        maxLevel=LK_MAX_LEVEL,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, LK_CRITERIA_COUNT, LK_CRITERIA_EPS),
    )


def load_frames_gray(frame_paths: list[Path]) -> list[np.ndarray]:
    """Load a sequence of frame image files as grayscale arrays, in order."""
    frames = []
    for p in frame_paths:
        img = cv2.imread(str(p), cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise IOError(f"Could not read frame image: {p}")
        frames.append(img)
    return frames


def compute_lk_flow(frames_gray: list[np.ndarray]) -> list[dict]:
    """
    frames_gray: consecutive grayscale frames in temporal order (see
    src/frame_extraction.extract_frames_to_dir + load_frames_gray).

    Returns one dict per consecutive frame pair (len = len(frames_gray) - 1):
    {frame_idx, num_tracked, num_lost, mean_magnitude, max_magnitude, mean_angle_deg}
    `frame_idx` is the index of the *later* frame in each pair.
    """
    if len(frames_gray) < 2:
        raise ValueError("Need at least 2 frames to compute optical flow.")

    results = []
    prev_gray = frames_gray[0]
    prev_pts = cv2.goodFeaturesToTrack(prev_gray, mask=None, **LK_FEATURE_PARAMS)

    for i in range(1, len(frames_gray)):
        curr_gray = frames_gray[i]

        if prev_pts is None or len(prev_pts) == 0:
            # Re-seed if every tracked point has been lost, so a dropout
            # doesn't silently zero out the rest of the clip's flow.
            prev_pts = cv2.goodFeaturesToTrack(prev_gray, mask=None, **LK_FEATURE_PARAMS)

        if prev_pts is None or len(prev_pts) == 0:
            results.append(dict(
                frame_idx=i, num_tracked=0, num_lost=0,
                mean_magnitude=0.0, max_magnitude=0.0, mean_angle_deg=0.0,
            ))
            prev_gray = curr_gray
            continue

        next_pts, status, _err = cv2.calcOpticalFlowPyrLK(
            prev_gray, curr_gray, prev_pts, None, **_lk_params()
        )

        status = status.reshape(-1)
        good_prev = prev_pts.reshape(-1, 2)[status == 1]
        good_next = next_pts.reshape(-1, 2)[status == 1]
        num_tracked = len(good_next)
        num_lost = int((status == 0).sum())

        if num_tracked > 0:
            flow_vecs = good_next - good_prev
            magnitudes = np.linalg.norm(flow_vecs, axis=1)
            angles = np.degrees(np.arctan2(flow_vecs[:, 1], flow_vecs[:, 0])) % 360
            mean_magnitude = float(magnitudes.mean())
            max_magnitude = float(magnitudes.max())
            mean_angle_deg = float(angles.mean())
        else:
            mean_magnitude = max_magnitude = mean_angle_deg = 0.0

        results.append(dict(
            frame_idx=i, num_tracked=num_tracked, num_lost=num_lost,
            mean_magnitude=mean_magnitude, max_magnitude=max_magnitude, mean_angle_deg=mean_angle_deg,
        ))

        prev_gray = curr_gray
        prev_pts = good_next.reshape(-1, 1, 2).astype(np.float32) if num_tracked > 0 else None

    return results


def summarize_flow(flow_records: list[dict]) -> dict:
    """Collapse a clip's per-frame-pair flow records into scalar summary
    stats -- a first-pass feature vector for a per-clip classifier."""
    if not flow_records:
        return dict(mean_magnitude=0.0, max_magnitude=0.0, mean_angle_deg=0.0,
                     mean_tracked=0.0, frame_pairs=0)
    mags = [r["mean_magnitude"] for r in flow_records]
    max_mags = [r["max_magnitude"] for r in flow_records]
    angles = [r["mean_angle_deg"] for r in flow_records]
    tracked = [r["num_tracked"] for r in flow_records]
    return dict(
        mean_magnitude=float(np.mean(mags)),
        max_magnitude=float(np.max(max_mags)),
        mean_angle_deg=float(np.mean(angles)),
        mean_tracked=float(np.mean(tracked)),
        frame_pairs=len(flow_records),
    )
