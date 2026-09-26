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

### Test 5 — a different, trainable approach: combine motion + visual signals

Everything above asked a pretrained model "does this look like a riot?"
with no training at all (zero-shot). We also started a second, separate
approach: actually train something, using richer features than just "does
this image look riot-like." For each clip we now compute: how much motion
is happening and in what direction (a classic computer-vision technique
called optical flow), how many people/vehicles a detector counts in the
frame, plus two general-purpose "understand the image/video" AI models'
own internal representations. All four of those get combined into one
big feature list per clip, and a small trainable classifier learns to tell
riot from normal from that.

First real run: 970 real XD-Violence clips (485 riot, 485 calm/normal —
both from the actual target dataset now, not a stand-in). Result: **92%
accuracy**, and — importantly — it's not lopsided: it's about equally good
at catching riots (90% of real riots caught) and equally good at not crying
wolf on calm footage (95% of calm clips correctly left alone). That's a
meaningfully different and stronger signal than the zero-shot number above.

**One honest caveat before getting excited:** we don't yet know *which*
ingredient is doing the work. It could be that the motion-tracking piece is
pulling real weight, or it could be that the two general AI models alone
would get basically the same 92% on their own and the motion/detection
pieces aren't adding anything. We have a cheap follow-up test queued
(re-run with pieces removed one at a time) to find out before claiming
"combining these signals is what makes this work."

### Test 6 — we answered Test 5's caveat, and it's a bit deflating

We re-ran everything on the full real dataset (485 riot clips + all 2346
real calm clips, not just a small matched sample) and, separately, tried
each ingredient alone to see which one actually deserves credit for the
good numbers.

**The honest answer: one ingredient (DINOv2, one of the two general "look
at this and understand it" AI models) is doing basically all the work.**
Meanwhile, the motion-tracking piece and the people/vehicle-counting
piece — alone or combined — barely did better than just guessing "calm"
every single time. That's not "a small contribution," that's
"contributing nothing" as currently built.

**Update, same day:** the first pass looked like DINOv2 alone (97.9%) was
even slightly *better* than all four combined (97.5%) — but we double
checked that before trusting it (re-ran it 6 different ways, since one
single comparison can just be lucky or unlucky), and that specific gap
didn't hold up. Re-checked properly, the two are basically tied (~97.2%
either way). So the accurate way to say this is: **DINOv2 is clearly
doing almost all the work, but adding the other three ingredients on top
doesn't measurably help *or* hurt** — not "worse," not "better," just
not making a real difference yet.

**What this means in plain terms:** the story isn't "combining four
signals makes this work." It's closer to "one strong ingredient does
almost everything, and we're carrying two extra ingredients that aren't
currently pulling their weight." That's a very normal, useful thing to
find out early — it means effort should go into either improving how the
motion/counting signals are represented, or being honest that the
simpler, cheaper single-ingredient version is what's actually working
right now.

One thing that did genuinely improve: with all that extra real calm
footage, the model got *better* at fairly telling calm from riot (95.2%
vs. 92.3% before), not just look better on paper from having way more
calm examples to trivially guess.

### What's still missing

- XD-Violence request status update: the riot class (485 clips) and a
  matched normal class (485 clips) are now both actually in hand — no
  longer just pending. What's still missing from XD-Violence itself: a
  peaceful-protest class doesn't exist in this dataset at all (it's riot
  vs. everything-else, not riot vs. protest vs. calm) — we checked another
  dataset that sounded promising for this and confirmed directly it's
  100% more riot footage, not peaceful protest footage. So that third
  category still has no source.
- We haven't touched fire / burning-vehicle detection at all yet — that's
  intentionally phase two, once riot detection itself is solid.
- We haven't touched audio yet either — video only, for now.

### Next things to actually do

1. Decide what to do about the two underperforming ingredients — either
   give them a richer/better way to describe what they see, or accept
   they're not pulling weight yet and stop leaning on them by default.
2. Fix the wording we gave the zero-shot model for "fighting" (it's
   currently winning by default too often) and re-run the same real-footage
   test to see if the overall score goes up once that's corrected.
