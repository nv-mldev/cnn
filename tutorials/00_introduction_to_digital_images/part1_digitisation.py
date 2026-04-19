"""
Part 1: Digitisation — Sampling, Nyquist, and Aliasing (1D → 2D)

Pedagogical path:
  1. 1D sinusoid sampling  — what it means to "sample" a wave
  2. 1D Nyquist criterion  — the minimum rate to represent a signal faithfully
  3. 1D aliasing           — what happens when you violate Nyquist (frequency folding)
  4. Phase offset          — why sampling at exactly Nyquist is fragile in practice
  5. 2D extension          — same rules apply to image rows, columns, and diagonals
  6. 2D aliasing demos     — stripe patterns, checkerboard, moiré on a real texture

Run:  uv run python part1_digitisation.py
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

FIGURES_DIR = Path(__file__).parent / '../../book/figures'
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

def savefig(name: str) -> None:
    """Save current figure to book/figures/ — no display, batch-safe."""
    plt.savefig(FIGURES_DIR / f'{name}.png', dpi=120, bbox_inches='tight')
    plt.close()

COLORS = {
    'continuous': '#2196F3',   # blue   — the true signal
    'samples':    '#F44336',   # red    — the sample points
    'alias':      '#FF9800',   # orange — the aliased reconstruction
    'nyquist':    '#4CAF50',   # green  — the Nyquist boundary
    'correct':    '#9C27B0',   # purple — correct reconstruction
}

np.random.seed(42)

print("Part 1: Digitisation — Sampling, Nyquist, and Aliasing")
print("=" * 50)


# ══════════════════════════════════════════════════════════════
# SECTION 1 — What does "sampling" a 1D signal mean?
# ══════════════════════════════════════════════════════════════
#
# A continuous signal like cos(2π f t) exists at every real-valued t.
# A sensor can only measure it at a finite set of moments — the sample points.
# The gap between samples is the sampling interval Δt = 1 / f_s.
# The sampling rate f_s (in samples/second or samples/pixel) determines
# how finely we can resolve variation in the signal.
# ──────────────────────────────────────────────────────────────

f_m = 3.0       # Hz — the frequency of the cosine we want to capture
t_dense = np.linspace(0, 1, 2000)    # "continuous" approximation (very fine grid)
continuous_signal = np.cos(2 * np.pi * f_m * t_dense)

# Try three different sampling rates: dense, sparse, and in-between
sampling_rates = [30, 8, 5]   # samples/second

fig, axes = plt.subplots(3, 1, figsize=(13, 9), sharex=True)
fig.suptitle('§1.2 Sampling a 1D Signal at Different Rates\n'
             f'True signal: cos(2π × {f_m:.0f} × t)   '
             f'f_N = f_s/2 = {2 * f_m/2:.0f} Hz,  f_Nyquist_rate = 2·f_m = {2 * f_m:.0f} samples/sec',
             fontsize=13)

for ax, fs in zip(axes, sampling_rates):
    # Sample the true signal at this rate
    t_samples = np.arange(0, 1, 1.0 / fs)
    samples   = np.cos(2 * np.pi * f_m * t_samples)

    # --- sinc reconstruction from these samples ---
    recon = np.zeros_like(t_dense)
    for tn, sn in zip(t_samples, samples):
        recon += sn * np.sinc(fs * (t_dense - tn))

    # --- draw the continuous reference ---
    ax.plot(t_dense, continuous_signal, color=COLORS['continuous'],
            lw=1.5, label='True signal', zorder=1)

    # --- draw sinc reconstruction as dashed line ---
    ax.plot(t_dense, recon, color=COLORS['alias'], lw=1.8, linestyle='--',
            label='Reconstruction (what the system thinks the signal is)', zorder=2)

    # --- draw vertical stems ---
    for ts, sv in zip(t_samples, samples):
        ax.plot([ts, ts], [0, sv], color=COLORS['samples'], lw=0.8,
                alpha=0.6, zorder=3)

    # --- draw the sample dots ---
    ax.scatter(t_samples, samples, color=COLORS['samples'], zorder=4,
               s=50, label=f'Samples (f_s = {fs} Hz, Δt = {1/fs:.3f} s)')

    # --- label whether this rate is above/below Nyquist ---
    f_N_required = 2 * f_m
    if fs >= f_N_required:
        status = f'✓ f_s={fs} ≥ {f_N_required:.0f} Hz — reconstruction matches true signal'
        color = COLORS['nyquist']
    else:
        status = f'✗ f_s={fs} < {f_N_required:.0f} Hz — reconstruction is WRONG (aliased)'
        color = COLORS['alias']

    ax.set_title(status, fontsize=10, color=color, loc='left')
    ax.set_ylim(-1.6, 1.8)
    ax.set_ylabel('Amplitude')
    ax.legend(loc='upper right', fontsize=9)
    ax.axhline(0, color='gray', lw=0.5)

axes[-1].set_xlabel('Time (seconds)')
plt.tight_layout()
savefig("ch01_1d_sampling")

print("Observation: at 30 samples/sec the continuous shape is well-captured.")
print("At 8 samples/sec (just above Nyquist) the shape is barely covered.")
print("At 5 samples/sec (below Nyquist) the dots no longer trace the true wave.\n")


# ══════════════════════════════════════════════════════════════
# SECTION §1.3a — What is sinc and how does it build reconstruction?
# ══════════════════════════════════════════════════════════════
#
# Four-panel figure showing the full reconstruction story:
#
#   Panel 1 — Stem plot: the discrete samples x[n] from cos(2π·f_m·t)
#             This is all we have after sampling — discrete dots, no curve.
#
#   Panel 2 — The sinc function itself: sinc(u) = sin(πu)/(πu)
#             Key property: 1 at u=0, exactly 0 at every other integer.
#             This is the "brick" used to build reconstruction.
#
#   Panel 3 — Shifted sinc kernels: one per sample, scaled by x[n]
#             x[n]·sinc(f_s·(t − n/f_s)) is 1·x[n] at t=n/f_s and 0 at
#             all other sample times → no cross-contamination between samples.
#
#   Panel 4 — Sum of all kernels = smooth reconstructed signal
#             Passes exactly through every sample dot.
# ──────────────────────────────────────────────────────────────

# Use 6 samples from cos(2π·f_m·t) at f_s=8 Hz — same signal as §1.2
fs_sinc_demo  = 8.0
sample_times  = np.arange(0, 6.0 / fs_sinc_demo, 1.0 / fs_sinc_demo)  # 6 samples
sample_values = np.cos(2 * np.pi * f_m * sample_times)

# Display window — slightly wider than sample range
t_display = np.linspace(-0.15, sample_times[-1] + 0.15, 3000)
t_cont    = np.linspace(-0.15, sample_times[-1] + 0.15, 3000)
true_cont = np.cos(2 * np.pi * f_m * t_cont)   # true continuous signal

# sinc function for panel 2 — shown in normalised time units
t_sinc_norm = np.linspace(-5, 5, 2000)
sinc_vals   = np.sinc(t_sinc_norm)   # np.sinc(x) = sin(πx)/(πx)

# Compute shifted kernels and sum
palette = ['#E91E63', '#9C27B0', '#FF9800', '#2196F3', '#4CAF50', '#FF5722']
colors_kernels = [palette[i % len(palette)] for i in range(len(sample_times))]

kernels        = []
reconstruction = np.zeros_like(t_display)
for tn, sn in zip(sample_times, sample_values):
    k = sn * np.sinc(fs_sinc_demo * (t_display - tn))
    kernels.append(k)
    reconstruction += k

fig, axes = plt.subplots(4, 1, figsize=(13, 14))
fig.suptitle('§1.3 — From Discrete Samples to Continuous Signal: How Sinc Reconstruction Works',
             fontsize=13)

# ── Panel 1: Stem plot of discrete samples ────────────────────
axes[0].plot(t_cont, true_cont, color=COLORS['continuous'], lw=1.2,
             alpha=0.35, linestyle='--', label='True continuous signal (hidden from sampler)')
axes[0].vlines(sample_times, 0, sample_values, color=COLORS['samples'], lw=2)
axes[0].scatter(sample_times, sample_values, color=COLORS['samples'], s=80, zorder=5)
for i, (tn, sn) in enumerate(zip(sample_times, sample_values)):
    axes[0].annotate(f'x[{i}]={sn:.2f}', xy=(tn, sn),
                     xytext=(tn + 0.01, sn + 0.08), fontsize=8.5,
                     color=COLORS['samples'], fontweight='bold')
axes[0].axhline(0, color='gray', lw=0.5)
axes[0].set_title('Step 1 — What we have: discrete samples x[n] from cos(2π·3·t) at f_s=8 Hz\n'
                  'The continuous curve is shown faint for reference — the sampler only sees the dots.',
                  fontsize=10, loc='left')
axes[0].set_ylabel('x[n]')
axes[0].legend(fontsize=9)
axes[0].set_ylim(-1.5, 1.5)

# ── Panel 2: The sinc function ────────────────────────────────
axes[1].plot(t_sinc_norm, sinc_vals, color=COLORS['continuous'], lw=2)
axes[1].axhline(0, color='gray', lw=0.5)
# Mark sinc(0)=1 and zeros at integers
axes[1].scatter([0], [1], color=COLORS['nyquist'], s=100, zorder=5,
                label='sinc(0) = 1  ← peak at own sample')
for n in [-4, -3, -2, -1, 1, 2, 3, 4]:
    axes[1].scatter([n], [0], color=COLORS['samples'], s=60, zorder=5)
axes[1].annotate('sinc(n)=0\nfor all n≠0', xy=(1, 0), xytext=(1.5, 0.25),
                 arrowprops=dict(arrowstyle='->', color=COLORS['samples']),
                 fontsize=9, color=COLORS['samples'])
axes[1].set_title('Step 2 — The sinc kernel: sinc(u) = sin(πu)/(πu)\n'
                  'Value is 1 at its own position (u=0), exactly 0 at every other integer → no cross-talk between samples.',
                  fontsize=10, loc='left')
axes[1].set_ylabel('sinc(u)')
axes[1].set_xlabel('Normalised time u')
axes[1].legend(fontsize=9)
axes[1].set_ylim(-0.35, 1.3)

# ── Panel 3: Shifted kernels, one per sample ─────────────────
for i, (tn, sn, k) in enumerate(zip(sample_times, sample_values, kernels)):
    axes[2].plot(t_display, k, lw=1.5, color=colors_kernels[i],
                 label=f'x[{i}]·sinc(8·(t−{tn:.3f}))')
    axes[2].scatter([tn], [sn], color=colors_kernels[i], s=80, zorder=5)
    axes[2].annotate(f'x[{i}]={sn:.2f}', xy=(tn, sn),
                     xytext=(tn + 0.01, sn + 0.09), fontsize=8,
                     color=colors_kernels[i], fontweight='bold')
axes[2].axhline(0, color='gray', lw=0.5)
axes[2].set_title('Step 3 — Shifted & scaled sinc kernels: one per sample\n'
                  'Each kernel peaks at its own sample value and is exactly 0 at every other sample position.',
                  fontsize=10, loc='left')
axes[2].set_ylabel('Amplitude')
axes[2].legend(fontsize=8, ncol=3)
axes[2].set_ylim(-1.3, 1.6)

# ── Panel 4: Sum = reconstruction ────────────────────────────
axes[3].plot(t_cont, true_cont, color=COLORS['continuous'], lw=1.5,
             alpha=0.4, linestyle='--', label='True signal (reference)')
axes[3].plot(t_display, reconstruction, color=COLORS['alias'], lw=2.5,
             label='Reconstruction = Σ x[n]·sinc(f_s·(t − n/f_s))')
axes[3].vlines(sample_times, 0, sample_values, color=COLORS['samples'], lw=1.5, alpha=0.6)
axes[3].scatter(sample_times, sample_values, color=COLORS['samples'], s=80, zorder=5,
                label='Sample points x[n]')
for i, (tn, sn) in enumerate(zip(sample_times, sample_values)):
    axes[3].annotate(f'x[{i}]={sn:.2f}', xy=(tn, sn),
                     xytext=(tn + 0.01, sn + 0.09), fontsize=8,
                     color=COLORS['samples'], fontweight='bold')
axes[3].axhline(0, color='gray', lw=0.5)
axes[3].set_title('Step 4 — Sum of all kernels = smooth reconstruction\n'
                  'Passes exactly through every sample. Matches the true signal when f_s ≥ 2·f_m.',
                  fontsize=10, loc='left')
axes[3].set_ylabel('Amplitude')
axes[3].set_xlabel('Time (seconds)')
axes[3].legend(fontsize=9)
axes[3].set_ylim(-1.5, 1.5)

plt.tight_layout()
savefig("ch01_sinc_explanation")

print("§1.3a sinc explanation figure saved.")


# ══════════════════════════════════════════════════════════════
# SECTION §1.3 — Sinc Reconstruction and the Truncation Problem
# ══════════════════════════════════════════════════════════════
#
# Given samples x[n], the Whittaker–Shannon formula reconstructs x(t):
#   x(t) = Σ_n  x[n] · sinc( f_s · (t − n/f_s) )
#
# sinc(u) = sin(πu)/(πu) — it is 1 at u=0 and 0 at all other integers.
# Each sample contributes a bump that is 1 at its own time and 0 elsewhere.
#
# TRUNCATION PROBLEM:
# The sum is infinite — it needs samples from all time.
# In practice we have a finite window. The sinc tails that extend outside
# the window are cut off, causing edge artefacts (wiggles near the boundaries).
#
# FIX: sample a LONG window (T_LONG=5s), reconstruct in the CENTRE (1.5–2.5s).
# The edges are discarded. This makes the reconstruction clean in the middle.
# ──────────────────────────────────────────────────────────────

T_LONG  = 5.0           # long sampling window — gives sinc tails enough room
T_SHOW  = (1.5, 2.5)    # display only this central region — edges discarded

t_show    = np.linspace(T_SHOW[0], T_SHOW[1], 3000)
true_show = np.cos(2 * np.pi * f_m * t_show)

fig, axes = plt.subplots(3, 1, figsize=(13, 10), sharex=True)
fig.suptitle(
    '§1.3 — Sinc Reconstruction at Three Sampling Rates\n'
    'Blue = true signal  |  Orange dashed = reconstruction  |  Red dots = samples\n'
    'Central window shown (1.5–2.5 s) — edges discarded to avoid truncation artefacts',
    fontsize=12
)

for ax, fs in zip(axes, [30, 8, 5]):
    t_s = np.arange(0, T_LONG, 1.0 / fs)
    s_s = np.cos(2 * np.pi * f_m * t_s)

    # Sinc reconstruction — sums over ALL samples in the long window
    recon = np.zeros_like(t_show)
    for tn, sn in zip(t_s, s_s):
        recon += sn * np.sinc(fs * (t_show - tn))

    # Samples that fall inside the display window
    mask = (t_s >= T_SHOW[0]) & (t_s <= T_SHOW[1])

    mse    = np.mean((true_show - recon) ** 2)
    status = '✓ Good reconstruction' if fs >= 2 * f_m else '✗ Aliased — wrong wave output'

    ax.plot(t_show, true_show, color=COLORS['continuous'], lw=1.5,
            label=f'True signal: cos(2π·{f_m}·t)')
    ax.plot(t_show, recon, color=COLORS['alias'], lw=2, linestyle='--',
            label='Sinc reconstruction')
    ax.scatter(t_s[mask], s_s[mask], color=COLORS['samples'], s=60, zorder=5,
               label=f'Samples (f_s={fs} Hz,  {fs/f_m:.1f} per cycle)')

    color = COLORS['nyquist'] if fs >= 2 * f_m else COLORS['alias']
    ax.set_title(f'f_s = {fs} Hz  |  MSE = {mse:.5f}  |  {status}',
                 fontsize=10, color=color, loc='left')
    ax.set_ylabel('Amplitude')
    ax.legend(loc='upper right', fontsize=9)
    ax.axhline(0, color='gray', lw=0.5)
    ax.set_ylim(-1.6, 1.8)

axes[-1].set_xlabel('Time (seconds) — central window [1.5, 2.5 s]')
plt.tight_layout()
savefig("ch01_reconstruction")

print("§1.3 Reconstruction:")
print(f"  f_s=30 Hz → MSE ≈ 0 (dense sampling, perfect reconstruction)")
print(f"  f_s=8  Hz → MSE ≈ 0 (just above Nyquist, still good)")
print(f"  f_s=5  Hz → MSE >> 0 (below Nyquist, outputs wrong wave = aliasing)\n")


# ══════════════════════════════════════════════════════════════
# SECTION 2 — The Nyquist Criterion (theorem statement + visual)
# ══════════════════════════════════════════════════════════════
#
# Theorem (Shannon–Nyquist):
#   To perfectly reconstruct a band-limited signal with highest frequency f_m,
#   you must sample at rate  f_s ≥ 2·f_m  (f_s ≥ f_Nyquist_rate).
#
# The factor of 2 comes from the requirement to capture both the peak and trough
# of the highest-frequency component — you need at least one sample per half-period.
#
# The Nyquist frequency is  f_N = f_s / 2.
# Any signal component with f > f_N cannot be distinguished from something at f′ < f_N.
# That indistinguishable low-frequency impostor is the *alias*.
# ──────────────────────────────────────────────────────────────

f_m_sec2 = 3.0   # Hz — signal to capture

# Sweep sampling rate from 1 to 20 Hz.
# Use 5 seconds of signal so sinc tails have enough support — short windows
# cause edge artefacts that make the MSE curve look jagged (zigzag).
# We evaluate MSE only on the central 1-second window to avoid edge effects.
sweep_rates = np.linspace(1.0, 20.0, 400)
T_LONG      = 5.0                                  # signal duration for sampling
T_EVAL      = (2.0, 3.0)                           # evaluate MSE only in this window
t_long      = np.linspace(0, T_LONG, 50000)
t_eval      = np.linspace(T_EVAL[0], T_EVAL[1], 5000)
true_eval   = np.cos(2 * np.pi * f_m_sec2 * t_eval)

errors = []
for fs in sweep_rates:
    t_s  = np.arange(0, T_LONG, 1.0 / fs)
    s_s  = np.cos(2 * np.pi * f_m_sec2 * t_s)
    # Sinc reconstruction evaluated only at central window
    recon = np.zeros_like(t_eval)
    for tn, sn in zip(t_s, s_s):
        recon += sn * np.sinc(fs * (t_eval - tn))
    errors.append(np.mean((true_eval - recon) ** 2))

# Also compute reference true_signal for bottom panel display (1 second)
t_ref      = np.linspace(0, 1, 5000)
true_signal = np.cos(2 * np.pi * f_m_sec2 * t_ref)

errors = np.array(errors)

# Figure 1: MSE sweep — shows the sharp drop at the Nyquist rate
fig, ax = plt.subplots(figsize=(11, 4))
fig.suptitle(f'§1.3 Nyquist Criterion — f_m = {f_m_sec2} Hz', fontsize=13)
ax.semilogy(sweep_rates, errors + 1e-10, color=COLORS['continuous'], lw=2)
ax.axvline(2 * f_m_sec2, color=COLORS['nyquist'], lw=2, linestyle='--',
           label=f'Nyquist rate = 2·f_m = {2*f_m_sec2} Hz')
ax.set_xlabel('Sampling rate f_s (Hz)')
ax.set_ylabel('Reconstruction MSE (log scale)')
ax.set_title('MSE vs f_s — reconstruction error collapses exactly at f_s = 2·f_m', fontsize=11)
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
savefig("ch01_nyquist_mse")

# ── Phase-offset ripple demo ───────────────────────────────────
# Why does MSE oscillate as f_s increases above 2·f_m?
#
# For each f_s the sample grid n/f_s hits a DIFFERENT PHASE of the cosine.
# When samples land near peaks/troughs they carry maximum information.
# When they land near zero-crossings they carry almost none.
# As f_s sweeps continuously this phase relationship cycles → periodic MSE ripple.
#
# We show 8 evenly-spaced f_s values in [6, 14] Hz, all above Nyquist (2·3=6 Hz).
# Left column: where samples land on cos(2π·3·t).
# Right column: MSE value for that f_s, with the ripple curve in background.
# ──────────────────────────────────────────────────────────────

demo_rates = np.linspace(6.2, 14.0, 8)   # 8 f_s values, all above Nyquist
n_demo     = len(demo_rates)

# Precompute MSE for the ripple background curve (reuse sweep_rates / errors from above)
# Only the above-Nyquist region is relevant here
above_nyq_mask = sweep_rates >= 2 * f_m_sec2

fig, axes = plt.subplots(n_demo, 2, figsize=(14, n_demo * 2.0))
fig.suptitle(
    '§1.4 — Why MSE Oscillates Above Nyquist: Phase Offset Between Sampler and Signal\n'
    'Left: where samples land on cos(2π·3·t)  |  Right: that f_s on the MSE ripple curve',
    fontsize=12)

for row, fs_demo in enumerate(demo_rates):
    # ── Left panel: sample positions on the cosine ──
    ax_wave = axes[row, 0]
    t_wave  = np.linspace(0, 1.0, 3000)
    ax_wave.plot(t_wave, np.cos(2 * np.pi * f_m_sec2 * t_wave),
                 color=COLORS['continuous'], lw=1.5, alpha=0.7)
    ax_wave.axhline(0, color='gray', lw=0.4)

    # Sample the long window, then display only the first 1 second
    t_s_long_demo = np.arange(0, T_LONG, 1.0 / fs_demo)
    s_s_long_demo = np.cos(2 * np.pi * f_m_sec2 * t_s_long_demo)
    t_s_show = t_s_long_demo[t_s_long_demo <= 1.0]
    s_s_show = s_s_long_demo[:len(t_s_show)]

    ax_wave.scatter(t_s_show, s_s_show, color=COLORS['samples'], s=55, zorder=5)
    ax_wave.vlines(t_s_show, 0, s_s_show, color=COLORS['samples'], lw=1.2, alpha=0.6)
    ax_wave.set_ylim(-1.5, 1.8)
    ax_wave.set_yticks([-1, 0, 1])
    ax_wave.set_ylabel('Amp', fontsize=8)
    ax_wave.tick_params(labelsize=8)

    # Compute MSE for this f_s
    recon_demo = np.zeros_like(t_eval)
    for tn, sn in zip(t_s_long_demo, s_s_long_demo):
        recon_demo += sn * np.sinc(fs_demo * (t_eval - tn))
    mse_demo = float(np.mean((true_eval - recon_demo) ** 2))

    # Color the row by MSE: green = low error, red = high error
    mse_max = errors[above_nyq_mask].max() + 1e-10
    mse_norm = min(mse_demo / mse_max, 1.0)
    row_color = plt.cm.RdYlGn(1.0 - mse_norm)  # green=low, red=high

    ax_wave.set_facecolor((*row_color[:3], 0.12))
    ax_wave.set_title(f'f_s = {fs_demo:.1f} Hz  — MSE = {mse_demo:.4f}',
                      fontsize=9, loc='left', color='black')
    if row == n_demo - 1:
        ax_wave.set_xlabel('Time (s)', fontsize=8)
    else:
        ax_wave.set_xticklabels([])

    # ── Right panel: MSE ripple curve with this f_s marked ──
    ax_mse = axes[row, 1]
    ax_mse.semilogy(sweep_rates[above_nyq_mask],
                    errors[above_nyq_mask] + 1e-10,
                    color='#90A4AE', lw=1.2)
    ax_mse.axvline(fs_demo, color=row_color, lw=2.0, linestyle='--')
    ax_mse.scatter([fs_demo], [mse_demo + 1e-10],
                   color=row_color, s=80, zorder=5)
    ax_mse.set_xlim(sweep_rates[above_nyq_mask][0], sweep_rates[-1])
    ax_mse.tick_params(labelsize=8)
    ax_mse.set_ylabel('MSE', fontsize=8)
    ax_mse.grid(True, alpha=0.2)
    if row == 0:
        ax_mse.set_title('MSE ripple (above Nyquist)', fontsize=9)
    if row == n_demo - 1:
        ax_mse.set_xlabel('f_s (Hz)', fontsize=8)
    else:
        ax_mse.set_xticklabels([])

plt.tight_layout()
savefig("ch01_phase_ripple")
print("§1.4 phase-offset ripple demo saved.")

# Figure 2: reconstruction at exactly the Nyquist rate — illustrates "sufficient"
fs_nyquist = 2.0 * f_m_sec2
t_s_long   = np.arange(0, T_LONG, 1.0 / fs_nyquist)
s_s_long   = np.cos(2 * np.pi * f_m_sec2 * t_s_long)
recon_ny   = np.zeros_like(t_ref)
for tn, sn in zip(t_s_long, s_s_long):
    recon_ny += sn * np.sinc(fs_nyquist * (t_ref - tn))

# display-only samples on t_ref window
t_s_display = t_s_long[(t_s_long >= 0) & (t_s_long <= 1)]
s_s_display = np.cos(2 * np.pi * f_m_sec2 * t_s_display)

fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(t_ref, true_signal, color=COLORS['continuous'], lw=1.5, label='True signal')
ax.plot(t_ref, recon_ny, color=COLORS['correct'], lw=1.5, linestyle='--',
        label='Sinc reconstruction at exactly f_s = 2·f_m')
ax.scatter(t_s_display, s_s_display, color=COLORS['samples'], zorder=5, s=70,
           label=f'Samples (f_s = {fs_nyquist} Hz = 2·f_m — exactly Nyquist)')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Amplitude')
ax.set_title('§1.3 Reconstruction at exactly the Nyquist rate — theoretically perfect\n'
             'But: any phase offset breaks this. Real systems use f_s ≫ 2·f_m (oversampling)',
             fontsize=11)
ax.legend(fontsize=9)
ax.axhline(0, color='gray', lw=0.5)
ax.grid(True, alpha=0.3)
plt.tight_layout()
savefig("ch01_nyquist_reconstruction")


# ══════════════════════════════════════════════════════════════
# SECTION 3 — 1D Aliasing: Frequency Folding
# ══════════════════════════════════════════════════════════════
#
# When f_m > f_N, the discrete samples produced by a signal at f_signal
# are *identical* to the samples produced by a lower-frequency signal at:
#
#   f_alias = | f_m − round(f_m / f_s) · f_s |
#
# This is called "frequency folding" — the spectrum folds at f_N.
# Example: f_s=8 Hz, f_m=11 Hz, f_N=f_s/2=4 Hz → f_alias = |11 − 8| = 3 Hz
#
# The sensor cannot tell the difference between the 11 Hz signal and a 3 Hz signal.
# The 11 Hz component "pretends" to be 3 Hz in the discrete domain.
# ──────────────────────────────────────────────────────────────

fs_demo  = 8.0          # sampling rate
f_N = fs_demo / 2   # f_N = f_s/2 = 4 Hz (max representable frequency)

# Zoom to 1 second so every cycle of the signal is clearly visible.
# At f_s=8 Hz we get 8 sample dots in this window — enough to see the spacing.
T_SHOW = 1.0
t_long = np.linspace(0, T_SHOW, 2000)

# ── Three examples ──────────────────────────────────────────
# Case 1: f_true = 5 Hz  — just ONE Hz above f_N = 4 Hz.
#   Each signal period is 0.2 s; sample spacing is 0.125 s.
#   The samples are slightly more than 2 per cycle → barely above Nyquist.
#   Alias: |5 − 8| = 3 Hz  (the reconstructor outputs a 3 Hz cosine)
#
# Case 2: f_true = 6.5 Hz — clearly above f_N.
#   Alias: |6.5 − 8| = 1.5 Hz
#
# Case 3: f_true = 2 Hz  — well below f_N = 4 Hz.
#   4 samples per period → faithful reconstruction, no alias.
# ──────────────────────────────────────────────────────────────
alias_examples = [
    (5.0,   3.0,  "f_m=5 Hz  just above f_N=f_s/2=4 Hz → alias at |5−8|=3 Hz"),
    (6.5,   1.5,  "f_m=6.5 Hz > f_N=f_s/2=4 Hz         → alias at |8−6.5|=1.5 Hz"),
    (2.0,   2.0,  "f_m=2 Hz  < f_N=f_s/2=4 Hz           → reconstructed correctly"),
]


def sinc_reconstruct(t_out: np.ndarray, t_samples: np.ndarray,
                     sample_values: np.ndarray, fs: float) -> np.ndarray:
    """
    Ideal sinc (Whittaker–Shannon) reconstruction:
      x(t) = Σ_n  x[n] · sinc( fs · (t − n/fs) )
    np.sinc uses the normalised form sinc(x) = sin(πx)/(πx).
    When f_s ≥ 2·f_m (f_s ≥ f_Nyquist_rate) this recovers the original exactly.
    When f_s < 2·f_m (f_s < f_Nyquist_rate) it recovers the alias — not the original.
    """
    recon = np.zeros_like(t_out, dtype=float)
    for t_n, x_n in zip(t_samples, sample_values):
        recon += x_n * np.sinc(fs * (t_out - t_n))
    return recon


# Each example: two-panel figure
#   Top panel   — the true (input) signal + sample dots
#                 Annotated with: signal period, sample spacing, and whether
#                 we have enough samples per cycle.
#   Bottom panel — sinc reconstruction vs true signal vs alias curve
#                 This is the money shot: the reconstruction IS the alias.
for f_true, f_alias, description in alias_examples:

    true_wave = np.cos(2 * np.pi * f_true * t_long)
    t_s       = np.arange(0, T_SHOW, 1.0 / fs_demo)   # 8 samples in 1 second
    s_true    = np.cos(2 * np.pi * f_true * t_s)

    recon     = sinc_reconstruct(t_long, t_s, s_true, fs_demo)
    is_alias  = (f_true != f_alias)

    signal_period  = 1.0 / f_true          # seconds per cycle of the true signal
    sample_spacing = 1.0 / fs_demo         # seconds between samples
    samples_per_cycle = fs_demo / f_true   # how many samples land per cycle

    fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(13, 8), sharex=True)
    fig.suptitle(
        f'§1.4 Aliasing:  f_s = {fs_demo} Hz,  f_N = {f_N} Hz\n'
        f'{description}',
        fontsize=13
    )

    # ── TOP PANEL: show the continuous signal and where samples land ──────────
    ax_top.plot(t_long, true_wave, color=COLORS['continuous'], lw=2,
                label=f'True signal: cos(2π × {f_true} t)   [period = {signal_period:.3f} s]')

    # Draw vertical stems so sample positions are unmistakeable
    for ts, sv in zip(t_s, s_true):
        ax_top.plot([ts, ts], [0, sv], color=COLORS['samples'], lw=1.0, alpha=0.6)
    ax_top.scatter(t_s, s_true, color=COLORS['samples'], zorder=5, s=70,
                   label=f'Samples  (spacing = {sample_spacing:.3f} s = {samples_per_cycle:.1f} per cycle)')

    # ── Annotate: show one signal period and one sample gap side-by-side ──────
    # Place the annotation near t=0 where the wave starts at +1
    y_ann = 1.35
    # Signal period bracket
    ax_top.annotate('', xy=(signal_period, y_ann), xytext=(0, y_ann),
                    arrowprops=dict(arrowstyle='<->', color=COLORS['continuous'], lw=1.5))
    ax_top.text(signal_period / 2, y_ann + 0.07,
                f'T_signal = {signal_period:.3f} s\n(1 full cycle)',
                ha='center', va='bottom', fontsize=8, color=COLORS['continuous'])

    # Sample spacing bracket (show first gap: t=0 to t=sample_spacing)
    ax_top.annotate('', xy=(sample_spacing, y_ann - 0.45), xytext=(0, y_ann - 0.45),
                    arrowprops=dict(arrowstyle='<->', color=COLORS['samples'], lw=1.5))
    ax_top.text(sample_spacing / 2, y_ann - 0.35,
                f'Δt = {sample_spacing:.3f} s\n(sample gap)',
                ha='center', va='bottom', fontsize=8, color=COLORS['samples'])

    # Flag whether we meet Nyquist
    if is_alias:
        nyquist_text = (f'⚠  Only {samples_per_cycle:.1f} samples/cycle\n'
                        f'Need ≥ 2 per cycle (Nyquist)\n→ ALIASING')
        box_color = '#FFF3E0'
        text_color = COLORS['alias']
    else:
        nyquist_text = (f'✓  {samples_per_cycle:.1f} samples/cycle\n'
                        f'≥ 2 per cycle (Nyquist met)\n→ No aliasing')
        box_color = '#E8F5E9'
        text_color = COLORS['nyquist']

    ax_top.text(0.98, 0.05, nyquist_text,
                transform=ax_top.transAxes, fontsize=9,
                ha='right', va='bottom', color=text_color,
                bbox=dict(boxstyle='round', facecolor=box_color, edgecolor=text_color, alpha=0.9))

    ax_top.set_ylabel('Amplitude')
    ax_top.set_title('Step 1 — Capture: the continuous signal is sampled at discrete points',
                     fontsize=10)
    ax_top.legend(fontsize=9, loc='upper right')
    ax_top.axhline(0, color='gray', lw=0.5)
    ax_top.set_ylim(-1.5, 1.9)

    # ── BOTTOM PANEL: sinc reconstruction — the alias made visible ────────────
    ax_bot.plot(t_long, true_wave, color=COLORS['continuous'], lw=1.5, alpha=0.5,
                linestyle='-',
                label=f'True signal: {f_true} Hz  (what we put in)')

    if is_alias:
        alias_wave = np.cos(2 * np.pi * f_alias * t_long)
        ax_bot.plot(t_long, alias_wave, color=COLORS['alias'], lw=2,
                    linestyle='--',
                    label=f'Predicted alias: {f_alias} Hz  (expected output)')

    ax_bot.plot(t_long, recon, color=COLORS['correct'], lw=2.5,
                label='Sinc reconstruction  (actual output of the system)')
    ax_bot.scatter(t_s, s_true, color=COLORS['samples'], zorder=5, s=70, alpha=0.5)

    ax_bot.set_ylabel('Amplitude')
    ax_bot.set_xlabel('Time (seconds)')
    ax_bot.axhline(0, color='gray', lw=0.5)
    ax_bot.set_ylim(-1.5, 1.9)

    if is_alias:
        ax_bot.set_title(
            f'Step 2 — Reconstruct: output is {f_alias} Hz, NOT {f_true} Hz\n'
            f'The reconstruction (purple) traces the alias (orange dashes) — the true signal is gone',
            fontsize=10
        )
    else:
        ax_bot.set_title(
            f'Step 2 — Reconstruct: output is {f_true} Hz — matches the input exactly\n'
            f'(below Nyquist → no alias)',
            fontsize=10
        )

    ax_bot.legend(fontsize=9, loc='upper right')
    plt.tight_layout()
    savefig(f's3_aliasing_reconstruction_fm{int(f_true*10):03d}')
    print(f"  f_true={f_true} Hz  →  reconstructed as {f_alias} Hz")

print()
print("Key insight: the reconstructor has NO CHOICE — the samples carry no information")
print("about frequencies above f_N.  The high frequency is not distorted; it is replaced.\n")


# ══════════════════════════════════════════════════════════════
# SECTION 4 — Phase Offset: Why Sampling Exactly at Nyquist is Fragile
# ══════════════════════════════════════════════════════════════
#
# The Nyquist theorem says:  f_s = 2·f_m  (= f_Nyquist_rate) is *sufficient* for perfect
# reconstruction.  But this is only true if the sample grid happens to align
# with the signal's peaks and troughs.
#
# In practice, the signal and the sampler have independent clocks.
# A phase offset φ between the signal and the sample grid changes what values
# are captured — even at exactly the Nyquist rate.
#
# Extreme case: sample a cosine at exactly f_s = 2·f:
#   φ = 0   → samples land at peak and trough → amplitude correctly measured
#   φ = π/2 → samples land at every zero crossing → all samples = 0
#               the reconstructor outputs a flat line (amplitude = 0!)
#   φ = π/4 → samples land between peak and zero → amplitude underestimated
#
# This is why the Nyquist theorem's "exactly f_Nyquist_rate" is a mathematical ideal.
# Real systems use f_s > 2·f_m  (oversampling), not f_s = 2·f_m.
# ──────────────────────────────────────────────────────────────

f_phase  = 4.0        # Hz — the signal we are sampling
fs_exact = 2 * f_phase  # exactly at Nyquist = 8 Hz
t_ref    = np.linspace(0, 1, 3000)

# Sweep phase offsets: 0, π/4, π/2, 3π/4
phase_offsets = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]

fig, axes = plt.subplots(len(phase_offsets), 1, figsize=(13, 11), sharex=True)
fig.suptitle(
    f'§1.6 Phase Offset: Why Exactly-Nyquist Sampling Breaks\n'
    f'Signal: cos(2π × {f_phase} t + φ),   f_s = {fs_exact} Hz = 2 × f_m\n'
    'Same sampling rate — different phase offset → wildly different reconstruction',
    fontsize=12
)

for ax, phi in zip(axes, phase_offsets):
    # True signal with this phase offset
    true_sig = np.cos(2 * np.pi * f_phase * t_ref + phi)

    # Sample grid: independent of signal phase (sampler has its own clock at t=0,1/fs,2/fs,...)
    t_s   = np.arange(0, 1, 1.0 / fs_exact)
    # The samples come from the true signal at these moments
    s_s   = np.cos(2 * np.pi * f_phase * t_s + phi)

    # Sinc reconstruction from these samples
    recon = np.zeros_like(t_ref, dtype=float)
    for t_n, s_n in zip(t_s, s_s):
        recon += s_n * np.sinc(fs_exact * (t_ref - t_n))

    # Measure how well the reconstruction matches
    amplitude_error = np.max(np.abs(recon)) / np.max(np.abs(true_sig))

    ax.plot(t_ref, true_sig, color=COLORS['continuous'], lw=1.5, alpha=0.7,
            label=f'True signal (φ = {phi:.2f} rad = {np.degrees(phi):.0f}°)')
    ax.plot(t_ref, recon, color=COLORS['correct'], lw=2.5,
            label=f'Sinc reconstruction   (captured amplitude = {amplitude_error:.2f}×)')
    ax.scatter(t_s, s_s, color=COLORS['samples'], zorder=5, s=70,
               label='Sample points')

    # Annotate the worst case
    if np.isclose(phi, np.pi / 2, atol=0.01):
        ax.text(0.5, 0.6, 'All samples = 0 !\nReconstruction is flat line',
                transform=ax.transAxes, fontsize=10, color=COLORS['alias'],
                ha='center',
                bbox=dict(boxstyle='round', facecolor='#FFF3E0', edgecolor=COLORS['alias']))

    ax.set_ylim(-1.5, 1.8)
    ax.axhline(0, color='gray', lw=0.5)
    ax.legend(loc='upper right', fontsize=9)
    ax.set_ylabel('Amplitude')

axes[-1].set_xlabel('Time (seconds)')
plt.tight_layout()
savefig("ch01_phase_offset")

print("Phase offset demo (f_s = f_Nyquist_rate = 2·f_m exactly):")
for phi in phase_offsets:
    t_s = np.arange(0, 1, 1.0 / fs_exact)
    s_s = np.cos(2 * np.pi * f_phase * t_s + phi)
    recon = np.zeros_like(t_ref, dtype=float)
    for t_n, s_n in zip(t_s, s_s):
        recon += s_n * np.sinc(fs_exact * (t_ref - t_n))
    captured = np.max(np.abs(recon))
    print(f"  φ={np.degrees(phi):5.0f}° → captured amplitude = {captured:.3f}  "
          f"(true = 1.000)")

print()
print("Lesson: at exactly f_Nyquist_rate = 2·f_m, a π/2 phase offset loses the signal entirely.")
print("Real systems oversample (f_s >> 2·f_m (f_s >> f_Nyquist_rate)) to make this a non-issue.\n")


# ══════════════════════════════════════════════════════════════
# SECTION 5 — The Aliasing Formula and the Folding Diagram
# ══════════════════════════════════════════════════════════════
#
# WHY DO TWO FREQUENCIES PRODUCE IDENTICAL SAMPLES?  (derivation)
#
# Take two cosines:
#   x1(t) = cos(2π · f_m · t)
#   x2(t) = cos(2π · (f_m + k·f_s) · t)   for any integer k
#
# Sample both at t = n/f_s  (n = 0, 1, 2, ...):
#
#   x1[n] = cos(2π · f_m · n/f_s)
#
#   x2[n] = cos(2π · (f_m + k·f_s) · n/f_s)
#          = cos(2π · f_m · n/f_s  +  2π · k · n)
#                                      ↑
#                         k and n are integers → this is always
#                         an exact multiple of 2π → cos ignores it
#          = cos(2π · f_m · n/f_s)
#          = x1[n]   ← IDENTICAL for every n
#
# So every frequency f_m + k·f_s  (k = ±1, ±2, ...) is an ALIAS of f_m.
# They all produce the same discrete sequence.
# This is the mathematical proof that aliasing is irreversible:
# the samples carry no information about which member of the alias
# family they came from.
#
# FOLDING:
# We keep only positive frequencies in [0, f_N].
# Any f_m outside this range is mapped back using:
#   Step 1: f_mod = f_m % f_s          (periodicity with period f_s)
#   Step 2: if f_mod > f_N: f_alias = f_s - f_mod   (mirror at f_N)
#
# Example with f_s=8, f_N=4:
#   f_m=5  → f_mod=5 > f_N=4 → f_alias = 8-5 = 3 Hz
#   f_m=6.5→ f_mod=6.5 > 4  → f_alias = 8-6.5 = 1.5 Hz
#   f_m=11 → f_mod=3 ≤ 4    → f_alias = 3 Hz  (same family as f_m=5!)
#   f_m=2  → f_mod=2 ≤ 4    → f_alias = 2 Hz  (no folding needed)
# ──────────────────────────────────────────────────────────────

fs_fold  = 8.0
f_N      = fs_fold / 2.0
f_range  = np.linspace(0, 2 * fs_fold, 2000)

def apparent_frequency(f_true: np.ndarray, f_s: float) -> np.ndarray:
    """
    Map any true frequency to its alias in [0, f_s/2].
    Implements the two-step folding derived above:
      1. f_mod = f_true % f_s          (period = f_s)
      2. fold:  if f_mod > f_N, return f_s - f_mod
    """
    f_N    = f_s / 2.0
    f_mod  = f_true % f_s
    folded = np.where(f_mod <= f_N, f_mod, f_s - f_mod)
    return folded

f_apparent = apparent_frequency(f_range, fs_fold)

fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(f_range, f_apparent, color=COLORS['continuous'], lw=2,
        label='Apparent (aliased) frequency')
ax.axvline(f_N,    color=COLORS['nyquist'], lw=2, linestyle='--',
           label=f'f_N = f_s/2 = {f_N:.0f} Hz')
ax.axvline(fs_fold, color=COLORS['samples'], lw=2, linestyle=':',
           label=f'f_s = {fs_fold} Hz')
ax.axvline(2 * fs_fold, color=COLORS['samples'], lw=2, linestyle=':')

# Annotate the three Section 3 examples — same alias family
# f_m=5  → alias=3,  f_m=6.5 → alias=1.5,  f_m=11 → also alias=3 (same family as f_m=5!)
for f_ex, f_al, color, note in [
    (5.0,  3.0, COLORS['alias'],   'f_m=5\n→ alias=3'),
    (6.5,  1.5, '#FF5722',         'f_m=6.5\n→ alias=1.5'),
    (11.0, 3.0, '#9C27B0',         'f_m=11\n→ alias=3\n(same as f_m=5!)'),
]:
    ax.annotate(note,
                xy=(f_ex, f_al),
                xytext=(f_ex + 0.3, f_al + 1.2),
                arrowprops=dict(arrowstyle='->', color=color),
                fontsize=8, color=color)
    ax.scatter([f_ex], [f_al], color=color, zorder=5, s=80)

ax.set_xlabel('True signal frequency f_m (Hz)')
ax.set_ylabel('Alias frequency  f_alias (Hz)')
ax.set_title(
    f'§1.5 Folding Diagram  (f_s={fs_fold} Hz, f_N=f_s/2={f_N} Hz)\n'
    'Rule: f_alias = f_m % f_s, then mirror at f_N  →  spectrum bounces between 0 and f_N\n'
    'f_m=5 and f_m=11 both alias to 3 Hz — they are in the same alias family (differ by f_s)',
    fontsize=11)
ax.legend(fontsize=9)
ax.set_xlim(0, 2 * fs_fold)
ax.set_ylim(-0.3, f_N + 0.5)
ax.grid(True, alpha=0.3)
plt.tight_layout()
savefig("ch01_folding_diagram")


# ══════════════════════════════════════════════════════════════
# SECTION 6 — Extending to 2D: Nyquist Now Applies Per Axis
# ══════════════════════════════════════════════════════════════
#
# An image is a 2D function  I(x, y).
# Sampling turns it into a grid  I[m, n]  with spacing Δx × Δy pixels.
# The pixel pitch is the 2D sampling interval.
#
# Nyquist in 2D:
#   - Along x (columns): f_s,x = 1/Δx → f_N,x = 1/(2Δx)
#   - Along y (rows):    f_s,y = 1/Δy → f_N,y = 1/(2Δy)
#
# A 2D sinusoidal pattern has a frequency vector (u, v) in cycles/pixel.
# It aliases when  |u| > f_N,x  OR  |v| > f_N,y.
#
# Below we show vertical, horizontal, and diagonal stripe patterns
# sampled at different rates to build the intuition before the
# full aliasing demonstration.
# ──────────────────────────────────────────────────────────────

HIGH_RES = 600   # the "continuous" scene resolution
x_c = np.linspace(0, 1, HIGH_RES)
y_c = np.linspace(0, 1, HIGH_RES)
XX_c, YY_c = np.meshgrid(x_c, y_c)

# A 2D pattern: stripes along x (horizontal spatial frequency u, no v component)
u_pattern = 15   # 15 cycles across the unit square
continuous_2d = np.sin(2 * np.pi * u_pattern * XX_c)

# Sample at three grid densities
sample_counts = [10, 20, 60]   # pixels across the same 1×1 unit area

fig, axes = plt.subplots(1, len(sample_counts) + 1, figsize=(15, 4))
fig.suptitle(f'§1.7 2D Sampling: {u_pattern}-cycle vertical stripe pattern\n'
             f'Nyquist limit: need ≥ {2 * u_pattern} samples across the domain',
             fontsize=12)

axes[0].imshow(continuous_2d, cmap='gray', extent=[0, 1, 0, 1])
axes[0].set_title(f'Continuous scene\n({HIGH_RES}×{HIGH_RES} reference)')
axes[0].set_xlabel('x'); axes[0].set_ylabel('y')

for ax, N in zip(axes[1:], sample_counts):
    x_s  = np.linspace(0, 1, N)
    XX_s, YY_s = np.meshgrid(x_s, x_s)
    sampled_2d = np.sin(2 * np.pi * u_pattern * XX_s)

    nyquist_needed = 2 * u_pattern
    status = '✓ OK' if N >= nyquist_needed else f'✗ Aliases! (need ≥{nyquist_needed})'
    ax.imshow(sampled_2d, cmap='gray', extent=[0, 1, 0, 1], interpolation='nearest')
    ax.set_title(f'{N}×{N} samples\n{status}', fontsize=10)
    ax.set_xlabel('x')

plt.tight_layout()
savefig("ch01_2d_stripe")


# ══════════════════════════════════════════════════════════════
# SECTION 7 — 2D Aliasing: Stripe Patterns at Various Frequencies
# ══════════════════════════════════════════════════════════════
#
# Fix the sensor resolution (sampling rate) and vary the spatial frequency
# of the pattern.  Patterns below Nyquist are captured correctly.
# Patterns above Nyquist alias to lower (wrong) frequencies.
# ──────────────────────────────────────────────────────────────

SENSOR_N = 40    # 40×40 pixel sensor (samples)

x_s = np.linspace(0, 1, SENSOR_N)
XX_s, _ = np.meshgrid(x_s, x_s)

pattern_freqs = [4, 10, 18, 30, 38]   # cycles across the domain
nyquist_limit = SENSOR_N / 2          # = 20 cycles

fig, axes = plt.subplots(1, len(pattern_freqs), figsize=(16, 3))
fig.suptitle(f'§1.7 2D Aliasing: {SENSOR_N}×{SENSOR_N} sensor, '
             f'Nyquist limit = {nyquist_limit} cycles/image\n'
             'As spatial frequency increases past Nyquist, a phantom lower frequency appears',
             fontsize=12)

for ax, u in zip(axes, pattern_freqs):
    sampled = np.sin(2 * np.pi * u * XX_s)
    is_alias = u > nyquist_limit
    title_color = COLORS['alias'] if is_alias else COLORS['nyquist']
    alias_freq  = abs(u - round(u / SENSOR_N) * SENSOR_N) if is_alias else u
    title = (f'u={u} cycles\n'
             + (f'ALIASES → {alias_freq:.0f} cycles' if is_alias else '✓ No alias'))
    ax.imshow(sampled, cmap='gray', interpolation='nearest')
    ax.set_title(title, fontsize=9, color=title_color)
    ax.axis('off')

plt.tight_layout()
savefig("ch01_2d_stripe_sweep")

print(f"Sensor resolution: {SENSOR_N}×{SENSOR_N} pixels  →  Nyquist = {nyquist_limit} cycles")
print("Patterns at u=4,10 are below Nyquist → look correct.")
print("Patterns at u=18,30,38 are above Nyquist → aliased to wrong (lower) frequencies.\n")


# ══════════════════════════════════════════════════════════════
# SECTION 8 — 2D Aliasing Along a Diagonal
# ══════════════════════════════════════════════════════════════
#
# In 2D the spatial frequency is a vector (u, v).
# A diagonal stripe has energy at both u and v simultaneously.
# Aliasing can occur along x, y, or both, depending on the direction of the pattern.
#
# Key concept: the 2D Nyquist region is a square in frequency space:
#   −f_N ≤ u ≤ f_N  AND  −f_N ≤ v ≤ f_N
# Any (u,v) outside this square will alias.
# ──────────────────────────────────────────────────────────────

SENSOR_D = 50

x_d = np.linspace(0, 1, SENSOR_D)
XX_d, YY_d = np.meshgrid(x_d, x_d)

# u=v=8 → in the safe zone (Nyquist = 25)
# u=v=22 → both above Nyquist (will alias along both axes)
# u=8, v=22 → aliases only along v
diagonal_cases = [
    (8,   8,  'u=8, v=8\n(both ✓ below Nyquist=25)'),
    (22, 22,  'u=22, v=22\n(both ✗ above Nyquist)'),
    (8,  22,  'u=8 ✓, v=22 ✗\n(alias along v only)'),
]

fig, axes = plt.subplots(1, 3, figsize=(13, 4))
fig.suptitle(f'§1.7 2D Aliasing Along Diagonals\n'
             f'{SENSOR_D}×{SENSOR_D} sensor, Nyquist = {SENSOR_D//2} cycles\n'
             'The 2D Nyquist region is a square: both u and v must be within bounds',
             fontsize=12)

for ax, (u, v, title) in zip(axes, diagonal_cases):
    sampled = np.sin(2 * np.pi * (u * XX_d + v * YY_d))
    ax.imshow(sampled, cmap='gray', interpolation='nearest')
    ax.set_title(title, fontsize=10)
    ax.axis('off')

plt.tight_layout()
savefig("ch01_diagonal_aliasing")


# ══════════════════════════════════════════════════════════════
# SECTION 9 — The Nyquist Square in 2D Frequency Space
# ══════════════════════════════════════════════════════════════
#
# This is the conceptual map.
# Horizontal axis = spatial frequency u (cycles per pixel along x)
# Vertical axis   = spatial frequency v (cycles per pixel along y)
# The green square [−f_N, f_N] × [−f_N, f_N] is the "safe zone".
# Any frequency outside the square aliases — it folds back inside.
# ──────────────────────────────────────────────────────────────

f_N_2d = 0.5   # Nyquist in normalised cycles/pixel (max representable = 0.5 cyc/px)

fig, ax = plt.subplots(figsize=(7, 7))

# Draw the Nyquist square
square = plt.Rectangle((-f_N_2d, -f_N_2d), 2 * f_N_2d, 2 * f_N_2d,
                        linewidth=3, edgecolor=COLORS['nyquist'], facecolor='#E8F5E9',
                        label='Nyquist region (safe zone)', zorder=1)
ax.add_patch(square)

# Plot some example frequency vectors: safe, unsafe, diagonal
examples = [
    (0.15, 0.10, True,  'safe: (0.15, 0.10)'),
    (0.40, 0.08, True,  'safe: (0.40, 0.08)'),
    (0.70, 0.10, False, 'aliases! (0.70, 0.10)'),
    (0.35, 0.65, False, 'aliases! (0.35, 0.65)'),
    (0.60, 0.55, False, 'aliases! (0.60, 0.55)'),
]

for u, v, safe, label in examples:
    color = COLORS['nyquist'] if safe else COLORS['alias']
    ax.annotate('', xy=(u, v), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color=color, lw=2))
    ax.scatter([u], [v], color=color, zorder=5, s=80)
    ax.text(u + 0.02, v + 0.02, label, fontsize=8, color=color)

ax.axhline(0, color='gray', lw=0.5)
ax.axvline(0, color='gray', lw=0.5)
ax.set_xlim(-0.9, 0.9)
ax.set_ylim(-0.9, 0.9)
ax.set_xlabel('Spatial frequency u (cycles/pixel)', fontsize=11)
ax.set_ylabel('Spatial frequency v (cycles/pixel)', fontsize=11)
ax.set_title('§1.7 The 2D Nyquist Region\n'
             'Green square = representable frequencies; outside = alias territory',
             fontsize=12)
ax.legend(fontsize=10)
ax.set_aspect('equal')
plt.tight_layout()
savefig("ch01_nyquist_square")


# ══════════════════════════════════════════════════════════════
# SECTION 10 — Moiré Pattern: The Classic 2D Aliasing Artefact
# ══════════════════════════════════════════════════════════════
#
# A fine sinusoidal grid (spatial frequency above Nyquist) aliases into
# a low-frequency envelope — the moiré pattern.
# This is exactly what you see when photographing fabric, screen-door mesh,
# or fine-pitched PCB traces at insufficient resolution.
#
# Construction:
#   True pattern: sin(2π · f_high · x)   where f_high > f_N
#   After sampling at f_s: the samples are identical to sin(2π · f_alias · x)
#   f_alias = f_s − f_high   (the "beat" frequency)
#
# We simulate this by creating a high-frequency pattern on a dense grid
# (the "continuous" scene) and then showing what happens when a coarse
# sensor captures it.
# ──────────────────────────────────────════════════════════════

SCENE_SIZE   = 800    # continuous scene resolution
SENSOR_SIZE  = 80     # sensor pixel count (10× downsampled)
f_high_moire = 38     # spatial frequency above SENSOR_SIZE/2 = 40 Nyquist

x_scene = np.linspace(0, 1, SCENE_SIZE)
XX_scene, YY_scene = np.meshgrid(x_scene, x_scene)

# Fine grid pattern — the "real scene"
scene_pattern = np.sin(2 * np.pi * f_high_moire * XX_scene)

# Naive downsample (no anti-aliasing): take every SCENE_SIZE//SENSOR_SIZE pixel
step = SCENE_SIZE // SENSOR_SIZE
aliased_image = scene_pattern[::step, ::step]

# Proper downsample: blur first (simulate anti-aliasing filter), then subsample
from scipy.ndimage import gaussian_filter
sigma = step / (2 * np.pi)   # sigma chosen to cut off above Nyquist
blurred_scene   = gaussian_filter(scene_pattern, sigma=sigma)
antialiased_img = blurred_scene[::step, ::step]

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle(f'§1.8 Moiré Pattern from 2D Aliasing\n'
             f'Scene: {f_high_moire}-cycle pattern on {SCENE_SIZE}×{SCENE_SIZE} grid → '
             f'captured at {SENSOR_SIZE}×{SENSOR_SIZE} (Nyquist = {SENSOR_SIZE//2} cycles)',
             fontsize=12)

axes[0].imshow(scene_pattern[:200, :200], cmap='gray', interpolation='nearest')
axes[0].set_title(f'True scene (crop)\n{f_high_moire} cycles — fine stripes', fontsize=11)
axes[0].axis('off')

axes[1].imshow(aliased_image, cmap='gray', interpolation='nearest')
axes[1].set_title(f'Sensor capture (no AA)\n{SENSOR_SIZE}×{SENSOR_SIZE} px\n'
                  'Moiré: phantom low-frequency pattern appears!', fontsize=11)
axes[1].axis('off')

axes[2].imshow(antialiased_img, cmap='gray', interpolation='nearest')
axes[2].set_title(f'Sensor capture (with AA filter)\n{SENSOR_SIZE}×{SENSOR_SIZE} px\n'
                  'Moiré gone — high frequencies correctly blurred out', fontsize=11)
axes[2].axis('off')

plt.tight_layout()
savefig("ch01_moire")

print("Summary of §1.7:")
print(f"  Fine pattern at {f_high_moire} cycles > Nyquist ({SENSOR_SIZE//2} cycles)")
alias_freq_moire = abs(f_high_moire - SENSOR_SIZE)
print(f"  Without AA: aliases to {alias_freq_moire} cycles → visible moiré")
print("  With AA:    high frequencies removed before sampling → no phantom pattern\n")


# ══════════════════════════════════════════════════════════════
# SECTION 10 — Summary: The 1D → 2D Connection
# ══════════════════════════════════════════════════════════════

print("=" * 60)
print("SUMMARY: Sampling, Nyquist, and Aliasing")
print("=" * 60)
print()
print("1D:")
print("  • Sampling captures discrete moments of a continuous wave")
print("  • Nyquist: f_s ≥ 2·f_m  (f_s ≥ f_Nyquist_rate) to reconstruct without error")
print("  • Aliasing: frequencies above f_N=f_s/2 fold back to f_s − f_true")
print("  • Aliases are irreversible — you cannot separate them from real content")
print()
print("2D (images):")
print("  • Each axis has its own Nyquist limit: f_N = pixels / (2 · image_width)")
print("  • The safe zone is a SQUARE in 2D frequency space: |u| ≤ f_N AND |v| ≤ f_N")
print("  • Aliasing along x → false horizontal patterns (wrong column frequency)")
print("  • Aliasing along y → false vertical patterns")
print("  • Aliasing along both → moiré, diagonal phantom patterns")
print()
print("Prevention:")
print("  • Apply a low-pass (anti-aliasing) filter BEFORE downsampling")
print("  • Match sensor resolution to the highest spatial frequency in the scene")
print("  • In practice: use LANCZOS / Gaussian blur before any resize operation")
print()
