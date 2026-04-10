# Part 1: From Light to Numbers — Sampling and Sensors

## Learning Objective

Understand how a camera converts continuous light from a scene into a discrete grid of numbers.
Every concept here is grounded in what the sensor physically does.

---

## 1.1 What Is a Digital Image?

A digital image is a **2D function sampled on a regular grid**.

The scene in front of a camera reflects or emits light of varying intensity at every point
$(x, y)$ in space. The camera's job is to measure that continuous function and convert it
into a finite array of numbers.

Formally, a grayscale image is:

$$I(i, j) = \text{intensity measured at grid position } (i, j)$$

where $i$ is the row and $j$ is the column. The result is a **2D array of integers** — the
pixel grid.

**Key insight:** An image is always a *lossy approximation* of the scene. Two decisions
control how much information is preserved:

| Decision | What it controls | Trade-off |
|----------|-----------------|-----------|
| **Spatial sampling** (resolution) | How fine the grid is | More pixels = more detail, more storage |
| **Intensity quantization** (bit depth) | How many discrete brightness levels | More bits = finer brightness steps, more storage |

---

## 1.2 A 1D Analogy: Sampling a Sine Wave

Before jumping to 2D images, build intuition with a 1D signal. Imagine a smooth, continuous
sine wave — this is our "scene". Sampling means measuring its value at evenly-spaced points.

**What the simulation shows:**
- The continuous wave is the true scene: it exists everywhere.
- Samples are the measurements: a finite set of numbers.
- With enough samples, you can reconstruct the wave faithfully.
- With too few samples, information is permanently lost — the reconstructed wave looks wrong.

**The rule:** you need at least **2 samples per period** of the highest frequency in the signal
to reconstruct it without error. This is the **Nyquist criterion**. Below that rate,
frequencies "fold over" and create phantom signals — **aliasing**.

---

## 1.3 Inside the Sensor: Photosites, Well Capacity, and Noise

A camera sensor is a grid of **photosites** (also called pixels on the sensor). Each photosite:

1. Collects photons during the **exposure time**
2. Converts photons to electrons via the **photoelectric effect**
3. Measures the electron count as a voltage
4. An **ADC** (Analog-to-Digital Converter) maps the voltage to a discrete integer

The physics of step 1 is a **Poisson process** — photon arrivals are random events. This
randomness is the fundamental source of **shot noise**.

### Key sensor parameters

| Parameter | Symbol | Typical phone | Typical DSLR | Effect |
|-----------|--------|--------------|-------------|--------|
| Photosite area | $A$ | ~1 µm² | ~25 µm² | Larger = more photons collected |
| Full-well capacity | $C$ | ~1,000 e⁻ | ~50,000 e⁻ | Maximum electrons before saturation |
| Read noise | $\sigma_r$ | ~3 e⁻ | ~5 e⁻ | Electronic noise floor |
| Quantum efficiency | QE | 0.4–0.6 | 0.5–0.8 | Fraction of photons converted to electrons |

### Signal-to-Noise Ratio

For shot-noise-dominated sensors:

$$\text{SNR} = \frac{S}{\sqrt{S + \sigma_r^2}}$$

where $S$ is the mean signal (in electrons). At high signal levels ($S \gg \sigma_r^2$):

$$\text{SNR} \approx \sqrt{S}$$

This has a key implication: **doubling the photosite area doubles S, which improves SNR
by $\sqrt{2} \approx 41\%$**. This is why DSLR cameras produce less noisy images in low
light — not because of better electronics, but because of physically larger photosites.

### Why this matters for computer vision

A pixel value is not a pure measurement of scene brightness. It is:

$$\text{pixel value} = f\left(\text{photons} \times \text{QE} + \text{read noise} + \text{dark current}\right)$$

This means:
- Two cameras imaging the same scene produce **different pixel values**
- The same camera at different exposures produces **different pixel values**
- Any algorithm that compares pixel values directly is comparing camera physics, not scene content

---

## 1.4 Phone vs DSLR: Sensor Size in Practice

The photosite area difference between a phone and a DSLR is approximately **25×**. This
directly affects how many photons are collected, which sets the SNR.

| Condition | Phone (small photosite) | DSLR (large photosite) |
|-----------|------------------------|----------------------|
| Bright daylight | Good — photons are plentiful | Good |
| Indoor lighting | Noisy — few photons per tiny site | Acceptable |
| Dim / night | Very noisy — SNR near 1 | Better — more photons collected |

The consequence: **pixel values from a phone and a DSLR of the same scene are not
numerically comparable**, even at the same exposure settings.

---

## Summary

| Concept | Key fact |
|---------|----------|
| Image as function | $I(i,j)$ = intensity on a grid; always an approximation |
| Sampling | Grid spacing determines spatial resolution; Nyquist sets the minimum rate |
| Photosite | Physical element that counts photons; size drives noise level |
| Shot noise | Poisson randomness in photon arrivals; $\sigma = \sqrt{S}$ |
| SNR | Scales as $\sqrt{\text{signal}}$; bigger pixels = lower noise |

**Next:** Part 2 — What a pixel actually is, spatial resolution, and quantization.
