---
tags: [concept, linear-algebra]
sources: [tutorials/01b_linear_algebra_for_matching/part3_orthogonality_and_projection.md]
last_updated: 2026-04-09
---

# Orthogonal Projection

Decomposing a vector into a component along a direction $\hat{u}$ and a component perpendicular to it: $\text{proj}_{\hat{u}}(v) = (v \cdot \hat{u})\hat{u}$.

## Why It Matters

Orthogonal projection is the mathematical operation underneath [[mean_subtraction]]. Projecting a pixel vector onto $[1,1,\ldots,1]/\sqrt{n}$ extracts the mean brightness; the residual (the perpendicular part) is the pure pattern with brightness removed. This is not a heuristic — it is a precise geometric decomposition where the two parts are guaranteed [[orthogonality|orthogonal]] and cannot interfere.

## Key Ideas

- $\text{proj}_{\hat{u}}(v) = (v \cdot \hat{u})\hat{u}$ — the component of $v$ along unit vector $\hat{u}$
- Residual: $v_\perp = v - \text{proj}_{\hat{u}}(v)$ — the component perpendicular to $\hat{u}$
- $v = \text{proj}_{\hat{u}}(v) + v_\perp$ — unique decomposition
- $\text{proj}_{\hat{u}}(v) \cdot v_\perp = 0$ — the two parts are orthogonal (guaranteed)
- For [[mean_subtraction]]: $\hat{u} = [1,1,\ldots,1]/\sqrt{n}$, and $v \cdot \hat{u} = \bar{v}\sqrt{n}$, so the projection broadcasts the mean

## Code Example

```python
import numpy as np

def project_along(v, u_hat):
    """Project v onto unit vector u_hat."""
    scalar = np.dot(v, u_hat)
    return scalar * u_hat

pixel_vector = np.array([100, 150, 200, 150, 100], dtype=float)
brightness_direction = np.ones(5) / np.sqrt(5)

# Project onto brightness direction
brightness_part = project_along(pixel_vector, brightness_direction)
pattern_part = pixel_vector - brightness_part

print(f"Original:   {pixel_vector}")
print(f"Brightness: {brightness_part}")  # [140, 140, 140, 140, 140] — the mean!
print(f"Pattern:    {pattern_part}")     # [-40, 10, 60, 10, -40] — mean-subtracted
```

## Mathematical Model

For projection onto unit vector $\hat{u}$:

$$\text{proj}_{\hat{u}}(v) = (v \cdot \hat{u})\hat{u}$$

When $\hat{u} = \frac{\mathbf{1}}{\sqrt{n}}$ (the brightness direction):

$$(v \cdot \hat{u}) = \frac{1}{\sqrt{n}} \sum_i v_i = \bar{v}\sqrt{n}$$

$$\text{proj}_{\hat{u}}(v) = \bar{v}\sqrt{n} \cdot \frac{\mathbf{1}}{\sqrt{n}} = \bar{v} \cdot \mathbf{1} = [\bar{v}, \bar{v}, \ldots, \bar{v}]$$

So the projection broadcasts the mean to every element — exactly what mean subtraction removes.

## Related Concepts

- [[orthogonality]] — projection creates orthogonal components
- [[mean_subtraction]] — the specific application to brightness removal
- [[dot_product]] — used to compute the scalar projection
- [[unit_vector]] — projection requires a unit direction vector

## Sources

- [[01b_linear_algebra_for_matching|Tutorial 01b: Linear Algebra for Matching]] — Part 3
