# Part 5: Combining Both Fixes — Pearson Correlation (CCOEFF_NORMED)

## Learning Objective

Understand how **mean subtraction + L2 normalisation together** produce the Pearson
correlation coefficient, which is invariant to any positive linear transform $I = aT + b$.
Connect the geometric proof to its statistical interpretation.

---

## 5.1 The Combined Formula

Combining mean subtraction (removes $b$) and L2 normalisation (removes $a$):

$$R = \frac{\sum (I_i - \bar{I})(T_i - \bar{T})}{\sqrt{\sum (I_i - \bar{I})^2} \cdot \sqrt{\sum (T_i - \bar{T})^2}}$$

This is exactly the **Pearson correlation coefficient** — and it is identical to
`TM_CCOEFF_NORMED` in OpenCV.

---

## 5.2 Why Centering Removes $b$, Normalising Removes $a$

Starting from $Y = aX + b$:

**Step 1: Centering removes $b$**

$$Y - \bar{Y} = (aX + b) - \overline{(aX + b)} = (aX + b) - (a\bar{X} + b) = a(X - \bar{X})$$

The constant $b$ cancels exactly. After centering, $Y_c = a \cdot X_c$.

**Step 2: Normalising removes $a$**

$$\sigma_Y = |a| \cdot \sigma_X$$

Dividing the centered $Y$ by $\sigma_Y$ gives:

$$\frac{Y - \bar{Y}}{\sigma_Y} = \frac{a(X - \bar{X})}{|a| \sigma_X} = \text{sign}(a) \cdot \frac{X - \bar{X}}{\sigma_X}$$

For $a > 0$, this equals $\frac{X - \bar{X}}{\sigma_X}$. The scale factor $a$ is gone.

**Result:** After both operations, $X$ and $Y = aX + b$ become **identical vectors**.
The Pearson correlation $r = 1.0$.

---

## 5.3 The Statistical View

The same operations we proved geometrically have exact statistical interpretations:

| Step | Geometric View | Statistical View |
|------|---------------|------------------|
| Subtract mean | Project out the $[1,1,1]$ component | Center the random variable (remove location) |
| Residual sums to zero | Centered vector ⊥ $[1,1,1]$ | Centered data has zero mean (by construction) |
| Divide by L2 norm | Project onto unit sphere | Divide by standard deviation (standardize) |
| Dot product of normalized centered vectors | Cosine of angle on perpendicular plane | Pearson correlation coefficient |
| Brightness offset cancels | $[1,1,1]$ component removed | Location parameter removed |
| Non-uniform brightness fails | Offset not aligned with $[1,1,1]$ | Non-constant offset is not a location shift |

---

## 5.4 Variance = Squared L2 Norm of Centered Vector

The variance of a set of values:
$$\text{Var}(X) = \frac{1}{n} \sum (x_i - \bar{x})^2$$

The squared L2 norm of the centered vector:
$$\| \vec{v}_{\text{centered}} \|^2 = \sum (v_i - \bar{v})^2$$

They differ only by $\frac{1}{n}$. Standard deviation and L2 norm of the centered vector
are the same quantity (up to a factor of $\sqrt{n}$).

---

## 5.5 CCOEFF_NORMED ≡ Pearson Correlation

The `TM_CCOEFF_NORMED` formula and the Pearson correlation coefficient $r$ are
**exactly the same formula** — just written with image notation (I, T) instead of
statistical notation (X, Y).

---

## 5.6 What Each Method Handles

| Method | SSD | SQDIFF\_NORMED | CCOEFF\_NORMED |
|--------|-----|---------------|----------------|
| Raw SSD = 0? | Only exact copy | Only direction match | Only pattern match |
| Brightness invariant? | No | No | **Yes** (uniform only) |
| Contrast invariant? | No | Yes | **Yes** |
| Best match at | min → 0 | min → 0 | **max → 1** |

---

## Summary

> CCOEFF_NORMED = Pearson correlation. It cancels $a$ (by L2 normalisation of centred
> vectors) and cancels $b$ (by mean subtraction). The result is invariant to any affine
> transform $I = aT + b$ with $a > 0$.  This is the ceiling of what normalisation can
> do — further improvements (for rotation, scale, occlusion) require features.
