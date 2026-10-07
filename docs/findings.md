# Findings Log

Chronological, append-only. Never delete an entry — mark it superseded and
point to the entry that supersedes it. See `docs/README.md` for the
[MECHANICS CHECK] vs [REAL RESULT] tagging rule.

---

## 2026-09-11 — [MECHANICS CHECK] Synthetic dummy clips, 3-class zero-shot

**Dataset:** 6 synthetic OpenCV-generated clips (2 each: riot/normal/
fighting), `scripts/make_dummy_videos.py`. Colored-shape caricatures, not
real footage.

**Measured:** CLIP ViT-B-32 (openai weights) zero-shot classification
accuracy against `src/config.py` text prompts.

**Result:** 33.33% overall accuracy (2/6 correct).

**Caveat:** Purely validates that the pipeline (extract → embed → classify →
evaluate) runs end-to-end without errors. The accuracy number is
meaningless as a research result — synthetic colored circles have no
semantic relationship to real riot/fighting/normal content. Results:
`results/riot_zeroshot_baseline.md`.

**Status:** Not superseded — still the reference mechanics-check run for
this pipeline.

---

## 2026-09-11 — [MECHANICS CHECK] RLVS Violence→riot proxy + RLVS NonViolence→normal

**Dataset:** 100 real RLVS (Real Life Violence Situations) clips downloaded
via Kaggle (`mohamedmustafa/real-life-violence-situations-dataset`), 50/class.
Label mapping: `Violence → riot` (proxy), `NonViolence → normal` (real).

**Measured:** CLIP ViT-B-32 zero-shot accuracy, same 3-class prompt config.

**Result:** 2.00% overall accuracy (2/100 correct).
- riot: precision 0.00, recall 0.00 (all 50 true-riot/Violence clips
  predicted "fighting")
- normal: precision 1.00, recall 0.04 (46/50 true-normal clips ALSO
  predicted "fighting")

**Caveat (two distinct effects — do not conflate):**
1. *Expected label mismatch:* RLVS "Violence" is one-on-one/small-group
   street fighting, not crowd-scale riots — semantically closer to this
   project's `fighting` prompt class than to `riot`. The 0% riot
   recall/precision here reflects a labeling mismatch, not a CLIP failure.
2. *Unexpected prompt-calibration bias:* the `fighting` prompt set scores
   systematically higher in raw cosine similarity than `riot` or `normal`
   **regardless of actual clip content** — mean cosine sim across all 100
   clips: fighting 0.245 (σ=0.042) vs. riot 0.218 (σ=0.032) vs. normal 0.211
   (σ=0.026). This is a property of the `CLASS_PROMPTS["fighting"]` wording
   in `src/config.py`, not of this dataset. Not yet fixed as of this entry.

Results: `results/rlvs_zeroshot_realdata.md`,
`results/rlvs_zeroshot_realdata_predictions.csv`.

**Status:** The `Violence → riot` proxy mapping is **superseded** by the
2026-09-11 Capitol+RLVS entry below, which uses real riot footage for the
positive class instead. RLVS `NonViolence → normal` is **not superseded** —
still in active use as the real negative class. The prompt-calibration bias
found here is confirmed to persist in the entry below (same root cause).

---

## 2026-09-11 — [REAL RESULT] US Capitol riot footage + RLVS NonViolence — first real positive + real negative riot benchmark

**Dataset:**
- riot (positive, n=30): real US Capitol riot footage, Jan 6 2021, from
  Kaggle dataset `jpmiller/protests-against-police-violence`
  (`us_capitol/capitol_vids*` folders). Verified as genuine video content via
  direct inspection (opened with OpenCV: 608x1080 vertical mobile video,
  ~17s clips) and via the dataset's own metadata (keyword "video", capitol
  directory description explicitly mentions videos from Parler).
- normal (negative, n=50): real RLVS `NonViolence` clips (same source as
  the mechanics-check entry above). RLVS `Violence` clips deliberately
  excluded from this pairing (`scripts/build_protest_manifest.py`).

**Measured:** CLIP ViT-B-32 zero-shot accuracy, same 3-class prompt config,
80 total clips.

**Result:** 36.25% overall accuracy.
- riot: precision 0.93, recall 0.90, f1 0.92 (27/30 correct; 3 misclassified
  as "fighting")
- normal: precision 1.00, recall 0.04, f1 0.08 (2/50 correct; 46/50
  misclassified as "fighting")

