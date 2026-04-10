---
tags: [concept, linear-algebra]
sources: [tutorials/01b_linear_algebra_for_matching/part1_vectors_and_dot_product.md]
last_updated: 2026-04-09
---

# Vector Representation

Flattening an image patch into a 1D array, treating it as a point (or arrow) in $n$-dimensional space where $n$ is the number of pixels.

## Why It Matters

This is the conceptual bridge between "image" and "math." Once a $3 \times 3$ patch becomes a 9-element vector, every tool from linear algebra — norms, dot products, projections, transforms — applies directly. Without this step, images are just grids of numbers with no algebraic structure. With it, comparing two patches becomes measuring the distance or angle between two points in $\mathbb{R}^n$.

## Key Ideas

- A $3 \times 3$ grayscale patch has 9 pixels → flatten to a vector in $\mathbb{R}^9$
- A $640 \times 480$ image lives in $\mathbb{R}^{307200}$ — impossibly high-dimensional, but the math still works
- Each axis corresponds to one pixel location; the coordinate is the pixel value
- Two similar patches are nearby points; two different patches are far apart
- This representation makes [[dot_product]], [[l2_norm]], and [[cosine_similarity]] meaningful

## Code Example

```python
import numpy as np

# A 3x3 image patch
patch = np.array([
    [120, 130, 125],
    [140, 200, 145],
    [122, 132, 128]
])

# Flatten to a vector in R^9
vector = patch.flatten()
print(f"Shape: {vector.shape}")  # (9,)
print(f"This patch is a point in {vector.size}-dimensional space")
```

## Related Concepts

- [[dot_product]] — first operation enabled by vector form
- [[l2_norm]] — measures magnitude (energy) of the vector
- [[cosine_similarity]] — compares direction (pattern) between vectors
- [[manifold_hypothesis]] — natural images occupy a thin manifold in this high-dimensional space

## Sources

- [[01b_linear_algebra_for_matching|Tutorial 01b: Linear Algebra for Matching]] — Part 1
