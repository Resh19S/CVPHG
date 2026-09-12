# RLVS Zero-Shot Results (Riot/Normal Proxy)

Zero-shot CLIP (ViT-B-32, openai weights) classification of riot vs. negative-class clips. No fine-tuning. See README.md for scope and limitations.

> RLVS Violence/NonViolence used as a real-world stand-in for XD-Violence Riot while formal access is pending -- not a claim RLVS fights equal riots. RLVS Violence is predominantly one-on-one/small-group fights, semantically closer to this project's fighting prompt class than to riot (crowd-scale unrest); a fighting prediction here is plausibly more correct than the riot ground truth, not a CLIP failure. See data/manifest_rlvs.README.md.

**Clips evaluated:** 100  
**Overall accuracy:** 2.00%

## Observations

Two distinct effects are visible here, and they should not be conflated:

1. **Expected label-mismatch confusion (riot vs. fighting):** all 50 true
   "riot" (RLVS Violence) clips predicted "fighting" — consistent with the
   caveat above; RLVS Violence is physical fighting, not crowd-scale riots,
   so this is a labeling artifact, not a CLIP failure.
2. **Unexpected prompt-calibration bias (fighting dominates normal too):**
   46/50 true "normal" (RLVS NonViolence) clips were *also* predicted
   "fighting." Raw mean cosine similarity across all 100 clips: fighting
   0.245 (σ=0.042) vs. riot 0.218 (σ=0.032) vs. normal 0.211 (σ=0.026) —
   the "fighting" prompt set scores systematically higher regardless of
   ground truth, not just on true-fighting-ish content. This points to a
   prompt-calibration/class-prior imbalance in the current
   `CLASS_PROMPTS` wording (`src/config.py`), not a fundamental limit of
   zero-shot CLIP. Next step before trusting any accuracy number from this
   pipeline: rebalance/tune prompt phrasing per class (e.g. equal prompt
   counts, prompt ensembling, or per-class score normalization) and re-run.

## Per-class precision / recall / F1

| class | precision | recall | f1 | support |
|---|---|---|---|---|
| riot | 0.00 | 0.00 | 0.00 | 50 |
| normal | 1.00 | 0.04 | 0.08 | 50 |
| fighting | 0.00 | 0.00 | 0.00 | 0 |

## Confusion matrix (rows = true label, cols = predicted)

| true \ pred | riot | normal | fighting |
|---|---|---|---|
| riot | 0 | 0 | 50 |
| normal | 2 | 2 | 46 |
| fighting | 0 | 0 | 0 |

## Per-clip predictions

| id | true label | predicted | confidence | correct |
|---|---|---|---|---|
| Violence_V_1 | riot | fighting | 0.842 | no |
| Violence_V_10 | riot | fighting | 0.944 | no |
| Violence_V_11 | riot | fighting | 0.982 | no |
| Violence_V_12 | riot | fighting | 0.991 | no |
| Violence_V_13 | riot | fighting | 0.988 | no |
| Violence_V_14 | riot | fighting | 0.957 | no |
| Violence_V_15 | riot | fighting | 0.993 | no |
| Violence_V_16 | riot | fighting | 0.994 | no |
| Violence_V_17 | riot | fighting | 0.877 | no |
| Violence_V_18 | riot | fighting | 0.964 | no |
| Violence_V_19 | riot | fighting | 0.992 | no |
| Violence_V_2 | riot | fighting | 0.960 | no |
| Violence_V_20 | riot | fighting | 0.678 | no |
| Violence_V_21 | riot | fighting | 0.996 | no |
| Violence_V_22 | riot | fighting | 0.979 | no |
| Violence_V_23 | riot | fighting | 0.982 | no |
| Violence_V_24 | riot | fighting | 0.990 | no |
| Violence_V_25 | riot | fighting | 0.568 | no |
| Violence_V_26 | riot | fighting | 0.771 | no |
| Violence_V_27 | riot | fighting | 0.997 | no |
| Violence_V_28 | riot | fighting | 0.998 | no |
| Violence_V_29 | riot | fighting | 0.983 | no |
| Violence_V_3 | riot | fighting | 0.995 | no |
| Violence_V_30 | riot | fighting | 0.980 | no |
| Violence_V_31 | riot | fighting | 0.981 | no |
| Violence_V_32 | riot | fighting | 0.868 | no |
| Violence_V_33 | riot | fighting | 0.900 | no |
| Violence_V_34 | riot | fighting | 0.974 | no |
| Violence_V_35 | riot | fighting | 0.954 | no |
| Violence_V_36 | riot | fighting | 0.936 | no |
| Violence_V_37 | riot | fighting | 0.911 | no |
| Violence_V_38 | riot | fighting | 0.972 | no |
| Violence_V_39 | riot | fighting | 0.657 | no |
| Violence_V_4 | riot | fighting | 0.994 | no |
| Violence_V_40 | riot | fighting | 0.926 | no |
| Violence_V_41 | riot | fighting | 0.501 | no |
| Violence_V_42 | riot | fighting | 0.532 | no |
| Violence_V_43 | riot | fighting | 0.896 | no |
| Violence_V_44 | riot | fighting | 0.986 | no |
| Violence_V_45 | riot | fighting | 0.994 | no |
| Violence_V_46 | riot | fighting | 0.921 | no |
| Violence_V_47 | riot | fighting | 0.952 | no |
| Violence_V_48 | riot | fighting | 0.971 | no |
| Violence_V_49 | riot | fighting | 0.985 | no |
| Violence_V_5 | riot | fighting | 0.996 | no |
| Violence_V_50 | riot | fighting | 0.973 | no |
| Violence_V_6 | riot | fighting | 0.991 | no |
| Violence_V_7 | riot | fighting | 0.932 | no |
| Violence_V_8 | riot | fighting | 0.914 | no |
| Violence_V_9 | riot | fighting | 0.902 | no |
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