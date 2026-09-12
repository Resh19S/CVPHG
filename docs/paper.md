# Paper / Write-up Draft Notes

*Every section below must be tagged `[DRAFT — supported by verified
findings]` or `[DRAFT — speculative, not yet supported by results]`. If a
claim stops being supported (e.g. its source finding gets superseded in
`findings.md`), flag it here rather than silently leaving it. No actual
paper drafting has happened yet as of 2026-09-11/12 — this file is a
skeleton, populated only with what's already defensible from
`findings.md`, ready to receive real drafted text in future sessions.*

---

## Motivation / framing

`[DRAFT — speculative, not yet supported by results]`

No text drafted yet. Likely direction (not yet written, not yet backed by
any run): framing riot/protest escalation detection as an extension of the
prior stampede-detection work's "anticipate before full crowd panic" logic,
with fire/burning-vehicle as a later-phase leading indicator (per
`docs/context.md`). This is project framing, not a result — do not cite
findings.md in support of this paragraph until it's actually written.

## Related work

`[DRAFT — speculative, not yet supported by results]`

Not started. Placeholder for stampede-detection paper (CNN-LSTM +
Farneback optical flow, *Scientific Reports*, 2026), CLIP zero-shot
literature, XD-Violence / RLVS dataset papers, group-activity-recognition
literature.

## Method

`[DRAFT — supported by verified findings]`

Zero-shot classification of short video clips using CLIP (ViT-B-32, openai
pretrained weights, unmodified — no fine-tuning): N evenly-spaced frames
extracted deterministically per clip, each frame embedded, mean-pooled
cosine similarity against per-class text-prompt embeddings, argmax over
classes. This is exactly what has been implemented and run
(`src/zero_shot_classifier.py`, `src/frame_extraction.py`) — see
`findings.md` for the three runs executed against this method so far.

## Preliminary results

`[DRAFT — supported by verified findings]`

**Updated 2026-09-12 — the n=30 figures below were superseded same-day by a
5x scale-up check; numbers revised accordingly, claim direction unchanged.**
On a real riot-footage benchmark (150 real US Capitol riot clips vs. 50 real
non-violent street-scene clips, zero-shot, no fine-tuning), the riot class
was correctly identified with 0.99 precision and 0.93 recall (140/150
correct). This held up — and if anything strengthened — from an initial
smaller check at n=30 (0.93 precision / 0.90 recall), which is meaningful:
it indicates the result is a robust signal, not a small-sample artifact.
Backed by `findings.md` REAL RESULT entries 2026-09-11 ("US Capitol riot
footage + RLVS NonViolence") and 2026-09-12 ("Scale-up check: 150 Capitol
riot clips").

`[DRAFT — supported by verified findings]`

The same n=200 run's overall accuracy (71.00%) is substantially lower than
the riot-class numbers above and should not be reported without the
accompanying caveat: a prompt-calibration bias causes the `fighting` class
to be over-predicted regardless of actual content, which suppresses
`normal`-class recall to 0.04 (unchanged from the n=80 check — same 50
normal clips, same result, confirming the bias is stable). Additionally,
71% vs. the earlier run's 36.25% is a sample-composition effect (riot clips,
which the model gets right ~93-99% of the time, now make up 75% of the
sample instead of 37.5%) — not model improvement. If this file ever states
an overall-accuracy number for either benchmark, it must carry both caveats
inline — do not report the accuracy figure alone, and do not compare the
two overall-accuracy numbers to each other without explaining why they
differ.

`[DRAFT — speculative, not yet supported by results]`

No claim can yet be made about performance against XD-Violence itself
(request still pending, per `docs/context.md`), against audio-augmented
detection (not started), or against fire/burning-vehicle detection (phase 2,
not started).

## Limitations (for eventual write-up)

`[DRAFT — supported by verified findings]`

- No fine-tuning has been performed anywhere in this project — all results
  are zero-shot.
- The current real-data benchmark's negative class (RLVS `NonViolence`) is
  a stand-in, not XD-Violence's own Normal class or genuine
  protest-that-stayed-peaceful footage.
- A known, twice-confirmed prompt-calibration bias affects the `fighting`
  class and has not yet been fixed (see `findings.md`, "Known open issue").

## Open items before any claim here can be strengthened

- [ ] Resolve XD-Violence access and re-run against the actual target
      dataset.
- [ ] Diagnose and fix the `fighting` prompt-calibration bias, re-run, and
      update the precision/recall/accuracy figures above accordingly.
- [ ] Add fire/burning-vehicle as a class (phase 2, per Hith's direction) —
      not before riot/protest detection is considered solid.
