# Branch Ablation Results — Full Scope (Riot vs. Normal, Full XD-Violence)

Answers the open question flagged in `docs/findings.md` (2026-09-19 entry):
which branch is actually driving the fusion classifier's accuracy? Same
2831-clip dataset, same 80/20 stratified split, same seed (42) as
`results/mlp_fusion_full_scope.md` — only the feature columns fed to the
MLP change per row below.

| branch group | features | test accuracy | normal precision | normal recall | riot precision | riot recall | best val score |
|---|---|---|---|---|---|---|---|
| dinov2_only | 768 | **97.88%** | 0.985 | 0.989 | 0.947 | 0.928 | 0.960 |
| full_fusion | 1544 | 97.53% | 0.983 | 0.987 | 0.937 | 0.918 | 0.974 |
| dinov2_videomae | 1536 | 97.18% | 0.979 | 0.987 | 0.935 | 0.897 | 0.969 |
| videomae_only | 768 | 93.83% | 0.947 | 0.981 | 0.888 | 0.732 | 0.956 |
| lk_only | 4 | 82.89% | 0.829 | 1.000 | 0.000 | 0.000 | 0.828 |
| rfdetr_only | 4 | 82.89% | 0.829 | 1.000 | 0.000 | 0.000 | 0.828 |
| lk_rfdetr | 8 | 82.72% | 0.842 | 0.974 | 0.478 | 0.113 | 0.837 |

## Interpretation

1. **DINOv2 alone is carrying essentially all the signal.** `dinov2_only`
   is the single best-performing group in the table — better than
   `full_fusion` (all four branches combined).
2. **LK and RF-DETR, as currently engineered, carry zero riot-
   discriminating signal at this scale.** `lk_only` and `rfdetr_only` are
   both exactly at the trivial majority-class baseline (82.89% = 470/567,
   the fraction of the test set that's Normal) with riot precision/recall
   of 0.00/0.00 — the MLP simply predicts "normal" for every clip when
   given only these 4-dimensional summary features. Combining them
   (`lk_rfdetr`) barely moves off that baseline (11.3% riot recall).
3. **Adding branches to DINOv2 does not help, and may cost a small
   amount.** `dinov2_videomae` (97.18%) and `full_fusion` (97.53%) both
   score below `dinov2_only` (97.88%) alone.
4. **Caveat, not yet resolved:** this is a single 80/20 split, not
   cross-validated. The ~0.35-point gap between `dinov2_only` and
   `full_fusion` could plausibly be split-noise rather than a real,
   reproducible effect — a multi-seed check is needed before treating
   "DINOv2 alone beats full fusion" as a settled conclusion rather than
   "roughly tied, fusion doesn't clearly help." See
   `notebooks/ablation_fusion_branches.ipynb`'s multi-seed section
   (added 2026-09-27) for that check.

## What this means for the architecture

The current 4-branch fusion design is **not yet earning its complexity**.
Two honest paths forward, not mutually exclusive:
- Improve the LK/RF-DETR feature representations (currently just 4 scalar
  summary stats each — e.g. richer motion descriptors, per-frame detection
  sequences instead of aggregated counts) before concluding they're
  fundamentally uninformative for this task.
- Or accept that DINOv2 alone is the strongest, cheapest option found so
  far, and treat the other branches as not yet justified rather than
  keep them by default because the architecture diagram included them.
