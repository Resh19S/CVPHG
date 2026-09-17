"""
Preprocessing pipeline: video -> frames on disk -> sparse Lucas-Kanade
optical flow features.

For each clip in a manifest CSV (id,label,filepath): dumps its frames as
JPEGs under data/frames/<id>/, computes per-frame-pair LK flow, writes
data/optical_flow/<id>.csv (per-frame-pair records) plus one summary row per
clip into results/<output-name>_summary.csv.

This only produces motion features -- it does not classify anything.
"""

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.config import LK_FRAME_SIZE, LK_FRAME_STRIDE, set_seed
from src.frame_extraction import extract_frames_to_dir
from src.optical_flow import compute_lk_flow, load_frames_gray, summarize_flow

DEFAULT_MANIFEST_PATH = REPO_ROOT / "data" / "manifest.csv"
FRAMES_DIR = REPO_ROOT / "data" / "frames"
FLOW_DIR = REPO_ROOT / "data" / "optical_flow"
RESULTS_DIR = REPO_ROOT / "results"


def load_manifest_present(manifest_path: Path) -> list[dict]:
    if not manifest_path.exists():
        raise SystemExit(f"[preprocess] No manifest at {manifest_path}.")
    rows = []
    with open(manifest_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if Path(row["filepath"]).exists():
                rows.append(row)
    return rows


def process_clip(video_id: str, video_path: str, stride: int, frame_size: int) -> dict:
    frame_out_dir = FRAMES_DIR / video_id
    frame_paths = extract_frames_to_dir(video_path, frame_out_dir, stride=stride, resize=frame_size)

    frames_gray = load_frames_gray(frame_paths)
    flow_records = compute_lk_flow(frames_gray)

    FLOW_DIR.mkdir(parents=True, exist_ok=True)
    clip_flow_csv = FLOW_DIR / f"{video_id}.csv"
    with open(clip_flow_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["frame_idx", "num_tracked", "num_lost", "mean_magnitude", "max_magnitude", "mean_angle_deg"]
        )
        writer.writeheader()
        writer.writerows(flow_records)

    summary = summarize_flow(flow_records)
    summary["video_id"] = video_id
    summary["num_frames_extracted"] = len(frame_paths)
    return summary


def main():
    set_seed()

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=str, default=str(DEFAULT_MANIFEST_PATH))
    parser.add_argument("--stride", type=int, default=LK_FRAME_STRIDE)
    parser.add_argument("--frame-size", type=int, default=LK_FRAME_SIZE)
    parser.add_argument("--output-name", type=str, default="optical_flow_lk")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    rows = load_manifest_present(manifest_path)
    if not rows:
        raise SystemExit(
            f"[preprocess] No manifest rows in {manifest_path} point to files present on disk."
        )

    print(f"[preprocess] Processing {len(rows)} clips (stride={args.stride}, frame_size={args.frame_size}).")

    summaries = []
    for i, row in enumerate(rows, 1):
        print(f"[preprocess] ({i}/{len(rows)}) {row['id']}")
        try:
            summary = process_clip(row["id"], row["filepath"], args.stride, args.frame_size)
            summary["label"] = row["label"]
            summaries.append(summary)
        except Exception as exc:
            print(f"[preprocess] WARNING: {row['id']} failed: {exc}")

    if not summaries:
        raise SystemExit("[preprocess] All clips failed -- nothing to write.")

    RESULTS_DIR.mkdir(exist_ok=True)
    summary_csv = RESULTS_DIR / f"{args.output_name}_summary.csv"
    with open(summary_csv, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "video_id", "label", "num_frames_extracted", "frame_pairs",
            "mean_magnitude", "max_magnitude", "mean_angle_deg", "mean_tracked",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summaries)

    print(f"[preprocess] Wrote per-clip flow summary -> {summary_csv}")
    print(f"[preprocess] Wrote per-clip frame images -> {FRAMES_DIR}/<id>/")
    print(f"[preprocess] Wrote per-clip per-frame-pair flow -> {FLOW_DIR}/<id>.csv")


if __name__ == "__main__":
    main()
