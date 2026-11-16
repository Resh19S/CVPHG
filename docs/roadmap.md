# Model Roadmap & Brainstorm

*Candidate ideas for future sessions — models beyond CLIP, model
combinations, and directions nobody has tried yet. Nothing on this page has
been run. This is not a result and not yet an endorsed plan — see
`findings.md` for verified results. When an item here actually gets run,
move it there (tagged MECHANICS CHECK or REAL RESULT) and delete or mark it
done here.*

---

## Up next — escalation-stage prediction pivot (decided 2026-11-09, current top priority)

**Why:** PI review of the fusion-architecture work said the architecture
itself isn't novel (frozen-backbone fusion is already published on XD-
Violence — see below) and asked for a live color-coded risk indicator.
Full reasoning and scope: `docs/context.md`, "Major pivot 2026-11-09."
This section is the research grounding and build plan; everything in the
"supervised fusion pipeline" section below this one is now background —
its confirmed findings (DINOv2/OpenCLIP strong, LK/RF-DETR not
contributing) carry forward into this pivot, but the clip-level
classification task itself is no longer the active target.

**Prior art checked before committing (verified directly, not assumed):**
- **Architecture-level fusion is not novel** — VadCLIP (AAAI 2024,
  84.51% AP on XD-Violence), AnomalyCLIP, and CLIP-TSA all use frozen
  CLIP-family embeddings for exactly this dataset/task already (see
  `docs/context.md`, 2026-10-08 entry for the full benchmark table).
- **Closest near-miss checked and ruled distinct:** a 2026 IJACSA paper
  ("Predicting Crowd Agitation from Raw Video") fuses frozen CLIP +
  Farneback optical flow into a continuous regressed risk score,
  thresholded — architecturally close to what was first considered. It
  trains on RLVS/RWF-2000/HockeyFight (small-scale one-on-one fight
  datasets, not crowd-scale riots) with labels its own limitations
  section calls "constructed," flagging subjectivity concerns. Not a
  per-window ordinal trajectory, no formal earliness metric, not
  crowd-scale.
- **Explicit confirmation the gap is real:** a CVPR 2023 paper (NWPU
  Campus benchmark) states directly that "weakly-supervised datasets
  such as UCF-Crime and XD-Violence are not designed for anticipation"
  — naming this exact limitation as their own motivation for building a
  different dataset.
- **Closest "lead-time on a real benchmark" hit:** "Latent Clarity"
  (2026 preprint) builds an actual lead-time protocol (offset windows
  0-5s before annotated onset) — but on **UCF-Crime**, not XD-Violence,
  and for general anomaly anticipation, not escalation staging or
  crowd/riot specifically.
- **Closest "XD-Violence + pre-event" hit, and a real risk to design
  around:** "Pre-Event Separability in Weakly-Supervised Violence
  Detection" (2026 preprint, uses XD-Violence) is a diagnostic, not a
  model — it found 39-91% of apparent pre-event separability on XD-
  Violence/UCF-Crime comes from non-content source artifacts (editorial
  title cards, platform watermarks), not genuine early signal. This is a
  real methodological risk for this pivot specifically and needs an
  explicit sanity check before any early-detection claim is trusted, not
  just a caveat after the fact.
- **Formal earliness metrics exist and should be adapted, not invented:**
  Minimum Observation Ratio (Furnari & Farinella, first-person action
  anticipation — the smallest observation fraction at which a correct
  prediction is first made) and Harmonic-Mean(Accuracy, 1-Earliness)
  from the early time-series classification literature (TEASER/
  MultiETSC lineage). Both transplant cleanly onto "how many seconds
  before the true onset did the model first flag Escalating."
- **Verdict:** the specific combination — ordinal 3-tier escalation
  staging, crowd-scale riot footage specifically, XD-Violence, a formal
  earliness metric — does not appear to already exist. Legitimate gap,
  not a rediscovery risk like the fusion-architecture question was.

