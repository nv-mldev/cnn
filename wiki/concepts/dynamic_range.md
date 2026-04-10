---
tags: [concept, sensor-physics]
sources: [tutorials/00_introduction_to_digital_images/part3_contrast_and_dynamic_range.md, tutorials/02_why_not_pixels/part6_dynamic_range.md]
last_updated: 2026-04-09
---

# Dynamic Range

The ratio between the brightest and darkest values a sensor can capture simultaneously, usually measured in stops or decibels.

$$DR_{dB} = 20 \cdot \log_{10}\left(\frac{I_{max}}{I_{min}}\right)$$

## Why It Matters

Real-world scenes often have enormous brightness ranges — a sunlit window next to a shadowed interior can span 20+ stops. No camera captures the full range. Highlights clip to white, shadows clip to black, and the information in those regions is lost permanently. This is why HDR photography exists — it merges multiple exposures to extend effective dynamic range.

## Key Ideas

- Each "stop" = factor of 2 in brightness
- Human eye (adapted): ~21 stops (126 dB)
- Modern DSLR: ~14 stops (84 dB)
- Phone camera: ~10–12 stops (60–72 dB)
- 8-bit image: ~48 dB (256:1 ratio)
- Exceeding dynamic range → [[clipping]] — permanent information loss
- [[full_well_capacity|Full-Well Capacity]] sets the bright end; read noise sets the dark end

## Related Concepts

- [[clipping]] — what happens at the limits of dynamic range
- [[full_well_capacity|Full-Well Capacity]] — determines the upper limit
- [[signal_to_noise_ratio|Signal-to-Noise Ratio]] — related quality metric
- [[contrast]] — how much of the dynamic range is used
- [[contrast_stretching]] — linear rescaling to use the full representable range
- [[bit_depth]] — limits the representable dynamic range in stored images

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 3
- [[02_why_not_pixels|Tutorial 02: Why Not Pixels]] — Part 6 (contrast stretching and clipping effects on matching)
