---
tags: [concept, artefacts]
sources: [tutorials/00_introduction_to_digital_images/part2_pixels_and_resolution.md]
last_updated: 2026-04-05
---

# False Contours

Visible step-like banding artefacts in smooth gradients caused by insufficient [[bit_depth]], where the quantization step size is large enough to see.

## Why It Matters

False contours are the visual evidence that quantization discards information. They appear as hard edges in regions that should be smooth gradients — most obvious in sky, skin tones, and shadows. At 2-bit depth (4 levels), a smooth gradient becomes 4 flat bands with visible steps. This demonstrates that even without spatial resolution loss, intensity precision loss alone corrupts image content.

## Key Ideas

- Appear when quantization step Δ is large enough to span a perceptible brightness difference
- Worst in smooth gradients where adjacent pixels should have very similar values
- At 8-bit (Δ = 1): invisible; at 4-bit (Δ = 16): subtle; at 2-bit (Δ = 85): dramatic
- Cannot be removed after quantization — the original smooth transitions are lost

## Related Concepts

- [[quantization]] — the process that causes false contours
- [[bit_depth]] — more bits prevent false contours

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 2
