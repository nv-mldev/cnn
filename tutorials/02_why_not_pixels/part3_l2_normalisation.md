# Part 3: Fixing the Scaling Factor — L2 Normalisation

## Learning Objective

Understand how **dividing by the L2 norm** removes the contrast/gain factor $a$ from
the affine model, and why this corresponds geometrically to projecting vectors onto the
**unit sphere**.

---

## 3.1 SSD Fails on Both $a$ and $b$

The affine model says $I \approx a \cdot T + b$. Raw SSD is sensitive to both:

- **Scaling ($a \neq 1$):** every pixel value is multiplied — distances blow up proportionally
- **Offset ($b \neq 0$):** every pixel shifts — even identical patterns have nonzero SSD

We fix each separately. Part 3 fixes $a$. Part 4 fixes $b$.

---

## 3.2 The Scaling Factor $a$ — Treating Pixels as Vectors

When contrast changes ($I = a \cdot T$), the **ratios** between pixel values are preserved
(same direction in vector space), but the **magnitude** is different (different vector
length).

Think of a 3-pixel patch $[100, 150, 200]$ as a point in 3D space. A patch $[200, 300, 400]$
(contrast ×2) is a different point — but both lie on the **same ray** from the origin.

**Insight:** scaling changes the *length* of the vector, not its *direction*.

---

## 3.3 The L2 Norm

The L2 norm of a vector $\vec{v}$ with $n$ elements is:

$$\|\vec{v}\|_2 = \sqrt{\sum_{i=1}^n v_i^2}$$

For our 3-pixel patch $[100, 150, 200]$:

$$\|[100, 150, 200]\| = \sqrt{100^2 + 150^2 + 200^2} = \sqrt{67500} \approx 259.8$$

---

## 3.4 Dividing by L2 Norm — Projection onto the Unit Sphere

Dividing a vector by its L2 norm yields a **unit vector** of length 1:

$$\hat{v} = \frac{\vec{v}}{\|\vec{v}\|_2}$$

This operation **throws away the magnitude** (how bright the patch is) and keeps only
the **direction** (the pattern of ratios between pixels).

Two patches with the **same pattern but different brightness** point in the **same
direction** from the origin → they land on the **same point on the unit sphere**.

---

## 3.5 Geometric Meaning

In $n$-dimensional pixel space, the unit sphere is the surface of all points at distance
1 from the origin. After L2 normalisation:

- $[10, 20, 30]$ and $[100, 200, 300]$ and $[1000, 2000, 3000]$ all map to the same point
- The cosine of the angle between two unit vectors = their dot product = 1.0 for identical patterns

This is why `TM_SQDIFF_NORMED` (which internally uses this normalisation) is more robust
than raw SSD to contrast changes.

---

## 3.6 Why Offset ($b$) Changes Direction

Adding a constant $c$ to every element is equivalent to adding the vector $c \cdot [1,1,1]$.
This **nudges the original vector toward the diagonal direction $[1,1,1,...,1]$**, changing
its direction — not just its length.

| Operation | Geometric effect | L2 normalisation fixes it? |
|-----------|-----------------|--------------------------|
| Scaling ($I = a \cdot T$) | Changes length, same direction | **Yes** — both land on same point on unit sphere |
| Offset ($I = T + b$) | Shifts direction toward $[1,1,1]$ | **No** — they land on different points |

This is why `TM_SQDIFF_NORMED` handles contrast changes but still fails on brightness
offset — and why we need mean subtraction (Part 4) as an additional step.

---

## Summary

> L2 normalisation removes the multiplicative factor $a$ by projecting both vectors onto
> the unit sphere. It compares **directions**, not magnitudes. But it cannot remove an
> additive offset — that requires a separate operation (mean subtraction).
