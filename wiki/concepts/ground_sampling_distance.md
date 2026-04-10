---
tags: [concept, fundamentals]
sources: [tutorials/00_introduction_to_digital_images/part2_pixels_and_resolution.md]
last_updated: 2026-04-05
---

# Ground Sampling Distance (GSD)

The physical scene width represented by a single pixel.

$$GSD = \frac{\text{physical scene width}}{\text{image width in pixels}}$$

## Why It Matters

GSD bridges the gap between pixel counts and real-world detail. A 1000-pixel-wide image of a 10-metre scene has GSD = 1 cm/pixel — each pixel represents 1 cm of the scene. Two images with the same pixel count but different GSDs capture different levels of physical detail. GSD is the metric that matters for applications like satellite imaging, industrial inspection, and microscopy.

## Key Ideas

- Smaller GSD = finer physical detail per pixel
- Depends on both sensor resolution **and** imaging geometry (distance, lens focal length)
- Same sensor, closer distance → smaller GSD → more detail
- Used heavily in remote sensing, aerial photography, and industrial inspection

## Related Concepts

- [[spatial_resolution]] — pixel count, which GSD converts to physical scale
- [[pixel]] — each pixel covers one GSD × GSD patch of the scene
- [[sampling]] — GSD is the physical sampling interval

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 2
