# Riot/Protest Zero-Shot Results (Real Data: Capitol Riot + RLVS Normal)

Zero-shot CLIP (ViT-B-32, openai weights) classification of riot vs. negative-class clips. No fine-tuning. See README.md for scope and limitations.

> riot = real US Capitol riot footage (Jan 6, 2021, via Kaggle jpmiller/protests-against-police-violence); normal = real RLVS NonViolence clips. RLVS Violence (fighting) deliberately excluded -- see data/manifest_protest.README.md. First benchmark in this project with a real positive AND real negative class for riot detection.

**Clips evaluated:** 80  
**Overall accuracy:** 36.25%

## Observations

Two distinct effects, and they point in opposite directions:

1. **The core riot-detection signal is genuinely strong.** On the 30 real
   Capitol riot clips, zero-shot CLIP scores `riot` (mean cosine sim 0.259)
   clearly above `fighting` (0.242) and `normal` (0.231) — riot precision
   0.93, recall 0.90 (27/30 correct). This is the first result in this
   project where the model correctly separates real riot footage from other
   classes on raw similarity, not just by a mislabeled proxy. This is the
   "master the first aspect" signal Hith asked for, and it's positive.
2. **A separate, already-known prompt-calibration bias is capping overall
   accuracy.** On the 50 real RLVS `NonViolence` (true "normal") clips, the
   `fighting` prompt set still wins on average (mean 0.207) over both
   `normal` (0.188) and `riot` (0.190) — normal recall is only 0.04 (2/50).
   This is the same bias flagged in the RLVS-only run
   (`results/rlvs_zeroshot_realdata.md`): the `fighting` prompt set scores
   systematically high regardless of actual content, not specific to this
   dataset pairing. It is now clearly the single biggest lever on overall
   accuracy — riot detection itself is already working; normal-scene
   rejection is what's broken.

**Net read:** don't read the 36% overall accuracy as "zero-shot riot
detection doesn't work" — read it as "riot detection works (93%
precision/90% recall on real riot footage); the `fighting` prompt needs
recalibration before this pipeline can be trusted end-to-end." Next concrete
step: rebalance/tune `CLASS_PROMPTS["fighting"]` in `src/config.py` (or drop
it and re-run as a strict binary riot/normal classifier, since this
particular benchmark has no true "fighting" ground truth to justify keeping
a three-way classifier active) and re-run.

## Per-class precision / recall / F1

| class | precision | recall | f1 | support |
|---|---|---|---|---|
| riot | 0.93 | 0.90 | 0.92 | 30 |
| normal | 1.00 | 0.04 | 0.08 | 50 |
| fighting | 0.00 | 0.00 | 0.00 | 0 |

## Confusion matrix (rows = true label, cols = predicted)

| true \ pred | riot | normal | fighting |
|---|---|---|---|
| riot | 27 | 0 | 3 |
| normal | 2 | 2 | 46 |
| fighting | 0 | 0 | 0 |

## Per-clip predictions

