---
tags: [concept, sensor-physics, fundamentals]
sources: [tutorials/00_introduction_to_digital_images/part1_sampling_and_sensors.md]
last_updated: 2026-04-05
---

# Sampling

Converting a continuous signal into a discrete set of values by measuring it at regular intervals.

## Why It Matters

A camera sensor does not capture a continuous image — it measures brightness at a finite grid of photosites. This grid spacing determines what detail the image can represent. Every digital image is a sampled version of a continuous scene, and the sampling rate sets a hard limit on what information survives.

## Key Ideas

- A digital image is a **2D function sampled on a regular grid** — each sample is one pixel
- Spatial sampling (how many pixels) trades off against storage, processing cost, and detail preservation
- Sampling too coarsely loses detail permanently — no algorithm can recover it
- The minimum sampling rate to preserve a signal is defined by the [[nyquist_criterion]]
- Sampling below the Nyquist rate causes [[aliasing]] — phantom frequencies that weren't in the original scene

## Code Example

```python
# 1D sampling analogy: a 3 Hz sine wave
import numpy as np
continuous_time = np.linspace(0, 1, 1000)
signal = np.sin(2 * np.pi * 3 * continuous_time)

# High rate (30 samples) — faithful reconstruction
high_samples = np.linspace(0, 1, 30)
high_values = np.sin(2 * np.pi * 3 * high_samples)

# Low rate (5 samples) — below Nyquist, aliased
low_samples = np.linspace(0, 1, 5)
low_values = np.sin(2 * np.pi * 3 * low_samples)
```

## Related Concepts

- [[nyquist_criterion]] — the minimum sampling rate to avoid aliasing
- [[aliasing]] — what happens when you sample too slowly
- [[spatial_resolution]] — how many samples (pixels) the image has
- [[photosite]] — the physical element that performs the sampling
- [[quantization]] — the other half of digitisation (intensity discretisation)
- [[downsampling]] — reducing the number of samples after capture

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 1: From Light to Numbers
