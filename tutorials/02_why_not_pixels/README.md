# 02 — Why Not Pixels

**Series:** Bridging the Gap to CS231n
**Theme:** From physics of image formation to the motivation for learned features

---

## Overview

This module explains **why raw pixel comparison fails** in real-world imaging, derives
the mathematical fixes (normalisation and mean subtraction), and traces the path from
pixel matching to deep learning features.

Every concept is grounded in the physics of how cameras work: illumination × reflectance
→ sensor gain → digital value. The math is motivated by the imaging problem, not
presented abstractly.

---

## Parts

| File | Theory | Code | Topic |
|------|--------|------|-------|
| `part1_pixel_matching_failure` | .md | .py | SSD breaks under rotation, scale, brightness |
| `part2_physics_and_affine_model` | .md | .py | Image formation $f = i \cdot r$, sensor model $g = af + b$, affine collapse |
| `part3_l2_normalisation` | .md | .py | Fixing the scaling factor $a$ — unit sphere geometry |
| `part4_mean_subtraction` | .md | .py | Fixing the brightness offset $b$ — orthogonal decomposition proof |
| `part5_pearson_correlation` | .md | .py | Combining both fixes — Pearson $r$ = CCOEFF\_NORMED |
| `part6_dynamic_range` | .md | .py | Brightness/contrast terms, clipping, quantization loss |
| `part7_verification_and_features` | .md | .py | Real image tests, rotation failure, features, CNN motivation |
| `exercises` | .md | .py | Six practice problems with stub functions |

---

## Suggested Reading Order

1. Read `part1_pixel_matching_failure.md`, then run `part1_pixel_matching_failure.py`
2. Read `part2_physics_and_affine_model.md`, then run `part2_physics_and_affine_model.py`
3. Continue through parts 3–7 in order — each part builds on the previous
4. Attempt `exercises.py` after finishing part 7

---

## Key Concepts

- **Physics:** $f(x,y) = i(x,y) \cdot r(x,y)$ — pixel value = illumination × reflectance
- **Sensor model:** $g = a \cdot f + b$ — gain and bias from exposure, ISO, dark current
- **Affine collapse:** under locally uniform illumination, $I \approx a \cdot T + b$
- **L2 normalisation:** projects onto unit sphere, removes the gain factor $a$
- **Mean subtraction:** orthogonal projection removes the bias $b$
- **Pearson correlation:** the combination — invariant to any $aX + b$ transform
- **The ceiling:** normalisation fixes intensity problems but cannot fix spatial ones
- **Deep learning:** learns the feature space where semantic similarity = geometric distance

---

## Prerequisites

- [00 — Introduction to Digital Images](../00_introduction_to_digital_images/)
- [01a — Probability for Sensors](../01a_probability_for_sensors/)
- [01b — Linear Algebra for Matching](../01b_linear_algebra_for_matching/)

---

## Running the Scripts

```bash
# From the project root
uv run python tutorials/02_why_not_pixels/part1_pixel_matching_failure.py
uv run python tutorials/02_why_not_pixels/part2_physics_and_affine_model.py
# ... and so on for parts 3–7
uv run python tutorials/02_why_not_pixels/exercises.py
```

Scripts fall back to synthetic data if DIP3E images are not present.
