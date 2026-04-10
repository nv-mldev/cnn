---
tags: [concept, probability, distributions]
sources: [tutorials/01a_probability_for_cv/part1_bernoulli.md]
last_updated: 2026-04-05
---

# Bernoulli Distribution

The simplest probability distribution — a single binary trial with probability $p$ of success.

$$X \sim \text{Bernoulli}(p) \quad \Rightarrow \quad X \in \{0, 1\}$$

## Why It Matters

The Bernoulli trial is the atom of randomness in CV. Every yes/no decision is Bernoulli: Does this photon produce an electron? ([[quantum_efficiency]]). Is this pixel above the threshold? Does this descriptor pair match? Counting many Bernoulli outcomes gives the [[binomial_distribution]], which leads to [[poisson_distribution|Poisson]] and eventually [[normal_distribution|Normal]].

## Key Ideas

- $E[X] = p$
- $\text{Var}(X) = p(1 - p)$
- Maximum variance at $p = 0.5$ (maximum uncertainty)
- CV applications:
  - **Thresholding**: pixel > T? (Otsu's method)
  - **Feature matching**: true match or not?
  - **Quantum efficiency**: one photon → one electron with probability QE

## Code Example

```python
import numpy as np

# 20 Bernoulli trials with p=0.7
trials = np.random.binomial(1, p=0.7, size=20)
# [1, 0, 1, 1, 1, 0, 1, ...] — each element is one Bernoulli outcome
```

## Related Concepts

- [[binomial_distribution]] — counts successes over $n$ Bernoulli trials
- [[quantum_efficiency]] — Bernoulli probability for photon detection
- [[random_variable]] — Bernoulli is the simplest case

## Sources

- [[01a_probability_for_cv|Tutorial 01a: Probability for CV]] — Part 1
