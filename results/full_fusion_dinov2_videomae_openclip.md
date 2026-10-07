# Full Fusion Results (DINOv2 + VideoMAE + OpenCLIP, Riot vs. Normal)

Same 2831-clip full-scope dataset as `results/mlp_fusion_full_scope.md` (485
riot, 2346 normal). **Different branch composition from that earlier
result**: LK and RF-DETR are excluded here (their re-extraction with the
2026-10-05 fix was paused mid-run, 237/2831 clips, not used in this
comparison) — this fusion is DINOv2 + VideoMAE + OpenCLIP (ViT-L-14) only.
2304 feature dimensions (768 × 3).

## Branch ablation (single 80/20 split)

| branch group | features | test accuracy | riot precision | riot recall | best val score |
|---|---|---|---|---|---|
| **full_fusion** (dinov2+videomae+openclip) | 2304 | **98.41%** | 0.978 | 0.928 | 0.982 |
| dinov2_openclip | 1536 | 98.24% | 0.958 | 0.938 | 0.987 |
| openclip_only | 768 | 98.06% | 0.939 | 0.948 | 0.991 |
| dinov2_only | 768 | 97.88% | 0.947 | 0.928 | 0.960 |
| dinov2_videomae | 1536 | 97.18% | 0.935 | 0.897 | 0.969 |
| videomae_only | 768 | 93.83% | 0.888 | 0.732 | 0.956 |
| lk_only / rfdetr_only / lk_rfdetr | — | not evaluated this run | — | — | — |

(lk_only/rfdetr_only/lk_rfdetr skipped — their feature file was set aside
mid-re-extraction, see `docs/roadmap.md` for status.)

## Multi-seed robustness check (6 seeds: 0,1,2,3,4,42)

| group | mean accuracy | std |
|---|---|---|
| **full_fusion** (dinov2+videomae+openclip) | **98.35%** | ±0.33% |
| dinov2_only | 97.21% | ±0.85% |

Per-seed accuracies — full_fusion: [0.9824, 0.9806, 0.9877, 0.9877, 0.9788,
0.9841]; dinov2_only: [0.9577, 0.9683, 0.9683, 0.9841, 0.9753, 0.9788].

**Gap: 1.15 percentage points — exceeds the ~0.59-point average per-seed
noise, confirmed across all 6 seeds (full_fusion won every single one).**
This is the opposite outcome from the earlier (2026-09-27) multi-seed
check, which found the old full_fusion (including LK+RF-DETR) did NOT
reproducibly beat DINOv2 alone. The difference: that fusion carried two
dead-weight branches; this one swaps them for a second strong backbone
(OpenCLIP) instead.

**Not yet isolated:** whether `openclip_only` or `dinov2_openclip` (2-way)
are individually robust improvements over `dinov2_only` on their own, or
whether VideoMAE's presence in the winning 3-way combo specifically
matters (it's the weakest individual branch, 93.8%, so its contribution to
the best combination is not yet explained). Only the 2-group comparison
above (`dinov2_only` vs. this `full_fusion`) has been multi-seed confirmed.

## Context: how this compares to published XD-Violence benchmarks

**It doesn't, directly — see `docs/context.md`, "Published XD-Violence
benchmarks vs. this project's task" for the full explanation.** Short
version: published SOTA (~87% AP, DSANet) measures frame-level Average
Precision across all 6 violence classes lumped as "abnormal" on full
untrimmed test videos, weakly-supervised (video-level labels only). This
project measures clip-level accuracy, Riot only vs. pure Normal, on
pre-trimmed clips, with direct clip-level supervision — a narrower,
easier-to-define sub-problem. The 98% here is not "beating" the published
~87% AP; it's a strong result on a materially different, easier task.
