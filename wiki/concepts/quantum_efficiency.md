---
tags: [concept, sensor-physics]
sources: [tutorials/00_introduction_to_digital_images/part1_sampling_and_sensors.md, tutorials/01a_probability_for_cv/part1_bernoulli.md]
last_updated: 2026-04-05
---

# Quantum Efficiency (QE)

The fraction of incident photons that a sensor successfully converts into electrons, typically ranging from 0.4 to 0.8.

## Why It Matters

QE is a multiplier on the useful signal. A sensor with QE = 0.8 converts 80% of photons to electrons; one with QE = 0.4 wastes half the light. Higher QE means more signal for the same exposure, directly improving [[signal_to_noise_ratio|SNR]]. It's a fundamental property of the sensor material and design.

## Key Ideas

- Range: 0.4–0.8 for typical silicon sensors
- Wavelength-dependent — sensors are more efficient at some colours than others
- Signal in electrons = incident photons × QE × photosite area
- Higher QE → more electrons → higher SNR for the same scene

## Probabilistic Model

QE is formally a [[bernoulli_distribution|Bernoulli]] probability: each photon independently has probability QE of producing an electron. For $n$ incident photons, detected electrons follow [[binomial_distribution|Binomial]](n, QE). This reduces the effective signal: $\lambda_{detected} = \lambda_{incident} \times QE$.

## Related Concepts

- [[photosite]] — the element whose QE is measured
- [[signal_to_noise_ratio|Signal-to-Noise Ratio]] — directly improved by higher QE
- [[shot_noise]] — noise on the signal that QE helps collect
- [[bernoulli_distribution]] — each photon detection is a Bernoulli trial
- [[binomial_distribution]] — total detected electrons are Binomial(n, QE)

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 1