Raw mean cosine similarity, split by true class:
- True riot clips: riot 0.259 > fighting 0.242 > normal 0.231 — riot prompt
  correctly wins on average.
- True normal clips: fighting 0.207 > riot 0.190 > normal 0.188 — fighting
  prompt incorrectly wins on average.

**Caveat (must be read together, not separately):**
1. This is tagged REAL RESULT because the riot-positive class is, for the
   first time, genuine riot footage rather than a proxy label — the
   riot-vs-other separation (0.93 precision / 0.90 recall) is a real,
   verified signal that zero-shot CLIP can distinguish real riot footage
   from other content.
2. It is **not yet** a full XD-Violence-equivalent benchmark: the negative
   class is RLVS `NonViolence`, a stand-in for "not a riot," not XD-Violence's
   own Normal class or genuine protest-that-stayed-peaceful footage. This
   should be re-run against XD-Violence's actual Normal class once obtained.
3. The `fighting`-prompt calibration bias identified in the RLVS-only entry
   above is confirmed to persist here, unrelated to which dataset supplies
   the clips — it is the dominant cause of the low overall accuracy number.
   Overall accuracy (36.25%) should NOT be read as "riot detection doesn't
   work" — riot detection is working; normal-scene rejection is broken by
   this specific, now twice-confirmed bias.
4. Not yet fixed as of this entry: `CLASS_PROMPTS["fighting"]` in
   `src/config.py` needs rebalancing/recalibration, or should be dropped
   entirely for a strict binary riot/normal classifier (this benchmark has
   no true "fighting" ground truth to justify keeping it active).

Results: `results/protest_zeroshot_realdata.md`,
`results/protest_zeroshot_realdata_predictions.csv`.

**Status:** Superseded for the riot-class question by the 2026-09-12 n=200
scale-up entry below (same pairing, 5x the riot clips). Its normal-class
numbers and overall-accuracy caveat are unchanged at n=200 and still stand
— not superseded.

---

## 2026-09-12 — [REAL RESULT] Scale-up check: 150 Capitol riot clips (5x) + 50 RLVS NonViolence

**Dataset:** Same pairing as the 2026-09-11 Capitol+RLVS entry above, riot
class expanded from 30 to 150 real US Capitol riot clips
(`scripts/build_capitol_manifest.py --max-clips 150`); normal class
unchanged at 50 real RLVS `NonViolence` clips.

**Measured:** CLIP ViT-B-32 zero-shot accuracy, same 3-class prompt config,
200 total clips. Purpose: check whether the riot precision/recall found at
n=30 holds up at 5x the sample size, or was a small-sample fluke.

**Result:** 71.00% overall accuracy.
- riot: precision 0.99, recall 0.93, f1 0.96 (140/150 correct; 10
  misclassified as "fighting")
- normal: precision 1.00, recall 0.04, f1 0.08 (2/50 correct — **identical**
  confusion counts to the n=80 entry, as expected: same 50 clips, same
  deterministic pipeline, confirms no run-to-run drift)

Raw mean cosine similarity on true-riot clips: riot 0.262 (σ=0.014) >
fighting 0.240 (σ=0.015) > normal 0.232 (σ=0.010) — closely matches the
n=30 statistics (riot 0.259, fighting 0.242, normal 0.231), i.e. stable
across sample size, not noise.

**Caveat (read together with the n=80 entry above, not in isolation):**
1. **The riot-detection result holds up, and arguably strengthens, at 5x
   scale** — precision actually improved (0.93→0.99) and recall held
   (0.90→0.93) going from 30 to 150 real clips. This is meaningful evidence
   the riot signal is robust, not a small-sample artifact.
2. The `fighting`-prompt calibration bias is unchanged and remains the
   single cause of the lower overall accuracy number — still not fixed as
   of this entry. Same residual caveat as the n=80 entry: normal class here
   is still RLVS `NonViolence`, a stand-in, not XD-Violence's own Normal
   class.
3. Overall accuracy (71%) is higher than the n=80 run's 36.25% purely
   because riot clips (which the model gets right 93-99% of the time) now
   make up 75% of the sample instead of 37.5% — this is a sample-composition
   effect, not model improvement. Do not report "accuracy went up" without
   this explanation; report the per-class precision/recall instead.

Results: `results/protest_zeroshot_realdata_150.md`,
`results/protest_zeroshot_realdata_150_predictions.csv`.

