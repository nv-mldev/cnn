---
tags: [concept, signal-processing, fundamentals]
sources: [tutorials/00_introduction_to_digital_images/part1_sampling_and_sensors.md]
last_updated: 2026-04-05
---

# Nyquist Criterion

A signal must be sampled at least twice per period of its highest frequency component to be faithfully reconstructed.

## Why It Matters

When a camera sensor has too few pixels for the detail in the scene — or when you downsample an image — frequencies above the Nyquist limit fold back and create phantom patterns ([[aliasing]]). The Nyquist criterion tells you the minimum pixel density needed to capture a given level of detail without artefacts.

## Key Ideas

- Minimum sampling rate: $f_s \geq 2 \cdot f_{max}$ where $f_{max}$ is the highest frequency in the signal
- The Nyquist frequency is half the sampling rate: $f_{Nyquist} = f_s / 2$
- Any signal component above $f_{Nyquist}$ will alias — appear as a lower frequency that wasn't in the original
- In 2D images, this applies independently along rows and columns
- A checkerboard pattern at 1 pixel per square is exactly at the Nyquist limit — the hardest case

## Code Example

```python
# 3 Hz sine wave needs ≥6 samples/second
# 5 samples/second is below Nyquist → aliased reconstruction
frequency = 3  # Hz
nyquist_rate = 2 * frequency  # 6 samples/sec minimum

low_rate = 5   # below Nyquist → aliasing
high_rate = 30  # well above → faithful
```

## Related Concepts

- [[spatial_frequency]] — what "frequency" means for images (prerequisite if coming from a non-DSP background)
- [[sampling]] — the process that the Nyquist criterion governs
- [[aliasing]] — the consequence of violating the criterion
- [[anti_aliasing_filter|Anti-Aliasing Filter]] — the standard remedy
- [[downsampling]] — where Nyquist violations commonly occur in practice

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 1 and Part 4
