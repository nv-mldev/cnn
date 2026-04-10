# Part 6: Brightness, Contrast, Dynamic Range, and Clipping

## Learning Objective

Understand what $a$ and $b$ mean in image terms (brightness and contrast), what **dynamic
range** is, and what information is permanently lost when pixels are clipped or
over-quantized.

---

## 6.1 Terminology

| Term | What it is | Math |
|------|-----------|------|
| **Intensity** | Brightness of one pixel | Pixel value (0–255) |
| **Brightness change** | Uniform shift of all pixels | $I + b$ |
| **Contrast change** | Scaling the spread between pixels | $a \cdot I$ |
| **Dynamic range** | Span from darkest to brightest | $\max - \min$ |
| **Contrast stretching** | Rescaling to use full range | $(I - \min)/(\max - \min) \times 255$ |
| **Linear transform** | Both contrast and brightness | $a \cdot I + b$ |

---

## 6.2 Brightness Change ($I + b$)

Adding a constant $b$ shifts all pixel values uniformly. The **differences between
pixels stay unchanged** — the pattern is preserved, just lifted or lowered.

$$\text{If } I' = I + b: \quad I'(j) - I'(i) = I(j) - I(i)$$

Example: $[100, 150, 200]$ → $[130, 180, 230]$ (add 30). Differences: $[50, 50]$ in both.

---

## 6.3 Contrast Change ($a \cdot I$)

Multiplying by $a$ scales the **spread** between pixels. High contrast = large spread;
low contrast = narrow spread.

$$\text{Dynamic range of } a \cdot I = a \cdot (\max - \min)$$

The **ratios** between pixel values are preserved (both $150/100$ and $300/200$ equal 1.5).

---

## 6.4 Dynamic Range

Dynamic range is the span from the darkest to the brightest pixel:

$$\text{Dynamic range} = \max(I) - \min(I)$$

An 8-bit image can represent values from 0 to 255, so the maximum possible dynamic range
is 255. A low-contrast image uses only a fraction of this range.

---

## 6.5 Contrast Stretching

Contrast stretching remaps the range $[\min, \max]$ to the full $[0, 255]$:

$$I' = \frac{I - \min}{\max - \min} \times 255$$

This is a linear transform ($I' = a \cdot I + b$ with $a = 255/(\max - \min)$ and
$b = -255 \cdot \min / (\max - \min)$). Since it is linear, **Pearson correlation with
the original remains 1.0**.

The histogram spreads out — but the gaps it creates are **empty levels** with no data.
No new information is created.

---

## 6.6 Clipping: Irreversible Information Loss

In an 8-bit image, pixel values are clamped to $[0, 255]$. When you multiply a pixel
value by 2 and the result exceeds 255, it clips:

$$200 \times 2 = 400 \xrightarrow{\text{clip}} 255$$
$$250 \times 2 = 500 \xrightarrow{\text{clip}} 255$$

Two **different original values** (200 and 250) both map to 255. This is **irreversible**:
you cannot tell which value was clipped. The information is permanently lost.

The histogram shows a **spike at 255** — a characteristic artifact of clipping.

---

## 6.7 Quantization Loss

Even without clipping, information is lost when quantization is too coarse. An 8-bit
image has only 256 distinct values. If the original data had finer resolution than 1 part
in 256, those distinctions are thrown away at capture time.

Contrast stretching a narrow-range image reveals this: the stretched histogram has
**large gaps** because there were only a few distinct values to stretch.

| Bit depth | Levels | Use case |
|-----------|--------|---------|
| 8-bit | 256 | Standard photography, displays |
| 12-bit | 4,096 | RAW photography, machine vision cameras |
| 16-bit | 65,536 | Medical imaging, scientific instruments |
| float32 | ~$10^7$ unique levels | Computational pipelines, HDR |

---

## Summary

> $a$ and $b$ in the affine model correspond to contrast and brightness in image terms.
> CCOEFF_NORMED handles both. But clipping and quantization are **irreversible losses**
> that happen before our normalisation sees the data — they are constraints of the capture
> pipeline, not fixable by post-processing.
