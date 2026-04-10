---
tags: [concept, linear-algebra]
sources: [tutorials/01b_linear_algebra_for_matching/part2_norms_and_cosine.md]
last_updated: 2026-04-09
---

# Unit Vector

A vector with [[l2_norm]] equal to 1: $\hat{v} = v / \|v\|$. Preserves direction (pattern) while discarding magnitude (brightness/contrast).

## Why It Matters

Normalising a pixel vector to unit length is the key step that makes template matching invariant to contrast scaling. All unit vectors lie on the surface of the unit hypersphere in $\mathbb{R}^n$. Two patches with identical patterns but different contrast levels map to the same point on this sphere. The [[dot_product]] of two unit vectors directly gives $\cos\theta$ — the [[cosine_similarity]].

## Key Ideas

- $\hat{v} = v / \|v\|$, so $\|\hat{v}\| = 1$
- Removes magnitude (brightness/contrast), preserves direction (pattern)
- All normalised patches lie on the unit sphere in $\mathbb{R}^n$
- $\hat{a} \cdot \hat{b} = \cos\theta$ — dot product of unit vectors IS cosine similarity
- Undefined for the zero vector ($\|v\| = 0$) — a completely black patch has no "direction"

## Code Example

```python
import numpy as np

patch = np.array([40, 80, 120, 80, 40], dtype=float)
bright = 2.5 * patch  # same pattern, different contrast

unit_patch = patch / np.linalg.norm(patch)
unit_bright = bright / np.linalg.norm(bright)

print(f"Original norms: {np.linalg.norm(patch):.1f}, {np.linalg.norm(bright):.1f}")
print(f"Unit norms:     {np.linalg.norm(unit_patch):.4f}, {np.linalg.norm(unit_bright):.4f}")
print(f"Same direction? {np.allclose(unit_patch, unit_bright)}")  # True
```

## Related Concepts

- [[l2_norm]] — the denominator in normalisation
- [[cosine_similarity]] — equals the dot product of unit vectors
- [[mean_subtraction]] — needed before normalisation to handle brightness offset

## Sources

- [[01b_linear_algebra_for_matching|Tutorial 01b: Linear Algebra for Matching]] — Part 2
