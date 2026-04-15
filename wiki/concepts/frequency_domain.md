---
tags: [concept, frequency-domain, fourier, fundamentals]
sources: ["Gonzalez & Woods — Digital Image Processing 3rd ed., Ch. 4", "Oppenheim & Willsky — Signals and Systems"]
last_updated: 2026-04-15
---

# Frequency Domain Analysis

Any signal — a sound wave, a heartbeat trace, a row of pixels, a whole image — can be rewritten as a **sum of sinusoids**. The frequency domain is the view that shows *which sinusoids, and how strong each one is*.

## Why It Matters

The spatial-domain view of an image is "intensity at each pixel." The frequency-domain view is "how much of each wavy pattern is in this image." The two are **exactly equivalent** — no information is added or lost — but certain operations (blur, sharpen, denoise, compress, detect periodic texture, understand aliasing) are far easier to reason about in the frequency view.

This page walks from 1D time-domain intuition → 1D Fourier → 2D spatial Fourier → reading an image spectrum.

---

## Part 1 — Start in the Time Domain

### A signal is a function of time

A microphone records air pressure over time: $f(t)$. A pure musical note is a sinusoid:

$$f(t) = A \sin(2\pi f_0 t + \phi)$$

- $A$ — amplitude (how loud)
- $f_0$ — frequency in **cycles per second (Hz)** (how high-pitched)
- $\phi$ — phase (where the wave starts)

### Real signals are sums of sinusoids

A chord on a piano is three pure tones played together — literally the sum of three sinusoids at different $f_0$. A square wave is an **infinite** sum of sinusoids at odd harmonics:

$$\text{square}(t) = \frac{4}{\pi}\sum_{k=1,3,5,\dots} \frac{1}{k}\sin(2\pi k f_0 t)$$

### Fourier's claim

**Any reasonable signal** $f(t)$ can be written as a sum (or integral) of sinusoids. The Fourier transform $F(f)$ is the recipe — it tells you the amplitude and phase of every frequency present:

$$F(f) = \int_{-\infty}^{\infty} f(t)\, e^{-i 2\pi f t}\, dt$$

Don't panic at the complex exponential — Euler's identity says $e^{-i 2\pi f t} = \cos(2\pi f t) - i\sin(2\pi f t)$, so the integral is really *"correlate the signal with a cosine and a sine at frequency $f$, and report the result as a complex number."*

- $|F(f)|$ — **magnitude spectrum** — "how much of frequency $f$"
- $\angle F(f)$ — **phase spectrum** — "where that sinusoid sits in time"

### Code — the 1D FFT in action

```python
import numpy as np
import matplotlib.pyplot as plt

sampling_rate = 1000            # samples per second
duration      = 1.0             # seconds
t             = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Signal: 5 Hz + 50 Hz sinusoids summed
signal = np.sin(2*np.pi*5*t) + 0.5*np.sin(2*np.pi*50*t)

# FFT
spectrum   = np.fft.rfft(signal)
frequencies = np.fft.rfftfreq(len(signal), d=1/sampling_rate)
magnitude  = np.abs(spectrum)

# Two clean peaks at 5 Hz and 50 Hz
plt.stem(frequencies, magnitude)
plt.xlabel("Frequency (Hz)")
plt.ylabel("|F(f)|")
```

You will see **two sharp peaks** at exactly 5 Hz and 50 Hz — the FFT recovered the ingredients of the signal.

---

## Part 2 — The Jump from Time to Space

An image has no time axis. It has **position**. So we swap variables:

| Time domain | Spatial domain |
|---|---|
| $t$ (seconds) | $x$ (pixels, or mm) |
| $f(t)$ (amplitude vs. time) | $f(x)$ (intensity along a row) |
| Frequency: cycles / second (**Hz**) | Frequency: cycles / pixel (**cyc/px**) or cycles / mm |
| Sampling rate: samples / sec | Sampling rate: pixels / mm (pixel pitch $^{-1}$) |
| Nyquist: $f_s > 2 f_{\max}$ | **Same rule** — just reinterpret "frequency" |

**A single row of an image is a 1D signal.** Plot intensity along that row and you have something identical in form to an audio waveform — except the horizontal axis is pixels, not seconds.

```python
# One scanline of an image = a 1D signal in space
scanline = image[100, :]             # row 100, all columns
spectrum = np.fft.rfft(scanline)     # same FFT, different units
```

The spectrum now tells you what spatial patterns exist along that row:
- Peak at low frequency → slow brightness drift (e.g. shading)
- Peak at high frequency → fine striping or noise
- Multiple peaks → periodic texture (fabric, fence, brick)

---

## Part 3 — Images Are 2D

