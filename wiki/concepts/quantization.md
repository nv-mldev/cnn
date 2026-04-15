---
tags: [concept, fundamentals]
sources: [tutorials/00_introduction_to_digital_images/part2_pixels_and_resolution.md]
last_updated: 2026-04-05
---

# Quantization

Mapping a continuous voltage (from the sensor's ADC) to a discrete integer, rounding the measurement to the nearest available level.

## Why It Matters

Quantization is the second fundamental trade-off in digitisation (after [[sampling]]). It determines the precision of each pixel value. With 8-bit quantization (256 levels), the maximum rounding error is ±0.5. With 2-bit (4 levels), the error jumps to ±42.5 — enough to create visible [[false_contours]]. Like spatial sampling, quantization is **irreversible** — the lost precision cannot be recovered.

## Key Ideas

- Step size: $\Delta = \frac{V_{max}}{2^B - 1}$ where $B$ is [[bit_depth]]
- Maximum quantization error: $\pm \Delta / 2$
- 8-bit: Δ = 1, max error = 0.5 (imperceptible)
- 2-bit: Δ = 85, max error = 42.5 (visible banding)
- Fewer bits → larger steps → more visible artefacts
- The ADC (Analog-to-Digital Converter) performs quantization in hardware

## Code Example

```python
import numpy as np

def quantize(image, bits):
    levels = 2 ** bits
    step = 256 / levels
    return (np.floor(image / step) * step).astype(np.uint8)

# 8-bit original → 4-bit (16 levels) → 2-bit (4 levels)
img_4bit = quantize(original, 4)   # step = 16, max error = 8
img_2bit = quantize(original, 2)   # step = 64, max error = 32
```

## Figure — Reducing gray levels on a fixed image

A 452×374 skull X-ray at the same spatial resolution, rendered with 256 → 128 → 64 → 32 → 16 → 8 → 4 → 2 gray levels. As levels drop below ~16, [[false_contours]] appear: smooth gradients turn into visible bands. At 2 levels it becomes a pure binary image.

![[gw_quantization_skull_part1.jpg]]
![[gw_quantization_skull_part2.jpg]]

*Source: Gonzalez & Woods, Digital Image Processing 3rd ed., Fig. 2.21.*

## Related Concepts

- [[bit_depth]] — number of bits determines number of quantization levels
- [[false_contours]] — visible artefact of coarse quantization
- [[sampling]] — the spatial counterpart to intensity quantization
- [[pixel]] — the quantized output value

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 2
