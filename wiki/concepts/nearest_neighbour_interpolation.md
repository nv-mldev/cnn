---
tags: [concept, interpolation]
sources: [tutorials/00_introduction_to_digital_images/part4_zoom_and_aliasing.md]
last_updated: 2026-04-05
---

# Nearest-Neighbour Interpolation

An upsampling method that assigns each output pixel the value of the closest input pixel, producing a blocky, grid-like appearance.

## Why It Matters

It's the simplest and fastest interpolation — just copy the nearest pixel. It makes the pixel grid explicitly visible when zooming, which is useful for understanding that zooming reveals the grid, not hidden detail. But it produces blocky artefacts that make edges look jagged.

## Key Ideas

- Formula: $I_{out}(i,j) = I_{in}(\text{round}(i/s), \text{round}(j/s))$
- Fast — just a lookup, no computation
- Preserves exact original values (no averaging)
- Produces blocky artefacts — each pixel becomes a visible square
- Useful for visualising the pixel grid; poor for perceptual quality

## Related Concepts

- [[bilinear_interpolation]] — smoother alternative using 4-neighbour average
- [[pixel]] — nearest-neighbour makes the pixel grid visible
- [[downsampling]] — the inverse operation

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 4
