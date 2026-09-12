# Riot/Protest Zero-Shot CLIP Baseline

## Project context

This scaffold is part of a larger research collaboration under PI Geetanjali
Bhola (University of Delhi, Faculty of Technology), extending a previously
published stampede-detection paper (CNN-LSTM + Farneback optical flow,
*Scientific Reports*, 2026) that classified crowd states into a 4-class risk
taxonomy using hand-crafted motion features. The new project phase moves
toward multimodal zero-shot learning (ZSL) for crowd analysis, eventually
adding audio as a second modality and connecting to group-activity-recognition
literature, with a longer-term dataset plan involving real-world protest
footage (anonymization/ethics handled separately, out of scope here). One idea
that got traction: fire/burning-vehicle events during protests can act as a
*leading indicator* of escalation, tying into the same "anticipate before full
crowd panic" logic as the original stampede work — but the team has directed
that riot/protest detection be perfected **first**, with fire added as a
second phase later without refactoring. This repo is that first phase: a
zero-shot CLIP baseline for detecting riot/protest-type crowd behavior on the
XD-Violence dataset, using text prompts only, no fine-tuning.

## What this scaffold does and does NOT do

**Does:**
- Zero-shot classification of short video clips into `riot` / `normal` /
  `fighting` using a pretrained, un-fine-tuned CLIP model (ViT-B-32, openai
  weights) via `open_clip`, driven entirely by text prompts.
- Deterministic, evenly-spaced frame extraction (default 8 frames/clip).
- A small, config-driven class/prompt list (`src/config.py`) so a `fire` /
  `burning_vehicle` class can be added later by editing one file.
- End-to-end runnable pipeline validated tonight against synthetic dummy
  clips (see below) — inspect → select → extract → classify → evaluate.

**Does NOT do (yet):**
- No fine-tuning of CLIP or any other model — pure zero-shot.
- No fire / burning-vehicle class — deliberately excluded, phase 2.
- No audio modality — video-only, phase 2+ per the multimodal ZSL plan.
- No full 4,754-clip XD-Violence run — this is a small-subset scaffold pass.
- The `/results` baseline currently checked in was run against **synthetic
  placeholder clips** (`scripts/make_dummy_videos.py`), not real XD-Violence
  footage — see "Honest status" below. This validates the pipeline mechanics
  only; the accuracy number is not a research result.

## Repo structure

```
data/           gitignored — downloaded subset, annotations, manifest.csv
src/            reusable library code (config, frame extraction, classifier)
scripts/        runnable entry points (one per pipeline stage)
results/        evaluation output (riot_zeroshot_baseline.md, predictions.csv)
requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
```

Runs unmodified on CPU (local, no CUDA needed) or GPU (Colab) — device is
auto-detected in `src/zero_shot_classifier.py`.

## Honest status as of this commit

The real XD-Violence annotation file has **not yet been downloaded** into
this repo (it's gated behind a request form / OneDrive links on the official
site, not a stable scripted-download URL — see `scripts/select_subset.py`
docstring). So tonight's validation run uses `scripts/make_dummy_videos.py`
to generate 6 synthetic placeholder clips (2 per class) that exercise the
exact same code path real clips would. This proves scripts 2–6 work
end-to-end; it does **not** demonstrate CLIP's real zero-shot accuracy on
riot footage. That requires running against real XD-Violence clips, next.

## How to run locally (CPU) — scaffold validation with dummy clips

```bash
python scripts/make_dummy_videos.py     # generates 6 synthetic clips + manifest.csv
python scripts/inspect_dataset.py       # catalogs what's in data/
python scripts/evaluate.py              # runs CLIP zero-shot + writes /results
```

## How to run against the real dataset (local CPU or Colab GPU)

1. Manually download the XD-Violence annotation file from
   https://roc-ng.github.io/XD-Violence/ and place it at
   `data/annotations/xd_violence_annotations.txt` (or pass `--annotation-file`).
2. Confirm `XD_VIOLENCE_LABEL_CODES` in `src/config.py` matches the label
   scheme actually used in the downloaded file — the mapping documented there
   is unverified against a real download and may need adjusting.
3. Select the target subset:
   ```bash
   python scripts/select_subset.py --max-per-class 5
   ```
   This writes `data/annotations/target_ids.txt` and `data/manifest.csv`.
4. Fetch **only** the target video IDs listed in `target_ids.txt` into
   `data/videos/<video_id>.mp4` — either via a scripted fetch if the host
   supports selective download, or by manually placing files downloaded from
   the host's bulk-download mechanism (e.g. OneDrive) into that folder.
5. Check what's actually present vs. missing:
   ```bash
   python scripts/inspect_dataset.py
   ```
6. Run evaluation (only clips present on disk are evaluated):
   ```bash
   python scripts/evaluate.py
   ```

