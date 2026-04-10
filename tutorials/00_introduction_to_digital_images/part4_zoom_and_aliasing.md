# Part 4: Zoom and Aliasing — What Pixels Really Look Like

## Learning Objective

Understand what happens when you zoom into or shrink a digital image, why different
interpolation methods produce different results, and what aliasing is.

---

## 4.1 Zoom Reveals the Grid

When you zoom into a digital image, you do not see more detail — you see **the grid
itself**. Each pixel is a single uniform-colour square. There is no hidden detail
inside a pixel; it is just one number.

This is fundamentally different from zooming with a microscope, where you see *more*
detail. Digital zoom just makes the same information bigger.

**Important:** when an image is "zoomed in" on a screen, the display must invent
pixels that are not in the data. The method used to invent those pixels is
called **interpolation**.

---

## 4.2 Interpolation Methods

When upscaling an image, each output pixel maps to a fractional position in the
input. Interpolation defines what value to assign.

### Nearest-neighbour

Copy the value of the closest input pixel. Fast, but produces **blocky artefacts**
— smooth edges look like staircases.

$$I_{\text{out}}(i, j) = I_{\text{in}}\!\left(\text{round}(i / s),\, \text{round}(j / s)\right)$$

where $s$ is the scale factor.

### Bilinear

Compute a weighted average of the four surrounding input pixels. Smoother than
nearest-neighbour but slightly blurry at high zoom factors.

$$I_{\text{out}}(i, j) = (1 - \alpha)(1 - \beta)\, I_{00} + \alpha(1-\beta)\, I_{10} + (1-\alpha)\beta\, I_{01} + \alpha\beta\, I_{11}$$

where $(\alpha, \beta)$ are the fractional offsets within the input pixel cell.

### Bicubic and higher

Use larger neighbourhoods (4×4 for bicubic) for smoother results. More expensive
to compute.

**Key point:** all interpolation methods invent data. None of them recover detail
that was never captured. The only way to get real detail is to capture it with a
higher-resolution sensor.

---

## 4.3 Downsampling

When you shrink an image, you are also discarding information. Downsampling means
keeping only 1 in every $k$ pixels. If the image contains spatial frequencies
higher than $1/(2k)$ of the pixel rate, those frequencies will **alias**.

**Aliasing** occurs when:

$$f_{\text{signal}} > f_{\text{Nyquist}} = \frac{f_s}{2}$$

where $f_s$ is the sampling frequency (pixels per unit length). The aliased
frequency "folds back" and appears as a lower-frequency pattern that was not in the
original scene.

The fix: apply a **low-pass (anti-aliasing) filter** before downsampling to remove
all spatial frequencies above the Nyquist limit. PIL's `Image.LANCZOS` and
`Image.ANTIALIAS` modes do this automatically.

---

## 4.4 The Checkerboard Aliasing Demo

A checkerboard pattern at the Nyquist frequency is the canonical aliasing example.
The pattern has one black and one white square per pixel — it is already at the
limit. Downsampling it by 2× without filtering produces a completely different
(solid grey or wrong-frequency) pattern.

This is exactly what happens in practice when fine textures are downsampled:
- Brick walls → moiré patterns
- Fine mesh fabric → colour fringes
- High-frequency edges → jagged artefacts

---

## 4.5 Information Loss Is Permanent

Both downsampling and low-bit-depth quantization result in **irreversible information
loss**. After the image is captured, that information cannot be recovered:

- You cannot "enhance" a low-resolution image to see detail that was never sampled.
- You cannot undo quantization to recover the exact pre-quantized brightness.

This is a hard physical limit, not a software limitation.

---

## Summary

| Concept | Key fact |
|---------|----------|
| Digital zoom | Makes grid squares bigger; invents no new detail |
| Nearest-neighbour | Fastest; blocky artefacts |
| Bilinear | Smooth; slight blur |
| Aliasing | High frequencies fold to wrong frequencies when undersampled |
| Anti-aliasing filter | Low-pass filter before downsampling prevents aliasing |
| Information loss | Downsampling and quantization are irreversible |

**Next:** Part 5 — Colour channels and the imaging pipeline.
