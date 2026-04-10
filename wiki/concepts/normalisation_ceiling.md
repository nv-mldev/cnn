---
tags: [concept, matching, synthesis]
sources: [tutorials/02_why_not_pixels/part7_normalisation_ceiling.md]
last_updated: 2026-04-09
---

# Normalisation Ceiling

The boundary between problems that per-pixel normalisation (centering, scaling) can solve and problems that require spatial features. Intensity variations live above the ceiling (solvable); spatial and structural variations live below it (unsolvable by normalisation alone).

## Why It Matters

The normalisation ceiling is the conceptual turning point of the entire tutorial series. It explains exactly **where classical per-pixel methods stop working and why learned features are necessary**. Without understanding this boundary, students either over-rely on normalisation (expecting it to handle rotation) or under-value it (jumping to CNNs before understanding what simpler methods can do). The ceiling defines the precise motivation for feature learning and deep learning.

## Key Ideas

### Above the Ceiling (normalisation solves)

| Problem | Fix | Method |
|---------|-----|--------|
| Brightness offset ($b$) | Mean subtraction | Remove DC component |
| Contrast/gain ($a$) | L2 normalisation | Project to unit sphere |
| Full affine ($aT + b$) | Pearson correlation | Center + normalise |
| Contrast stretching | Already handled | Linear transform, $r = 1.0$ |

### Below the Ceiling (features required)

| Problem | Why Normalisation Fails | What's Needed |
|---------|------------------------|---------------|
| Rotation | Pixel positions change | Rotation-invariant descriptors |
| Scale | Pixel count changes | Multi-scale features |
| Occlusion | Part of template missing | Part-based representations |
| Non-rigid deformation | Spatial warping | Deformable models / learned features |
| Viewpoint change | 3D → 2D projection changes | 3D-aware features or data augmentation |

- The ceiling is sharp: there is no "partial" fix for rotation via normalisation
- [[clipping]] can push intensity problems below the ceiling by destroying linearity
- The [[feature_hierarchy]] is the solution architecture for below-ceiling problems

## Code Example

```python
import numpy as np

template = np.array([100.0, 120.0, 110.0, 130.0])

# ABOVE the ceiling — normalisation handles these
bright = template + 50           # brightness change
high_contrast = 2 * template - 60  # affine transform

r_bright = np.corrcoef(template, bright)[0, 1]          # 1.0
r_contrast = np.corrcoef(template, high_contrast)[0, 1]  # 1.0

# BELOW the ceiling — normalisation cannot help
rotated = np.roll(template, 2)  # spatial shift (simplest spatial transform)
r_rotated = np.corrcoef(template, rotated)[0, 1]  # < 1.0 — fails

print(f"Affine: r={r_bright:.2f}, Spatial: r={r_rotated:.2f}")
```

## Related Concepts

- [[pearson_correlation]] — the best metric above the ceiling
- [[affine_model]] — the intensity model that normalisation handles
- [[feature_hierarchy]] — the solution for below-ceiling problems
- [[ssd]] — fails even above the ceiling without normalisation
- [[clipping]] — can move problems from above to below the ceiling

## Sources

- [[02_why_not_pixels|Tutorial 02: Why Not Pixels]] — Part 7
