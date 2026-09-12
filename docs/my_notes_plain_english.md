# My Notes — Plain English

*A running translation of `findings.md` for talking out loud in a meeting.
No jargon, no hedge-words that would trip someone up. Update this every
time `findings.md` gets a new entry.*

---

## Where things stand (as of 2026-09-12)

We're testing whether an off-the-shelf AI model (CLIP) can recognize a riot
or protest turning violent, just by describing what a riot looks like in
plain sentences — no training involved, we're not teaching it anything, just
asking it "does this look more like a riot, a normal scene, or a fight?"
and seeing what it picks.

### Test 1 — "does the code even work?" (not a real result)

First we ran it on fake, computer-drawn test clips (colored dots moving
around) just to make sure the whole pipeline — read video, ask the model,
score the answer — runs without crashing. It got about 1 in 3 right, but
that number means nothing, because the clips aren't real footage of
anything. This was purely a plumbing check.

### Test 2 — real fight videos standing in for riots (a stand-in, not the real test)

We didn't have real riot footage yet, so we borrowed a public dataset of
real street-fight videos and used the "fight" clips as a rough stand-in for
"riot," and calm street-scene clips as the "normal" comparison. This got
almost nothing right (2%) — but not for the reason you'd think. Two things
went wrong:
1. A fistfight between two people isn't really the same thing as a crowd
   riot, so it's not surprising the model called them "fighting" instead of
   "riot" — that's actually a fair answer on the model's part, we just asked
   the wrong question.
2. More concerning: even the *calm, nothing-happening* clips got called
   "fighting" most of the time. That's a real problem with how we worded
   the "fighting" description we gave the model — it seems to just have a
   thumb on the scale for that one option no matter what's actually in the
   video. We haven't fixed this yet.

### Test 3 — real riot footage vs. real calm footage (our first real test)

We then got real footage of the January 6th Capitol riot and paired it with
real calm street-scene videos (from the same dataset as test 2). This time,
recognizing the actual riot footage as a riot worked well — it got about
9 out of 10 real riot clips right. That's the first genuinely encouraging
result: the model really can tell riot footage apart from other things when
we give it real riot footage.

But the same "fighting" bias from test 2 is still there — the model called
almost all the calm clips "fighting" instead of "normal," which is why the
overall score still looks low (about 1 in 3 overall) even though the riot
part is working well. So the honest summary is: **riot detection is working;
we have one specific, already-identified wording problem dragging the
overall number down, and we know exactly what to fix next.**

### Test 4 — same test, 5x more real riot clips (does it still hold up?)

Test 3 only used 30 real riot clips, which is a small sample — good enough
to be encouraging, not enough to be confident. So we reran the exact same
comparison with 150 real riot clips instead of 30 (same 50 calm clips as
before, unchanged). If test 3 had been a lucky small sample, this would
have shown it.

It didn't — the riot-recognition result held up, and if anything got
slightly better: it correctly recognized real riot footage as a riot about
93 times out of 100 essentially every time it was confident, and next to
never mistook riot footage for a calm scene. That's a meaningfully
stronger, more trustworthy result than test 3 alone, because it's no
longer just 30 clips. The "calls calm scenes 'fighting' too often" problem
is still there too, exactly as before — we changed nothing about it yet, so
that part not changing is expected, not new information.

**Bottom line to say out loud: riot recognition on real footage isn't just
working, it's holding up as we throw more real data at it. The remaining
known issue is entirely on the "calm scene" side, and we know what to fix.**

### What's still missing

- We still don't have the actual dataset we ultimately want to use
  (XD-Violence) — that request is still pending. Everything above used
  stand-in real-world footage while we wait.
- We haven't touched fire / burning-vehicle detection at all yet — that's
  intentionally phase two, once riot detection itself is solid.
- We haven't touched audio yet either — video only, for now.

### Next thing to actually do

Fix the wording we gave the model for "fighting" (it's currently winning
by default too often) and re-run the same real-footage test to see if the
overall score goes up once that's corrected.
