# MLP Fusion Classifier Results — Full Scope (Riot vs. Normal, Full XD-Violence)

Supervised MLP (256,64 hidden units) trained on fused features: Lucas-Kanade
optical flow summary stats + RF-DETR detection counts + DINOv2 frame
embeddings + VideoMAE clip embeddings. Real XD-Violence data for both
classes, **full Normal class this time** (not the capped 1:1 balanced
sample from the earlier run) — see `results/mlp_fusion_riot_normal.md` for
that earlier, smaller-scope result.

**Clips:** 2831 total (485 riot, 2346 normal — ~4.8:1 imbalanced, by design
per direction to train on the full dataset for comparability) —
**Train:** 2264 — **Test:** 567 — **Feature dimensions:** 1544 —
**Test accuracy:** 97.53% — **Balanced accuracy:** 95.24%

## Per-class precision / recall / F1

| class | precision | recall | f1 | support |
|---|---|---|---|---|
| normal | 0.98 | 0.99 | 0.99 | 470 |
| riot | 0.94 | 0.92 | 0.93 | 97 |

## Confusion matrix (rows = true label, cols = predicted)

| true \ pred | normal | riot |
|---|---|---|
| normal | 464 | 6 |
| riot | 8 | 89 |

## Comparison against the earlier balanced-scope result

| run | clips | test accuracy | balanced accuracy | riot recall |
|---|---|---|---|---|
| Balanced (485 riot / 485 normal), 2026-09-19 | 970 | 92.27% | 92.27% (already balanced) | 90% |
| **Full scope (485 riot / 2346 normal), 2026-09-27** | **2831** | **97.53%** | **95.24%** | **92%** |

Raw accuracy alone would be misleading to compare here (imbalance inflates
it), but **balanced accuracy also improved** (92.27% → 95.24%), and riot
recall held or slightly improved (90% → 92%) — the extra real Normal data
appears to have genuinely helped, not just made the number look better via
class imbalance. See `docs/findings.md` (2026-09-27 entry) for the branch
ablation that explains *why* — see `results/branch_ablation_full_scope.md`.
