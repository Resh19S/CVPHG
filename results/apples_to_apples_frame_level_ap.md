# Apples-to-Apples Evaluation: Official Split + Frame-Level AP

First evaluation in this project computed on the same metric, official
test set, and ground-truth source as published XD-Violence benchmarks.
Still narrower in class scope (Riot only vs. Normal, not all 6 violence
classes lumped as "abnormal") and uses a flat per-video broadcast score
(every frame of a clip gets that clip's single predicted probability)
rather than true temporal localization — see `docs/context.md`,
"Published XD-Violence benchmarks vs. this project's task" for the full
explanation of what this does and doesn't close.

**Setup:** MLP trained on XD-Violence's **official train split**
(not a random resample), predicting riot-probability for each clip in the
**official test split** (101 riot + 300 normal = 401 clips). Frame-level
ground truth pulled directly from the dataset's own `annotations.txt`
(local-to-clip frame intervals). Flat-broadcast score per clip, frame-level
AP computed via `sklearn.metrics.average_precision_score` over all
1,601,767 concatenated test frames.

## Result

**Frame-level AP: 85.45%**

| method | AP (%) | task scope |
|---|---|---|
| DSANet | 86.95% | all 6 classes lumped, true localization, weakly-supervised |
| ReFLIP | 85.81% | all 6 classes lumped, true localization, weakly-supervised |
| TCVADS | 85.58% | all 6 classes lumped, true localization, weakly-supervised |
| **This project** | **85.45%** | **Riot only, flat broadcast, directly-supervised** |
| VadCLIP | 84.51% | all 6 classes lumped, true localization, weakly-supervised |

## Data quality note

100/101 riot test clips matched an `annotations.txt` entry; 1 clip
(`v=aWPWHU8x6kE__#1_label_B4-0-0.mp4`) had no match and was treated as
fully negative ground truth for its entire duration. This is a
conservative error (understates AP, doesn't inflate it) — the true number
is very slightly higher than 85.45%, not artificially boosted.

## Why this landed close to published numbers despite the flat-broadcast simplification

Published methods localize anomalies within long, untrimmed movies, where
the violent moment may be a small fraction of total runtime — flat
broadcasting would badly hurt AP there. This project's clips are already
pre-trimmed to the event: 271,322 of 1,601,767 test frames (~17%) are
marked anomalous, concentrated in the 101 riot clips specifically, meaning
each riot clip's anomalous interval already covers a large share of its
own duration. Flat-broadcasting a single score loses much less information
in this setting than it would on full-length source movies. This is a
structural property of the task as scoped (pre-trimmed clips), not
evidence the method performs true temporal localization.

## What this still doesn't prove

- Not evaluated against the other 5 XD-Violence violence classes (Abuse,
  Car Accident, Explosion, Fighting, Shooting) — the published number is
  for detecting *any* of 6 classes as "abnormal," this is Riot-only.
- Not weakly-supervised — trained with direct clip-level labels, not the
  video-level-only MIL paradigm published methods use.
- No genuine temporal localization — a model that scored every frame of
  the correct clips highly, with zero internal temporal discrimination,
  would still have produced this number, given the structural note above.

