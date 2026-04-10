---
tags: [concept, image-formation, critical]
sources: [tutorials/00_introduction_to_digital_images/part3_contrast_and_dynamic_range.md, tutorials/01b_linear_algebra_for_matching/part4_linear_and_orthogonal_transforms.md, tutorials/02_why_not_pixels/part2_physics_model.md]
last_updated: 2026-04-09
---

# Affine Model

The relationship between pixel values of the same scene under different lighting/exposure conditions: $I_2(i,j) = a \cdot I_1(i,j) + b$, where $a$ controls [[contrast]] and $b$ controls brightness.

## Why It Matters

This is the single most important concept for understanding why raw pixel comparison fails. The same scene content produces **completely different pixel values** when lighting changes. Two images of the same face can differ by 100+ grey levels at every pixel — not because the content changed, but because the affine parameters ($a$, $b$) changed. Any algorithm that compares pixels directly (SSD, SAD, MAE) will declare these images "different" even though they show the same thing. This motivates the need for normalisation (Tutorial 01b) and eventually learned features.

## Key Ideas

- $a$ (gain/contrast): scales the spread of pixel values; $a > 1$ increases contrast, $a < 1$ decreases it
- $b$ (offset/brightness): shifts all pixel values up or down
- Different cameras, exposures, or lighting conditions produce different $(a, b)$ pairs for the same scene
- SSD between affine-transformed versions of the same image can be enormous
- **This is not a bug — it's physics.** Pixel values encode lighting, not just content.

## Code Example

```python
import numpy as np

# Same scene, three different lighting conditions
reference = load_image("einstein.png")  # medium contrast
bright = 1.0 * reference + 40          # a=1, b=40 (brighter)
low_contrast = 0.5 * reference + 64    # a=0.5, b=64 (flatter)
high_contrast = 1.5 * reference - 40   # a=1.5, b=-40 (more spread)

# SSD is huge despite identical content
ssd = np.sum((reference - bright) ** 2)  # Large!
```

## Related Concepts

- [[contrast]] — controlled by parameter $a$
- [[dynamic_range]] — affine transforms can push values outside sensor range
- [[clipping]] — what happens when affine-transformed values exceed sensor limits
- [[shading]] — spatially varying affine parameters
- [[cosine_similarity]] — handles contrast ($a$) but fails on offset ($b$)
- [[mean_subtraction]] — removes brightness offset ($b$) via orthogonal projection
- [[linear_transform]] — contrast ($a$) is linear; offset ($b$) is affine (not linear)
- [[vector_representation]] — affine model expressed in vector space: $b$ shifts along $[1,\ldots,1]$, $a$ scales magnitude
- [[image_formation_model]] — the physics ($f = i \cdot r$) from which the affine model is derived
- [[pearson_correlation]] — handles the full affine model: centering removes $b$, normalising removes $a$

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 3
- [[01b_linear_algebra_for_matching|Tutorial 01b: Linear Algebra for Matching]] — Part 4 (affine model decomposed in vector space)
- [[02_why_not_pixels|Tutorial 02: Why Not Pixels]] — Part 2 (derived from physics model)
