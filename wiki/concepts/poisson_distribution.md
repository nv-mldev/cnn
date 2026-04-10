---
tags: [concept, probability, distributions, critical]
sources: [tutorials/01a_probability_for_cv/part3_poisson.md]
last_updated: 2026-04-05
---

# Poisson Distribution

The distribution of counts of rare events in a large region, parameterised by the expected count $\lambda$.

$$P(k \mid \lambda) = \frac{\lambda^k e^{-\lambda}}{k!}$$

## Why It Matters

Poisson is the **exact physical model** for photon counting — not an approximation. An LED emits ~10¹⁸ photons/second (huge $n$), the probability any specific photon hits a 6µm photosite is ~10⁻¹⁸ (tiny $p$), but $\lambda = np$ is tens to thousands. This is the Poisson regime by definition. The Poisson distribution's key property — **mean equals variance** ($E[k] = \text{Var}(k) = \lambda$) — determines all noise behaviour in imaging.

## Key Ideas

- Derived from [[binomial_distribution|Binomial]] in the limit $n \to \infty$, $p \to 0$, $\lambda = np$ constant
- $E[k] = \lambda$, $\text{Var}(k) = \lambda$, $\sigma = \sqrt{\lambda}$
- **Signal-dependent noise**: brighter pixels have more absolute noise but better SNR
  - Dark (λ=5): σ ≈ 2.2, relative noise 45%
  - Bright (λ=200): σ ≈ 14.1, relative noise 7%
- $SNR = \lambda / \sqrt{\lambda} = \sqrt{\lambda}$
- Approximated by [[normal_distribution|Normal]](λ, λ) for λ > 30

**CV applications beyond photons:**
- Defect detection: rare defects in large area → Poisson count
- Keypoint detection: SIFT keypoints are rare per patch → Poisson
- Background subtraction: noise-changed pixels → Poisson count

## Code Example

```python
import numpy as np

# Simulate 1D sensor: brightness gradient from λ=5 to λ=200
lambdas = np.linspace(5, 200, 200)
capture = np.array([np.random.poisson(lam) for lam in lambdas])

# Verify σ = √λ over 1000 captures
captures = np.array([[np.random.poisson(lam) for lam in lambdas] for _ in range(1000)])
measured_std = captures.std(axis=0)
theoretical_std = np.sqrt(lambdas)
# measured_std ≈ theoretical_std
```

## Related Concepts

- [[binomial_distribution]] — Poisson is its limiting case
- [[normal_distribution]] — Poisson ≈ Normal for large λ
- [[shot_noise]] — the physical phenomenon modelled by Poisson
- [[signal_to_noise_ratio|Signal-to-Noise Ratio]] — SNR = √λ for Poisson
- [[dark_current]] — additional Poisson noise source
- [[noise_regimes]] — Poisson dominates in the shot-noise regime
- [[anscombe_transform]] — stabilises Poisson variance for Gaussian denoising

## Sources

- [[01a_probability_for_cv|Tutorial 01a: Probability for CV]] — Part 3
