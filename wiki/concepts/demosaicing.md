---
tags: [concept, colour, image-processing]
sources: [tutorials/00_introduction_to_digital_images/part5_colour_and_pipeline.md]
last_updated: 2026-04-05
---

# Demosaicing

The process of interpolating missing colour channels at each pixel from the [[bayer_filter]] mosaic to produce a full RGB image.

## Why It Matters

Since each photosite only captures one colour, demosaicing must **invent** the other two channels at every pixel. This is an estimation — the interpolated values are not measurements but computed guesses based on neighbouring pixels. This introduces another layer of processing between the scene and the stored pixel values, and can create colour artefacts at sharp edges.

## Key Ideas

- Input: raw Bayer mosaic (one colour per pixel)
- Output: full RGB image (three colours per pixel)
- Simple methods: bilinear interpolation of missing channels
- Advanced methods: edge-aware algorithms that avoid colour bleeding across edges
- Artefacts: colour moiré, zipper effect at high-contrast edges
- Part of the [[imaging_pipeline]] — happens before white balance and tone mapping

## Related Concepts

- [[bayer_filter]] — the mosaic pattern that requires demosaicing
- [[imaging_pipeline]] — demosaicing is an early stage
- [[bilinear_interpolation]] — simplest demosaicing method

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 5