**Status:** Current best real-data benchmark for the riot/protest detection
task. Not yet superseded.

---

## 2026-09-18 — [MECHANICS CHECK] XD-Violence riot (B4) class acquired via public HF mirror

**What this is:** a data-acquisition/access check, not a model result — no
classifier was run against this data yet. Tagged mechanics-check because it
validates that the target dataset is actually obtainable and clean, which
every prior entry in this log has been blocked on.

**Access path:** XD-Violence's own site
(https://roc-ng.github.io/XD-Violence/) is still gated behind a request
form / OneDrive bulk download, confirmed directly. However, a public
HuggingFace mirror of the same dataset was found (`jherng/xd-violence`),
serving individual files over plain HTTPS with no auth or request process.
Verified directly before committing to a full pull: two sample files
(one movie-titled filename, one YouTube-ID-style filename) test-downloaded
successfully (200 OK, valid MP4 per `file`).

**Dataset survey (via the HF tree API, listing every video directory, not
assumed from documentation):** 4750 total video files across the 5 training
directories + `test_videos`; 485 carry a B4 (riot) label, including
combined-label cases like `label_B4-G-0` (a naive `label_B4` substring
filter would miss these — the filter used checks each hyphenated label
code). Riot-only subset: 9.78 GiB.

**Result:** all 485 riot clips downloaded via
`notebooks/xdviolence_riot_pull.ipynb` directly into Colab from the HF
mirror (no local machine, no OneDrive), saved to Google Drive at
`My Drive/CVPHG/xdviolence_riot/`. Validated 485/485 on every check: exists
on disk, correct size vs. manifest, opens in OpenCV, first frame readable.
Manifest (`manifest_xdviolence_riot.csv`, id/label/split/size/url) saved
alongside the clips.

**Caveat:** this is the riot/positive class only. The Normal/negative class
from XD-Violence itself has not been pulled yet (see `context.md`) — the
same HF-mirror approach should work (filter for the `A` label code instead
of `B4`), just not run. Until that happens, a real-riot-vs-real-normal
XD-Violence-native benchmark doesn't exist yet; the n=200 Capitol+RLVS
result above remains the best real-data benchmark for that comparison. The
clips also live on Google Drive, not yet copied into this project's local
`data/` directory.

**Status:** Not superseded. This is the first entry establishing that real
XD-Violence riot data is actually in hand, not just a stand-in.

---

## 2026-09-19 — [REAL RESULT] Supervised MLP fusion classifier, real XD-Violence riot vs. normal

**Dataset:** 970 real XD-Violence clips — 485 riot (B4), 485 normal (A),
both classes pulled from the same public HF mirror used in the entry
above (`notebooks/xdviolence_riot_pull.ipynb` /
`xdviolence_normal_pull.ipynb`), both seeded/deterministic samples. Unlike
every prior real-data entry in this log, both positive and negative class
come from the *same* source dataset — not a cross-dataset pairing (Capitol
riot vs. RLVS normal).

**Pipeline:** `notebooks/feature_extraction_fusion.ipynb` builds a 1544-dim
fused feature vector per clip — Lucas-Kanade optical flow summary stats (4
dims: mean/max magnitude, mean angle, mean tracked points) + RF-DETR
person/vehicle detection counts (4 dims) + DINOv2 frame embedding,
mean-pooled (768 dims) + VideoMAE clip embedding (768 dims). No fine-tuning
on DINOv2/VideoMAE — frozen pretrained backbones. `notebooks/
mlp_fusion_classifier.ipynb` trains an MLP (256,64 hidden units) on top,
80/20 stratified train/test split (776/194, balanced).

**Result:** 92.27% test accuracy. Per-class: normal precision 0.90 / recall
0.95 / f1 0.92; riot precision 0.95 / recall 0.90 / f1 0.92 (97 support
each). Confusion matrix: 92/97 normal correct (5 misclassified as riot),
87/97 riot correct (10 misclassified as normal). Full report:
`results/mlp_fusion_riot_normal.md`. Raw per-clip predictions CSV
currently lives only on Drive (`My Drive/CVPHG/fusion_features/results/
mlp_fusion_riot_normal_predictions.csv`) — not yet copied into this
project's local `results/` directory.

**Caveat (must be read together, not separately — see full list in the
results file):**
1. The MLP's internal validation split hit a perfect 1.0000 score during
   training (sklearn's `early_stopping` carves ~78 clips off the training
   set automatically). Test accuracy is 92.27%, not 100%, so this isn't
   necessarily a red flag, but it means **which branch is actually driving
   this result is not yet known** — an ablation (DINOv2+VideoMAE alone vs.
   LK+RF-DETR alone) has not been run. Do not present this as "fusion
   works" until that's checked; a single strong branch could plausibly
   explain most of the 92.27%.
2. Binary riot/normal only. The 3-class target (Normal/Protest/Riot) from
   the architecture this pipeline implements is still blocked — no data
   source identified for a peaceful-protest class (checked directly:
   Kaggle `jpmiller/protests-against-police-violence` is 744/748 files
   Capitol riot footage, confirmed via a live API query, not assumed).
3. This is a genuinely cleaner real-data setup than every prior entry in
   this log — both classes share one source dataset, reducing (not
   eliminating) the dataset-of-origin confound risk that the Capitol/RLVS
   pairing carried.

**Status:** Not superseded on the accuracy numbers (a different, larger,
imbalanced-scope run below reports its own numbers rather than replacing
these). Caveat 1's open question — which branch is actually driving this
— **is answered by the 2026-09-27 entry below.**

---

## 2026-09-27 — [REAL RESULT] Full-scope MLP + branch ablation — DINOv2 alone drives the result, LK/RF-DETR contribute nothing

**Dataset:** 2831 real XD-Violence clips — 485 riot (unchanged), 2346
normal (full class this time, not the capped 485-clip balanced sample —
direction from Hith's brother, to make results comparable to published
XD-Violence benchmarks that use the full dataset). ~4.8:1 imbalanced by
design. Same seed (42), same 80/20 stratified split as every other entry
in this log.

**Part A — full-fusion MLP at full scope:** 97.53% test accuracy, 95.24%
balanced accuracy (2264 train / 567 test). Per-class: normal precision
0.98 / recall 0.99 / f1 0.99 (470 support); riot precision 0.94 / recall
0.92 / f1 0.93 (97 support). Confusion matrix: 464/470 normal correct (6
misclassified as riot), 89/97 riot correct (8 misclassified as normal).
Full report: `results/mlp_fusion_full_scope.md`. Compared against the
2026-09-19 balanced-scope entry, **balanced accuracy improved** (92.27% →
95.24%) and riot recall held/improved (90% → 92%) — the extra real Normal
data appears to have genuinely helped, not just made the raw number look
better via class imbalance.

**Part B — branch ablation (answers the 2026-09-19 open question):**
same dataset/split, MLP retrained on different column subsets. Full
table: `results/branch_ablation_full_scope.md`.

| branch group | features | test accuracy | riot precision | riot recall |
|---|---|---|---|---|
| dinov2_only | 768 | **97.88%** | 0.947 | 0.928 |
| full_fusion | 1544 | 97.53% | 0.937 | 0.918 |
| dinov2_videomae | 1536 | 97.18% | 0.935 | 0.897 |
| videomae_only | 768 | 93.83% | 0.888 | 0.732 |
| lk_only | 4 | 82.89% | 0.000 | 0.000 |
| rfdetr_only | 4 | 82.89% | 0.000 | 0.000 |
| lk_rfdetr | 8 | 82.72% | 0.478 | 0.113 |

**Result — the open question is answered, and it's not the answer the
architecture assumed:**
1. **DINOv2 alone is the single best-performing group in the entire
   table** — it beats `full_fusion` (all four branches combined).
2. **LK and RF-DETR, as currently engineered (4 scalar summary stats
   each), carry zero riot-discriminating signal at this scale.**
   `lk_only` and `rfdetr_only` sit exactly at the trivial majority-class
   baseline (82.89% = 470/567, the Normal fraction of the test set) with
   riot precision/recall of 0.00/0.00 — the MLP is simply predicting
   "normal" for every clip when given only these features. `lk_rfdetr`
   combined barely moves off that baseline (11.3% riot recall).
3. **Adding branches on top of DINOv2 does not help, and costs a small
   amount** — `dinov2_videomae` and `full_fusion` both score below
   `dinov2_only` alone.

**Caveat (must be read together, not separately):**
1. This is a single 80/20 split, not cross-validated. The ~0.35-point gap
   between `dinov2_only` and `full_fusion` could plausibly be split-noise
   rather than a reproducible effect — treat the finding as "fusion
   doesn't clearly help" rather than "DINOv2 alone is definitively best"
   until a multi-seed check confirms it (queued in
   `notebooks/ablation_fusion_branches.ipynb`, not yet run).
2. This does not mean motion/detection signals are inherently useless for
   riot detection — it means *this specific 4-scalar-summary encoding* of
   them carries no signal at this scale. A richer representation (e.g.
   per-frame detection sequences instead of aggregated counts, denser
   motion descriptors) has not been tried.
3. Still binary riot/normal only — same Protest-class data gap as every
   prior entry.

**Status:** Not superseded, but caveat 1's specific claim ("DINOv2 alone
beats full fusion") is **revised** by the multi-seed check entry directly
below, run the same day — read the two together. First result in this
project to identify which branch is actually responsible for a fusion
classifier's accuracy, rather than assuming the whole architecture is
jointly responsible; that finding (DINOv2 dominant, LK/RF-DETR contribute
nothing) stands. Only the finer point of whether DINOv2 alone beats
full fusion is walked back.

---

## 2026-09-27 — [REAL RESULT] Multi-seed check: DINOv2-only vs. full-fusion gap is noise, not a real effect

**What this is:** the robustness check the entry above explicitly queued
before treating "DINOv2 alone beats full fusion" as settled. Same
2831-clip full-scope dataset, same two feature sets (`dinov2_only`,
`full_fusion`), retrained across 6 different train/test split seeds
(`notebooks/ablation_fusion_branches.ipynb`, Step 5) instead of the single
split used above.

**Result:**

| branch group | mean accuracy | std | per-seed accuracies |
|---|---|---|---|
| dinov2_only | 97.21% | ±0.85% | 0.9577, 0.9683, 0.9683, 0.9841, 0.9753, 0.9788 |
| full_fusion | 97.24% | ±0.65% | 0.9806, 0.9753, 0.9612, 0.9753, 0.9665, 0.9753 |

Mean gap: **-0.03 percentage points** (full_fusion very slightly ahead on
average now, effectively reversed from the single-split result).
Average per-seed std: 0.75 percentage points — the gap is smaller than
the run-to-run noise.

**Revised conclusion:** the single-split finding that "DINOv2 alone beats
full fusion" does not hold up — across seeds the two are statistically
indistinguishable (~97.2% either way). The correct, defensible statement
is: **DINOv2 is clearly the dominant contributor (LK/RF-DETR alone remain
at the trivial baseline per the entry above, unaffected by this check),
but adding VideoMAE/LK/RF-DETR on top of DINOv2 neither reliably helps nor
reliably hurts** — not "fusion is worse," not "fusion is better," just
not measurably different from DINOv2 alone at this scale, with this MLP,
on this split methodology.

**Caveat:** only `dinov2_only` and `full_fusion` were re-checked across
seeds (the two closest contenders) — `videomae_only`, `dinov2_videomae`,
and the degenerate LK/RF-DETR groups were not re-run multi-seed, since
their single-split gaps were large enough relative to typical noise here
(multiple points, not fractions of a point) to not be in question.

**Status:** Not superseded. Revises the specific "DINOv2 alone wins"
claim from the entry directly above — read together, not in isolation.

---

## 2026-10-08 — [REAL RESULT] OpenCLIP added — DINOv2+VideoMAE+OpenCLIP fusion confirmed to beat DINOv2 alone (multi-seed)

**What changed:** per two direct requests (2026-10-05) — (1) rewrite the
LK branch to fix two verified bugs (no resize before flow computation,
motion only sampled from the first ~2-3 seconds of each clip), and (2)
add OpenCLIP (ViT-L-14, `open_clip`) as a new frozen-backbone branch,
pure brainstorm on whether another model could match/surpass DINOv2.
This entry covers (2) and its downstream results. (1) is **prepared but
not completed** — see caveat below.

**Dataset:** same 2831-clip full-scope set (485 riot, 2346 normal) as the
2026-09-27 entries.

**Part A — OpenCLIP branch ablation (single 80/20 split):**

| branch group | features | test accuracy | riot precision | riot recall |
|---|---|---|---|---|
| full_fusion (dinov2+videomae+openclip) | 2304 | **98.41%** | 0.978 | 0.928 |
| dinov2_openclip | 1536 | 98.24% | 0.958 | 0.938 |
| openclip_only | 768 | 98.06% | 0.939 | 0.948 |
| dinov2_only | 768 | 97.88% | 0.947 | 0.928 |
| dinov2_videomae | 1536 | 97.18% | 0.935 | 0.897 |
| videomae_only | 768 | 93.83% | 0.888 | 0.732 |

`lk_only`/`rfdetr_only`/`lk_rfdetr` not evaluated this run — their
feature file was incomplete (see caveat 1 below) and deliberately
excluded rather than merged in, since the ablation notebook's merge+
`dropna()` would otherwise have silently shrunk every group's sample to
~237 clips.

**Part B — multi-seed confirmation (6 seeds):** this time the fusion
result holds up, unlike the 2026-09-27 single-split finding that didn't
survive multi-seed testing.

| group | mean accuracy | std |
|---|---|---|
| full_fusion (dinov2+videomae+openclip) | **98.35%** | ±0.33% |
| dinov2_only | 97.21% | ±0.85% |

Gap: 1.15 points, exceeding the ~0.59-point average per-seed noise —
full_fusion won every one of the 6 seeds. Full tables, per-seed numbers,
and interpretation: `results/full_fusion_dinov2_videomae_openclip.md`.

**Interpretation — this changes the architecture story, not just the
number:** the 2026-09-27 conclusion ("fusion doesn't reliably help over
DINOv2 alone") was specifically about a fusion that included two
dead-weight branches (LK, RF-DETR, both at the trivial baseline). Swap
those for a second strong backbone (OpenCLIP) instead of padding with
non-contributing branches, and fusion *does* reliably help — a
genuinely different, more encouraging result than "one model does
everything."

**Caveats (read together, not separately):**
1. **The LK rewrite (fix 1 from 2026-10-05) is incomplete, not
   abandoned.** The re-extraction run was paused at 237/2831 clips to
   prioritize OpenCLIP (interrupting Colab for GPU-queue reasons);
   the partial file was renamed `_incomplete_lk_rfdetr.csv` on Drive so
   it wouldn't get silently merged into other ablation runs. It can be
   resumed later by renaming it back to `features_lk_rfdetr.csv` and
   re-running `feature_extraction_fusion.ipynb` with
   `BRANCHES = {'lk', 'rfdetr'}` — the resumability logic will pick up
   from clip 238 onward. Whether the LK fix actually gets `lk_only` off
   its 82.89%/0% riot-recall floor is **still an open, unanswered
   question** — nothing in this entry resolves it.
2. **Only the 2-group comparison (`dinov2_only` vs. this `full_fusion`)
   was multi-seed confirmed.** Whether `openclip_only` or
   `dinov2_openclip` individually beat `dinov2_only` robustly, or
   whether VideoMAE's presence in the winning combination is doing real
   work vs. just along for the ride (it's the weakest branch alone,
   93.8%), is not yet checked.
3. **This result is still not comparable to published XD-Violence
   benchmarks**, now with real numbers behind that caveat (previously
   stated in `docs/roadmap.md`, 2026-09-26, without specifics). Verified
   via the actual comparison table in a 2023 paper plus cross-checking
   other recent work: published SOTA is ~85-87% **frame-level Average
   Precision**, measuring all 6 XD-Violence violence classes lumped as
   one "abnormal" label against Normal, evaluated on the **800 official
   full untrimmed test videos**, trained **weakly-supervised** (only
   video-level labels). This project measures **clip-level accuracy**,
   **Riot only** vs. **pure Normal**, on **pre-trimmed clips**, with
   **direct clip-level supervision** — a narrower, materially easier
   sub-problem. The 98.35% here is not "beating" published ~87% AP; it's
   a strong result on a different, easier task. Matching the published
   protocol (frame-level, 6-class-lumped, untrimmed, weakly-supervised)
   would be substantially more work than anything built so far.

**Status:** Not superseded. First confirmed (multi-seed-validated)
evidence in this project that fusion of two strong backbones beats a
single strong backbone — contrast directly with the 2026-09-27 entries,
where fusion-with-dead-weight-branches did not.

---

## Known open issue carried across entries (not yet resolved)

**Fighting-prompt calibration bias**, first observed 2026-09-11, confirmed
in two independent real-data runs (RLVS-only and Capitol+RLVS). The
`fighting` prompt set in `src/config.py` scores systematically higher in
raw CLIP cosine similarity than other classes regardless of actual clip
content. Root cause not yet diagnosed (candidates: prompt phrasing/
specificity, known CLIP class-prior imbalance). No fix has been attempted
or verified yet — do not report a fix here until one has actually been run.
