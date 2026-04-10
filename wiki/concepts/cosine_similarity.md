---
tags: [concept, linear-algebra, matching]
sources: [tutorials/01b_linear_algebra_for_matching/part2_norms_and_cosine.md]
last_updated: 2026-04-09
---

# Cosine Similarity

The cosine of the angle between two vectors: $\cos\theta = \frac{a \cdot b}{\|a\|\|b\|}$. Equivalently, the [[dot_product]] of their [[unit_vector|Unit Vectors]].

## Why It Matters

Cosine similarity is the first step toward robust template matching. It removes sensitivity to contrast scaling ($a$ in the [[affine_model]]) by normalising out vector magnitudes. However, it **fails on brightness offset** ($b$): adding a constant to all pixels changes the vector's direction, not just its length. This limitation motivates [[mean_subtraction]] as a necessary preprocessing step.

## Key Ideas

- $\cos\theta = \frac{a \cdot b}{\|a\|\|b\|} = \hat{a} \cdot \hat{b}$
- Range: $[-1, 1]$; 1 = identical pattern, 0 = unrelated, -1 = inverted
- **Handles contrast**: $\cos(a, ka) = 1$ for any $k > 0$
- **Fails on offset**: $\cos(a, a + c\mathbf{1}) \neq 1$ — brightness shift changes direction
- This is why cosine similarity alone is not enough for normalised cross-correlation

## Code Example

```python
import numpy as np

template = np.array([10, 20, 30, 20, 10], dtype=float)
contrast = 3.0 * template          # a=3, b=0
offset = template + 50             # a=1, b=50

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print(f"Contrast only: {cosine_sim(template, contrast):.4f}")  # 1.0000 — perfect
print(f"Offset only:   {cosine_sim(template, offset):.4f}")    # < 1.0  — fails!
```

## Mathematical Model

$$\cos\theta = \frac{\sum_i a_i b_i}{\sqrt{\sum_i a_i^2} \cdot \sqrt{\sum_i b_i^2}}$$

For affine-transformed image $b = \alpha a + \beta\mathbf{1}$:
- If $\beta = 0$: $\cos\theta = 1$ (contrast handled)
- If $\beta \neq 0$: $\cos\theta < 1$ (offset not handled)

Fix: subtract the mean first → [[mean_subtraction]] + cosine similarity = normalised cross-correlation.

## Related Concepts

- [[dot_product]] — the unnormalised version
- [[unit_vector]] — cosine similarity = dot product of unit vectors
- [[l2_norm]] — the normalising denominator
- [[mean_subtraction]] — required to handle brightness offset before cosine similarity
- [[affine_model]] — cosine handles $a$ but not $b$

## Sources

- [[01b_linear_algebra_for_matching|Tutorial 01b: Linear Algebra for Matching]] — Part 2
