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
