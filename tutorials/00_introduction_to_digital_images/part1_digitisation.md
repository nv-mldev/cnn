# Part 1: Digitisation — Sampling, Nyquist, and Aliasing

## Learning Objective

Understand what it means to convert a continuous signal into a discrete set of numbers.
This is the foundational act of digital imaging — everything downstream (pixels, resolution,
artefacts) follows from the rules established here.

---

## 1.1 What Is Sampling?

A continuous signal — a sound wave, a light intensity field, a temperature gradient — exists
at every real-valued point. A sensor can only measure it at a **finite number of moments or
locations**. The act of measuring at a discrete set of points is called **sampling**.

For a 1D signal $x(t)$, sampling at rate $f_s$ produces:

$$x[n] = x\!\left(\frac{n}{f_s}\right), \quad n = 0, 1, 2, \ldots$$

The gap between consecutive samples is the **sampling interval** $\Delta t = 1 / f_s$.

For a 2D image, sampling happens on a grid:

$$I[m, n] = I_{\text{continuous}}(m \cdot \Delta x,\; n \cdot \Delta y)$$

Each grid cell becomes one pixel. The pixel pitch $\Delta x$ is the 2D sampling interval.

**The core trade-off:** finer sampling (smaller $\Delta t$ or $\Delta x$) preserves more
detail but produces more data. Coarser sampling loses information — permanently.

---

## 1.2 The Nyquist–Shannon Sampling Theorem

**Theorem:** A band-limited signal with highest frequency $f_{\max}$ can be perfectly
reconstructed from its samples *if and only if* the sampling rate satisfies:

$$f_s \geq 2 \cdot f_{\max}$$

The minimum acceptable rate $2 f_{\max}$ is the **Nyquist rate**.
The maximum representable frequency at a given $f_s$ is the **Nyquist frequency**:

$$f_N = \frac{f_s}{2}$$

**Why the factor of 2?** To capture a cosine at frequency $f$, you need to observe at least
one peak and one trough per cycle. That requires at least two samples per period — one at the
peak, one at the trough. Any fewer and the period is ambiguous.

### In images

A camera with pixel pitch $\Delta x$ has:

$$f_N = \frac{1}{2 \Delta x} \quad \text{(cycles per unit length)}$$

Or equivalently, in cycles per pixel: $f_N = 0.5$ cycles/pixel.
Any scene detail finer than 2 pixels per cycle cannot be faithfully captured.

---

## 1.3 Aliasing: What Happens Below Nyquist

When $f_{\text{signal}} > f_N$, the samples produced by the true signal are **identical** to
the samples of a different, lower-frequency signal — the **alias**:

$$f_{\text{alias}} = \left| f_{\text{signal}} - \text{round}\!\left(\frac{f_{\text{signal}}}{f_s}\right) \cdot f_s \right|$$

Example: $f_s = 8$ Hz, $f_{\text{signal}} = 11$ Hz → $f_{\text{alias}} = |11 - 8| = 3$ Hz.

The reconstructor receives the samples and has **no way to distinguish** whether they came
from the 11 Hz or the 3 Hz signal. It will output 3 Hz — a phantom frequency that was never
in the scene.

### Derivation: why two frequencies produce identical samples

Start with two cosines at different frequencies $f_m$ and $f_m + k f_s$ (where $k$ is any integer):

$$x_1(t) = \cos(2\pi f_m t)$$
$$x_2(t) = \cos(2\pi (f_m + k f_s) t)$$

Now sample both at rate $f_s$ — that means evaluating at $t = n / f_s$ for integer $n$:

$$x_1[n] = \cos\!\left(2\pi f_m \cdot \frac{n}{f_s}\right)$$

$$x_2[n] = \cos\!\left(2\pi (f_m + k f_s) \cdot \frac{n}{f_s}\right)$$

Expand $x_2[n]$:

$$x_2[n] = \cos\!\left(2\pi f_m \cdot \frac{n}{f_s} + 2\pi k f_s \cdot \frac{n}{f_s}\right)
         = \cos\!\left(2\pi f_m \cdot \frac{n}{f_s} + 2\pi k n\right)$$

Since $k$ and $n$ are both integers, $2\pi k n$ is always an exact multiple of $2\pi$.
Cosine is $2\pi$-periodic, so this extra term vanishes:

$$x_2[n] = \cos\!\left(2\pi f_m \cdot \frac{n}{f_s}\right) = x_1[n]$$

**The samples are identical — for every $n$, at every time step.**

This is the root cause of aliasing. Any frequency of the form $f_m + k f_s$ (for any integer $k$) produces exactly the same discrete sequence as $f_m$. They form an **alias family** — infinitely many continuous signals that are indistinguishable once sampled.

### The folding picture follows directly

From the derivation: all frequencies $f_m,\; f_m \pm f_s,\; f_m \pm 2f_s, \ldots$ alias to the same sequence.

We always work with positive frequencies, so we fold everything into $[0, f_s/2]$:

- A frequency in $[0,\; f_N]$ → already in the safe zone, kept as-is
- A frequency in $[f_N,\; f_s]$ → set $k = -1$: maps to $f_s - f_m \in [0, f_N]$
- A frequency in $[f_s,\; 3f_N]$ → set $k = -1$ then fold: maps back into $[0, f_N]$
- And so on — the pattern tiles with period $f_s$

