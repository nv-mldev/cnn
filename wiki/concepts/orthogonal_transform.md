---
tags: [concept, linear-algebra]
sources: [tutorials/01b_linear_algebra_for_matching/part4_linear_and_orthogonal_transforms.md]
last_updated: 2026-04-09
---

# Orthogonal Transform

A [[linear_transform]] whose matrix $Q$ satisfies $Q^TQ = I$ (columns are orthonormal). Geometrically, a pure rotation and/or reflection — no stretching, no compression.

## Why It Matters

Orthogonal transforms are energy-preserving: $\|Qx\| = \|x\|$ for all $x$. This means distances and angles computed in the transform domain are identical to those in pixel space. The DFT, DCT, and Hadamard transform are all orthogonal — so you can compute template matching in the frequency domain and get the same answer as in pixel space. Parseval's theorem formalises this guarantee.

## Key Ideas

- $Q^TQ = QQ^T = I$ — the inverse is the transpose
- Columns of $Q$ form an orthonormal basis: mutually [[orthogonality|orthogonal]], each with unit [[l2_norm]]
- **Energy preservation**: $\|Qx\| = \|x\|$ for all $x$
- **Distance preservation**: $\|Qx - Qy\| = \|x - y\|$
- **Angle preservation**: $\cos\theta$ between vectors is unchanged
- **Parseval's theorem**: $\sum_i |x_i|^2 = \sum_i |X_i|^2$ — total energy in pixel domain equals total energy in transform domain
- Examples: DFT, DCT, Hadamard, rotation matrices, permutation matrices

## Code Example

```python
import numpy as np
from scipy.fft import dct

# Create orthonormal DCT matrix for n=4
n = 4
Q = np.zeros((n, n))
for k in range(n):
    basis = np.zeros(n)
    basis[k] = 1.0
    Q[:, k] = dct(basis, type=2, norm='ortho')

# Verify orthogonality: Q^T Q = I
print(f"Q^T Q ≈ I: {np.allclose(Q.T @ Q, np.eye(n))}")

# Verify energy preservation (Parseval's theorem)
x = np.array([10, 20, 30, 20], dtype=float)
X = Q.T @ x  # transform to DCT domain

print(f"Pixel energy:    {np.sum(x**2):.2f}")
print(f"Transform energy: {np.sum(X**2):.2f}")  # Same!
print(f"Parseval holds: {np.allclose(np.sum(x**2), np.sum(X**2))}")
```

## Mathematical Model

For orthogonal matrix $Q$ with $Q^TQ = I$:

$$\|Qx\|^2 = (Qx)^T(Qx) = x^TQ^TQx = x^Tx = \|x\|^2$$

**Parseval's theorem** (discrete form):

$$\sum_{i=0}^{n-1} |x_i|^2 = \sum_{k=0}^{n-1} |X_k|^2$$

where $X = Q^T x$. This guarantees that SSD, cosine similarity, and all norm-based metrics give identical results in either domain.

## Related Concepts

- [[linear_transform]] — orthogonal transforms are a special case
- [[orthogonality]] — columns of $Q$ are mutually orthogonal
- [[l2_norm]] — preserved by orthogonal transforms
- [[unit_vector]] — columns of $Q$ are unit vectors

## Sources

- [[01b_linear_algebra_for_matching|Tutorial 01b: Linear Algebra for Matching]] — Part 4
