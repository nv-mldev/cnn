---
tags: [concept, sensor-physics, noise]
sources: [tutorials/00_introduction_to_digital_images/part1_sampling_and_sensors.md, tutorials/01a_probability_for_cv/part3_poisson.md]
last_updated: 2026-04-05
---

# Signal-to-Noise Ratio (SNR)

The ratio of useful signal to unwanted noise, quantifying how "clean" a measurement is.

## Why It Matters

SNR determines whether you can distinguish real scene content from random noise. A low-SNR image (dim scene, small sensor) may have pixel values dominated by noise rather than actual brightness differences. This directly impacts any algorithm that compares pixel values — noise makes identical scenes look different.

## Key Ideas

- General formula: $SNR = \frac{S}{\sqrt{S + \sigma_r^2}}$ where $S$ is signal (electrons) and $\sigma_r$ is read noise
- At high signal (shot-noise dominated): $SNR \approx \sqrt{S}$
- Doubling SNR requires **4× more photons** (because $\sqrt{4S} = 2\sqrt{S}$)
- Larger [[photosite|Photosites]] collect more photons → higher SNR
- DSLR photosite is ~25× larger than phone → ~5× better SNR in dim light

**SNR comparison (dim scene, 50 photons/µm²):**

| Camera | Signal (e⁻) | Shot Noise | Read Noise | SNR |
|--------|------------|------------|------------|-----|
| Phone (1 µm²) | 20 | 4.5 | 3 | 3.7 |
| DSLR (25 µm²) | 500 | 22.4 | 5 | 21.8 |

## Related Concepts

- [[shot_noise]] — the dominant noise source at normal light levels
- [[photosite]] — size determines signal collection and SNR
- [[full_well_capacity|Full-Well Capacity]] — sets the maximum achievable SNR
- [[quantum_efficiency]] — affects how much signal is collected
- [[dynamic_range]] — related metric covering full brightness range

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 1
