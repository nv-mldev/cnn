# Part 7: Verification on Real Images, Features, and CNN Motivation

## Learning Objective

Verify the normalisation theory on real images, understand **what pixels fundamentally
cannot fix**, and see why the path forward is learned features (CNNs).

---

## 7.1 Verification: All Methods on All Transforms

Running `TM_SQDIFF_NORMED` and `TM_CCOEFF_NORMED` on real images confirms the theory:

| Property | `TM_SQDIFF_NORMED` | `TM_CCORR_NORMED` | `TM_CCOEFF_NORMED` |
|----------|--------------------|--------------------|---------------------|
| **Measures** | Difference | Correlation | Correlation |
| **Mean subtracted?** | No | No | Yes |
| **Best match at** | min → 0 | max → 1 | max → 1 |
| **Brightness invariant?** | No | No | Yes (uniform shifts) |
| **Contrast invariant?** | Scaling only | Scaling only | Yes ($aX + b$) |

---

## 7.2 What Pixels Can Never Fix

Normalisation handles the lighting model $I = aT + b$ — where **the same pixels are in
the same positions**, just with different values.

But rotation, scale, and viewpoint changes move **which pixel is where**. No amount of
per-pixel math can fix a problem where the pixel grid itself has changed.

### The Classification of Problems

| Problem type | What changes | Per-pixel fix? | Needed approach |
|-------------|-------------|----------------|-----------------|
| **Intensity** (brightness/contrast) | Pixel *values* | Yes — Normalisation | `TM_CCOEFF_NORMED` |
| **Spatial** (rotation/scale) | Pixel *positions* | No — Impossible | Position-invariant features |
| **Structural** (occlusion/viewpoint) | Which pixels *exist* | No — Impossible | Features that capture "what" not "where" |

### Why Rotation Breaks Pixels

When you rotate an image by even 5°, every pixel moves to a new position. The template
expects pixel $(i, j)$ to have a specific value, but after rotation that value has shifted
to a fractional position and been **interpolated** with its neighbours.

This isn't a $b$ offset or $a$ scaling — it's a **spatial rearrangement** of the data.

---

## 7.3 Features, Not Pixels

The solution is to stop comparing raw pixel values and instead compare **features** —
higher-level descriptions of the image that are invariant to transforms.

```
Pixel level:    [100, 150, 200, 120, 180, ...]   ← fragile
Feature level:  ["has a corner here", "edge at 45°", "circular shape"]  ← robust
```

A feature should describe **what's in the image**, not **which exact pixels encode it**.

Even a simple hand-designed feature (edge count) is more robust than raw pixels:
- Pixel SSD: T rotated 15° looks as different as a circle
- Edge count: all T shapes have similar counts regardless of rotation

---

## 7.4 The Feature Hierarchy

Computer vision has evolved through increasingly powerful feature representations:

```
Level 0: Raw pixels                    → template matching (this notebook)
Level 1: Hand-designed features        → edges, corners, gradients (Sobel, Canny, HOG)
Level 2: Engineered feature descriptors → SIFT, SURF, ORB (rotation + scale invariant)
Level 3: LEARNED features              → CNNs learn what features matter from data
```

Each level is more robust but also more complex to design — until Level 3, where you stop
designing features entirely and let the network **learn** them.

---

## 7.5 What a CNN Does

A CNN replaces the hand-designed chain:

```
pixels → [human designs edge detector] → [corner detector] → [descriptor] → compare
```

with:

```
pixels → [learned conv filters] → [learned conv filters] → ... → [learned features] → compare
```

The early layers learn edge-like and texture-like features (similar to Sobel/Gabor
filters). Deeper layers learn object parts, shapes, and eventually whole-object concepts.
The network discovers what features matter for the task **from the training data**.

---

## 7.6 Pixel Space vs Feature Space

**In pixel space:** similar images can be far apart. A rotated T is as far from the
original T (by SSD) as a circle is.

**In learned feature space:** similar concepts are close. All T shapes cluster together,
regardless of rotation/scale/lighting, and are far from circles.

This is the **feature space** — a learned coordinate system where geometric distance
corresponds to semantic similarity.

---

## 7.7 The Complete Picture

```
PROBLEM                    FIX                        METHOD
──────────────────────────────────────────────────────────────────
Different brightness       Remove DC (mean subtract)  TM_CCOEFF_NORMED
Different contrast         Remove scale (L2 norm)     TM_CCOEFF_NORMED
                           ─── normalisation ceiling ───
Small rotation             Keypoint descriptors       SIFT, ORB
Scale change               Multi-scale search         Image pyramids + SIFT
Large rotation             Rotation-invariant desc.   SIFT
Viewpoint change           Learned features           CNN
Partial occlusion          Learned features           CNN
Deformation                Learned features           CNN
"Is this a cat?"           Learned features           CNN
                           ─── deep learning begins ───
```

Everything above the normalisation ceiling is **solvable by math on pixels**.
Everything below requires **features** — either hand-designed (SIFT) or learned (CNN).

---

## Key Takeaways

1. **The physics is multiplicative:** $f(x,y) = i(x,y) \cdot r(x,y)$.

2. **Under locally uniform illumination, the physics collapses to an affine model:**
   $I \approx a \cdot T + b$.

3. **Normalisation cancels the affine transform exactly:**
   - Mean subtraction removes $b$ (the DC/brightness offset)
   - L2 normalisation removes $a$ (the gain/contrast factor)
   - Together = Pearson correlation = `TM_CCOEFF_NORMED`

4. **The geometric and statistical views are equivalent.** Mean subtraction = centering;
   L2 norm = standard deviation; Pearson $r$ = cosine of centred vectors.

5. **The affine model breaks** when illumination varies spatially, reflectance is
   view-dependent, or the sensor response is nonlinear.

6. **Rotation, scale, and occlusion are fundamentally different** — they rearrange which
   pixels map to which positions. No per-pixel normalisation can fix this.

7. **Deep learning solves the remaining problems** by learning features that are invariant
   to spatial transforms, not just intensity transforms.
