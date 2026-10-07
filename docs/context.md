# Project Context

*Update this file only when the plan, scope, or dataset situation actually
changes — not after every code change or pipeline run. For that, see
`findings.md`.*

## PI and broader direction

PI: **Geetanjali Bhola** (University of Delhi, Faculty of Technology). This
work extends a previously published stampede-detection paper (CNN-LSTM +
Farneback optical flow, *Scientific Reports*, 2026), which classified crowd
states into a 4-class risk taxonomy (normal/moderate/dense/risky) using
hand-crafted motion features.

The new project phase moves toward **multimodal zero-shot learning (ZSL)**
for crowd analysis:
- Adding **audio** as a second modality (not yet started).
- An activity-pattern angle connected to group-activity-recognition
  literature (CVPR-adjacent).
- Eventual dataset plan involves real-world protest footage referred to
  internally as **"the CJP dataset"**. Anonymization/ethics considerations
  have been flagged separately by the team and are explicitly **out of
  scope** for the current scaffold work.

## Why riot/protest detection before fire

The idea that got traction with Geetanjali: protests can escalate — a
peaceful protest turns violent, and the crowd sometimes retaliates by
setting vehicles on fire. Fire in this context is framed as a potential
**leading indicator of escalation** (ideally detected as, or before, it
starts), tying into the same "anticipate before full crowd panic" logic as
the original stampede-detection work.

**Hith's call:** perfect riot/protest detection first; add fire /
burning-vehicle as a second phase only once the base capability is solid.
All current scaffolding is structured (config-driven class list in
`src/config.py`) so a `fire` / `burning_vehicle` class can be added later
without refactoring extraction, classification, or evaluation code — but it
has **not** been added yet, by design.

## XD-Violence status

**Status as of 2026-09-18: riot (B4) class obtained. Normal/negative class
not yet pulled.**

The dataset's own site (https://roc-ng.github.io/XD-Violence/) is still
gated behind a request form / OneDrive-style manual bulk download — that
part of the earlier assessment was correct. What changed: a public,
ungated HuggingFace mirror of the same dataset was found
(`jherng/xd-violence`), serving individual files over plain HTTPS with no
auth and no request process. Verified directly (not assumed): two sample
files test-downloaded successfully (200 OK, valid MP4) before committing to
a full pull.

