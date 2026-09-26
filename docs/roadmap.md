# Model Roadmap & Brainstorm

*Candidate ideas for future sessions — models beyond CLIP, model
combinations, and directions nobody has tried yet. Nothing on this page has
been run. This is not a result and not yet an endorsed plan — see
`findings.md` for verified results. When an item here actually gets run,
move it there (tagged MECHANICS CHECK or REAL RESULT) and delete or mark it
done here.*

---

## Up next — supervised fusion pipeline (decided 2026-09-19)

**Scope change, confirmed with the user 2026-09-19:** this project now has
a second, explicitly supervised track alongside the original zero-shot CLIP
work (which stands as-is, not replaced). Motion branch (Lucas-Kanade
optical flow) + visual branch (object detection + generic frame embedding
+ video-native action embedding) fused and fed to a trainable
classification head. Diagram source: pasted into chat 2026-09-18, drawn by
someone else on the team.

**Confirmed decisions (do not re-litigate without a new instruction):**
- **RF-DETR first, YOLO later.** The diagram's visual-detection box said
  YOLO; RF-DETR runs first (already had a mechanics-check notebook before
  this was raised) since swapping RF-DETR -> YOLO later is a mechanical
  change, not an architecture change.
- **MLP head first, present those results, Transformer head after.** Not
  a simultaneous dual-head ensemble — sequential, MLP results reviewed
  before starting the Transformer variant.
- **Binary riot/normal only, for now.** The diagram's 3rd class
  ("Protest", peaceful/pre-escalation) has **no identified data source**.
  Checked directly 2026-09-19: the Kaggle
  `jpmiller/protests-against-police-violence` dataset — the only
  protest-named dataset already in this project — is 744/748 files real
  Capitol riot footage, the remaining 4 are non-video metadata
  (`protests.csv`, `press_incidents.csv`, a PDF codebook, a `.tab` file).
  It cannot supply peaceful-protest video. Finding a real source for this
  class is still open and blocks the diagram's full 3-way target.
- **Runs in Colab on a T4**, reading data straight from Drive (matches how
  the riot/normal pulls already work) — not local, not CPU.

**Pipeline built 2026-09-19, run the same day — DONE, results logged:**
1. `notebooks/xdviolence_normal_pull.ipynb` — Normal (A-label) class,
   capped to a seeded 485-clip sample (matched 1:1 to the riot class; full
   Normal class is 2346 clips / 53.4 GiB, deliberately not all pulled). Run
   successfully.
2. `notebooks/feature_extraction_fusion.ipynb` — per clip: LK flow summary
   stats + RF-DETR person/vehicle counts + DINOv2 frame embedding
   (mean-pooled) + VideoMAE clip embedding, concatenated into one fused
   vector. Run successfully over all 970 clips.
3. `notebooks/mlp_fusion_classifier.ipynb` — trained/evaluated an MLP
   (256,64 hidden units) on the fused features, riot vs. normal: **92.27%
   test accuracy**, balanced precision/recall both classes. See
   `docs/findings.md` (2026-09-19 entry) and `results/
   mlp_fusion_riot_normal.md` for the full numbers and caveats.

Note: the Drive-hosted riot/normal clips and intermediate feature CSVs were
deleted after this run to free Drive storage (see chat 2026-09-19) — they
are reproducible on demand via the seeded pull notebooks, not gone for
good, but don't assume they're sitting on Drive ready to reuse without
re-running the pulls first.

**Scope change 2026-09-26 — train on the full Normal class, not the capped
485-clip sample.** Direction from Hith's brother: train fully on
XD-Violence so the architecture is comparable to published results, not
just internally. `xdviolence_normal_pull.ipynb`'s `TARGET_COUNT` default
changed from `485` to `None` (full class — 2346 clips, 53.4 GiB). Real
consequences of this, not glossed over:
- **Class imbalance:** 2346 normal vs. 485 riot (~4.8:1), not the balanced
  1:1 set the 92.27% result was measured on. `mlp_fusion_classifier.ipynb`
  and `ablation_fusion_branches.ipynb` now report balanced accuracy
  alongside raw accuracy for this reason — raw accuracy alone is
  misleading here (always predicting "normal" already scores ~83%).
- **Storage:** full scope is ~63 GiB combined (riot + normal) vs. the
  ~19.5 GiB that already forced a paid Drive upgrade. Confirm the current
  plan has headroom before running the pull.
- **Comparability caveat, not yet resolved:** pulling the full Normal
  class is necessary but not sufficient for genuine comparability to
  published XD-Violence benchmarks. Most published baselines on this
  dataset (a) use the dataset's official train/test split specifically
  (not a fresh random 80/20 over a re-pooled sample) and (b) report
  frame-level Average Precision on the anomaly-detection task, not
  whole-clip accuracy on a riot-vs-normal binary split. Matching either
  of those would be more work than what's built so far — flagging this
  now so "comparable to others' results" isn't assumed true just because
  the full class was pulled.

**DONE 2026-09-27 — branch ablation ran at full scope, then confirmed
multi-seed.** DINOv2 is clearly the dominant contributor — LK and RF-DETR
(as currently engineered — 4 scalar summary stats each) carry zero
riot-discriminating signal at this scale, confirmed stable, not a
single-split fluke. **Revised from the initial single-split read:**
"DINOv2 alone beats full fusion" did NOT hold up across a 6-seed check
(dinov2_only 97.21%±0.85% vs. full_fusion 97.24%±0.65% — statistically
tied, gap smaller than the noise). Correct conclusion: DINOv2 dominates;
adding VideoMAE/LK/RF-DETR on top neither reliably helps nor hurts. Full
numbers: `docs/findings.md` (two 2026-09-27 entries, read together),
`results/branch_ablation_full_scope.md`.

