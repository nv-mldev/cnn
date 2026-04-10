---
tags: [concept, colour, fundamentals, critical]
sources: [tutorials/00_introduction_to_digital_images/part5_colour_and_pipeline.md]
last_updated: 2026-04-05
---

# Imaging Pipeline

The end-to-end chain of transformations from continuous light in the scene to stored pixel values, each stage modifying what the final number represents.

## Why It Matters

A pixel value is not a direct measurement of scene brightness — it's the output of a long processing chain. Every stage adds noise, rounds values, interpolates, or applies non-linear transforms. Understanding the pipeline is essential for understanding why pixel values are unreliable and why the same scene can produce different values across cameras, settings, or even positions in the same image.

## Key Ideas

The pipeline, end to end:

```
Scene (continuous light field)
  ↓ Lens focuses light onto sensor
Sensor (photosites collect photons)
  ↓ Shot noise added (Poisson process)
Bayer filter (one colour per photosite)
  ↓ ADC: analog voltage → digital integer (quantization)
Raw image (12–16 bit, single-channel mosaic)
  ↓ Demosaicing (interpolate missing colours)
  ↓ White balance (per-channel scaling)
  ↓ Tone mapping (non-linear curve)
  ↓ Sharpening, noise reduction
RGB image (3 channels, 8–16 bit)
  ↓ JPEG/PNG compression
Stored image (2D array, uint8)
```

Each stage transforms pixel values:
1. **Photon collection** — [[shot_noise]] adds random error
2. **Quantization** — rounds to discrete levels
3. **[[demosaicing]]** — interpolates 2 of 3 colour channels
4. **White balance** — scales channels differently
5. **Tone mapping** — non-linear (changes relative differences)
6. **Compression** — introduces quantization artefacts (JPEG)

## Related Concepts

- [[photosite]] — where light enters the pipeline
- [[shot_noise]] — noise added at capture
- [[quantization]] — ADC stage
- [[bayer_filter]] — colour filter stage
- [[demosaicing]] — mosaic to RGB
- [[shading]] — spatially varying gain in the pipeline
- [[pixel]] — the output of the entire pipeline

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 5
