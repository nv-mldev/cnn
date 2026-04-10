---
tags: [concept, probability, distributions, critical]
sources: [tutorials/01a_probability_for_cv/part4_normal.md]
last_updated: 2026-04-05
---

# Normal (Gaussian) Distribution

The continuous bell-curve distribution, parameterised by mean $\mu$ and variance $\sigma^2$.

$$f(x \mid \mu, \sigma^2) = \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(x - \mu)^2}{2\sigma^2}\right)$$

## Why It Matters

The Normal distribution is the most important distribution in CV — not because noise is inherently Gaussian, but because the [[central_limit_theorem]] makes sums of **any** random variables converge to Gaussian. This is why `cv2.GaussianBlur`, GMM background subtraction, NLM/BM3D denoising, and SIFT/HOG descriptors all assume Gaussian — they all involve averaging many values.

## Key Ideas

- $E[X] = \mu$ (location), $\text{Var}(X) = \sigma^2$ (spread)
- $\mu$ and $\sigma$ are independent — changing one doesn't affect the other
- First **continuous** distribution in the Bernoulli→Binomial→Poisson→Normal chain
- [[poisson_distribution|Poisson]](λ) ≈ Normal(λ, λ) for λ > 30
- Practical convergence thresholds:
  - λ = 1: clearly not Gaussian (skewed)
  - λ = 10: rule-of-thumb minimum
  - λ = 30: good match (typical sensor)
  - λ = 100: excellent (typical industrial camera)
  - λ = 500: indistinguishable

**Why Normal appears everywhere in CV:**
- Filter outputs (averaging many pixels → CLT)
- Pixel intensities in uniform regions (many noise sources add)
- Feature descriptors (HOG/SIFT average over many gradients)
- Calibration errors (repeated measurements)
- [[read_noise]] (amplifier electronics)

## Related Concepts

- [[central_limit_theorem]] — explains why Normal appears everywhere
- [[poisson_distribution]] — converges to Normal for large λ
- [[read_noise]] — inherently Gaussian (electronics)
- [[noise_budget]] — total noise is approximately Normal by CLT
- [[shot_noise]] — Poisson, but ≈ Normal at typical signal levels

## Sources

- [[01a_probability_for_cv|Tutorial 01a: Probability for CV]] — Part 4
