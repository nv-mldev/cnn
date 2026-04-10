# Part 2: Pixels and Resolution — What a Pixel Actually Is

## Learning Objective

Understand what a pixel is, what spatial resolution means, and how quantization maps
continuous brightness to discrete integer values.

---

## 2.1 The Pixel Grid

An image is stored as a 2D array of shape `(height, width)` for grayscale or
`(height, width, 3)` for colour. We use the convention:

- **Row $i$** runs top to bottom (the $y$ axis, increasing downward)
- **Column $j$** runs left to right (the $x$ axis)
- **Origin** is the top-left corner: pixel $(0, 0)$

In NumPy: `image[i, j]` retrieves the value at row $i$, column $j$.

---

## 2.2 What a Pixel Actually Is

A pixel is **not** a tiny square photo of reality. It is a **single number** — the
average brightness measured by one sensor element at one grid location. It has:

- A **position** $(i, j)$ on the grid
- A **value** (brightness / intensity)
- **No internal structure** — it is just a number

When we display an image we *render* each pixel as a coloured square. That is just
visualisation — the underlying data is a 2D array of integers.

**Consequence:** zooming into a digital image does not reveal more detail. It only
makes the grid squares bigger. There is no hidden information inside a pixel.

---

## 2.3 Spatial Resolution

**Spatial resolution** is the number of pixels used to represent the scene:

$$\text{Resolution} = \text{width} \times \text{height} \quad \text{(pixels)}$$

More pixels means finer sampling of the scene, which preserves more spatial detail.
But resolution is always a trade-off:

| Resolution | Detail | File size | Processing cost |
|------------|--------|-----------|-----------------|
| High | Fine details preserved | Large | Slow |
| Low | Fine details lost | Small | Fast |

### Resolution and physical scale

Resolution alone is not enough. The **physical size** each pixel represents in the
scene also matters. This is called **ground sampling distance (GSD)**:

$$\text{GSD} = \frac{\text{physical scene width}}{\text{image width in pixels}}$$

For example: a 1000 × 1000 image of a 1 m² surface has GSD = 1 mm/pixel. The same
resolution image of a 10 m² surface has GSD = 10 mm/pixel — 10× less detail.

---

## 2.4 Quantization

After the sensor counts electrons, the **ADC** maps the continuous voltage to a
discrete integer. This mapping is called **quantization**.

For an 8-bit image: 256 possible values (0–255).
For a 12-bit image: 4096 possible values (0–4095).

The **quantization step size** is:

$$\Delta = \frac{V_{\max}}{2^B - 1}$$

where $B$ is the bit depth and $V_{\max}$ is the maximum voltage. Any brightness
that falls between two quantization levels is rounded to the nearest level.

### Quantization error

The rounding introduces a **quantization error** of up to $\pm \Delta / 2$. For 8-bit:

$$\Delta = \frac{255}{255} = 1 \quad \Rightarrow \quad \text{max error} = 0.5 \text{ intensity unit}$$

For 2-bit (4 levels):

$$\Delta = \frac{255}{3} = 85 \quad \Rightarrow \quad \text{max error} = 42.5 \text{ intensity units}$$

This means: **reducing bit depth adds structured error to every pixel value**, even
for a perfect sensor with no shot noise.

### False contours

When bit depth is very low (2–4 bits), smooth gradients in the scene produce
**false contours** — visible step edges where the true scene is smooth. This is a
direct visual artefact of quantization error.

---

## 2.5 The Two Sources of Error So Far

| Source | Type | Controllable? |
|--------|------|--------------|
| Shot noise | Random (Poisson) | Partially — more light reduces it |
| Quantization error | Deterministic (rounding) | Yes — more bits eliminate it |

Both errors affect pixel values. Neither is about the scene content. Any algorithm
that does pixel-level comparison is affected by both.

---

## Summary

| Concept | Key fact |
|---------|----------|
| Pixel | Single number = average brightness at one grid location |
| Resolution | Grid dimensions; more pixels = more spatial detail |
| GSD | Physical size per pixel; determines real-world detail |
| Quantization | Rounding to nearest discrete level; error ≤ Δ/2 |
| Bit depth | 8-bit = 256 levels; 2-bit = 4 levels with visible artefacts |

**Next:** Part 3 — Contrast, dynamic range, and what happens when scenes are washed out.
