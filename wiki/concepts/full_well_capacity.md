---
tags: [concept, sensor-physics]
sources: [tutorials/00_introduction_to_digital_images/part1_sampling_and_sensors.md]
last_updated: 2026-04-05
---

# Full-Well Capacity

The maximum number of electrons a photosite can hold before saturating, setting the upper limit of the sensor's measurable brightness range.

## Why It Matters

Full-well capacity determines the brightest signal a sensor can measure. Beyond this point, additional photons produce no additional signal — the value clips at maximum ([[clipping]]). It also sets the maximum achievable [[signal_to_noise_ratio|SNR]]: $SNR_{max} = \sqrt{FWC}$. Larger photosites have higher FWC, which is why DSLRs have better dynamic range than phones.

## Key Ideas

- Phone photosites: ~1,000 e⁻ → max SNR ≈ 31.6
- DSLR photosites: ~50,000 e⁻ → max SNR ≈ 224
- Once full, extra photons are lost — this is sensor [[clipping]]
- Determines the upper end of [[dynamic_range]]

## Related Concepts

- [[photosite]] — the element with finite capacity
- [[signal_to_noise_ratio|Signal-to-Noise Ratio]] — max SNR = √FWC
- [[dynamic_range]] — FWC sets the bright end
- [[clipping]] — what happens when FWC is exceeded

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 1
