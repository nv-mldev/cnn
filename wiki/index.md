---
tags: [index]
last_updated: 2026-04-10
---

# Foundations of Machine Vision — Wiki

From photons to transformers to VLMs: the complete visual intelligence stack, built from first principles.

The structure follows the learning progression: **sensor physics → linear algebra → probability → matching → features → CNNs → attention → transformers → VLMs**. Each level builds on the previous — drill down from the top.

---

## Sources (Tutorial Summaries)

- **00** — [[00_introduction_to_digital_images|Introduction to Digital Images]] — Photons to pixels: sensor physics, sampling, quantization, colour, and why pixel values are unreliable
- **01** — [[01b_linear_algebra_for_matching|Linear Algebra for Images]] — Vectors, norms, cosine similarity, orthogonal projection — the math behind normalised matching
- **02** — [[01a_probability_for_cv|Probability for Sensors]] — Bernoulli→Binomial→Poisson→Normal→CLT: the math behind sensor noise
- **03** — [[02_why_not_pixels|Why Not Pixels]] — Physics → affine model → normalisation → ceiling → features: why raw pixels fail and what replaces them

---

## Concepts

### 1. Sensor Physics — How light becomes electrons

How a camera sensor converts photons into electrical signals. The physical layer that everything else builds on.

- [[photosite]] — Physical light-sensitive element that collects photons
- [[quantum_efficiency]] — Fraction of photons converted to electrons (0.4–0.8)
- [[full_well_capacity|Full-Well Capacity]] — Maximum electrons before saturation
- [[dynamic_range]] — Ratio of brightest to darkest capturable values
- [[dark_current]] — Thermal electrons accumulating without light
- [[read_noise]] — Electronic noise from amplifier/ADC

### 2. Linear Algebra for Images — Images as vectors

Treating image patches as high-dimensional vectors unlocks the linear algebra toolkit for comparison.

- [[vector_representation]] — A 3×3 patch is a point in 9D space
- [[dot_product]] — Pixel-by-pixel agreement; magnitude-dependent
- [[l2_norm]] — Vector length / magnitude
- [[unit_vector]] — Direction without magnitude
- [[cosine_similarity]] — Handles contrast ($a$) but fails on brightness offset ($b$)
- [[orthogonality]] — Zero dot product; independent directions
- [[orthogonal_projection]] — Decomposing a vector along a direction
- [[mean_subtraction]] — Projection onto $[1,\ldots,1]$ direction removes brightness offset
- [[linear_transform]] — Matrix that preserves vector addition and scalar multiplication
- [[orthogonal_transform]] — Norm-preserving rotation: $\|Qx\| = \|x\|$ (Parseval's theorem)

### 3. Probability Foundations — The math behind noise

The distribution families that model sensor noise, building from simple to complex.

- [[random_variable]] — Function mapping outcomes to numbers; every pixel is one
- [[probability_distribution]] — Complete probability assignment: PMF, PDF, CDF
- [[bernoulli_distribution]] — Binary trial with probability p; one photon → detected or not
- [[binomial_distribution]] — Count of successes in n Bernoulli trials
- [[poisson_distribution]] — Rare events in large regions; exact photon counting model
- [[normal_distribution]] — Bell curve; the endpoint of the CLT
- [[central_limit_theorem]] — Sum of any independent RVs → Gaussian; why sensor noise is Gaussian

### 4. Noise — Why repeated captures differ

The physics of randomness in imaging. Every concept here is a probability distribution applied to photons or electrons.

- [[shot_noise]] — Poisson-distributed photon arrival noise, σ = √λ
- [[signal_to_noise_ratio|Signal-to-Noise Ratio]] — SNR ≈ √λ at high signal
- [[noise_budget]] — Complete accounting of all noise sources
- [[noise_regimes]] — Read-limited, shot-limited, saturated: which noise dominates
- [[anscombe_transform]] — Variance stabilisation: Poisson → unit-variance Gaussian

### 5. Sampling & Quantization — Continuous world to discrete pixels

How continuous signals become the discrete grid of numbers we call an image.

- [[spatial_frequency]] — How quickly intensity changes across space; the bridge from DSP time-domain frequency to images
- [[frequency_domain]] — Fourier analysis: time-domain sinusoids → 1D FFT → 2D image spectra → frequency-domain filtering
- [[sampling]] — Continuous signal → discrete values on a regular grid
- [[nyquist_criterion]] — Minimum 2 samples per period to avoid aliasing
- [[aliasing]] — Phantom frequencies from undersampling, irreversible
- [[anti_aliasing_filter|Anti-Aliasing Filter]] — Low-pass filter before downsampling
- [[downsampling]] — Reducing resolution, permanently losing detail
- [[pixel]] — A single number at (i,j), not a tiny photograph
- [[spatial_resolution]] — Width × height in pixels
- [[ground_sampling_distance]] — Physical scene size per pixel
- [[quantization]] — Continuous voltage → discrete integer, irreversible
- [[bit_depth]] — Number of bits per pixel (8-bit = 256 levels)
- [[false_contours]] — Visible banding from coarse quantization

### 6. Image Formation & Colour — From scene to stored file

The full chain from scene light through the sensor pipeline to a stored image file.

- [[image_formation_model]] — $f(x,y) = i(x,y) \cdot r(x,y)$: illumination × reflectance
- [[affine_model]] — $I = aT + b$: same scene, different pixel values under different lighting
- [[contrast]] — Spread of pixel values, controlled by affine parameter $a$
- [[contrast_stretching]] — Linear rescaling to full range; preserves $r = 1.0$
- [[clipping]] — Permanent information loss when values exceed sensor range
- [[shading]] — Position-dependent brightness variation (vignetting)
- [[bayer_filter]] — RGGB colour filter mosaic over monochrome sensor
- [[demosaicing]] — Interpolating missing colour channels from Bayer mosaic
- [[luminance]] — Perceptual brightness: $L = 0.2126R + 0.7152G + 0.0722B$
- [[imaging_pipeline]] — End-to-end chain from scene light to stored pixels
- [[nearest_neighbour_interpolation|Nearest-Neighbour Interpolation]] — Copy closest pixel, fast but blocky
- [[bilinear_interpolation]] — 4-neighbour weighted average, smooth but blurry

### 7. Matching & Normalisation — Comparing images correctly

Building matching metrics that are invariant to the affine imaging model.

- [[ssd]] — Sum of Squared Differences; simplest metric, fails on intensity changes
- [[pearson_correlation]] — Center + normalise = full affine invariance; = `TM_CCOEFF_NORMED`
- [[normalisation_ceiling]] — Boundary: intensity problems (solvable) vs spatial problems (not solvable by normalisation)

### 8. Beyond Pixels — Why features are needed

Where normalisation fails and what replaces it.

- [[manifold_hypothesis]] — Natural images occupy a thin manifold in pixel space
- [[feature_hierarchy]] — Pixels → edges → descriptors (SIFT) → learned features (CNNs)

---

## Synthesis (Cross-cutting analysis)

- [[why_pixels_fail|Why Pixel Values Are Unreliable]] — The error stack: noise + quantization + affine + aliasing + pipeline = unreliable pixels
- [[distribution_chain|The Distribution Chain]] — Bernoulli→Binomial→Poisson→Normal→CLT: each step a limiting case of the previous
- [[normalisation_to_features|From Normalisation to Features]] — Physics → affine model → normalisation → ceiling → features → CNNs: the complete progression
