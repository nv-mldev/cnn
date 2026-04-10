---
tags: [concept, matching, statistics]
sources: [tutorials/02_why_not_pixels/part5_pearson_correlation.md]
last_updated: 2026-04-09
---

# Pearson Correlation

The normalised correlation coefficient between two signals, combining mean subtraction and L2 normalisation to handle the full affine intensity model:

$$r = \frac{\sum(I - \bar{I})(T - \bar{T})}{\sqrt{\sum(I - \bar{I})^2} \cdot \sqrt{\sum(T - \bar{T})^2}}$$

Equivalent to OpenCV's `TM_CCOEFF_NORMED`.

## Why It Matters

Pearson correlation is the "correct" metric for template matching under the affine intensity model $I = aT + b$. Centering (subtracting the mean) removes the offset $b$; normalising (dividing by the norm) removes the gain $a$. The result is $r = 1.0$ for any positive affine transform of the template, regardless of brightness or contrast differences. This is the most robust per-pixel matching metric — and understanding where it still fails defines the boundary where features become necessary.

## Key Ideas

- **Centering** removes $b$ (brightness offset) — orthogonal projection away from the ones-vector
- **Normalising** removes $a$ (contrast/gain) — projection onto unit sphere
- $r = 1.0$: perfect positive linear relationship (same content, any brightness/contrast)
- $r = -1.0$: perfect negative (inverted image)
- $r = 0$: no linear relationship
- Handles the full affine model: if $I = aT + b$ with $a > 0$, then $r = 1.0$ exactly
- Fails when clipping destroys the linear relationship

### Geometric ≡ Statistical Equivalence

| Geometric View | Statistical View |
|---|---|
| Subtract mean = project off ones-vector | Subtract mean = centre the data |
| Divide by norm = project onto unit sphere | Divide by std = standardise to z-scores |
| Cosine of angle between centred vectors | Correlation coefficient |
| Angle = 0° → r = 1.0 | Perfect linear relationship |
| Angle = 90° → r = 0 | No linear relationship |

## Code Example

```python
import numpy as np

def pearson_correlation(template: np.ndarray, patch: np.ndarray) -> float:
    """Pearson r — handles full affine model I = aT + b."""
    template_centred = template - template.mean()
    patch_centred = patch - patch.mean()
    numerator = np.sum(template_centred * patch_centred)
    denominator = np.linalg.norm(template_centred) * np.linalg.norm(patch_centred)
    return float(numerator / denominator)

# Same content, different brightness AND contrast → r = 1.0
template = np.array([100.0, 120.0, 110.0, 130.0])
transformed = 0.5 * template + 60  # a=0.5, b=60

print(f"r = {pearson_correlation(template, transformed):.4f}")  # 1.0000
```

## Related Concepts

- [[ssd]] — the naive metric that Pearson correlation fixes
- [[affine_model]] — the intensity model that Pearson handles exactly
- [[image_formation_model]] — the physics that creates affine relationships
- [[contrast_stretching]] — a linear transform, so $r = 1.0$ with original
- [[clipping]] — breaks the linear relationship, defeating Pearson
- [[normalisation_ceiling]] — Pearson solves intensity; spatial problems remain

## Sources

- [[02_why_not_pixels|Tutorial 02: Why Not Pixels]] — Part 5
