---
tags: [concept, linear-algebra]
sources: [tutorials/01b_linear_algebra_for_matching/part3_orthogonality_and_projection.md]
last_updated: 2026-04-09
---

# Orthogonality

Two vectors are orthogonal when their [[dot_product]] is zero: $a \cdot b = 0$. Geometrically, they are perpendicular — completely independent, with no component of one along the other.

## Why It Matters

Orthogonality is the mathematical reason why [[mean_subtraction]] works. After subtracting the mean, the residual vector is orthogonal to the brightness direction $[1,1,\ldots,1]$. This means no brightness offset — no matter how large — can affect the residual. Brightness and pattern live in perpendicular subspaces, so they cannot interfere with each other. This orthogonal decomposition is the foundation of normalised template matching.

## Key Ideas

- $a \cdot b = 0$ means the vectors are perpendicular — zero projection of one onto the other
- Any vector can be decomposed into a component along a direction and a component orthogonal to it
- After mean subtraction: the mean component (along $[1,\ldots,1]$) and the residual are orthogonal
- Pythagoras in $n$-D: if $a \perp b$, then $\|a + b\|^2 = \|a\|^2 + \|b\|^2$
- Orthogonal decomposition is unique — there is exactly one way to split a vector into parallel and perpendicular parts

## Code Example

```python
import numpy as np

vector = np.array([10, 20, 30, 20, 10], dtype=float)
ones = np.ones(5) / np.sqrt(5)  # unit vector along [1,1,...,1]

# Decompose into brightness (along ones) and pattern (orthogonal to ones)
brightness_component = np.dot(vector, ones) * ones
pattern_component = vector - brightness_component

# Verify orthogonality
print(f"Dot product: {np.dot(brightness_component, pattern_component):.10f}")  # ~0
print(f"Pythagoras:  {np.linalg.norm(vector)**2:.2f} = "
      f"{np.linalg.norm(brightness_component)**2:.2f} + "
      f"{np.linalg.norm(pattern_component)**2:.2f}")
```

## Related Concepts

- [[dot_product]] — orthogonality is defined by dot product being zero
- [[orthogonal_projection]] — the operation that creates the orthogonal decomposition
- [[mean_subtraction]] — the specific case of projecting out the brightness direction
- [[orthogonal_transform]] — transforms whose columns are mutually orthogonal

## Sources

- [[01b_linear_algebra_for_matching|Tutorial 01b: Linear Algebra for Matching]] — Part 3