**Reused components are not the novel contribution — flagged directly by
the user 2026-11-09, correctly.** DINOv2/OpenCLIP (reused), a generic
sequence model, and a generic MIL ranking loss applied to a new task is
still "a combination," not an architecture — the same critique Geetanjali
already gave once. Two specific, designed mechanisms (not generic
components) are what would make this defensible as actually novel, both
motivated by real, cited problems rather than invented for the occasion:
1. **An ordinal-constrained temporal head** — existing MIL-VAD models
   (RTFM, VadCLIP, etc.) score each snippet independently with no
   structural notion that risk should escalate monotonically. Building
   that constraint into the architecture (e.g. penalizing backward jumps
   from Critical to Normal mid-escalation) is a structural difference
   from how every published method in this space works.
2. **A source-artifact-invariance mechanism** — see the deep-research
   update directly below; this one is no longer optional.

**Sequencing decision, confirmed with the user 2026-11-09 — build the
plain version first, as an internal baseline, before investing in either
novel mechanism above.** Reasoning: if there's no exploitable escalation
signal in the data at all, no architectural cleverness saves it, and
that's cheaper to learn early. If the baseline does find signal, that's
when committing to (1) and/or (2) turns from a bet into the thing that
makes this publishable. **Do not present the plain baseline to Geetanjali
as the novel architecture** — it answers "is there something here," not
"what's new."

**Deep-research pass completed 2026-11-09 (full report: chat, not yet
filed as a doc — ask if a standalone copy is wanted). Verdict unchanged
and more confident under a much deeper search, but two things changed
the plan:**
- **Checked directly and ruled out:** "Can We Anticipate Violence?"
  (Penchala et al., arXiv 2609.40014) is real, uses XD-Violence, but is
  binary (Normal/Risky, no stages), reports no lead-time metric, and its
  features (facial region + body-motion keypoints) target
  individual/interpersonal risk, not crowd-scale. Does not overlap this
  project's gap.
- **The source-artifact confound is confirmed severe specifically on
  XD-Violence, not just a general risk — this elevates mechanism (2)
  above from optional to required.** The Pre-Event Separability paper's
  full numbers: on XD-Violence, even after length-matching normal
  controls, **70% of apparent pre-event separability survives** (down
  from 98% uncontrolled, still far above chance). A naive version of
  this pipeline would plausibly look like it detects early escalation
  while actually reading title cards and watermarks. Their length-matched
  control protocol needs to be run as a required validation step before
  trusting any early-detection result, not an optional sanity check.
- **Better lead-time metric identified than the MOR/harmonic-mean
  framework first proposed:** Achenchabe et al.'s cost-based ETSC
  criterion (`arXiv 2005.09945`) is the only verified early-classification
  metric that natively lets a missed/late critical alarm cost more than
  a premature one — the right asymmetry for riot warning (a false alarm
  is a nuisance; a missed riot is the actual failure mode). The deep
  research sketches a direct 3-tier ordinal extension of it (its
  "Proposal C") — adopt and cite that instead of inventing a metric from
  scratch.
- **Closest real neighbors, worth citing as related work, not a
  redirect:** AssistPDA (`arXiv 2503.21904`) pairs anticipation with
  XD-Violence and reports a lead-time number (Average Advance Time,
  29.19s) — but event-level, not crowd-specific, timestamps from a
  third-party annotation set, no formula given. RiskCueBench
  (`arXiv 2601.03369`) annotates a pre-incident risk cue specifically on
  protest footage (484 videos) — closest in spirit, but binary, not
  XD-Violence-based, and the paper's own numbers are internally
  inconsistent per the research notes.
- **Expectation-setting, not a blocker:** XD-Violence's original paper
  reports Riot as its own **weakest class** (70.54 AP RGB-only, 76.42
  with audio) among all 6 violence categories. This is a genuinely hard
  subproblem on its own terms, not an easy class picked for a demo.

