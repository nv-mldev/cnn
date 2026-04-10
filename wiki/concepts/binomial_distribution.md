---
tags: [concept, probability, distributions]
sources: [tutorials/01a_probability_for_cv/part2_binomial.md]
last_updated: 2026-04-05
---

# Binomial Distribution

The number of successes in $n$ independent [[bernoulli_distribution|Bernoulli]] trials, each with probability $p$.

$$P(k \mid n, p) = \binom{n}{k} p^k (1-p)^{n-k}$$

## Why It Matters

The Binomial distribution is the natural model for "how many out of $n$?" questions in imaging: how many edge pixels in a patch? How many photons detected out of $n$ arriving? How many true matches out of $n$ tested? It's also the stepping stone to [[poisson_distribution|Poisson]] — when $n$ is huge and $p$ is tiny, Binomial simplifies to Poisson.

## Key Ideas

- **Binomial coefficient**: $\binom{n}{k} = \frac{n!}{k!(n-k)!}$ — number of ways to choose which $k$ trials succeed
- $E[k] = np$, $\text{Var}(k) = np(1-p)$
- Formula breakdown: $\binom{n}{k}$ (arrangements) × $p^k$ (successes) × $(1-p)^{n-k}$ (failures)
- As $n$ increases with fixed $p$: distribution widens and becomes bell-shaped (first hint of [[normal_distribution|Normal]])
- As $n \to \infty$, $p \to 0$, $np = \lambda$ constant: Binomial → [[poisson_distribution|Poisson]]
- Convergence rate: $O(1/n)$

## Code Example

```python
import numpy as np
from math import comb

# Manual PMF for Binomial(n=10, p=0.3)
n, p = 10, 0.3
for k in range(n + 1):
    prob = comb(n, k) * p**k * (1 - p)**(n - k)
    print(f"P(k={k}) = {prob:.4f}")
```

## Related Concepts

- [[bernoulli_distribution]] — each trial in the Binomial is Bernoulli
- [[poisson_distribution]] — limiting case when n→∞, p→0
- [[normal_distribution]] — shape approaches Normal as n increases
- [[quantum_efficiency]] — photon detection is Binomial(n_photons, QE)

## Sources

- [[01a_probability_for_cv|Tutorial 01a: Probability for CV]] — Part 2
