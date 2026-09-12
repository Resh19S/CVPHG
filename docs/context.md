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

**Status as of 2026-09-11: request pending / not yet obtained.**

XD-Violence (https://roc-ng.github.io/XD-Violence/) is the intended primary
benchmark dataset (Riot class + negative classes). It is gated behind a
request form / OneDrive-style manual bulk download, not a stable scripted
download URL — confirmed directly, not assumed. As of the last check, the
annotation file has not been downloaded and no XD-Violence clips have been
fetched into this project.

Because of this, two real-world **stand-in** datasets have been used to get
real-data signal while the XD-Violence request is pending:
1. **RLVS** (Real Life Violence Situations, via Kaggle) — used first as a
   `Violence → riot` proxy (superseded — see `findings.md`), and currently
   still used for its `NonViolence` clips as a real negative class.
2. **US Capitol riot footage** (Kaggle dataset
   `jpmiller/protests-against-police-violence`) — real Jan 6, 2021 riot
   video, now the real positive class for riot detection. This dataset
   ships **no negative class and no per-clip labels** (verified directly
   against its accompanying CSV/metadata files, not assumed).

**Update this section the moment the XD-Violence request status changes**
(approved / rejected / data obtained), since it changes which dataset is
the "real result" target vs. a stand-in.

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
