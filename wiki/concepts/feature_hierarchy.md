---
tags: [concept, features, deep-learning]
sources: [tutorials/02_why_not_pixels/part7_normalisation_ceiling.md]
last_updated: 2026-04-09
---

# Feature Hierarchy

The progression of image representations from raw pixels to learned features, where each level provides more invariance to transformations at the cost of greater design complexity — until CNNs learn the hierarchy automatically from data.

## Why It Matters

The feature hierarchy explains **why deep learning exists**. Hand-designing features that handle rotation, scale, occlusion, and deformation is extraordinarily difficult. Each level of the hierarchy solves more problems but requires more expertise to design. CNNs bypass this bottleneck by learning the entire hierarchy from labelled data, which is why they displaced decades of hand-crafted feature engineering.

## Key Ideas

| Level | Representation | Invariance | Design |
|-------|---------------|------------|--------|
| 0 | Raw pixels | None | None needed |
| 1 | Hand-designed (edges, gradients) | Small translations | Manual, domain-specific |
| 2 | Engineered descriptors (SIFT, HOG, SURF) | Rotation, scale, some illumination | Years of research per descriptor |
| 3 | Learned features (CNNs) | Whatever the training data requires | Learned from data |

- Each level builds on the previous: SIFT uses gradients, which use edges, which use pixels
- The jump from Level 2 to Level 3 is qualitative: design is replaced by learning
- CNNs stack convolutional layers that progressively build from edges → textures → parts → objects
- The [[normalisation_ceiling]] is the boundary between Level 0 problems and Level 1+ problems

## Code Example

```python
import numpy as np

# Level 0: Raw pixel comparison — fails on brightness
template = np.array([100, 120, 110, 130], dtype=float)
bright = template + 50
ssd = np.sum((template - bright) ** 2)  # Large — fails

# Level 0 + normalisation: handles intensity, not spatial
r = np.corrcoef(template, bright)[0, 1]  # 1.0 — works for intensity

# Level 1+: spatial invariance requires features
# Rotation of the template → pixel order changes → r drops
rotated = np.array([130, 100, 120, 110], dtype=float)  # shuffled
r_rot = np.corrcoef(template, rotated)[0, 1]  # < 1.0 — fails
# This is where features (edges, SIFT, CNNs) become necessary
```

## Related Concepts

- [[normalisation_ceiling]] — the boundary that motivates features
- [[ssd]] — Level 0 metric, fails at the first hurdle
- [[pearson_correlation]] — best Level 0 metric, still hits the ceiling
- [[image_formation_model]] — the physics that creates the intensity problems Level 0 can solve

## Sources

- [[02_why_not_pixels|Tutorial 02: Why Not Pixels]] — Part 7
