---
tags: [concept, linear-algebra]
sources: [tutorials/01b_linear_algebra_for_matching/part2_norms_and_cosine.md]
last_updated: 2026-04-09
---

# L2 Norm

The Euclidean length of a vector: $\|v\| = \sqrt{\sum_i v_i^2}$. Measures the total "energy" or magnitude of the vector.

## Why It Matters

In imaging, the L2 norm of a pixel vector directly reflects brightness and contrast. A brighter image has a larger norm. This is why raw pixel comparison (SSD) fails under lighting changes — SSD is $\|a - b\|^2$, which is enormous when the norms differ even if the patterns are identical. Dividing by the norm (creating a [[unit_vector]]) strips away brightness/contrast and isolates the pattern.

## Key Ideas

- $\|v\| = \sqrt{\sum_i v_i^2} = \sqrt{v \cdot v}$
- $\|v\|^2 = v \cdot v$ — squared norm equals self-dot-product
- Bright images have large norms; dark images have small norms
- Contrast scaling: $\|av\| = |a| \cdot \|v\|$ — scaling pixel values scales the norm proportionally
- SSD between two vectors: $\|a - b\|^2 = \|a\|^2 - 2a \cdot b + \|b\|^2$

## Code Example

```python
import numpy as np

dark_patch = np.array([20, 30, 25, 35, 20], dtype=float)
bright_patch = 3.0 * dark_patch  # same pattern, 3x brighter

print(f"Dark norm:   {np.linalg.norm(dark_patch):.1f}")    # ~56.4
print(f"Bright norm: {np.linalg.norm(bright_patch):.1f}")   # ~169.1 (3x larger)

# SSD is huge despite identical pattern
ssd = np.sum((dark_patch - bright_patch) ** 2)
print(f"SSD: {ssd:.0f}")  # Large!
```

## Mathematical Model

$$\|v\|_2 = \sqrt{\sum_{i=1}^{n} v_i^2}$$

Key properties:
- $\|v\| \geq 0$, with equality iff $v = 0$
- $\|\alpha v\| = |\alpha| \|v\|$ (homogeneity)
- $\|a + b\| \leq \|a\| + \|b\|$ (triangle inequality)

## Related Concepts

- [[dot_product]] — $\|v\|^2 = v \cdot v$
- [[unit_vector]] — $\hat{v} = v / \|v\|$, norm equals 1
- [[cosine_similarity]] — divides out norms to compare direction only
- [[orthogonal_transform]] — preserves L2 norm: $\|Qx\| = \|x\|$

## Sources

- [[01b_linear_algebra_for_matching|Tutorial 01b: Linear Algebra for Matching]] — Part 2
