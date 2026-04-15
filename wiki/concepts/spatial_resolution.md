---
tags: [concept, fundamentals]
sources: [tutorials/00_introduction_to_digital_images/part2_pixels_and_resolution.md]
last_updated: 2026-04-05
---

# Spatial Resolution

The number of pixels in an image (width × height), determining how finely the scene is sampled.

## Why It Matters

Higher spatial resolution means finer [[sampling]] — more detail is preserved. But resolution has a hard floor: once you downsample, the lost detail is gone permanently. No upsampling algorithm can recover it. This is a fundamental information-theoretic limit, not a software limitation.

## Key Ideas

- Measured in pixels: e.g., 1920×1080, 4096×4096
- More pixels = finer sampling = more scene detail preserved
- Reducing resolution (e.g., 256→128→64→32) permanently destroys detail
- Related to physical sampling by [[ground_sampling_distance]]
- "Megapixels" = total pixel count / 1,000,000

## Figure — The same scene at four resolutions

A pocket watch shown at 1250 dpi, 300 dpi, 150 dpi, and 72 dpi. As resolution drops, fine features (numerals, minute markings) disappear. The coarser samplings cannot represent detail that exceeds the grid's spatial frequency — this information is permanently lost.

![[gw_spatial_resolution_watch.jpg]]

*Source: Gonzalez & Woods, Digital Image Processing 3rd ed., Fig. 2.20.*

## Related Concepts

- [[sampling]] — spatial resolution is the 2D sampling rate
- [[ground_sampling_distance]] — physical size each pixel represents
- [[downsampling]] — reducing spatial resolution
- [[pixel]] — the individual sample
- [[nyquist_criterion]] — minimum resolution needed for a given detail level

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 2
