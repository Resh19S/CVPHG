"""
Parse the XD-Violence annotation file and select a target subset:
riot + negative classes defined in src/config.TARGET_CLASSES.

This script does NOT scripted-download the annotation file itself -- the
official XD-Violence release (https://roc-ng.github.io/XD-Violence/) gates
downloads behind a request form / OneDrive links rather than a stable public
URL, so we can't reliably script that fetch. Grab the annotation file
manually per the project README and pass its path with --annotation-file.

Supports two annotation formats, auto-detected per line:

  1. Simple CSV/TSV:            video_id,label            (or tab-separated)
  2. XD-Violence label codes:   video_id  B4-0-100-0-0     (whitespace-sep,
                                 first token after the id is the label code,
                                 mapped via src.config.XD_VIOLENCE_LABEL_CODES)

Outputs:
  data/annotations/target_ids.txt   -- one video_id per line
  data/manifest.csv                 -- id,label,filepath (filepath populated
                                        later by inspect_dataset.py once the
                                        actual files are present)
"""

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.config import TARGET_CLASSES, XD_VIOLENCE_LABEL_CODES, set_seed


def parse_annotation_line(line: str) -> tuple[str, str] | None:
    """Return (video_id, our_class_name) or None if unparseable / not a target class."""
    line = line.strip()
    if not line:
        return None

    # CSV/TSV: "video_id,label" or "video_id\tlabel"
    if "," in line:
        parts = [p.strip() for p in line.split(",")]
    else:
        parts = line.split()

    if len(parts) < 2:
        return None

    video_id, raw_label = parts[0], parts[1]

    # Direct match against our own class names (already-normalized CSV input)
    if raw_label.lower() in TARGET_CLASSES:
        return video_id, raw_label.lower()

    # XD-Violence label-code style, e.g. "B4-0-100-0-0" or "B4"
    code = raw_label.split("-")[0]
    if code in XD_VIOLENCE_LABEL_CODES:
        return video_id, XD_VIOLENCE_LABEL_CODES[code]

    return None


def select_subset(annotation_file: Path, max_per_class: int) -> list[tuple[str, str]]:
    selected: dict[str, list[str]] = {c: [] for c in TARGET_CLASSES}

    with open(annotation_file, "r", encoding="utf-8") as f:
        for line in f:
            parsed = parse_annotation_line(line)
            if parsed is None:
                continue
            video_id, class_name = parsed
            if class_name in selected and len(selected[class_name]) < max_per_class:
                selected[class_name].append(video_id)

    rows = []
    for class_name, ids in selected.items():
        for vid in ids:
            rows.append((vid, class_name))
    return rows


def main():
    set_seed()

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--annotation-file",
        type=str,
        default=str(REPO_ROOT / "data" / "annotations" / "xd_violence_annotations.txt"),
        help="Path to a manually-downloaded XD-Violence annotation file.",
    )
    parser.add_argument(
        "--max-per-class",
        type=int,
        default=5,
        help="Max video IDs to select per target class (kept small for the CPU scaffold pass).",
    )
    args = parser.parse_args()

    annotation_path = Path(args.annotation_file)
    if not annotation_path.exists():
        print(f"[select_subset] Annotation file not found: {annotation_path}")
        print("[select_subset] Download it manually from https://roc-ng.github.io/XD-Violence/")
        print("[select_subset] and pass its path via --annotation-file.")
        raise SystemExit(1)

    rows = select_subset(annotation_path, args.max_per_class)

    if not rows:
        print("[select_subset] No matching rows found for target classes:", TARGET_CLASSES)
        print("[select_subset] Check that XD_VIOLENCE_LABEL_CODES in src/config.py matches")
        print("[select_subset] the label-code scheme actually used in the downloaded file.")
        raise SystemExit(1)

    out_ids = REPO_ROOT / "data" / "annotations" / "target_ids.txt"
    out_ids.parent.mkdir(parents=True, exist_ok=True)
    with open(out_ids, "w", encoding="utf-8") as f:
        for vid, _ in rows:
            f.write(f"{vid}\n")

    manifest_path = REPO_ROOT / "data" / "manifest.csv"
    videos_dir = REPO_ROOT / "data" / "videos"
    with open(manifest_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "label", "filepath"])
        for vid, label in rows:
            # filepath is a guess (video files aren't fetched by this script);
            # inspect_dataset.py reconciles this against what's actually on disk.
            writer.writerow([vid, label, str(videos_dir / f"{vid}.mp4")])

    print(f"[select_subset] Selected {len(rows)} clips across {len(TARGET_CLASSES)} classes.")
    for class_name in TARGET_CLASSES:
        count = sum(1 for _, l in rows if l == class_name)
        print(f"  {class_name:10s}: {count}")
    print(f"[select_subset] Wrote target ID list -> {out_ids}")
    print(f"[select_subset] Wrote manifest       -> {manifest_path}")


if __name__ == "__main__":
    main()
