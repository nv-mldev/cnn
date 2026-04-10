---
tags: [concept, signal-processing]
sources: [tutorials/00_introduction_to_digital_images/part4_zoom_and_aliasing.md]
last_updated: 2026-04-05
---

# Downsampling

Reducing the spatial resolution of an image by discarding pixels, permanently losing detail.

## Why It Matters

Downsampling is everywhere — resizing images for display, creating image pyramids, reducing computational cost. But naively discarding pixels (taking every Nth pixel) violates the [[nyquist_criterion]] and causes [[aliasing]]. Proper downsampling requires an [[anti_aliasing_filter|Anti-Aliasing Filter]] first. The lost detail is gone forever — no upsampling can recover it.

## Key Ideas

- Naive approach: take every Nth pixel → risks aliasing
- Proper approach: low-pass filter first, then decimate
- Each 2× downsample halves resolution and permanently discards high-frequency detail
- Cascade: 256→128→64→32→16 — detail loss compounds at each step
- The MAE between original and downsample→upsample round-trip is always >0 — proof of information loss

## Related Concepts

- [[aliasing]] — caused by downsampling without filtering
- [[anti_aliasing_filter|Anti-Aliasing Filter]] — must be applied before downsampling
- [[nyquist_criterion]] — determines when downsampling will alias
- [[spatial_resolution]] — downsampling reduces it
- [[nearest_neighbour_interpolation|Nearest-Neighbour Interpolation]] — one method for upsampling after downsampling
- [[bilinear_interpolation]] — smoother upsampling after downsampling

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 4
