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

**Status:** Not superseded. First supervised (non-zero-shot) result in this
project. Does not replace or invalidate the zero-shot CLIP track above —
a separate, deliberately-added track (see `docs/context.md`, "Supervised
fusion track").

---

## Known open issue carried across entries (not yet resolved)

**Fighting-prompt calibration bias**, first observed 2026-09-11, confirmed
in two independent real-data runs (RLVS-only and Capitol+RLVS). The
`fighting` prompt set in `src/config.py` scores systematically higher in
raw CLIP cosine similarity than other classes regardless of actual clip
content. Root cause not yet diagnosed (candidates: prompt phrasing/
specificity, known CLIP class-prior imbalance). No fix has been attempted
or verified yet — do not report a fix here until one has actually been run.