**What's actually in hand now:** all 485 riot (B4)-labeled clips across the
full dataset (train + test splits combined; verified against every video
directory in the HF repo, not just a subset), 9.78 GiB total, downloaded via
`notebooks/xdviolence_riot_pull.ipynb` and validated 485/485 clean — exists
on disk, correct size, opens in OpenCV, first frame readable. Stored on
Google Drive at `My Drive/CVPHG/xdviolence_riot/` (not local, and not yet
copied into this project's `data/` directory), alongside
`manifest_xdviolence_riot.csv` (id/label/split/size/url).

**Not yet done:** the Normal/negative class from XD-Violence itself hasn't
been pulled — the same HF-mirror approach should work for it (list the
video dirs, filter for the `A` label code instead of `B4`), just not run
yet. Until that happens, real-riot-vs-real-normal evaluation still needs
either the RLVS `NonViolence` stand-in (see below) or a fresh XD-Violence
Normal pull.

The two stand-in datasets used while XD-Violence access was blocked are now
partially superseded on the positive-class side:
1. **RLVS** (Real Life Violence Situations, via Kaggle) — its `Violence →
   riot` proxy mapping was already superseded (see `findings.md`); its
   `NonViolence` clips remain the only real negative class currently paired
   with real riot footage, pending an XD-Violence Normal pull. **Local
   copy deleted 2026-09-14** (freed ~152 MiB) — would need
   re-downloading via `scripts/build_rlvs_manifest.py` if used again.
2. **US Capitol riot footage** (Kaggle `jpmiller/protests-against-police-
   violence`) — was the real riot-positive stand-in; now superseded by the
   actual XD-Violence riot (B4) clips above as the primary riot source.
   **Local copy deleted 2026-09-14** (freed ~4.7 GiB) — would need
   re-downloading via `scripts/build_capitol_manifest.py` if used again
   (e.g. as a secondary/cross-dataset check).

**Update this section the moment** the XD-Violence Normal class is pulled,
or the riot clips are copied from Drive into this project's `data/`
directory, since either changes what "the real benchmark" actually is.

## Supervised fusion track (added 2026-09-19)

Alongside the zero-shot CLIP work above (which continues as-is, not
replaced), the project now also has a **supervised** track: motion branch
(Lucas-Kanade optical flow) + visual branch (RF-DETR detection + DINOv2 +
VideoMAE embeddings) fused and fed to a trainable classifier head (MLP
first, Transformer later). This was a deliberate scope decision, confirmed
with the user 2026-09-19 — not an accidental drift from the zero-shot
framing. Full decision record, including the RF-DETR/YOLO and MLP/
Transformer sequencing and the still-unresolved "Protest" class data-source
gap, is in `docs/roadmap.md` under "Up next — supervised fusion pipeline".

## Compute environment

Local: dual-boot Fedora/Windows laptop, AMD GPU (no CUDA) — pipeline runs on
CPU locally. Written to also run unmodified in Google Colab (GPU runtime,
Colab Pro) for heavier future passes (full untrimmed XD-Violence, audio
processing). As of 2026-09-11, every real-data pass run so far (RLVS,
Capitol) has been small enough to run comfortably on the local CPU in under
a minute — Colab has not actually been needed yet.

**Project location (moved 2026-09-12):** the project now lives at
`/home/resh/projects/CV research hith` on the Linux (`/home`) filesystem,
**not** `/mnt/windows/projects/CV research hith`. It was moved because the
Windows mount (`/mnt/windows`, NTFS, 334G total) ran down to ~6.7GB free
partway through scaling up the Capitol riot-clip download; `/home` has
~91GB free as of the move. The old `/mnt/windows/...` copy was deleted
after verifying an identical `rsync` copy — it no longer exists. **If a
future session finds itself operating under `/mnt/windows/...`, that's
stale — the real project is under `/home/resh/projects/...`.**

Practical consequences of the move, already handled but worth knowing:
- The Python venv does **not** survive a directory move (absolute paths
  baked into `.venv/bin/activate`) — it was recreated from scratch at the
  new location (`python3 -m venv .venv && pip install -r requirements.txt`).
  If the project moves again, redo this rather than trying to move `.venv`.
- All manifest CSVs (`data/manifest*.csv`) store **absolute filepaths** —
  these were rewritten from the old `/mnt/windows/...` prefix to the new
  `/home/resh/...` prefix and verified (every row's file confirmed present
  at its new path). If paths ever go stale again after another move, fix
  the manifest CSVs' `filepath` column directly (a simple prefix swap) or
  regenerate via the `build_*_manifest.py` scripts.
- Kaggle credentials (`~/.kaggle/access_token`) live outside the project
  directory and were unaffected by the move.

## Published XD-Violence benchmarks vs. this project's task (added 2026-10-08)

**This project's accuracy numbers (currently ~97-98%) are not directly
comparable to published XD-Violence SOTA results (~85-87% AP), and
presenting them side by side without this context would be misleading.**
Checked directly (not assumed) via the actual comparison table in a 2023
paper ("Weakly-Supervised Video Anomaly Detection with Snippet Anomalous
Attention," arXiv:2309.16309) plus cross-checking other recent work —
current best found: DSANet at 86.95% AP; other recent methods (ReFLIP
85.81%, TCVADS 85.58%, VadCLIP 84.51%) cluster in the low-to-mid 80s.

**The published task is a different, harder problem, not a worse version
of the same one:**
- **Metric:** frame-level Average Precision (a precision-recall curve
  over every frame), not clip-level classification accuracy.
- **Classes:** all 6 XD-Violence violence classes (Abuse, Car Accident,
  Explosion, Fighting, Riot, Shooting) lumped together as one "abnormal"
  label against Normal — not Riot specifically vs. Normal.
- **Input:** the 800 official full **untrimmed** test videos — the model
  must locate *where* in a long, multi-scene video an anomaly occurs.
  This project classifies already-**pre-trimmed** clips, isolated to the
  event in advance.
- **Supervision:** published methods train **weakly-supervised** (only a
  video-level "contains an anomaly somewhere" label). This project
  trains on direct, already-correct clip-level labels.

**What would be needed to produce a genuinely comparable number:**
reframe as frame-level anomaly localization over the official untrimmed
test set, with all 6 classes lumped as "abnormal," trained weakly-
supervised — a substantially larger undertaking than the current
clip-level binary classifier. Not started, not currently planned unless
explicitly requested.

**How to talk about current results until/unless that's built:** as "a
strong result on a well-defined, narrower sub-problem" (Riot vs. Normal,
pre-trimmed, directly supervised) — never as "beats published SOTA,"
since the tasks aren't the same thing.
