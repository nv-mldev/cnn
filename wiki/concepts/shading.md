---
tags: [concept, image-formation]
sources: [tutorials/00_introduction_to_digital_images/part5_colour_and_pipeline.md]
last_updated: 2026-04-05
---

# Shading (Vignetting)

Spatially non-uniform illumination or sensor response that causes the same material to produce different pixel values depending on its position in the image.

## Why It Matters

Shading means a pixel's value depends not just on what's there but **where** it is. The centre of an image is typically brighter than the edges (vignetting from the lens, or non-uniform lighting). A uniform white surface won't produce uniform pixel values. This is yet another reason why comparing pixel values directly is unreliable — position-dependent gain corrupts the measurement.

## Key Ideas

- Modelled as: $I(i,j) = T(i,j) \times S(i,j)$ where $T$ is reflectance (what you want) and $S$ is the shading field (what you don't)
- Causes: lens vignetting, non-uniform illumination, sensor edge effects
- A tungsten filament example: same material reads 50–150 at centre vs 20–80 at edges
- Makes the [[affine_model]] position-dependent — $a$ and $b$ vary spatially
- Can be corrected with flat-field calibration (divide by image of uniform surface)

## Related Concepts

- [[affine_model]] — shading makes affine parameters spatially varying
- [[imaging_pipeline]] — shading is a pre-capture phenomenon
- [[pixel]] — shading makes pixel values position-dependent

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 5