An image is $f(x, y)$, so it has frequency in **two directions**. The 2D Fourier transform is:

$$F(u, v) = \iint f(x, y)\, e^{-i 2\pi (u x + v y)}\, dx\, dy$$

- $u$ — horizontal spatial frequency (cycles across width)
- $v$ — vertical spatial frequency (cycles down height)
- $(u, v)$ together — a frequency and a **direction** (diagonal stripes have both $u \ne 0$ and $v \ne 0$)

The basis "sinusoids" are now 2D sinusoidal plane waves:

$$g_{u,v}(x, y) = \cos\!\big(2\pi(u x + v y)\big)$$

Horizontal stripes, vertical stripes, diagonal stripes — each is one basis pattern. Every image is a weighted sum of all of them.

### Reading a 2D spectrum

```python
image     = plt.imread("photo.png").mean(axis=2)      # to grayscale
spectrum  = np.fft.fftshift(np.fft.fft2(image))       # shift DC to center
magnitude = np.log1p(np.abs(spectrum))                # log scale to see faint peaks

plt.imshow(magnitude, cmap="gray")
```

How to read the plot:

- **Center** — DC component = average brightness
- **Near the center** — low spatial frequencies (smooth regions, slow gradients)
- **Outer rings** — high spatial frequencies (edges, fine texture, noise)
- **A bright streak in a direction** — strong periodic pattern perpendicular to that direction (e.g. horizontal fence → vertical streak in spectrum)
- **A diffuse halo everywhere** — broadband content like natural noise

### Magnitude vs. phase — a surprise

If you swap the magnitude spectra of two images but keep each one's phase, the images stay **mostly recognizable**. Swap the phases instead and the images scramble. **Most of the "where" information lives in the phase** — a fact that does not exist in the time-domain view.

---

## Part 4 — Filtering in the Frequency Domain

Once you have $F(u, v)$, multiplying it by a mask $H(u, v)$ and inverse-transforming gives a filtered image:

$$\text{filtered}(x, y) = \mathcal{F}^{-1}\big\{ F(u, v) \cdot H(u, v) \big\}$$

- **Low-pass mask** (circle around the center, zeros outside) → blur
- **High-pass mask** (zeros at center, ones outside) → edges / sharpen
- **Band-pass** (annulus) → isolate a range of scales
- **Notch** (zero a few specific peaks) → remove periodic interference (scanner stripes, mains hum)

```python
rows, cols = image.shape
cy, cx = rows // 2, cols // 2
yy, xx = np.ogrid[:rows, :cols]
radius_squared = (xx - cx)**2 + (yy - cy)**2

cutoff = 30                                 # frequencies inside this radius survive
low_pass_mask = radius_squared <= cutoff**2

filtered_spectrum = spectrum * low_pass_mask
blurred = np.fft.ifft2(np.fft.ifftshift(filtered_spectrum)).real
```

**Convolution theorem:** multiplication in the frequency domain ↔ convolution in the spatial domain. Gaussian blur *is* a low-pass filter. A Sobel edge detector *is* a high-pass filter. CNN kernels are learned linear filters — each one picks out specific frequency-and-orientation content in its input.

---

## Part 5 — Why This Matters For Vision and CNNs

- [[nyquist_criterion]] is stated in frequency language — you can't understand sampling without it.
- [[aliasing]] and moiré are frequencies folding over — visible only in the frequency view.
- **JPEG** transforms 8×8 blocks with the DCT (a cousin of the FT) and throws away small high-frequency coefficients. That's the whole compression trick.
- **CNN early layers** learn filters that look like oriented band-pass filters — Fourier on training data shows why.
- **Diffusion models** inject Gaussian noise, which is flat across the frequency spectrum; training teaches the model to recover the image's natural frequency profile.
- **GAN artifacts** are often diagnosed by comparing the high-frequency spectra of real vs. generated images.

---

## Related Concepts

- [[spatial_frequency]] — the bridge page: "what does frequency even mean for an image?"
- [[nyquist_criterion]] — the sampling rule, stated in frequency terms
- [[aliasing]] — frequency folding when sampling below Nyquist
- [[anti_aliasing_filter]] — a low-pass filter applied before sampling
- [[sampling]] — the operation the frequency view lets you reason about
- [[convolutions]] *(upcoming)* — convolution theorem connects spatial and frequency filtering

## Sources

- Gonzalez & Woods, *Digital Image Processing*, 3rd ed., Chapter 4 — Filtering in the Frequency Domain
- Oppenheim & Willsky, *Signals and Systems* — for the 1D Fourier foundations
- 3Blue1Brown, "But what is the Fourier Transform?" — standard visual primer