**Immediate next steps, not yet run:**
1. **Decide what to do about LK/RF-DETR being dead weight.** Two honest
   options, not mutually exclusive: (a) improve their feature
   representation (currently just 4 aggregated scalars each — try
   per-frame detection sequences, richer motion descriptors) before
   concluding they're fundamentally uninformative, or (b) accept DINOv2
   alone as the strongest/cheapest option found so far and stop carrying
   the other branches by default just because the original diagram
   included them.
2. **RF-DETR → YOLO swap** (mechanical, deferred, lower priority now):
   swapping the detection branch doesn't matter much if that branch
   isn't contributing regardless of which detector produces it — worth
   revisiting only after (2) above is resolved.

## Other single-model candidates to test (not yet run)

- **Larger/other OpenCLIP backbones** (ViT-L-14, ViT-H-14 laion2b, etc.) —
  same zero-shot method as now, just a bigger encoder. Cheapest thing to
  try first: swap `CLIP_MODEL_NAME`/`CLIP_PRETRAINED` in `src/config.py`
  and re-run against the existing n=200 Capitol+RLVS benchmark to see if
  riot recall improves or the `fighting`-bias persists at scale.
- **SigLIP** — sigmoid-loss CLIP variant, known to calibrate differently
  across classes than softmax-style CLIP. Directly relevant to the
  confirmed prompt-calibration bias in `findings.md` — worth testing
  whether that bias is specific to CLIP ViT-B-32 or a more general
  zero-shot artifact.
- **ImageBind / LanguageBind** — joint video+audio+text embedding space.
  Relevant because audio is the next planned modality (`context.md`); could
  replace a separately-built audio pipeline with one already-aligned model.
- **VideoMAE / InternVideo / VideoCLIP** — true video-native (temporal)
  encoders, vs. the current per-frame-then-mean-pool approach in
  `src/frame_extraction.py`. Could pick up motion cues the current
  pipeline can't, and connects to the activity-pattern/group-activity-
  recognition angle in `context.md`.
- **BLIP-2 / LLaVA-style VLM prompting** — ask a vision-language model
  directly ("does this look like a riot?") instead of ranking cosine
  similarity against class text embeddings. Different failure mode than
  the current argmax-over-similarity method, worth comparing.

## Combination / ensemble ideas (not yet tried)

- **CLIP + Farneback optical flow**, fused as two independent signals —
  the most direct bridge back to the PI's original stampede-detection
  method (CNN-LSTM + Farneback), since that motion-feature approach is
  already published and validated.
- **Prompt ensembling via majority vote** instead of averaging prompt text
  embeddings (current method) — score each prompt independently, vote,
  rather than blend embeddings first. Might reduce the fighting-bias
  differently than just rewording prompts would.
- **Per-class score calibration** (temperature scaling or per-class
  threshold) instead of raw argmax over cosine similarity — a cheap thing
  to try before or alongside swapping models, given the bias is confirmed
  to be a calibration issue, not a content-understanding failure.
- **Late fusion of video-CLIP + audio-CLIP scores** once audio is added —
  simple weighted average or logistic combination as the first pass,
  before anything more architecturally complex.

## Brainstorm — directions nobody has tried yet

- Test whether the fighting-bias is tied to the specific prompt template
  ("a photo of X") by trying alternate templates ("a video of X", "this is
  X", "footage showing X") and comparing bias magnitude.
- A few-shot linear probe on frozen CLIP embeddings using the labeled real
  clips already on hand (150 Capitol + 50 RLVS) — still not full
  fine-tuning, just a linear head, cheap enough to run on CPU locally.
- Ablate whether the "riot" score is driven by actual scene content (crowd
  density, smoke, signage) vs. incidental correlates (vertical mobile-video
  aspect ratio, compression artifacts) by testing on cropped/reformatted
  copies of the same clips.
- Apply group-activity-recognition literature's spatial-relational models
  to riot detection — the activity-pattern angle from `context.md`,
  currently just a literature pointer, not investigated at all yet.
- Sub-segment labeling within a single riot clip (calm opening moments vs.
  escalation moments) to test an "early warning" framing analogous to the
  original stampede paper's premise — **no longer fully blocked**: Hith's
  brother raised this exact idea 2026-09-26 ("tell when a protest/riot is
  starting, via a threshold over segments"), and a concrete partial lead
  already exists — `annotations.txt` (fetched directly from
  roc-ng.github.io while investigating the XD-Violence access path, see
  the 2026-09-18 findings entry) has frame-level start/end intervals per
  anomaly, but **only for the `test_videos` split** (800 clips, not the
  full 4750). Training clips only carry a whole-clip label baked into the
  filename, no frame-level timing. Worth checking whether the test-split
  intervals alone (101 riot clips) are enough to prototype a threshold/
  onset detector before deciding whether train-split labels need to be
  created by hand. Explicitly deferred as its own phase ("work
  independently for now, integrate later") — not blocking the current
  clip-level fusion classifier work.

## Status

Nothing above has been run or approved for compute spend — check with
Geetanjali/Hith before committing time to any specific item. This list
exists so ideas aren't lost between sessions, not as a committed plan.
