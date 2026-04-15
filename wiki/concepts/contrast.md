---
tags: [concept, image-formation]
sources: [tutorials/00_introduction_to_digital_images/part3_contrast_and_dynamic_range.md, tutorials/02_why_not_pixels/part6_dynamic_range.md]
last_updated: 2026-04-09
---

# Contrast

The spread of pixel values in an image, quantifying how much brightness variation exists between the darkest and brightest regions.

## Why It Matters

Low-contrast images have pixel values bunched in a narrow range — different objects may produce nearly identical pixel values, making them hard to distinguish. High-contrast images use the full range. Contrast changes with lighting conditions via the [[affine_model]] ($a$ parameter), which means the same scene can have wildly different contrast depending on when and how it was captured.

## Key Ideas

- **Michelson contrast**: $C = \frac{I_{max} - I_{min}}{I_{max} + I_{min}}$
- **Standard deviation contrast**: $C_\sigma = \text{std}(I)$ — how spread out pixel values are
- Low contrast → narrow histogram → objects hard to separate by pixel value
- Controlled by the $a$ parameter in the [[affine_model]]
- Same face at low/medium/high contrast: pixel values differ by ~100 grey levels

## Figure — Same scene, three contrast levels

Three renderings of Einstein at low, medium, and high contrast. The content is identical — only the affine parameter $a$ changes. The low-contrast version uses only a narrow band of gray levels; the high-contrast version uses the full range.

![[gw_contrast_einstein.jpg]]

*Source: Gonzalez & Woods, Digital Image Processing 3rd ed., Fig. 2.41.*

## Related Concepts

- [[affine_model]] — contrast is the $a$ parameter
- [[dynamic_range]] — maximum contrast a sensor can capture
- [[clipping]] — high-contrast scenes may exceed sensor range
- [[contrast_stretching]] — linear rescaling to increase contrast; $r = 1.0$ with original

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 3
- [[02_why_not_pixels|Tutorial 02: Why Not Pixels]] — Part 6 (contrast stretching as information-preserving linear transform)
