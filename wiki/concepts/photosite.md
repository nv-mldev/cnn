---
tags: [concept, sensor-physics]
sources: [tutorials/00_introduction_to_digital_images/part1_sampling_and_sensors.md]
last_updated: 2026-04-05
---
can we 
# Photosite

The individual light-sensitive element on a camera sensor that collects photons during exposure and converts them to electrons via the photoelectric effect.

## Why It Matters

The photosite is where the physical world becomes a number. Its size determines how many photons it can collect, which directly sets the [[signal_to_noise_ratio|Signal-to-Noise Ratio]]. Larger photosites (DSLRs) collect more photons and produce cleaner images; smaller photosites (phone cameras) are noisier, especially in dim light. This is why "more megapixels" doesn't always mean better images.

## Key Ideas

- Each photosite produces one sample — one pixel in the raw image
- Photosite area determines photon collection capacity
- Larger area → more photons → higher SNR → cleaner image
- Limited by [[full_well_capacity|Full-Well Capacity]] — the maximum electrons it can hold before saturating
- Subject to [[shot_noise]] — random variation in photon arrivals

**Typical photosite sizes:**

| Camera | Photosite Area | Full-Well Capacity | Read Noise |
|--------|---------------|-------------------|------------|
| Phone | ~1 µm² | ~1,000 e⁻ | ~3 e⁻ |
| DSLR | ~25 µm² | ~50,000 e⁻ | ~5 e⁻ |

## Related Concepts

- [[shot_noise]] — Poisson noise from random photon arrivals
- [[signal_to_noise_ratio|Signal-to-Noise Ratio]] — quality metric determined by photosite physics
- [[quantum_efficiency]] — fraction of photons converted to electrons
- [[full_well_capacity|Full-Well Capacity]] — saturation limit
- [[sampling]] — photosite grid performs spatial sampling
- [[bayer_filter]] — colour filter placed over the photosite

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 1
