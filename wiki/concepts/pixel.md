---
tags: [concept, fundamentals]
sources: [tutorials/00_introduction_to_digital_images/part2_pixels_and_resolution.md]
last_updated: 2026-04-05
---

# Pixel

A single number at position $(i, j)$ in a 2D grid, representing the average brightness captured by one [[photosite]]. Not a tiny photograph — just an integer.

## Why It Matters

The most common misconception in imaging is that a pixel contains rich information about a tiny patch of the scene. It doesn't. A pixel is one number — an average brightness value that has been corrupted by [[shot_noise]], rounded by [[quantization]], and transformed by the [[imaging_pipeline]]. Zooming into an image makes the grid squares bigger; it does not reveal hidden detail.

## Key Ideas

- A pixel is a **single integer** (typically 0–255 for 8-bit images)
- Position: row $i$, column $j$ (origin at top-left)
- Grayscale: one value per pixel; Colour: three values (R, G, B) per pixel
- The value depends on scene content **and** lighting, exposure, noise, ISP processing, and spatial position
- Digital zoom = making grid squares bigger — no new information is created
- A pixel value is **not** a reliable measure of scene content — this is the central lesson of Tutorial 00

## Related Concepts

- [[photosite]] — the physical element that produces the pixel value
- [[spatial_resolution]] — how many pixels the image has
- [[quantization]] — how continuous voltage becomes a discrete pixel value
- [[bit_depth]] — how many possible values a pixel can take
- [[affine_model]] — why the same scene produces different pixel values

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 2
