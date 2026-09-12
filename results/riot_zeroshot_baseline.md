# Riot Zero-Shot Baseline Results

Zero-shot CLIP (ViT-B-32, openai weights) classification of riot vs. negative-class clips. No fine-tuning. See README.md for scope and limitations.

**Clips evaluated:** 6  
**Overall accuracy:** 33.33%

## Per-class precision / recall / F1

| class | precision | recall | f1 | support |
|---|---|---|---|---|
| riot | 0.00 | 0.00 | 0.00 | 2 |
| normal | 0.00 | 0.00 | 0.00 | 2 |
| fighting | 0.33 | 1.00 | 0.50 | 2 |

## Confusion matrix (rows = true label, cols = predicted)

| true \ pred | riot | normal | fighting |
|---|---|---|---|
| riot | 0 | 0 | 2 |
| normal | 0 | 0 | 2 |
| fighting | 0 | 0 | 2 |

## Per-clip predictions

| id | true label | predicted | confidence | correct |
|---|---|---|---|---|
| dummy_riot_01 | riot | fighting | 0.390 | no |
| dummy_riot_02 | riot | fighting | 0.464 | no |
| dummy_normal_01 | normal | fighting | 0.865 | no |
| dummy_normal_02 | normal | fighting | 0.865 | no |
| dummy_fighting_01 | fighting | fighting | 0.921 | yes |
| dummy_fighting_02 | fighting | fighting | 0.921 | yes |