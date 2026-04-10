---
tags: [concept, image-formation, physics]
sources: [tutorials/02_why_not_pixels/part2_physics_model.md]
last_updated: 2026-04-09
---

# Image Formation Model

The multiplicative model of image formation: $f(x,y) = i(x,y) \cdot r(x,y)$, where $i(x,y)$ is the illumination falling on surface point $(x,y)$ and $r(x,y) \in [0,1]$ is the reflectance of the surface at that point.

## Why It Matters

This model explains a fundamental ambiguity in images: a dark pixel could mean low illumination (shadow) OR low reflectance (dark material) — the sensor cannot distinguish between the two. Since the model is multiplicative, changes in illumination scale the entire signal, leading directly to the [[affine_model]] that normalisation must handle. Understanding this physics is what motivates the mathematical machinery of normalisation.

## Key Ideas

- $i(x,y)$ — illumination: determined by light source position, intensity, and scene geometry
- $r(x,y)$ — reflectance: intrinsic surface property, what we usually want to measure
- Multiplication means illumination acts as a spatially varying gain on reflectance
- Sensor adds its own gain and offset: $g = a \cdot f + b$
- Under **locally uniform illumination** ($i$ constant over a small patch), $g \approx a \cdot r + b$ — the affine model
- The assumption of locally uniform illumination is what makes normalisation work; when it breaks (shadows, specularities), normalisation fails

## Code Example

```python
import numpy as np

# Simulate image formation: same surface, different illumination
reflectance = np.array([0.2, 0.5, 0.8, 0.3])  # surface property (fixed)

illumination_bright = 200.0  # bright lighting
illumination_dim = 80.0      # dim lighting

image_bright = illumination_bright * reflectance  # [40, 100, 160, 60]
image_dim = illumination_dim * reflectance         # [16, 40, 64, 24]

# Same reflectance, completely different pixel values
# But image_bright = 2.5 * image_dim — affine with a=2.5, b=0
```

## Related Concepts

- [[affine_model]] — the simplification under locally uniform illumination
- [[ssd]] — fails because it cannot handle the multiplicative illumination effect
- [[pearson_correlation]] — handles the affine relationship that image formation creates
- [[contrast]] — illumination changes alter the contrast of the captured image
- [[dynamic_range]] — the range of $f$ values the sensor can capture

## Sources

- [[02_why_not_pixels|Tutorial 02: Why Not Pixels]] — Part 2
