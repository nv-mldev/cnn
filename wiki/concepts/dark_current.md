---
tags: [concept, sensor-physics, noise]
sources: [tutorials/01a_probability_for_cv/part6_putting_it_together.md]
last_updated: 2026-04-05
---

# Dark Current

Thermal electrons that accumulate in a photosite even without light, adding a [[poisson_distribution|Poisson]]-distributed noise floor to every measurement.

## Why It Matters

Dark current sets a baseline noise that exists even in complete darkness. It's typically small (1–10 electrons for cooled sensors) but becomes significant in long exposures or hot environments. It's one of the four noise sources in the [[noise_budget]] and follows Poisson statistics — adding variance $\lambda_d$ to the total.

## Key Ideas

- Distribution: $\text{Poisson}(\lambda_d)$ where $\lambda_d$ = expected dark electrons
- Increases with temperature and exposure time
- Cooled scientific cameras have near-zero dark current
- Adds to total variance: $\sigma^2_{total} = \lambda + \lambda_d + \sigma_r^2 + \Delta^2/12$
- Can be partially corrected by subtracting a dark frame (image taken with lens cap on)

## Related Concepts

- [[shot_noise]] — the other Poisson noise source (from photons)
- [[read_noise]] — electronic noise added during readout
- [[noise_budget]] — dark current is one of four noise terms
- [[poisson_distribution]] — the statistical model for dark current

## Sources

- [[01a_probability_for_cv|Tutorial 01a: Probability for CV]] — Part 6
