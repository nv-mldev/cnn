---
tags: [concept, linear-algebra]
sources: [tutorials/01b_linear_algebra_for_matching/part4_linear_and_orthogonal_transforms.md]
last_updated: 2026-04-09
---

# Linear Transform

A function $T: \mathbb{R}^n \to \mathbb{R}^m$ that preserves addition and scaling: $T(\alpha a + \beta b) = \alpha T(a) + \beta T(b)$. Representable as matrix multiplication: $y = Ax$.

## Why It Matters

The [[affine_model]] $I = aT + b$ is almost a linear transform — the contrast parameter $a$ is a linear scaling (multiplies vector length), but the offset $b$ is a translation (not linear). Understanding this distinction clarifies why contrast is handled by [[cosine_similarity]] (which divides out magnitude, a linear effect) but offset requires [[mean_subtraction]] (which removes a non-linear shift). Linear transforms also provide the framework for [[orthogonal_transform|Orthogonal Transforms]] — a special class that preserves distances.

## Key Ideas

- $y = Ax$ — every linear transform is a matrix multiplication
- Preserves origin: $T(0) = 0$
- Contrast scaling $I' = aI$ is linear: it scales the vector's [[l2_norm]] by $|a|$
- Brightness offset $I' = I + b\mathbf{1}$ is NOT linear — it's an affine (not linear) operation
- Composition of linear transforms is linear: $A(Bx) = (AB)x$

## Code Example

```python
import numpy as np

# A 2D rotation matrix (a linear transform)
theta = np.pi / 4  # 45 degrees
rotation = np.array([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta),  np.cos(theta)]
])

v = np.array([1.0, 0.0])
rotated = rotation @ v
print(f"Original: {v}, Rotated: {rotated}")
print(f"Norms: {np.linalg.norm(v):.4f}, {np.linalg.norm(rotated):.4f}")  # Same!
```

## Related Concepts

- [[affine_model]] — $I = aT + b$ combines linear ($a$) and non-linear ($b$) parts
- [[orthogonal_transform]] — special linear transforms that preserve norms
- [[l2_norm]] — linear transforms can change norms; orthogonal ones don't

## Sources

- [[01b_linear_algebra_for_matching|Tutorial 01b: Linear Algebra for Matching]] — Part 4
