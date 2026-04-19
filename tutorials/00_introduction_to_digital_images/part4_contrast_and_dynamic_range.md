# Part 3: Contrast and Dynamic Range

## Learning Objective

Understand what contrast means numerically, how the sensor's dynamic range limits
what it can capture, and why low-contrast images are hard for pixel-comparison algorithms.

---

## 3.1 What Is Contrast?

**Contrast** is the spread of pixel values in an image — how far apart the dark and
bright regions are.

Formally, the contrast of a region can be quantified as:

$$C = \frac{I_{\max} - I_{\min}}{I_{\max} + I_{\min}} \quad \text{(Michelson contrast)}$$

or simply as the standard deviation of pixel values:

$$C_\sigma = \text{std}(I)$$

A high-contrast image has pixel values spread across the full 0–255 range. A
low-contrast image has pixel values clustered in a narrow band.

**Key implication for computer vision:** if two images of the same object have
different contrast, their pixel values are numerically different — even though the
content is identical. Any algorithm that compares pixels directly will see them as
"different."

---

## 3.2 The Affine Relationship Between Exposures

When the same scene is photographed under different lighting conditions, the pixel
values obey an **affine transformation**:

$$I_2(i, j) = a \cdot I_1(i, j) + b$$

where:
- $a$ controls **contrast** (global scaling of all values)
- $b$ controls **brightness** (global offset to all values)

This is the core reason raw pixel comparison fails. Even a small change in
illumination (like moving a lamp slightly) changes both $a$ and $b$, invalidating
any pixel-level comparison.

---

## 3.3 Dynamic Range

**Dynamic range** is the ratio between the brightest and darkest values a sensor can
capture simultaneously:

$$\text{DR} = 20 \log_{10}\!\left(\frac{I_{\max}}{I_{\min}}\right) \quad \text{(in dB)}$$

or equivalently: the number of stops, where each stop is a factor of 2.

| System | Dynamic range |
|--------|--------------|
| Human eye (adapted) | ~21 stops (126 dB) |
| Modern DSLR | ~14 stops (84 dB) |
| Phone camera | ~10–12 stops (60–72 dB) |
| 8-bit image | ~48 dB (log₁₀(255/1) × 20) |

### The dynamic range problem

Real-world scenes often have **higher dynamic range than the sensor can capture**.
For example: a window in a dark room. If the sensor exposes for the window, the room
is black (underexposed). If it exposes for the room, the window is white (overexposed).
Both cases result in **clipped pixel values** — information is permanently lost.

---

## 3.4 Low-Contrast Images

A low-contrast image is one where all pixel values are compressed into a narrow range.
Common causes:

- **Overcast lighting** (soft, shadowless scenes): the dynamic range of the scene is
  small so the sensor maps it to a narrow band.
- **Underexposure**: the scene is dim; all pixels cluster near 0.
- **Fog or haze**: scattering adds a constant offset to all values, pushing them toward
  the same grey.

The histogram of a low-contrast image is **narrow** — most intensity levels are unused.

**Consequence:** two objects that are genuinely different in the real world may produce
pixel values that are nearly identical in a low-contrast image. Pixel-comparison
algorithms are fooled into calling them "similar."

---

## 3.5 Contrast Levels: The Einstein Example

The Gonzalez & Woods DIP textbook contains three versions of an Einstein portrait at
different contrast levels (Figs 0241a, b, c). These are the same image — same content,
same spatial layout — but the pixel values differ dramatically.

- **Low contrast:** pixels cluster in the 100–180 range. The image appears washed out.
- **Medium contrast:** pixels spread across 50–220. The image looks natural.
- **High contrast:** pixels span nearly the full 0–255 range. The image looks "punchy."

**The same face produces pixel values that differ by up to 100 grey levels** depending
only on the contrast setting. This makes pixel-level matching unreliable.

---

## Summary

| Concept | Key fact |
|---------|----------|
| Contrast | Spread of pixel values; same content → different values at different contrast |
| Affine model | $I_2 = a \cdot I_1 + b$; contrast and brightness change break pixel comparison |
| Dynamic range | Ratio of max to min; real scenes often exceed sensor DR |
| Low contrast | Narrow histogram; different objects → similar pixel values |

**Next:** Part 4 — Zooming in and aliasing.
