---
tags: [synthesis, probability]
sources: [tutorials/01a_probability_for_cv/]
last_updated: 2026-04-05
---

# The Distribution Chain: Bernoulli → Binomial → Poisson → Normal → CLT

Tutorial 01a builds a mathematical ladder where each distribution is a limiting case of the previous one, culminating in the Central Limit Theorem.

## The Chain

```
Bernoulli(p)
    ↓ count n trials
Binomial(n, p)
    ↓ n→∞, p→0, np=λ
Poisson(λ)
    ↓ λ→∞
Normal(μ=λ, σ²=λ)
    ↓ generalised by CLT
Sum of anything → Normal(nμ, nσ²)
```

## Why Each Step Matters for CV

| Step | Mathematical Insight | CV Implication |
|------|---------------------|----------------|
| [[bernoulli_distribution|Bernoulli]] | Binary outcome with probability p | Each photon detection, each threshold decision |
| [[binomial_distribution|Binomial]] | Count of n binary outcomes | Total detected photons = Binomial(n, QE) |
| [[poisson_distribution|Poisson]] | Limit of many rare events; mean = variance | **Exact** model for photon counting; σ = √λ |
| [[normal_distribution|Normal]] | Poisson ≈ Normal for λ > 30 | Gaussian noise assumption valid at typical signal levels |
| [[central_limit_theorem|CLT]] | Sum of any distributions → Normal | Pixel = sum of noise sources → Gaussian (justifies all Gaussian-based CV algorithms) |

## The Convergence Rates

- Binomial → Poisson: $O(1/n)$ — fast
- Poisson → Normal: practical threshold λ > 30
- CLT general: $O(1/\sqrt{n})$ — depends on skewness of original distribution
- Symmetric distributions converge fastest; skewed distributions converge slowest

## The Payoff

This chain explains why:
- `cv2.GaussianBlur` works (averaging pixels → CLT)
- GMM background subtraction works (pixel time series → CLT)
- BM3D/NLM denoising works (assumes Gaussian noise → validated by CLT)
- The [[anscombe_transform]] is needed for low-signal Poisson data (where Gaussian approximation breaks down)
