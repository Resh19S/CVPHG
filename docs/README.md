# /docs — How This Folder Works

This folder tracks project state across sessions, separately from code.
Five files, each with one job — don't duplicate content across them.

- **`context.md`** — the stable project picture: PI (Geetanjali Bhola), the
  broader multimodal zero-shot crowd-analysis direction, why riot/protest
  detection comes before fire/burning-vehicle detection (Hith's call), and
  the current status of the XD-Violence dataset request. Update this only
  when the plan, scope, or dataset situation actually shifts — not after
  routine code changes or pipeline runs.

- **`findings.md`** — the append-only, chronological log of every verified
  result from an actual pipeline run. Never edit or delete old entries;
  superseded ones stay in place, marked `Status: superseded by <entry>`.
  Every entry is tagged either **[MECHANICS CHECK]** (validates the
  pipeline runs — synthetic clips, or a proxy dataset like RLVS standing in
  for a real target class — not a research result) or **[REAL RESULT]**
  (run against the actual target dataset/class for the question being
  asked). Every entry states the dataset used, what was measured, the
  actual number, and any caveat that changes how the number should be read
  — caveats are never softened or omitted to make a result look cleaner.

- **`my_notes_plain_english.md`** — a plain-English translation of
  `findings.md`, written for explaining status out loud in a meeting: no
  jargon, no hedge-words a non-technical listener would trip on, but still
  accurate to what `findings.md` says. Updated every time `findings.md`
  gets a new entry.

- **`paper.md`** — any text drafted toward an eventual paper/write-up.
  Every section is tagged `[DRAFT — supported by verified findings]` or
  `[DRAFT — speculative, not yet supported by results]`. No claim here may
  outrun what `findings.md` backs up without the speculative tag, and if a
  supporting finding later gets superseded, the affected section must be
  flagged, not silently left as-is.

- **`roadmap.md`** — candidate ideas for future work: other models to test
  beyond CLIP, model-combination/ensemble ideas, and open brainstorm items
  nobody has tried yet. Nothing here is a result. When an item actually
  gets run, move it to `findings.md` (tagged appropriately) rather than
  leaving stale duplicate status in both places.

## The one rule that matters most

**Never let any file in this folder state something more confidently than
what was actually run and verified.** When in doubt, tag down (mechanics
check instead of real result; speculative instead of supported) rather than
up. After any session that produces a new result, a bug fix that changes
prior results, or a scope/plan change, update the relevant file(s) here
before the session ends — don't let this folder go stale.
