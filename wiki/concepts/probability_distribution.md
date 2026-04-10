---
tags: [concept, probability, fundamentals]
sources: [tutorials/01a_probability_for_cv/part0_what_is_a_distribution.md]
last_updated: 2026-04-05
---

# Probability Distribution

A complete assignment of probabilities to all possible values of a [[random_variable]], describing how likely each outcome is.

## Why It Matters

A distribution captures **everything** about a measurement's uncertainty — not just the average, but the spread, shape, and tails. In imaging, the distribution of pixel values tells you: where is the signal? (centre), how noisy is it? (spread), is clipping occurring? (skewness), are there defects? (heavy tails). Two patches with the same mean can have completely different distributions.

## Key Ideas

- **PMF** (Probability Mass Function): for discrete variables — $P(X = k)$ for each integer $k$
- **PDF** (Probability Density Function): for continuous variables — $f(x)$ such that $P(a \leq X \leq b) = \int_a^b f(x)dx$
- **CDF** (Cumulative Distribution Function): $F(x) = P(X \leq x)$ — works for both discrete and continuous
- **Parameters compress distributions**: [[binomial_distribution|Binomial]] needs just $(n, p)$; [[poisson_distribution|Poisson]] needs just $\lambda$
- Distribution shape encodes physical meaning: centre = signal, spread = noise, skew = clipping

## Related Concepts

- [[random_variable]] — the quantity whose distribution we describe
- [[bernoulli_distribution]], [[binomial_distribution]], [[poisson_distribution]], [[normal_distribution]] — specific distribution families

## Sources

- [[01a_probability_for_cv|Tutorial 01a: Probability for CV]] — Part 0
