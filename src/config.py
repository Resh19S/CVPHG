"""
Central config for the riot/protest zero-shot scaffold.

Everything class- and prompt-related lives here on purpose: adding a future
"fire" / "burning_vehicle" class (phase 2, explicitly out of scope for this
scaffold per team direction) should mean adding one entry to CLASS_PROMPTS
and TARGET_CLASSES, not editing extraction/classification/eval logic.
"""

import random

import numpy as np

# Fixed seed for every script that touches randomness (frame-sampling
# fallback, dummy-data generation, any shuffling). Printed by each script
# that uses it -- never rely on an unset/implicit seed.
SEED = 42


def set_seed(seed: int = SEED) -> int:
    random.seed(seed)
    np.random.seed(seed)
    print(f"[seed] using fixed random seed = {seed}")
    return seed


# XD-Violence classes we are including in this scaffold. "riot" is the
# positive class of interest; the rest are negatives used for contrast.
# Fire/burning-vehicle is deliberately NOT included yet (phase 2).
TARGET_CLASSES = ["riot", "normal", "fighting"]

# Text prompts per class, used as CLIP zero-shot classifier weights.
# Multiple prompts per class are averaged in embedding space to reduce
# sensitivity to exact phrasing.
CLASS_PROMPTS = {
    "riot": [
        "a photo of a riot",
        "a violent protest with crowds clashing",
        "police and protesters fighting in the street",
        "a crowd throwing objects and clashing with authorities",
    ],
    "normal": [
        "a photo of a normal street scene",
        "people calmly walking on a city street",
        "an ordinary crowd going about their day",
    ],
    "fighting": [
        "a photo of people fighting",
        "two people physically fighting each other",
        "a violent physical altercation between individuals",
    ],
}

# Mapping from raw XD-Violence annotation label codes to our class names.
# XD-Violence multi-label codes (per the dataset's published label set):
#   A  = Normal
#   B1 = Fighting
#   B2 = Shooting
#   B4 = Riot
#   B5 = Abuse
#   B6 = Car accident
#   G  = Explosion
# NOTE: confirm this mapping against the actual annotation file once
# downloaded -- label-code schemes have shifted across dataset releases,
# and this scaffold has not been run against the real file yet.
XD_VIOLENCE_LABEL_CODES = {
    "A": "normal",
    "B1": "fighting",
    "B4": "riot",
}

CLIP_MODEL_NAME = "ViT-B-32"
CLIP_PRETRAINED = "openai"
NUM_FRAMES_PER_CLIP = 8
FRAME_SIZE = 224  # CLIP ViT-B-32 default input resolution
