---
tags: [concept, probability, critical]
sources: [tutorials/01a_probability_for_cv/part5_clt.md]
last_updated: 2026-04-05
---

# Central Limit Theorem (CLT)

If $X_1, X_2, \ldots, X_n$ are independent random variables with mean $\mu$ and variance $\sigma^2$, then their sum converges to a Normal distribution as $n \to \infty$:

$$S_n = \sum_{i=1}^n X_i \sim \mathcal{N}(n\mu, n\sigma^2)$$

$$\bar{X} = \frac{1}{n}\sum_{i=1}^n X_i \sim \mathcal{N}\left(\mu, \frac{\sigma^2}{n}\right)$$

## Why It Matters

The CLT is the reason Gaussian assumptions work in CV. The individual $X_i$ can be from **any** distribution — Poisson, Uniform, Bernoulli, anything. As long as enough terms are summed, the result is Gaussian. A pixel value is a sum of multiple noise sources (Poisson shot + Poisson dark + Gaussian read + Uniform quantization) — by CLT, the total is Gaussian even though the individual sources aren't all Gaussian.

## Key Ideas

- Works for **any** distribution — the individual terms don't need to be Gaussian
- Convergence rate ≈ $O(1/\sqrt{n})$ — measured by Kolmogorov-Smirnov distance
- Symmetric distributions (Uniform) converge fastest; skewed distributions (Exponential, Pareto) converge slowest
- Practical threshold: n ≈ 10–50 for visible convergence; n = 50 is tight for most distributions
- KS distance < 0.02 ≈ "effectively Gaussian"

**This explains why these CV algorithms work:**
- `cv2.GaussianBlur` — averages many pixels → CLT → Gaussian output
- GMM background subtraction — pixel averages over time → Gaussian components
- NLM, BM3D, Wiener denoising — assume Gaussian noise (valid by CLT)
- SIFT/HOG descriptors — averaged gradients over patches → Gaussian components

## Code Example

```python
import numpy as np

# Four very non-Gaussian distributions all become Gaussian when summed
uniform = np.random.uniform(0, 1, (10000, 50))    # flat
exponential = np.random.exponential(1, (10000, 50))  # skewed
bernoulli = np.random.binomial(1, 0.3, (10000, 50))  # discrete
bimodal = np.where(np.random.rand(10000, 50) < 0.5,
                   np.random.normal(-2, 0.5, (10000, 50)),
                   np.random.normal(2, 0.5, (10000, 50)))

# Sum of 50 terms — all four are approximately Gaussian
sums = [d.sum(axis=1) for d in [uniform, exponential, bernoulli, bimodal]]
```

## Related Concepts

- [[normal_distribution]] — the distribution that CLT produces
- [[poisson_distribution]] — Poisson → Normal is a special case of CLT
- [[noise_budget]] — CLT justifies treating the total as Gaussian
- [[noise_regimes]] — CLT applies differently in each regime

## Sources

- [[01a_probability_for_cv|Tutorial 01a: Probability for CV]] — Part 5