| id | true label | predicted | confidence | correct |
|---|---|---|---|---|
| 0RkqluQmLWCt | riot | fighting | 0.483 | no |
| 0gEXueOMmwi8 | riot | riot | 0.913 | yes |
| 0jaHRfXYTxdk | riot | riot | 0.840 | yes |
| 1Ta9ZdFfiNrZ | riot | riot | 0.930 | yes |
| 1Zvr7Xtfv0Yt | riot | riot | 0.873 | yes |
| 1do91KWUgjXQ | riot | riot | 0.653 | yes |
| 2XwJn0Iqphrc | riot | riot | 0.637 | yes |
| 3PkLpHaNWWeH | riot | riot | 0.904 | yes |
| 3ZXOHhUdKlYd | riot | riot | 0.935 | yes |
| 3vGQyQIMf9H5 | riot | riot | 0.762 | yes |
| 4AquVMy2oe6C | riot | riot | 0.883 | yes |
| 4wIDySD7tKxo | riot | riot | 0.445 | yes |
| 5an2kTUFQs2t | riot | fighting | 0.476 | no |
| 650ut3VxB679 | riot | riot | 0.823 | yes |
| 6FY6c0d8IMjz | riot | riot | 0.956 | yes |
| 6VYEdaOOP3hD | riot | riot | 0.440 | yes |
| 7ImZGTdfdcUk | riot | riot | 0.954 | yes |
| 7WJTCduTUKpl | riot | riot | 0.440 | yes |
| 7fckI1220tbu | riot | riot | 0.929 | yes |
| 7pyX4y0Z2wiy | riot | riot | 0.655 | yes |
| 8fsC1EfPO70k | riot | riot | 0.704 | yes |
| 8ziKp2FKa3Sb | riot | fighting | 0.425 | no |
| 99Z6yIaTknNG | riot | riot | 0.897 | yes |
| 9bJLFfPeZlk8 | riot | riot | 0.937 | yes |
| 9mroY9bM530c | riot | riot | 0.672 | yes |
| ATHRnnmNpayv | riot | riot | 0.515 | yes |
| AYijYnzI0Gbr | riot | riot | 0.602 | yes |
| B7yh3YgnbcFT | riot | riot | 0.910 | yes |
| BnoDFbldwdly | riot | riot | 0.782 | yes |
| BvNA5CiE47yt | riot | riot | 0.895 | yes |
| NonViolence_NV_1 | normal | fighting | 0.862 | no |
| NonViolence_NV_10 | normal | fighting | 0.706 | no |
| NonViolence_NV_11 | normal | riot | 0.443 | no |
| NonViolence_NV_12 | normal | fighting | 0.864 | no |
| NonViolence_NV_13 | normal | fighting | 0.733 | no |
| NonViolence_NV_14 | normal | normal | 0.385 | yes |
| NonViolence_NV_15 | normal | fighting | 0.734 | no |
| NonViolence_NV_16 | normal | fighting | 0.752 | no |
| NonViolence_NV_17 | normal | fighting | 0.691 | no |
| NonViolence_NV_18 | normal | fighting | 0.936 | no |
| NonViolence_NV_19 | normal | fighting | 0.936 | no |
| NonViolence_NV_2 | normal | fighting | 0.606 | no |
| NonViolence_NV_20 | normal | fighting | 0.891 | no |
| NonViolence_NV_21 | normal | fighting | 0.894 | no |
| NonViolence_NV_22 | normal | fighting | 0.681 | no |
| NonViolence_NV_23 | normal | fighting | 0.684 | no |
| NonViolence_NV_24 | normal | fighting | 0.609 | no |
| NonViolence_NV_25 | normal | fighting | 0.838 | no |
| NonViolence_NV_26 | normal | fighting | 0.838 | no |
| NonViolence_NV_27 | normal | fighting | 0.891 | no |
| NonViolence_NV_28 | normal | fighting | 0.734 | no |
| NonViolence_NV_29 | normal | fighting | 0.947 | no |
| NonViolence_NV_3 | normal | fighting | 0.785 | no |
| NonViolence_NV_30 | normal | fighting | 0.673 | no |
| NonViolence_NV_31 | normal | fighting | 0.770 | no |
| NonViolence_NV_32 | normal | fighting | 0.775 | no |
| NonViolence_NV_33 | normal | fighting | 0.578 | no |
| NonViolence_NV_34 | normal | fighting | 0.772 | no |
| NonViolence_NV_35 | normal | fighting | 0.797 | no |
| NonViolence_NV_36 | normal | fighting | 0.931 | no |
| NonViolence_NV_37 | normal | fighting | 0.680 | no |
| NonViolence_NV_38 | normal | fighting | 0.911 | no |
| NonViolence_NV_39 | normal | fighting | 0.665 | no |
| NonViolence_NV_4 | normal | fighting | 0.636 | no |
| NonViolence_NV_40 | normal | fighting | 0.632 | no |
| NonViolence_NV_41 | normal | fighting | 0.515 | no |
| NonViolence_NV_42 | normal | fighting | 0.890 | no |
| NonViolence_NV_43 | normal | normal | 0.427 | yes |
| NonViolence_NV_44 | normal | fighting | 0.645 | no |
| NonViolence_NV_45 | normal | fighting | 0.635 | no |
| NonViolence_NV_46 | normal | fighting | 0.965 | no |
| NonViolence_NV_47 | normal | fighting | 0.809 | no |
| NonViolence_NV_48 | normal | fighting | 0.569 | no |
| NonViolence_NV_49 | normal | fighting | 0.649 | no |
| NonViolence_NV_5 | normal | fighting | 0.636 | no |
| NonViolence_NV_50 | normal | fighting | 0.672 | no |
| NonViolence_NV_6 | normal | fighting | 0.562 | no |
| NonViolence_NV_7 | normal | riot | 0.633 | no |
| NonViolence_NV_8 | normal | fighting | 0.549 | no |
| NonViolence_NV_9 | normal | fighting | 0.679 | no |