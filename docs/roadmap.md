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

**Immediate next step, not yet run:** branch ablation (DINOv2+VideoMAE
alone vs. LK+RF-DETR alone) to find out which branch is actually driving
the 92.27% — flagged as a real open question in the findings entry, not
yet answered.

- **RF-DETR → YOLO swap** (mechanical, deferred): once the RF-DETR-based
  pipeline above is validated, swap `rfdetr` for a YOLO model in
  `feature_extraction_fusion.ipynb`'s detection step and re-run to compare.

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
  original stampede paper's premise — blocked on whether that granularity
  of labels exists or would need to be created by hand.

## Status

Nothing above has been run or approved for compute spend — check with
Geetanjali/Hith before committing time to any specific item. This list
exists so ideas aren't lost between sessions, not as a committed plan.
