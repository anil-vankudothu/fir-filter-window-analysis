import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin, lfilter, freqz
import os

os.makedirs("results", exist_ok=True)

# Parameters
fs       = 1000        # Sampling frequency (Hz)
t        = np.arange(0, 1, 1/fs)
f_signal = 50          # Signal frequency (Hz)
fc       = 100         # cut off frequency
N        = 51          # Filter order

#  Generate signals
clean = np.sin(2 * np.pi * f_signal * t)

np.random.seed(42)
noise = 0.5 * np.random.randn(len(t))     # Gaussian white noise
noisy = clean + noise

def compute_snr(original, processed):      #  Metrics
    noise_residual = original - processed
    return 10 * np.log10(np.sum(original**2) / np.sum(noise_residual**2))

def compute_rmse(original, processed):
    return np.sqrt(np.mean((original - processed)**2))

snr_before = compute_snr(clean, noisy)

windows = {                               #  Window definitions
    "Rectangular": "boxcar",
    "Hamming":     "hamming",
    "Hanning":     "hann",
    "Blackman":    "blackman",
    "Kaiser":      ("kaiser", 14),
}

colors = {
    "Rectangular": "blue",
    "Hamming":     "orange",
    "Hanning":     "green",
    "Blackman":    "purple",
    "Kaiser":      "brown",
}

plt.figure(figsize=(10, 5))                      # Figure 1: Original vs Noisy 
plt.plot(t[:300], clean[:300], color='blue',   linewidth=2,   label="Original Signal (50 Hz)")
plt.plot(t[:300], noisy[:300], color='orange', alpha=0.6,     label="Noisy Signal")
plt.title("Figure 1: Original vs Noisy Signal (Zoomed to 300 samples)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True, linestyle='--')
plt.tight_layout()
plt.savefig("results/figure1_noisy_signal.png", dpi=150)
plt.close()

results          = {}               #  Apply filters
filtered_signals = {}
delay = N // 2                      #  Group delay of a linear-phase FIR of order N is N/2 samples.
               
for name, w in windows.items():
    h        = firwin(N, fc / (fs / 2), window=w)
    filtered = lfilter(h, 1.0, noisy)

    filtered_aligned = np.roll(filtered, -delay)

    filtered_signals[name] = filtered_aligned

    snr_after   = compute_snr(clean, filtered_aligned)
    improvement = snr_after - snr_before
    rmse        = compute_rmse(clean, filtered_aligned)

    results[name] = (snr_after, improvement, rmse)

plt.figure(figsize=(14, 10))     # Figure 2: Subplot per window 
for i, (name, sig) in enumerate(filtered_signals.items()):
    plt.subplot(3, 2, i + 1)
    plt.plot(t[:300], clean[:300],  color='black',      linewidth=2,  label="Original")
    plt.plot(t[:300], noisy[:300],  color='grey',       alpha=0.3,    label="Noisy")
    plt.plot(t[:300], sig[:300],    color=colors[name], linewidth=1.8, label=name)
    plt.title(f"{name} Window Output")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend(fontsize=8)
    plt.grid(True, linestyle='--')
plt.tight_layout()
plt.savefig("results/figure2_filtered_outputs.png", dpi=150)
plt.close()

plt.figure(figsize=(14, 10))                      # Figure 3: Error signals
for i, (name, sig) in enumerate(filtered_signals.items()):
    plt.subplot(3, 2, i + 1)
    error = clean - sig
    plt.plot(t[:300], error[:300], color=colors[name])
    plt.title(f"{name} Error Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Error")
    plt.grid(True, linestyle='--')
plt.tight_layout()
plt.savefig("results/figure3_error_signals.png", dpi=150)
plt.close()

plt.figure(figsize=(12, 6))                 #Figure 4: Frequency response
for name, w in windows.items():
    h = firwin(N, fc / (fs / 2), window=w)
    freq, H = freqz(h, worN=2048, fs=fs)
    plt.plot(freq, 20 * np.log10(np.abs(H) + 1e-12),
             color=colors[name], linewidth=1.8, label=name)
plt.axvline(fc,          color='red',  linestyle='--', linewidth=1.2, label=f'Cutoff = {fc} Hz')
plt.axvline(f_signal,    color='gray', linestyle=':',  linewidth=1.2, label=f'Signal = {f_signal} Hz')
plt.title("Figure 4: Magnitude Frequency Response of FIR Filters")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dB)")
plt.ylim(-100, 5)
plt.xlim(0, 400)
plt.legend()
plt.grid(True, linestyle='--')
plt.tight_layout()
plt.savefig("results/figure4_frequency_response.png", dpi=150)
plt.close()


print("\n" + "=" * 60)
print("  RESULTS — Window-Based FIR Filter Performance")
print("=" * 60)
print(f"  SNR Before Filtering : {snr_before:.2f} dB\n")
print(f"  {'Window':<14} {'SNR After':>10} {'Improvement':>13} {'RMSE':>10}")
print("  " + "-" * 50)
for name, (snr_a, imp, rmse) in results.items():
    print(f"  {name:<14} {snr_a:>10.2f} {imp:>13.2f} {rmse:>10.4f}")
print("=" * 60)