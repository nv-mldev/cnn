# Part 4: Fixing the Brightness Offset — Mean Subtraction

## Learning Objective

Understand **why mean subtraction removes the brightness offset $b$**, prove it using
orthogonal decomposition, and visualise this geometrically and on image patches.

---

## 4.1 The Problem

When there is a uniform brightness offset ($I = T + b$), every pixel shifts by the same
constant. After L2 normalisation, the two vectors point in **different directions** — so
even `TM_SQDIFF_NORMED` gives a nonzero score.

The shift is equivalent to adding $b \cdot [1,1,...,1]$ to the vector, which nudges it
**toward the diagonal direction** $[1,1,...,1]$.

---

## 4.2 The Fix: Subtract the Mean

For any vector $\vec{v}$ with mean $\bar{v}$:

$$\vec{v} = \underbrace{\bar{v} \cdot [1,1,...,1]}_{\text{mean component}} + \underbrace{(\vec{v} - \bar{v} \cdot [1,1,...,1])}_{\text{residual}}$$

Subtracting the mean removes the $[1,1,...,1]$ component. But is this split *special*?
We need to prove the two parts are **orthogonal** — otherwise this decomposition tells us
nothing useful.

---

## 4.3 Proof: The Residual is Always Orthogonal to $[1,1,...,1]$

### Step 1: The residual always sums to zero

$$\sum_i (v_i - \bar{v}) = \sum_i v_i - n \cdot \bar{v} = \sum_i v_i - n \cdot \frac{\sum_i v_i}{n} = 0$$

This is true **by construction** — subtracting the mean forces the sum to zero.

### Step 2: Zero sum → zero dot product with $[1,1,...,1]$

$$(\vec{v} - \bar{v} \cdot [1,1,...,1]) \cdot [1,1,...,1] = \sum_i (v_i - \bar{v}) \cdot 1 = 0$$

The dot product equals the sum, and we proved the sum is always zero.

### Conclusion: Orthogonal Decomposition

$$\vec{v} = \underbrace{\bar{v} \cdot [1,1,...,1]}_{\vec{v}_\parallel \text{ (brightness)}} + \underbrace{(\vec{v} - \bar{v} \cdot [1,1,...,1])}_{\vec{v}_\perp \text{ (pattern)}}$$

Mean subtraction is an **orthogonal projection** onto the plane perpendicular to
$[1,1,...,1]$. The two components live in completely independent subspaces.

---

## 4.4 Why This Fixes the Brightness Offset

Since the decomposition is orthogonal:
- The brightness component $\vec{v}_\parallel$ (the $[1,1,...,1]$ part) is removed
- The pattern component $\vec{v}_\perp$ survives unchanged
- Any uniform brightness shift **only changes the $[1,1,...,1]$ component**, which is
  exactly what we remove

Three patches with the same pattern but different brightness:

| Patch | Mean | Centered (pattern) |
|-------|------|-------------------|
| $[100, 150, 200]$ | 150 | $[-50, 0, 50]$ |
| $[130, 180, 230]$ | 180 | $[-50, 0, 50]$ |
| $[500, 550, 600]$ | 550 | $[-50, 0, 50]$ |

Different means (different brightness) → **same centered pattern**.

---

## 4.5 The DC/AC Analogy

In signal processing terms:
- **DC component** = mean value = the $\bar{v} \cdot [1,1,...,1]$ part = uniform brightness
- **AC component** = the variation around the mean = the pattern

Mean subtraction removes the DC. The AC (pattern) is what the sensor cares about for
template matching.

---

## 4.6 Limitation: Non-Uniform Brightness

This only works when the brightness change is **uniform** (same offset for every pixel).
If the change is non-uniform (a shadow falls on part of the template), the offset is an
arbitrary vector — not aligned with $[1,1,...,1]$. Mean subtraction cannot fully cancel it.

---

## Summary

> Mean subtraction is a proven orthogonal projection. It removes exactly the $[1,1,...,1]$
> component (uniform brightness), leaving only the pattern. Combined with L2 normalisation
> (which removes scaling), we get a metric that is invariant to any affine transform
> $I = a \cdot T + b$.
