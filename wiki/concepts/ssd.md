---
tags: [concept, matching]
sources: [tutorials/02_why_not_pixels/part1_ssd_fails.md]
last_updated: 2026-04-09
---

# Sum of Squared Differences (SSD)

The simplest template matching metric: $SSD(T, I) = \sum_{x,y} (I(x,y) - T(x,y))^2$, measuring the total squared pixel-wise error between a template $T$ and an image patch $I$.

## Why It Matters

SSD is the default "naive" comparison that most people reach for first. Understanding why it fails is the starting point for understanding why we need normalisation and eventually learned features. SSD treats every pixel difference equally and has no mechanism to handle the fact that the same scene produces different pixel values under different conditions.

## Key Ideas

- $SSD = 0$ only when patches are identical — any change in brightness, contrast, or content increases it
- Fails under brightness change: if $I = T + b$, then $SSD = N \cdot b^2$ (large even for small $b$)
- Fails under contrast change: if $I = a \cdot T$, then $SSD = (a-1)^2 \cdot \sum T^2$
- Fails under rotation and scale — these are spatial transforms, not per-pixel fixable
- Brightness failure is fixable (normalisation); spatial failure is not (requires features)
- Related to L2 distance: $SSD = \|I - T\|_2^2$

## Code Example

```python
import numpy as np

def ssd(template: np.ndarray, patch: np.ndarray) -> float:
    """Sum of Squared Differences — simplest matching metric."""
    return float(np.sum((patch - template) ** 2))

# Same content, different brightness → SSD is large
template = np.array([100, 120, 110, 130], dtype=float)
bright_version = template + 40  # just brighter

print(f"SSD = {ssd(template, bright_version)}")  # 6400, not 0!
```

## Related Concepts

- [[affine_model]] — the intensity transformation that SSD cannot handle
- [[pearson_correlation]] — the metric that fixes SSD's affine sensitivity
- [[normalisation_ceiling]] — even better metrics hit a wall at spatial transforms
- [[image_formation_model]] — the physics behind why pixel values change

## Sources

- [[02_why_not_pixels|Tutorial 02: Why Not Pixels]] — Part 1