**Sequencing changed by the user 2026-11-16 — build the novel
architecture now, not baseline-first.** Reason: window extraction was
running at ~22 s per clip (~800 of 2,831 clips after ~5 hours), and the
user did not want to spend another round-trip on a plain baseline before
seeing the real thing. What keeps this honest: the plain baseline was not
dropped, it became one **arm** of the same notebook (same data, same
seeds), so the "is there signal at all" question and the "does each
mechanism add anything" question are answered by the same run. The rule
from the 2026-11-09 decision still stands — the baseline arm is never
presented as the architecture.

**Architecture as built 2026-11-16
(`notebooks/escalation_stage_model.ipynb`). Built and tested on synthetic
data only — NOT yet run on real features; no result exists yet.**

Input: per-window DINOv2 + OpenCLIP embeddings (each L2-normalised,
concatenated, 1536-d), one window per second. Everything is causal (a
window's output uses only earlier windows), which a live indicator
requires and which keeps the lead-time evaluation honest.

1. **Ordinal stage filter (mechanism 1).**
   - Two evidence signals per window: *Critical evidence* ρ (causal GRU
     over absolute content) and *Escalation evidence* ε (a second causal
     GRU, see mechanism 2).
   - Rank-consistent ordinal emissions: P(Critical)=ρ,
     P(Escalating)=(1−ρ)ε, P(Normal)=(1−ρ)(1−ε).
   - Those go through the **forward filter of a 3-state HMM with a banded
     transition matrix** — Normal↔Escalating↔Critical only, so a clip
     cannot jump Normal→Critical without passing through Escalating. The
     filtered posterior is the green/amber/red output. Initial-state
     distribution is learned, because most riot clips start mid-riot (see
     the finding below).
   - Trained from video-level labels only: riot video → its top-k windows
     must reach Critical; normal video → nothing above Normal anywhere.
   - **Self-anticipation gives "Escalating" a testable meaning:** ε is
     trained to predict that the model's *own* Critical stage fires within
     `horizon_s` (10 s) — pseudo-onsets from MIL localisation, no frame
     labels. Windows already Critical are down-weighted, so riot-from-
     frame-0 clips do not inject an unlearnable target.
2. **Clip-referenced escalation pathway (mechanism 2).** ε is computed
   only from `x_t − mean(x_1..x_{t−1})` — how the current window differs
   from the running mean of the same clip. Anything constant across a clip
   (watermark, logo, letterbox, compression signature) cancels **by
   construction**; the amber light cannot be triggered by what a video
   looks like, only by how it is changing.
3. **Optional arm — medium adversary.** Gradient-reversal discriminator on
   the Critical pathway's per-window features, trained on normal videos
   only, predicting movie-vs-YouTube. Motivated by a measured imbalance:
   riot clips are 95% YouTube, normal clips ~52% (finding 2026-11-16).

**Why mechanism 2 is structural rather than the adversarial regulariser
first sketched on 2026-11-09 — a design change, stated plainly.** An
adversary needs a set of windows *inside riot videos* that are known to
be calm, to compare against normal videos. With video-level labels the
only candidate is "windows the model itself calls Normal", and on this
dataset 59 of 101 annotated riot test clips are riot from frame 0, so a
model that paints every riot video red from the start is never
contradicted and the adversary never engages. Clip-referencing needs no
such anchor and gives a guarantee instead of a penalty.

**Known limits of this design — do not paper over these:**
- Mechanism 2 protects the *Escalation* evidence only. The Critical
  pathway sees absolute content, like every published MIL detector, and
  can still lean on static source cues. The evaluation measures that
  ("far pre-onset" checks) rather than assuming it away.
- Clip-referencing removes *time-constant* signatures. A source that
  differs in its *dynamics* (e.g. news footage cuts more often than film)
  is not cancelled.
- If the footage before a riot is an unrelated shot (studio anchor → hard
  cut to riot), there is no precursor to find; expect zero lead on those
  clips regardless of architecture.
- On the synthetic check the medium adversary *raised* the Critical
  pathway's far-pre-onset separability (0.65 vs 0.47) — removing one
  static cue can push a model onto another. Treat `full_adv` as an
  experiment, not a default.

**Novelty status of the two mechanisms — spot-checked 2026-11-16, three
targeted searches, not exhaustive.** Building blocks all exist: HMMs,
ordinal regression (Pang et al., CVPR 2020, "Self-Trained Deep Ordinal
Regression for End-to-End Video Anomaly Detection" — ordinal regression
as a two-class surrogate for anomaly scoring, unsupervised, no stages or
time structure), HMMs inside weakly-supervised VAD (Sapkota & Yu, CVPR
2022 — an HDP-HMM that *partitions* a video into scene segments before
MIL; hidden states are scenes, not ordered severity stages),
gradient-reversal for cross-dataset VAD generalisation, and debiasing of
noisy MIL pseudo-labels (D²MIL, CVPR 2026). Not found: an
ordinal-staged, banded-transition filter as the scoring head of a
weakly-supervised detector; weak self-anticipation from the model's own
pseudo-onsets; clip-referenced features as a source-invariance device.
**Cite Pang et al. and Sapkota & Yu as related work and state the
difference; do not claim "first to use an HMM/ordinal anything."**

**Arms in the notebook (3 seeds each):** `baseline` (one causal GRU,
top-k MIL) · `ordinal_abs` (mechanism 1, ε from absolute features) ·
`full` (mechanisms 1+2) · `full_adv` (+ medium adversary).

**Evaluation in the notebook (official test split; thresholds from
validation normals only):** frame-level AP/AUC against `annotations.txt`;
per-onset outcome — *early warning* (alarm switches on during the calm
span, within 30 s of onset), *premature* (already on when the calm span
began, or earlier than 30 s — an always-amber light earns nothing),
*late*, *miss* — with median lead; an asymmetric average cost adapted
from Achenchabe et al. (missed riot = 5× a premature/false alarm); and
the confound check — AUC of each model's scores on calm windows *near*
(<10 s) vs. *far* (>20 s) before onset, against normal-video windows,
also against YouTube-only normals, plus the same numbers for a raw
per-window linear probe.

**Build plan:**
1. **DONE:** `notebooks/sliding_window_feature_extraction.ipynb`. Run
   partially by the user (~800 clips as of 2026-11-16: all riot, a random
   ~300 normals). Reworked 2026-11-16: batched embedding, single-pass
   read, queue reordered (riot → all test normals → train normals capped
   at `MAX_NORMAL_TRAIN = 600`), atomic writes. Reader/queue logic tested
   locally against the old seek-based reader; the batched embedders have
   **not** been run against the real models here.
2. **BUILT 2026-11-16, not yet run on real data:**
   `notebooks/escalation_stage_model.ipynb` — all four arms, training,
   evaluation, timeline plot.
3. **Next (user, Colab):** finish extraction of the test normals + the
   capped train normals, run the model notebook, paste back the summary
   table and the Step 1 counts.
4. **Then:** log the real result; decide from the arm comparison which
   mechanisms earned their place. If lead-time n (25 onsets) is too thin
   to separate arms, the cheapest fix is more annotated onsets — the
   other five XD-Violence violence classes' test clips have the same
   frame-level annotations and are not yet pulled.
5. **Not built:** the live overlay on a playing video. The static
   green/amber/red timeline (Step 8 of the notebook) exists.

---

## Background — supervised fusion pipeline (decided 2026-09-19, superseded as the active target by the 2026-11-09 pivot above)

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

**2026-10-05, queued per Hith's direct asks — status as of 2026-10-08:**
1. **LK branch rewrite** (`feature_extraction_fusion.ipynb`), targeting
   "can we get the dead-weight branches from ~83% toward ~90%":
   two verified fixes, not guesses — (a) frames are now resized to a
   fixed size before flow computation (the original never resized;
   raw pixel-magnitude flow wasn't comparable across clips of very
   different native resolutions — movie vs. YouTube sources), and
   (b) motion is now sampled from 3 windows spread across the clip
   (start/~40%/~80%) instead of only the first ~2-3 seconds from the
   start. Same 4-dim output schema, so the existing ablation groups
   keep working unmodified.
   **STILL NOT VALIDATED — re-extraction run paused at 237/2831 clips**
   (interrupted to prioritize OpenCLIP, see item 2). Partial file
   renamed `My Drive/CVPHG/fusion_features/_incomplete_lk_rfdetr.csv` so
   it doesn't get silently picked up by `ablation_fusion_branches.ipynb`'s
   glob. **To resume:** rename it back to `features_lk_rfdetr.csv`, set
   `BRANCHES = {'lk', 'rfdetr'}`, re-run `feature_extraction_fusion.ipynb`
   — resumability picks up from clip 238. Whether `lk_only` actually
   moves off the 82.89%/0%-riot-recall floor is **still an open,
   unanswered question.**
2. **OpenCLIP branch added** (ViT-L-14, `open_clip`, frozen, same
   sparse-frame-then-mean-pool pattern as DINOv2) — per the "pure
   brainstorm, could another backbone match/surpass DINOv2" question.
   **DONE AND CONFIRMED 2026-10-08:** `openclip_only` (98.06%) edges
   out `dinov2_only` (97.88%) on a single split (too small a gap to
   trust alone), but combining DINOv2+VideoMAE+OpenCLIP into one fusion
   (98.35% mean, multi-seed confirmed, +1.15pp over DINOv2 alone,
   exceeds noise) is a **real, validated improvement** — the first
   confirmed case in this project where fusion beats a single backbone.
   Full numbers: `docs/findings.md` (2026-10-08 entry),
   `results/full_fusion_dinov2_videomae_openclip.md`.
3. RF-DETR frame-count bump (4→12-16 sparse frames) was also discussed
   as a lever but **not requested yet** — only LK items (a)/(b) above
   and OpenCLIP were asked to be made ready. Revisit RF-DETR's own
   sparse-sampling blind-spot separately if/when asked.

**DONE 2026-10-09 — LK/RF-DETR re-extraction completed.** Verdict:
marginal improvement only, target (~90%) not met. `lk_only` riot recall
moved 0%→4.1%; `lk_rfdetr` combined actually got *worse* at catching
riots despite higher raw accuracy (F1 0.183→0.131 — accuracy alone was
misleading). Full numbers: `docs/findings.md` (2026-10-09 entry). These
two branches remain not worth their complexity as currently engineered;
closing the gap would need sequence modeling or dense flow, not more
tweaking of the current encoding — not attempted.

**DONE 2026-10-19 — comparability to published benchmarks, priority #1
per Hith's reordering.** `notebooks/apples_to_apples_eval.ipynb` closes 2
of 3 gaps: real official train/test split (not a resample) + real
frame-level AP against official ground truth. **Result: 85.45% AP**,
inside the published cluster (VadCLIP 84.51%–DSANet 86.95%). Remaining
gap (all 6 classes lumped, weakly-supervised) is a separate, larger
build — not started, not currently planned unless requested. Full
numbers: `docs/findings.md` (2026-10-19 entry), `results/
apples_to_apples_frame_level_ap.md`.

**Immediate next steps, not yet run — priority #2 per Hith's reordering:**
1. **Sequence modeling or dense flow for LK/RF-DETR**, now that
   incremental fixes are confirmed insufficient — feed per-frame-pair
   values to a small GRU/1D-CNN instead of collapsing to mean/max, or
   try dense Farneback flow instead of sparse LK.
2. **Isolate which part of the OpenCLIP win matters**: multi-seed check
   was only run for `dinov2_only` vs. the 3-way `full_fusion` — not yet
   confirmed whether `openclip_only` or `dinov2_openclip` (2-way) alone
   are robust improvements, or whether VideoMAE's presence in the
   winning combo is doing real work (it's the weakest branch alone,
   93.8%) vs. just coming along for the ride.
3. **Full published-protocol match** (all 6 classes lumped,
   weakly-supervised MIL training) remains the only way to close the
   last comparability gap — substantially bigger build, not started.

**Deferred, lower priority:**
- **RF-DETR → YOLO swap** (mechanical): moot while RF-DETR's branch
  itself isn't contributing regardless of which detector produces it —
  revisit once the LK/RF-DETR dead-weight question above is resolved.

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
