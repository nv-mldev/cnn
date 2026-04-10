---
tags: [concept, fundamentals]
sources: [tutorials/00_introduction_to_digital_images/part2_pixels_and_resolution.md]
last_updated: 2026-04-05
---

# Bit Depth

The number of bits used to represent each pixel value, determining how many distinct intensity levels are available.

## Why It Matters

Bit depth controls the precision of pixel values. Most images use 8-bit (256 levels), which is sufficient for display. But raw sensor data is typically 12–16 bit (4096–65536 levels) to preserve fine gradations for post-processing. Reducing bit depth increases [[quantization]] error and can produce visible [[false_contours]].

## Key Ideas

- $2^B$ levels for $B$ bits: 8-bit = 256 levels, 4-bit = 16, 2-bit = 4, 1-bit = 2
- Higher bit depth → finer intensity resolution → less quantization error
- Raw images: 12–16 bit; display images: 8-bit; binary masks: 1-bit
- The 8-bit standard (0–255) comes from the minimum depth where quantization steps are imperceptible to humans

| Bit Depth | Levels | Step Size (Δ) | Max Error |
|-----------|--------|---------------|-----------|
| 8 | 256 | 1 | 0.5 |
| 4 | 16 | 16 | 8 |
| 2 | 4 | 85 | 42.5 |
| 1 | 2 | 255 | 127.5 |

## Related Concepts

- [[quantization]] — the process that bit depth governs
- [[false_contours]] — artefact of insufficient bit depth
- [[dynamic_range]] — bit depth limits the representable dynamic range

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 2