In Colab, run the same four commands (`inspect_dataset.py`, `select_subset.py`,
`inspect_dataset.py` again, `evaluate.py`) with `data/` pointed at a Google
Drive-mounted folder — no code changes needed, GPU is auto-detected.

## [Superseded] Interim real-data pass: RLVS as a stand-in for XD-Violence Riot

`scripts/build_rlvs_manifest.py` builds a manifest from the RLVS (Real Life
Violence Situations) dataset, mapping RLVS `Violence` (one-on-one/small-group
street fights) to `riot` as a **real-world proxy** while nothing better was
available. This has been superseded by the Capitol-riot benchmark below,
which uses genuinely real riot footage for the positive class instead. The
RLVS-only run is kept for the record at `results/rlvs_zeroshot_realdata.md`
(100 real clips, 50/class, 2% accuracy — see that file's own Observations
section). RLVS `NonViolence` clips are still used as the real negative class
below; RLVS `Violence` is not used anywhere going forward.

```bash
kaggle datasets download -d mohamedmustafa/real-life-violence-situations-dataset
unzip real-life-violence-situations-dataset.zip -d data/rlvs   # ensure enough free disk first
python scripts/build_rlvs_manifest.py --max-per-class 50
```

## Current real-data benchmark: Capitol riot footage + RLVS normal

The first benchmark in this project with a **real positive class and a real
negative class** for riot detection:

- **riot** — real Jan 6, 2021 US Capitol riot footage, via the Kaggle
  dataset `jpmiller/protests-against-police-violence`
  (`scripts/build_capitol_manifest.py`). Verified as genuinely a video
  dataset (742 real `.mp4` clips, ~36GB total, spread across four sibling
  folders `capitol_vids`/`capitol_vids2`/`capitol_vids3`/`capitol_vids4` —
  confirmed via the Kaggle API's full paginated file listing, not assumed
  from the first page). **No negative class or per-clip labels ship with
  this dataset** — its other files (`protests.csv`, `press_incidents.csv`,
  `us_capitol/charges.csv`, `us_capitol/parler-videos-geocoded.csv`) are
  event-level/legal/geocoding records, checked directly, not violence labels.
- **normal** — RLVS `NonViolence` clips (real, not synthetic). RLVS
  `Violence` is deliberately excluded from this pairing — see
  `scripts/build_protest_manifest.py` docstring.

The Kaggle host for the Capitol dataset supports scripted per-file download
(unlike XD-Violence), so only the selected subset is ever fetched — never
the full 36GB. Runs on CPU: 80 real clips classified in under a minute.

```bash
# 1. Fetch a capped, deterministic subset of real Capitol riot clips
python scripts/build_capitol_manifest.py --max-clips 30

# 2. Combine with the RLVS NonViolence clips already fetched above
python scripts/build_protest_manifest.py

# 3. Evaluate into its own results file
python scripts/evaluate.py \
  --manifest data/manifest_protest.csv \
  --output-name protest_zeroshot_realdata \
  --report-title "Riot/Protest Zero-Shot Results (Real Data: Capitol Riot + RLVS Normal)" \
  --report-note "riot = real US Capitol riot footage; normal = real RLVS NonViolence clips. RLVS Violence excluded -- see data/manifest_protest.README.md."
```

**Status:** run (30 riot / 50 normal, 80 clips total). Overall accuracy
36.25%, but the breakdown is the actual finding — see
`results/protest_zeroshot_realdata.md`'s Observations section:

- **Riot detection itself works well on real footage:** precision 0.93,
  recall 0.90 (27/30 real Capitol clips correctly called "riot"). This is
  the first result where the model separates real riot content from other
  classes on raw similarity, not via a mislabeled proxy.
- **Normal-scene rejection is broken by a known prompt-calibration bias:**
  recall on `normal` is only 0.04 — the `fighting` prompt set scores
  systematically higher than `riot` or `normal` regardless of actual
  content (same bias flagged in the superseded RLVS-only run above, so it's
  a property of the prompt set, not this particular dataset pairing).

Next concrete step: rebalance/tune `CLASS_PROMPTS["fighting"]` in
`src/config.py`, or drop it and treat this as a strict binary riot/normal
classifier (this benchmark has no true "fighting" ground truth to justify
keeping a three-way classifier active), then re-run.

## Reproducibility

Every script that touches randomness (`select_subset.py`,
`make_dummy_videos.py`, `evaluate.py`) calls `src.config.set_seed()` first and
prints the seed used (fixed at `SEED = 42` in `src/config.py`). No silent
default seeds anywhere in this pipeline.

## Extending to the fire / burning-vehicle class (phase 2)

Add an entry to `CLASS_PROMPTS` and `TARGET_CLASSES` in `src/config.py` (and,
if pulling from XD-Violence, a code mapping in `XD_VIOLENCE_LABEL_CODES` for
whatever label represents car/explosion-adjacent events). No other file needs
to change — extraction, classification, and evaluation are all driven off
that config.
