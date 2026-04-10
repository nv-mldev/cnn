---
tags: [concept, signal-processing]
sources: [tutorials/00_introduction_to_digital_images/part4_zoom_and_aliasing.md]
last_updated: 2026-04-05
---

# Anti-Aliasing Filter

A low-pass filter applied before downsampling to remove frequencies above the new Nyquist limit, preventing [[aliasing]].

## Why It Matters

Naively discarding pixels (e.g., taking every other row and column) leaves high-frequency content that folds back into the downsampled image as phantom patterns. An anti-aliasing filter smooths the image first, removing detail that can't be represented at the lower resolution. The result is blurrier but correct — no moiré, no phantom stripes.

## Key Ideas

- Applied **before** reducing resolution, not after
- Removes frequencies above the target Nyquist limit
- LANCZOS resampling in PIL/Pillow includes an anti-aliasing filter
- Trade-off: prevents artefacts but introduces blur (lost sharpness)
- Without it, a checkerboard pattern downsampled 2× produces wrong patterns; with it, it produces uniform grey (correct average)

## Related Concepts

- [[aliasing]] — the artefact this filter prevents
- [[nyquist_criterion]] — determines the cutoff frequency
- [[downsampling]] — the operation that requires this filter

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 4
