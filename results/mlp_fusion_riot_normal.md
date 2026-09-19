# MLP Fusion Classifier Results (Riot vs. Normal)

Supervised MLP (256,64 hidden units) trained on fused features: Lucas-Kanade
optical flow summary stats + RF-DETR detection counts + DINOv2 frame
embeddings + VideoMAE clip embeddings. Real XD-Violence data for both
classes (not a stand-in). Binary riot/normal only — see
`docs/roadmap.md` for why (no data source yet for a third "Protest" class).

**Clips:** 970 total (485 riot / 485 normal) — **Train:** 776 (388/388) —
**Test:** 194 (97/97) — **Feature dimensions:** 1544 (4 motion + 4 detection
+ 768 DINOv2 + 768 VideoMAE) — **Test accuracy:** 92.27%

## Per-class precision / recall / F1

| class | precision | recall | f1 | support |
|---|---|---|---|---|
| normal | 0.90 | 0.95 | 0.92 | 97 |
| riot | 0.95 | 0.90 | 0.92 | 97 |

## Confusion matrix (rows = true label, cols = predicted)

| true \ pred | normal | riot |
|---|---|---|
| normal | 92 | 5 |
| riot | 10 | 87 |

## Caveats (read together, not in isolation)

1. **Internal validation score hit a perfect 1.0000 during training**
   (sklearn's `early_stopping=True` carves 10% off the 776 training rows
   as an internal validation set — ~78 clips). Test accuracy is 92.27%, not
   100%, so this isn't necessarily a problem, but it means it's not yet
   known which branch is actually driving the separation. An ablation
   (DINOv2+VideoMAE only vs. LK+RF-DETR only) has not been run yet — until
   it is, don't present this as evidence that *fusion specifically* (motion
   + visual combined) is what's working, since a single strong branch alone
   could plausibly explain most of this number.
2. **Binary riot/normal only.** The 3-class target (Normal/Protest/Riot)
   from the original architecture diagram is not achievable yet — no data
   source has been found for a peaceful-protest class (checked directly:
   the Kaggle `jpmiller/protests-against-police-violence` dataset is
   744/748 files Capitol riot footage, not peaceful protest content).
3. **Methodologically cleaner than the earlier CLIP zero-shot benchmark**,
   worth noting explicitly: both classes here are real XD-Violence data
   (same source distribution — movies/YouTube clips, same filming/
   compression conventions), unlike the earlier Capitol-riot-vs-RLVS-normal
   pairing, which mixed two unrelated datasets and risked the model keying
   on dataset-of-origin artifacts rather than riot content itself. Not
   proof that confound is fully absent, just a weaker version of the risk
   than before.
4. No fine-tuning was performed on DINOv2 or VideoMAE — both are frozen,
   pretrained backbones; only the MLP head was trained.