```
Frequency axis:  0 ──── f_N ──── f_s ──── f_N+f_s ──── 2f_s
                        ↑fold         ↑fold
                 Safe zone: [0, f_N]  ← everything maps here
```

**Concrete example** ($f_s = 8$ Hz, $f_N = 4$ Hz):

| True $f_m$ | Alias family member | $f_{alias}$ | Why |
|-----------|---------------------|-------------|-----|
| 5 Hz | $5 - 8 = -3$ → $|{-3}| = 3$ Hz | **3 Hz** | $k=-1$, then take absolute value |
| 6.5 Hz | $6.5 - 8 = -1.5$ → $1.5$ Hz | **1.5 Hz** | $k=-1$ |
| 11 Hz | $11 - 8 = 3$ Hz | **3 Hz** | $k=-1$ |
| 2 Hz | already $< f_N$ | **2 Hz** | no folding needed |

Notice 5 Hz and 11 Hz both alias to 3 Hz — they are in the same alias family ($f_m + k f_s$ with $k = -1$ and $k = -2$ respectively).

### The folding picture

```
0 ──── f_N ──── f_s ──── 3f_N ──── 2f_s
      ↑                  ↑
   mirror              mirror
```

Frequencies in $[f_N,\; f_s]$ map back to $[0,\; f_N]$.
Frequencies in $[f_s,\; 3f_N]$ map back to $[0,\; f_N]$ again.
And so on — the pattern repeats with period $f_s$.

### Key properties of aliasing

| Property | Detail |
|----------|--------|
| **Irreversible** | Once aliased, phantom and real frequencies are indistinguishable |
| **Not distortion** | The signal is not degraded — it is *replaced* by a different signal |
| **Prevention** | Apply a low-pass filter (anti-aliasing filter) *before* sampling |

---

## 1.4 Sinc Reconstruction — The Ideal Reconstructor

Given samples $x[n]$, the Shannon–Whittaker formula reconstructs the original signal exactly
(when $f_s \geq 2 f_{\max}$):

$$x(t) = \sum_{n=-\infty}^{\infty} x[n] \cdot \text{sinc}\!\left(f_s \cdot (t - n/f_s)\right)$$

where $\text{sinc}(u) = \sin(\pi u) / (\pi u)$.

This formula fills in the values *between* samples using a weighted sum of sinc "kernels"
centred at each sample. When the sampling rate is sufficient, the kernels cancel perfectly
everywhere the signal has no energy — giving exact reconstruction.

When below Nyquist, the sinc reconstruction still runs — but it faithfully reconstructs the
*alias*, not the true signal. **The simulation in the code makes this visible:** you can
watch a 11 Hz input emerge from the reconstructor as a 3 Hz output.

---

## 1.5 From 1D to 2D: Nyquist Applies Per Axis

An image is a 2D signal. The Nyquist criterion applies **independently along each spatial axis**:

- Along $x$ (columns): need $f_{s,x} \geq 2 \cdot u_{\max}$
- Along $y$ (rows):    need $f_{s,y} \geq 2 \cdot v_{\max}$

A 2D sinusoidal pattern has a **frequency vector** $(u, v)$ in cycles/pixel.
The representable region is the **Nyquist square** in 2D frequency space:

$$|u| \leq f_{N,x} \quad \text{AND} \quad |v| \leq f_{N,y}$$

Any $(u, v)$ outside this square aliases. The direction of aliasing depends on which
axis is violated:

| Violation | Artefact |
|-----------|----------|
| $u > f_{N,x}$ only | False horizontal stripe pattern |
| $v > f_{N,y}$ only | False vertical stripe pattern |
| Both | Moiré — diagonal phantom pattern |

### Moiré in practice

Moiré appears whenever a fine periodic texture (fabric, mesh, PCB traces, brick) is
photographed at insufficient resolution. The fine pattern aliases to a coarser phantom
pattern. It is not a lens defect — it is a sampling artefact.

Camera manufacturers place an **optical low-pass filter** (OLPF) in front of the sensor
to blur the image slightly before it hits the photosite grid, preventing the scene from
containing frequencies above $f_N$ in the first place.

---

## Summary

| Concept | Statement |
|---------|-----------|
| Sampling | Measuring a continuous signal at discrete points |
| Sampling interval | $\Delta t = 1/f_s$ (1D) or pixel pitch $\Delta x$ (2D) |
| Nyquist rate | Minimum $f_s = 2 f_{\max}$ for lossless representation |
| Nyquist frequency | $f_N = f_s / 2$ — highest representable frequency |
| Aliasing | $\cos(2\pi(f_m + kf_s)t)$ produces identical samples to $\cos(2\pi f_m t)$ — high frequencies fold back as phantom lower frequencies |
| Reconstruction | Sinc interpolation recovers the signal — but outputs the alias when below Nyquist |
| 2D extension | Nyquist applies per axis; violation → moiré / false stripe patterns |
| Prevention | Low-pass filter *before* sampling (anti-aliasing filter / OLPF) |

**Next:** Part 2 — Sensor physics: what the photosite physically does to execute the
sampling operation (photon counting, shot noise, phone vs DSLR SNR).
