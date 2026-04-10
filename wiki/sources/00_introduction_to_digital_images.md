---
tags: [source, tutorial-00]
source_path: tutorials/00_introduction_to_digital_images/
last_updated: 2026-04-05
---

# Tutorial 00: Introduction to Digital Images

## Summary

This tutorial builds the foundational understanding of what a digital image actually is — not as a picture, but as a noisy, quantized, processed 2D array of numbers. Across five parts, it traces the complete journey from photons hitting a sensor to stored pixel values, systematically demonstrating why those values are unreliable representations of scene content.

The central argument: pixel values encode not just scene content but also sensor physics (noise, spectral response), lighting conditions, exposure settings, spatial position (shading), ISP processing (white balance, tone mapping), and compression. This makes raw pixel comparison fundamentally flawed — the motivation for normalisation and learned features in later tutorials.

## Key Claims

- A digital image is a 2D function sampled on a regular grid, not a miniature photograph
- Shot noise follows a Poisson distribution with σ = √S, setting a fundamental SNR limit
- Quantization is irreversible — lost precision cannot be recovered
- The same scene content produces vastly different pixel values under different lighting (affine model: I₂ = a·I₁ + b)
- Downsampling without anti-aliasing creates aliasing artefacts; upsampling cannot recover lost detail
- Colour images are 3-channel arrays where each channel obeys the same physics as grayscale
- The imaging pipeline (lens → sensor → ADC → ISP → compression) transforms pixel values at every stage

## Concepts Introduced

- [[sampling]]
- [[nyquist_criterion]]
- [[aliasing]]
- [[anti_aliasing_filter|Anti-Aliasing Filter]]
- [[photosite]]
- [[shot_noise]]
- [[signal_to_noise_ratio|Signal-to-Noise Ratio]]
- [[quantum_efficiency]]
- [[full_well_capacity|Full-Well Capacity]]
- [[pixel]]
- [[spatial_resolution]]
- [[ground_sampling_distance]]
- [[quantization]]
- [[bit_depth]]
- [[false_contours]]
- [[affine_model]]
- [[contrast]]
- [[dynamic_range]]
- [[clipping]]
- [[nearest_neighbour_interpolation|Nearest-Neighbour Interpolation]]
- [[bilinear_interpolation]]
- [[downsampling]]
- [[bayer_filter]]
- [[demosaicing]]
- [[luminance]]
- [[imaging_pipeline]]
- [[shading]]

## Connections to Other Sources

- Builds the foundation for [[01a_probability_for_cv|Tutorial 01a: Probability for Sensors]] — shot noise and Poisson statistics are introduced here and developed fully there
- Builds the foundation for [[01b_linear_algebra_for_matching|Tutorial 01b: Linear Algebra for Matching]] — the affine model motivates the need for normalisation
- Directly motivates [[02_why_not_pixels|Tutorial 02: Why Not Pixels]] — every part adds another reason why raw pixel comparison fails
