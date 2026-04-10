# Part 2: Physics of Image Formation and the Affine Model

## Learning Objective

Understand **where pixel values come from physically**, derive the affine approximation
$I \approx a \cdot T + b$ from first principles, and know exactly **when it holds and when
it breaks**.

---

## 2.1 The Image Formation Model

The pixel value at any location is the product of two independent physical quantities:

$$f(x, y) = i(x, y) \cdot r(x, y)$$

| Symbol | Name | What it is | Range |
|--------|------|-----------|-------|
| $i(x,y)$ | **Illumination** | Energy arriving at point $(x,y)$ from the light source(s) | $[0, \infty)$ |
| $r(x,y)$ | **Reflectance** | Fraction of light the surface reflects back to the camera | $[0, 1]$ |
| $f(x,y)$ | **Image irradiance** | Light that actually reaches the sensor | product of the two |

**Key insight:** This is a *multiplicative* model, not additive. A dark pixel could mean
low illumination (shadow) OR low reflectance (dark material) — the sensor cannot tell the
difference.

---

## 2.2 The Sensor Model — From Light to Numbers

The sensor converts the continuous irradiance $f(x,y)$ into a stored digital value
$g(x,y)$ through an approximately linear process:

$$g(x, y) = a \cdot f(x, y) + b$$

| Symbol | Name | Physical source |
|--------|------|----------------|
| $a$ | **System gain** | Sensor gain (ISO), exposure time $t$, amplifier gain |
| $b$ | **System bias** | Dark current, analog offset, black level |

The full pipeline from scene to pixel:

$$g(x,y) = a \cdot \big[\, i(x,y) \cdot r(x,y) \,\big] + b$$

---

## 2.3 From Physics to the Computational Model

The physics is **multiplicative** ($i \cdot r$), but we model differences between images
as **affine** ($a \cdot T + b$). How is this justified?

### The Collapse: When Illumination is Approximately Uniform

Consider two captures of the same object — a **template** $T$ and a **query** $I$:

**Template capture:**
$$T(x,y) = a_T \cdot \big[\, i_T(x,y) \cdot r(x,y) \,\big] + b_T$$

**Query capture:**
$$I(x,y) = a_I \cdot \big[\, i_I(x,y) \cdot r(x,y) \,\big] + b_I$$

Now assume illumination is **approximately constant** over the small template window:
- $i_T(x,y) \approx i_T$ (a scalar)
- $i_I(x,y) \approx i_I$ (a different scalar)

Then the template simplifies to:
$$T(x,y) = (a_T \cdot i_T) \cdot r(x,y) + b_T = \alpha_T \cdot r(x,y) + b_T$$

And the query to:
$$I(x,y) = (a_I \cdot i_I) \cdot r(x,y) + b_I = \alpha_I \cdot r(x,y) + b_I$$

**The illumination $i$, exposure time, and sensor gain all collapse into a single scalar $\alpha$.**

Eliminating $r(x,y)$ between the two equations:

$$I = \frac{\alpha_I}{\alpha_T} \cdot (T - b_T) + b_I = \underbrace{\frac{\alpha_I}{\alpha_T}}_{a} \cdot T + \underbrace{\left(b_I - \frac{\alpha_I}{\alpha_T} \cdot b_T\right)}_{b}$$

$$\boxed{I \approx a \cdot T + b}$$

**This is the affine model.** It is not a separate model from the physics — it *is* the
physics, under the assumption of locally uniform illumination.

---

## 2.4 What the Affine Model Absorbs

| Physical factor | How it enters | Absorbed into |
|----------------|---------------|---------------|
| Illumination level $i$ | Multiplicative on $r(x,y)$ | $a$ (gain) |
| Exposure time $t$ | Multiplicative on signal | $a$ (gain) |
| Sensor gain (ISO) | Multiplicative on signal | $a$ (gain) |
| Dark current / black level | Additive offset | $b$ (bias) |
| Sensor noise $\eta$ | Stochastic, per-pixel | Residual |

**Goal:** Use ZNCC (normalised cross-correlation) to make the match **invariant to $a$
and $b$**, leaving only the correlation of the underlying reflectance pattern $r(x,y)$.

---

## 2.5 Why We Use This Approximation

| Approach | Requires | Complexity | When to use |
|----------|----------|-----------|-------------|
| Full physics ($i \cdot r$) | 3D geometry, light sources, BRDF | Very high | Rendering engines |
| Affine approximation ($a \cdot T + b$) | Nothing — $a, b$ are cancelled by normalisation | $O(1)$ extra | Template matching |

The affine model is **computationally free** — normalisation cancels $a$ and $b$ without
ever estimating them.

---

## 2.6 When the Approximation Breaks

| Failure mode | What happens physically | Why affine breaks |
|-------------|----------------------|-------------------|
| **Shadow across template** | $i(x,y)$ varies within the window | No single scalar $a$ models a spatially varying multiplier |
| **Specular highlight** | $r(x,y)$ becomes view-dependent (BRDF) | Reflectance itself changes with viewing angle |
| **Sensor nonlinearity / gamma** | $g = f^\gamma$ instead of $g = a \cdot f + b$ | Relationship is no longer linear |
| **Geometric change** | Different surface region visible | $r(x,y)$ itself is different |
| **Sensor noise** | $\eta$ is stochastic, per-pixel, per-frame | Even perfect $a, b$ can't achieve $r = 1.0$ |

> **Summary:** We don't ignore the physics — we *exploit* the fact that, locally, the
> physics simplifies to a linear model that normalisation can cancel exactly.
