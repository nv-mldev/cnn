---
tags: [concept, linear-algebra]
sources: [tutorials/01b_linear_algebra_for_matching/part1_vectors_and_dot_product.md]
last_updated: 2026-04-09
---

# Dot Product

The sum of element-wise products of two vectors. Algebraic definition: $a \cdot b = \sum_i a_i b_i$. Geometric definition: $a \cdot b = \|a\|\|b\|\cos\theta$, where $\theta$ is the angle between the vectors.

## Why It Matters

The dot product is the most fundamental operation in template matching. When you slide a template across an image and compute the sum of pixel-by-pixel products, you are computing a dot product. However, the raw dot product conflates two things: how well the patterns align (the $\cos\theta$ part) and how bright the images are (the $\|a\|\|b\|$ part). This is why raw correlation fails under lighting changes — it responds to brightness, not just pattern.

## Key Ideas

- Algebraic: $a \cdot b = \sum_{i=1}^{n} a_i b_i$ — sum of pixel-by-pixel products
- Geometric: $a \cdot b = \|a\|\|b\|\cos\theta$ — magnitude times alignment
- **Magnitude-dependent**: a brighter version of the same pattern gives a larger dot product
- $a \cdot a = \|a\|^2$ — the dot product of a vector with itself gives the squared [[l2_norm]]
- If $a \cdot b = 0$, the vectors are [[orthogonality|orthogonal]] — completely independent

## Code Example

```python
import numpy as np

template = np.array([10, 20, 30, 20, 10], dtype=float)
patch_same = np.array([10, 20, 30, 20, 10], dtype=float)
patch_bright = np.array([50, 60, 70, 60, 50], dtype=float)  # same pattern, brighter

# Raw dot product is magnitude-dependent
print(f"Same:   {np.dot(template, patch_same):.0f}")    # 1500
print(f"Bright: {np.dot(template, patch_bright):.0f}")   # 5500 — much larger!

# But the angle (pattern agreement) is the same
cos_same = np.dot(template, patch_same) / (np.linalg.norm(template) * np.linalg.norm(patch_same))
cos_bright = np.dot(template, patch_bright) / (np.linalg.norm(template) * np.linalg.norm(patch_bright))
print(f"Cosine (same):   {cos_same:.4f}")   # 1.0
print(f"Cosine (bright): {cos_bright:.4f}")  # < 1.0 (offset changes direction!)
```

## Mathematical Model

The two definitions are equivalent via the law of cosines:

$$a \cdot b = \|a\|\|b\|\cos\theta$$

This means the dot product encodes both magnitude and direction. To isolate direction (pattern), divide out the magnitudes → [[cosine_similarity]].

## Related Concepts

- [[vector_representation]] — vectors must exist before we can dot them
- [[l2_norm]] — $\|a\|^2 = a \cdot a$
- [[cosine_similarity]] — normalised dot product, removes magnitude dependence
- [[orthogonality]] — $a \cdot b = 0$ means perpendicular

## Sources

- [[01b_linear_algebra_for_matching|Tutorial 01b: Linear Algebra for Matching]] — Part 1
