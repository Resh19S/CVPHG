"""
Run zero-shot classification over the manifest's present clips and evaluate
against ground-truth labels: accuracy, per-class precision/recall, confusion
matrix. Writes /results/riot_zeroshot_baseline.md and raw predictions CSV.
"""

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.config import TARGET_CLASSES, set_seed
from src.zero_shot_classifier import ZeroShotRiotClassifier

DEFAULT_MANIFEST_PATH = REPO_ROOT / "data" / "manifest.csv"
RESULTS_DIR = REPO_ROOT / "results"


def load_manifest_present(manifest_path: Path) -> list[dict]:
    if not manifest_path.exists():
        raise SystemExit(
            f"[evaluate] No manifest at {manifest_path}. Run scripts/select_subset.py first."
        )
    rows = []
    with open(manifest_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if Path(row["filepath"]).exists():
                rows.append(row)
    return rows


def compute_confusion_matrix(y_true: list[str], y_pred: list[str], classes: list[str]) -> dict:
    matrix = {t: {p: 0 for p in classes} for t in classes}
    for t, p in zip(y_true, y_pred):
        if t in matrix and p in matrix[t]:
            matrix[t][p] += 1
    return matrix


def compute_precision_recall(matrix: dict, classes: list[str]) -> dict:
    metrics = {}
    for c in classes:
        tp = matrix[c][c]
        fn = sum(matrix[c][p] for p in classes if p != c)
        fp = sum(matrix[t][c] for t in classes if t != c)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
        metrics[c] = {"precision": precision, "recall": recall, "f1": f1, "support": tp + fn}
    return metrics


def write_markdown_report(
    predictions: list[dict],
    y_true: list[str],
    y_pred: list[str],
    classes: list[str],
    out_path: Path,
    title: str = "Riot Zero-Shot Baseline Results",
    note: str | None = None,
):
    n = len(y_true)
    accuracy = sum(1 for t, p in zip(y_true, y_pred) if t == p) / n if n > 0 else 0.0
    matrix = compute_confusion_matrix(y_true, y_pred, classes)
    metrics = compute_precision_recall(matrix, classes)

    lines = []
    lines.append(f"# {title}\n")
    lines.append(
        "Zero-shot CLIP (ViT-B-32, openai weights) classification of riot vs. "
        "negative-class clips. No fine-tuning. See README.md for scope and "
        "limitations.\n"
    )
    if note:
        lines.append(f"> {note}\n")
    lines.append(f"**Clips evaluated:** {n}  \n**Overall accuracy:** {accuracy:.2%}\n")

    lines.append("## Per-class precision / recall / F1\n")
    lines.append("| class | precision | recall | f1 | support |")
    lines.append("|---|---|---|---|---|")
    for c in classes:
        m = metrics[c]
        lines.append(
            f"| {c} | {m['precision']:.2f} | {m['recall']:.2f} | {m['f1']:.2f} | {m['support']} |"
        )
    lines.append("")

    lines.append("## Confusion matrix (rows = true label, cols = predicted)\n")
    header = "| true \\ pred | " + " | ".join(classes) + " |"
    sep = "|---|" + "|".join(["---"] * len(classes)) + "|"
    lines.append(header)
    lines.append(sep)
    for t in classes:
        row = " | ".join(str(matrix[t][p]) for p in classes)
        lines.append(f"| {t} | {row} |")
    lines.append("")

    lines.append("## Per-clip predictions\n")
    lines.append("| id | true label | predicted | confidence | correct |")
    lines.append("|---|---|---|---|---|")
    for pred in predictions:
        correct = "yes" if pred["true_label"] == pred["predicted_label"] else "no"
        lines.append(
            f"| {pred['video_id']} | {pred['true_label']} | {pred['predicted_label']} | "
            f"{pred['confidence']:.3f} | {correct} |"
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    set_seed()

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--num-frames", type=int, default=8)
    parser.add_argument(
        "--manifest",
        type=str,
        default=str(DEFAULT_MANIFEST_PATH),
        help="Path to the id,label,filepath manifest CSV to evaluate.",
    )
    parser.add_argument(
        "--output-name",
        type=str,
        default="riot_zeroshot_baseline",
        help="Basename (no extension) for results/<name>.md and results/<name>_predictions.csv.",
    )
    parser.add_argument(
        "--report-title",
        type=str,
        default="Riot Zero-Shot Baseline Results",
        help="Title line for the markdown report.",
    )
    parser.add_argument(
        "--report-note",
        type=str,
        default=None,
        help="Optional callout note (e.g. dataset-proxy caveat) inserted near the top of the report.",
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    rows = load_manifest_present(manifest_path)
    if not rows:
        raise SystemExit(
            f"[evaluate] No manifest rows in {manifest_path} point to files present on disk. "
            "Run scripts/inspect_dataset.py to check what's missing, or "
            "scripts/make_dummy_videos.py for a scaffold test run."
        )

    print(f"[evaluate] Evaluating {len(rows)} clips present on disk.")

    classifier = ZeroShotRiotClassifier()
    predictions_raw = classifier.classify_clips(
        video_paths=[r["filepath"] for r in rows],
        video_ids=[r["id"] for r in rows],
    )

    predictions = []
    y_true, y_pred = [], []
    for row, pred in zip(rows, predictions_raw):
        if pred.error:
            print(f"[evaluate] WARNING: {pred.video_id} failed: {pred.error}")
            continue
        predictions.append(
            {
                "video_id": pred.video_id,
                "true_label": row["label"],
                "predicted_label": pred.predicted_label,
                "confidence": pred.confidence,
                **{f"score_{c}": pred.class_scores.get(c, "") for c in TARGET_CLASSES},
            }
        )
        y_true.append(row["label"])
        y_pred.append(pred.predicted_label)

    if not predictions:
        raise SystemExit("[evaluate] All clips failed classification -- nothing to evaluate.")

    RESULTS_DIR.mkdir(exist_ok=True)
    csv_path = RESULTS_DIR / f"{args.output_name}_predictions.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["video_id", "true_label", "predicted_label", "confidence"] + [
            f"score_{c}" for c in TARGET_CLASSES
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(predictions)
    print(f"[evaluate] Wrote raw predictions -> {csv_path}")

    md_path = RESULTS_DIR / f"{args.output_name}.md"
    write_markdown_report(
        predictions,
        y_true,
        y_pred,
        TARGET_CLASSES,
        md_path,
        title=args.report_title,
        note=args.report_note,
    )
    print(f"[evaluate] Wrote markdown report -> {md_path}")

    accuracy = sum(1 for t, p in zip(y_true, y_pred) if t == p) / len(y_true)
    print(f"[evaluate] Overall accuracy: {accuracy:.2%}")


if __name__ == "__main__":
    main()
