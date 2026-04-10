# Part 1: Pixel Matching Failure

## Learning Objective

Understand **why raw pixel comparison (SSD) breaks** under real-world imaging conditions,
and classify which failure modes are fixable by math versus fundamentally unfixable.

---

## 1.0 The Experiment

We use OpenCV's template matching to compare a reference patch against a scene under
three transforms that occur constantly in practice:

| Transform | Real-world cause | What changes |
|-----------|-----------------|---------------|
| **Rotation (5°)** | Camera tilt, part misalignment on conveyor | Pixel grid alignment |
| **Scale (90%)** | Different camera distance, zoom change | Object size in pixels |
| **Brightness (×0.7)** | Lighting change, cloud cover, aging LED | All pixel values |

---

## 1.1 The Ideal Case: Perfect Match

When the template is cropped from the exact same scene image, pixel values align
perfectly. `TM_SQDIFF_NORMED` gives a score near zero — the best possible result.

This is a **best-case scenario** that never occurs in practice.

---

## 1.2 SSD: Sum of Squared Differences

For a template $T$ of size $m \times n$ and a scene window $I$ of the same size:

$$\text{SSD}(T, I) = \sum_{i,j} \big(I(i,j) - T(i,j)\big)^2$$

The normalized version divides by the product of the L2 norms:

$$\text{SQDIFF\_NORMED}(T, I) = \frac{\sum (I - T)^2}{\sqrt{\sum I^2} \cdot \sqrt{\sum T^2}}$$

A score of **0.0** means a perfect pixel-level match. Any deviation inflates the score.

---

## 1.3 The Realistic Cases: When Pixels Break

All three transforms break SSD — but for **fundamentally different reasons**:

| Transform | Why SSD fails | Fixable by math? |
|-----------|--------------|------------------|
| **Brightness** | Pixel values shifted uniformly — same pattern, different numbers | **Yes** — normalisation + mean subtraction |
| **Rotation** | Pixels moved to different grid positions — can't align them | **No** — pixel positions changed |
| **Scale** | Object is different size — template doesn't tile-match anymore | **No** — pixel count changed |

---

## 1.4 Key Observation

Brightness is **qualitatively different** from rotation and scale:

- Brightness change: the **same pixels** carry the same pattern, just scaled/offset in value
- Rotation/scale: **different pixels** encode the object — the spatial structure has changed

This distinction drives the entire rest of the notebook. Parts 2–5 fix brightness.
Parts 8–9 explain why rotation/scale require a fundamentally different approach.

---

## Summary

> Raw SSD is fragile because it treats pixel values as absolute measurements. Real sensors
> produce values that depend on lighting, exposure, and gain — all of which change between
> captures. The first fix is to make the comparison **invariant to those sensor factors**.
