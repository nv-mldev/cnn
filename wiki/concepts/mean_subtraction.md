---
tags: [concept, linear-algebra, matching]
sources: [tutorials/01b_linear_algebra_for_matching/part3_orthogonality_and_projection.md]
last_updated: 2026-04-09
---

# Mean Subtraction

Removing the mean value from a pixel vector: $v' = v - \bar{v}\mathbf{1}$. Geometrically, this is [[orthogonal_projection]] that removes the component along the brightness direction $[1,1,\ldots,1]$.

## Why It Matters

Mean subtraction is the critical preprocessing step that makes template matching invariant to brightness offset ($b$ in the [[affine_model]]). [[cosine_similarity]] alone handles contrast ($a$) but fails on offset ($b$). Mean subtraction removes $b$ by projecting out the brightness direction. The residual lives in a subspace orthogonal to $[1,\ldots,1]$, so no brightness offset — regardless of magnitude — can affect the pattern. Combined with L2 normalisation, this gives full normalised cross-correlation.

## Key Ideas

- $v' = v - \bar{v}\mathbf{1}$, where $\bar{v} = \frac{1}{n}\sum_i v_i$
- Equivalent to projecting out the $[1,1,\ldots,1]/\sqrt{n}$ component
- The residual $v'$ is orthogonal to $[1,\ldots,1]$: $v' \cdot \mathbf{1} = 0$ (the sum of mean-subtracted values is zero)
- Brightness offset $b$ adds $b\mathbf{1}$ to the vector — this is entirely along the brightness direction, so mean subtraction removes it completely
- Mean subtraction + [[unit_vector|L2 normalisation]] = normalised cross-correlation = invariance to full affine model $I = aT + b$

## Code Example

```python
import numpy as np

template = np.array([10, 20, 30, 20, 10], dtype=float)
offset_version = template + 100  # same pattern, brightness offset b=100

# Without mean subtraction: cosine similarity fails
cos_raw = np.dot(template, offset_version) / (
    np.linalg.norm(template) * np.linalg.norm(offset_version))
print(f"Cosine (raw): {cos_raw:.4f}")  # < 1.0

# With mean subtraction: perfect match
t_centered = template - template.mean()
o_centered = offset_version - offset_version.mean()
cos_centered = np.dot(t_centered, o_centered) / (
    np.linalg.norm(t_centered) * np.linalg.norm(o_centered))
print(f"Cosine (mean-subtracted): {cos_centered:.4f}")  # 1.0000
```

## Mathematical Model

### Derivation: Mean subtraction as orthogonal projection

Let $\hat{u} = \frac{\mathbf{1}}{\sqrt{n}}$ be the unit vector along $[1,1,\ldots,1]$.

The [[orthogonal_projection]] of $v$ onto $\hat{u}$:

$$\text{proj}_{\hat{u}}(v) = (v \cdot \hat{u})\hat{u} = \left(\frac{1}{\sqrt{n}}\sum_i v_i\right) \cdot \frac{\mathbf{1}}{\sqrt{n}} = \bar{v}\mathbf{1}$$

The residual:

$$v' = v - \text{proj}_{\hat{u}}(v) = v - \bar{v}\mathbf{1}$$

This is exactly mean subtraction. Since $v' \perp \hat{u}$, any offset $b\mathbf{1}$ (which lies along $\hat{u}$) has zero dot product with $v'$ — brightness cannot affect the mean-subtracted pattern.

## Related Concepts

- [[orthogonal_projection]] — the geometric operation mean subtraction performs
- [[orthogonality]] — why the residual is immune to brightness offset
- [[cosine_similarity]] — handles contrast but needs mean subtraction for offset
- [[unit_vector]] — L2 normalisation after mean subtraction completes the pipeline
- [[affine_model]] — mean subtraction removes the $b$ parameter

## Sources

- [[01b_linear_algebra_for_matching|Tutorial 01b: Linear Algebra for Matching]] — Part 3
