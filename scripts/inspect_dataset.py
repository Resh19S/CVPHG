"""
Catalog whatever is actually present in /data before anything else runs.

Reports: class labels found (from manifest.csv, if present), per-class clip
counts, resolution/duration per file, and which target IDs (from
data/annotations/target_ids.txt, if present) are missing on disk.

Run this FIRST -- it never assumes the full pipeline has been run yet and
degrades gracefully if manifest/target files don't exist.
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.frame_extraction import get_video_metadata

REPO_ROOT = Path(__file__).resolve().parent.parent
VIDEOS_DIR = REPO_ROOT / "data" / "videos"
MANIFEST_PATH = REPO_ROOT / "data" / "manifest.csv"
TARGET_IDS_PATH = REPO_ROOT / "data" / "annotations" / "target_ids.txt"

VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}


def find_video_files() -> dict[str, Path]:
    """Map video_id (filename stem) -> path, for every video file on disk."""
    if not VIDEOS_DIR.exists():
        return {}
    files = {}
    for p in VIDEOS_DIR.iterdir():
        if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS:
            files[p.stem] = p
    return files


def load_manifest() -> list[dict]:
    if not MANIFEST_PATH.exists():
        return []
    with open(MANIFEST_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_target_ids() -> list[str]:
    if not TARGET_IDS_PATH.exists():
        return []
    return [line.strip() for line in TARGET_IDS_PATH.read_text().splitlines() if line.strip()]


def main():
    print("=" * 70)
    print("DATASET INSPECTION")
    print("=" * 70)

    on_disk = find_video_files()
    manifest = load_manifest()
    target_ids = load_target_ids()

    print(f"\nVideos directory : {VIDEOS_DIR}")
    print(f"Files found on disk        : {len(on_disk)}")
    print(f"Manifest entries (expected): {len(manifest)}")
    print(f"Target IDs (from selection): {len(target_ids)}")

    # --- per-class counts, from manifest joined against what's on disk ---
    if manifest:
        by_class: dict[str, list[dict]] = {}
        for row in manifest:
            by_class.setdefault(row["label"], []).append(row)

        print("\n--- Per-class clip counts (manifest vs. present on disk) ---")
        print(f"{'class':<12}{'expected':<10}{'present':<10}")
        for class_name, rows in sorted(by_class.items()):
            present = sum(1 for r in rows if r["id"] in on_disk)
            print(f"{class_name:<12}{len(rows):<10}{present:<10}")
    else:
        print("\n[inspect_dataset] No manifest.csv found -- run scripts/select_subset.py first.")

    # --- missing files vs target ID list ---
    if target_ids:
        missing = [vid for vid in target_ids if vid not in on_disk]
        print(f"\n--- Missing files vs. target ID list ---")
        print(f"Missing: {len(missing)}/{len(target_ids)}")
        if missing:
            preview = missing[:10]
            print("  " + "\n  ".join(preview))
            if len(missing) > 10:
                print(f"  ... and {len(missing) - 10} more")

    # --- per-file metadata for whatever IS present ---
    if on_disk:
        print("\n--- Present files: resolution / duration ---")
        print(f"{'id':<20}{'resolution':<14}{'duration(s)':<14}{'fps':<8}")
        for video_id, path in sorted(on_disk.items()):
            try:
                meta = get_video_metadata(path)
                res = f"{meta['width']}x{meta['height']}"
                print(f"{video_id:<20}{res:<14}{meta['duration_sec']:<14.2f}{meta['fps']:<8.1f}")
            except Exception as exc:
                print(f"{video_id:<20}ERROR reading metadata: {exc}")
    else:
        print("\n[inspect_dataset] No video files found in data/videos/.")
        print("[inspect_dataset] Run scripts/select_subset.py, fetch the target clips,")
        print("[inspect_dataset] or generate dummy clips for a scaffold test run.")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
