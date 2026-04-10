---
tags: [concept, probability, fundamentals]
sources: [tutorials/01a_probability_for_cv/part0_what_is_a_distribution.md]
last_updated: 2026-04-05
---

# Random Variable

A function that maps outcomes of a random process to real numbers: $X: \Omega \to \mathbb{R}$.

## Why It Matters

Every measurement in imaging is a random variable — the pixel value at position $(i,j)$ is not deterministic but drawn from a distribution governed by scene brightness, sensor physics, and noise. Thinking in terms of random variables (rather than fixed values) is the mental shift needed to understand why the same scene produces different pixel values on every capture.

## Key Ideas

- A random variable is **not** a number — it's a rule for assigning numbers to outcomes
- The same random process can define multiple random variables (e.g., from a word: vowel count, first letter position, starts-with-CV)
- A **random vector** maps outcomes to $\mathbb{R}^d$ — an image patch is a random vector
- A **random matrix** maps outcomes to $\mathbb{R}^{m \times n}$ — an entire image is a random matrix
- The [[probability_distribution]] describes which values are likely

## Code Example

```python
import numpy as np

# One random process (word generation), three random variables
word = ''.join(np.random.choice(list('abcdefghijklmnopqrstuvwxyz'), 3))

x1 = sum(c in 'aeiou' for c in word)  # vowel count → Binomial
x2 = ord(word[0]) - ord('a') + 1      # first letter position → Uniform
x3 = int(word[0] in 'cvmlr')          # starts with CV letter → Bernoulli
```

## Related Concepts

- [[probability_distribution]] — describes the likelihood of each value
- [[bernoulli_distribution]] — simplest random variable (binary)
- [[pixel]] — a random variable in the imaging context

## Sources

- [[01a_probability_for_cv|Tutorial 01a: Probability for CV]] — Part 0
