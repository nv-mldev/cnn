---
tags: [concept, colour]
sources: [tutorials/00_introduction_to_digital_images/part5_colour_and_pipeline.md]
last_updated: 2026-04-05
---

# Luminance

Perceptual brightness of a colour pixel, computed as a weighted sum of RGB channels: $L = 0.2126 \cdot R + 0.7152 \cdot G + 0.0722 \cdot B$.

## Why It Matters

Converting colour to grayscale isn't a simple average — human vision is much more sensitive to green than red or blue. The luminance formula reflects this by weighting green at 71.5%. Using equal weights (0.333 each) produces visibly different and less perceptually accurate results. This matters for any algorithm that operates on intensity (edge detection, template matching, histogram analysis).

## Key Ideas

- Standard (ITU-R BT.709): $L = 0.2126R + 0.7152G + 0.0722B$
- Green dominates because human cone density peaks in green wavelengths
- Equal-weight average differs from perceptual luminance by ~10–20 grey levels
- The [[bayer_filter]] oversamples green (2× more photosites) for the same reason

## Related Concepts

- [[bayer_filter]] — green oversampling mirrors luminance weighting
- [[imaging_pipeline]] — luminance conversion is a common pipeline step
- [[pixel]] — luminance reduces 3 values to 1

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 5
