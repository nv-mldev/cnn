---
tags: [concept, interpolation]
sources: [tutorials/00_introduction_to_digital_images/part4_zoom_and_aliasing.md]
last_updated: 2026-04-05
---

# Bilinear Interpolation

An upsampling method that computes each output pixel as a weighted average of the 4 nearest input pixels, producing smoother results than nearest-neighbour.

## Why It Matters

Bilinear interpolation is the standard trade-off between speed and quality for image resizing. It eliminates the blocky artefacts of [[nearest_neighbour_interpolation|Nearest-Neighbour Interpolation]] but introduces slight blur. Important to understand: it makes images look smoother but does **not** recover lost detail — it invents plausible values between known samples.

## Key Ideas

- Uses fractional offsets $(\alpha, \beta)$ to weight the 4 surrounding pixels:
  $$I_{out} = (1-\alpha)(1-\beta)I_{00} + \alpha(1-\beta)I_{10} + (1-\alpha)\beta I_{01} + \alpha\beta I_{11}$$
- Smoother than nearest-neighbour, slightly blurry
- Does NOT recover information lost during [[downsampling]]
- Higher-order methods (bicubic, LANCZOS) use larger neighbourhoods for even smoother results

## Related Concepts

- [[nearest_neighbour_interpolation|Nearest-Neighbour Interpolation]] — simpler, blockier alternative
- [[downsampling]] — bilinear is often used to upsample after downsampling
- [[spatial_resolution]] — interpolation cannot increase true resolution

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 4
