'''
scipy.signal  —  Signal Processing
====================================

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART A — CONVOLUTION & CORRELATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 1. convolve / fftconvolve / oaconvolve
 2. correlate / correlation_lags
 3. convolve2d / correlate2d
 4. choose_conv_method

PART B — FILTER APPLICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 5. lfilter / lfilter_zi            : causal IIR/FIR filtering
 6. filtfilt                        : zero-phase forward-backward filter
 7. sosfilt / sosfilt_zi / sosfiltfilt : SOS-form filtering (numerically stable)
 8. savgol_filter                   : Savitzky-Golay smoothing/differentiation
 9. medfilt / wiener / order_filter : nonlinear filters
10. hilbert / envelope              : analytic signal and amplitude envelope
11. decimate / resample / resample_poly / upfirdn : resampling

PART C — FIR FILTER DESIGN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
12. firwin                          : window method (lowpass / highpass / bandpass / bandstop)
13. firwin2                         : arbitrary frequency-response specification
14. firls / remez                   : optimal FIR (least-squares / Parks-McClellan)
15. kaiserord / kaiser_beta         : Kaiser window FIR sizing

PART D — IIR FILTER DESIGN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
16. butter / buttord                : Butterworth (maximally flat)
17. cheby1 / cheb1ord               : Chebyshev type I (equiripple passband)
18. cheby2 / cheb2ord               : Chebyshev type II (equiripple stopband)
19. ellip / ellipord                : Elliptic / Cauer (equiripple both bands)
20. bessel                          : Bessel/Thomson (maximally flat group delay)
21. iirdesign / iirfilter           : generic IIR design with prototype selection
22. iirnotch / iirpeak / iircomb    : targeted notch/peak/comb filters

PART E — FREQUENCY RESPONSE & FILTER REPRESENTATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
23. freqz / freqz_zpk / freqz_sos  : digital frequency response
24. freqs                           : analog frequency response
25. group_delay                     : phase delay per frequency
26. tf2zpk / tf2sos / zpk2sos / sos2tf / tf2ss and friends : representation conversion
27. residue / invres                : partial fraction expansion

PART F — WINDOW FUNCTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
28. get_window                      : look up by name
29. Key windows: boxcar, hann, hamming, blackman, blackmanharris,
                 kaiser, flattop, tukey, dpss, gaussian, nuttall

PART G — SPECTRAL ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
30. periodogram                     : power spectral density (no averaging)
31. welch                           : averaged PSD (Welch method)
32. csd / coherence                 : cross-spectral density and coherence
33. ShortTimeFFT                    : modern STFT/iSTFT (new class-based API)
34. stft / istft                    : legacy STFT
35. lombscargle                     : PSD for unevenly-sampled data
36. detrend                         : remove DC / linear trend

PART H — LTI SYSTEMS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
37. Continuous-time: TransferFunction, ZerosPolesGain, StateSpace,
                     lsim, impulse, step, bode, cont2discrete
38. Discrete-time:   dlti, dlsim, dimpulse, dstep, dbode

PART I — PEAK FINDING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
39. find_peaks / peak_prominences / peak_widths
40. argrelmin / argrelmax / argrelextrema

PART J — WAVEFORMS & CHIRP Z-TRANSFORM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
41. chirp / sawtooth / square / unit_impulse / gausspulse
42. czt / zoom_fft / CZT / ZoomFFT
'''

import numpy as np
import scipy.signal as sig
from scipy.signal import (
    # Convolution
    convolve, correlate, fftconvolve, oaconvolve,
    convolve2d, correlate2d, choose_conv_method, correlation_lags,
    # Filtering
    lfilter, lfilter_zi, filtfilt,
    sosfilt, sosfilt_zi, sosfiltfilt,
    savgol_filter, savgol_coeffs,
    medfilt, wiener,
    hilbert, envelope, decimate, resample, resample_poly, upfirdn, detrend,
    # FIR design
    firwin, firwin2, firls, remez, kaiserord, kaiser_beta, kaiser_atten, minimum_phase,
    # IIR design
    butter, buttord, cheby1, cheb1ord, cheby2, cheb2ord, ellip, ellipord,
    bessel, iirdesign, iirfilter, iirnotch, iirpeak, iircomb,
    # Frequency response
    freqz, freqz_zpk, freqz_sos, freqs, group_delay,
    # Representation conversions
    tf2zpk, tf2sos, tf2ss, zpk2tf, zpk2sos, zpk2ss, ss2tf, ss2zpk,
    sos2zpk, sos2tf, cont2discrete, bilinear,
    residue, invres, residuez, invresz,
    # Window functions
    get_window,
    # Spectral analysis
    periodogram, welch, csd, coherence, ShortTimeFFT,
    stft, istft, lombscargle, check_NOLA,
    # LTI systems
    TransferFunction, ZerosPolesGain, StateSpace,
    lsim, impulse, step, bode, freqresp,
    dlti, dlsim, dimpulse, dstep, dbode,
    # Peak finding
    find_peaks, peak_prominences, peak_widths,
    argrelmin, argrelmax, argrelextrema, find_peaks_cwt,
    # Waveforms
    chirp, sawtooth, square, unit_impulse, gausspulse,
    # Chirp Z-transform
    czt, zoom_fft, CZT, ZoomFFT,
)
from scipy.signal import windows as win

rng = np.random.default_rng(0)

# ── Common test signals ──────────────────────────────────────────────────────────────────────────
fs  = 1000.0                                # sample rate Hz
t   = np.arange(0, 1.0, 1/fs)              # 1-second timeline (1000 samples)
# Multi-tone: 50 Hz + 150 Hz (to filter) + 300 Hz
x_multi  = (np.sin(2*np.pi*50*t) +
             0.5*np.sin(2*np.pi*150*t) +
             0.3*np.sin(2*np.pi*300*t))
x_noisy  = np.sin(2*np.pi*50*t) + rng.normal(0, 0.3, len(t))   # 50 Hz + Gaussian noise


# =========================================================================================
#═════════════════════════════  PART A — CONVOLUTION & CORRELATION  ══════════════════════════════#
# =========================================================================================

##------------##
## convolve() ##
##------------##
'''
convolve(in1, in2, mode='full', method='auto') — convolve two N-D arrays.

mode:
  'full'  : output length = len(in1) + len(in2) - 1. Full linear convolution.
  'same'  : output length = max(len(in1), len(in2)). Centred.
  'valid' : output length = max - min + 1. Only the parts without zero-padding.

method:
  'auto'   : choose between 'direct' and 'fft' based on size.
  'direct' : O(n*m) explicit summation. Best for short signals or sparse kernels.
  'fft'    : O(n log n) via FFT. Best for long signals.

N-D: works on 2-D, 3-D arrays. For 2-D images prefer convolve2d.
'''

# 1-D: convolve a signal with a box (moving average) kernel
x_box = np.array([1., 2., 3., 4., 5.])
kernel_box = np.ones(3) / 3   # 3-point moving average

conv_full  = convolve(x_box, kernel_box, mode='full')   # length 7
conv_same  = convolve(x_box, kernel_box, mode='same')   # length 5 (same as input)
conv_valid = convolve(x_box, kernel_box, mode='valid')  # length 3 (no boundary effects)

print(conv_full.round(4))
# [0.3333 1.     2.     3.     4.     3.     1.6667]
print(conv_same.round(4))
# [1.     2.     3.     4.     3.    ]  ← centred on input
print(conv_valid.round(4))
# [2.  3.  4.]  ← interior only; no edge artefacts

# Convolution theorem: convolve <-> multiply in frequency domain
# Direct vs FFT method give the same result
c_direct = convolve(x_noisy, np.ones(11)/11, method='direct', mode='same')
c_fft    = convolve(x_noisy, np.ones(11)/11, method='fft',    mode='same')
print(np.allclose(c_direct, c_fft, atol=1e-10))  # True

# 2-D: convolve a "image" patch with a Gaussian kernel
img = rng.normal(0, 1, (10, 10))
kern_2d = np.outer(np.array([1,2,1]), np.array([1,2,1])) / 16   # 3x3 Gaussian approx
conv_2d = convolve(img, kern_2d, mode='same')
print(conv_2d.shape)  # (10, 10)

##---------------##
## fftconvolve() ##
##---------------##
'''
fftconvolve(in1, in2, mode='full', axes=None)

Always uses the FFT method — O(nlogn). Identical interface to convolve().

axes : convolve along specific axes of an N-D array. Other axes are treated
       independently (like batched 1-D convolutions).

Use when: signals are long (n > ~500) or you want guaranteed FFT method.
'''

# Long signal: FFT convolution is much faster
x_long = rng.normal(0, 1, 10000)
h_long = np.hanning(501)   # 501-tap Hann window kernel

y_fft    = fftconvolve(x_long, h_long, mode='same')
y_direct = convolve(x_long, h_long, mode='same', method='direct')
print(np.allclose(y_fft, y_direct, atol=1e-8))  # True

# Batched 2-D: convolve each row of a matrix with a 1-D filter along axis=1
matrix = rng.normal(0, 1, (5, 1000))
filt   = np.array([0.25, 0.5, 0.25])
result_batch = fftconvolve(matrix, filt[np.newaxis, :], mode='same', axes=1)
print(result_batch.shape)  # (5, 1000)

##--------------##
## oaconvolve() ##
##--------------##
'''
oaconvolve(in1, in2, mode='full', axes=None)

Overlap-add convolution: splits the input into blocks, convolves each with the
filter using FFT, and accumulates. Efficient when the filter is much shorter
than the signal (h << x).

Use when: streaming/block processing; or len(h) << len(x).
fftconvolve is usually slightly faster for equal lengths.
'''

y_oa = oaconvolve(x_long, h_long, mode='same')
print(np.allclose(y_oa, y_fft, atol=1e-8))  # True

##-------------##
## correlate() ##
##-------------##
'''
correlate(in1, in2, mode='full', method='auto')

Cross-correlation:  (in1 ⋆ in2)[k] = sum_n in1[n+k] * in2[n]

Unlike convolution, cross-correlation is NOT commutative: correlate(x,y) != correlate(y,x).
Autocorrelation: correlate(x, x).
Mode and method arguments identical to convolve().

Use for:
  - Time-delay estimation (peak of cross-correlation = lag).
  - Signal detection (matched filter).
  - Measuring signal similarity.
'''

# Autocorrelation of a sinusoid: should peak at 0 lag and repeat at period
x_sin = np.sin(2*np.pi*50*t)
acorr = correlate(x_sin, x_sin, mode='full')
lags  = correlation_lags(len(x_sin), len(x_sin), mode='full')
peak_lag = lags[np.argmax(acorr)]
print(peak_lag)   # 0 (zero lag = maximum self-similarity)

# Cross-correlation: detect a delayed version of a signal
delay_samples = 50
x_ref     = np.sin(2*np.pi*10*t)
x_delayed = np.roll(x_ref, delay_samples)   # shift by 50 samples
xcorr     = correlate(x_delayed, x_ref, mode='full')
lags_xc   = correlation_lags(len(x_delayed), len(x_ref), mode='full')
print(lags_xc[np.argmax(xcorr)])   # -50 ← detected delay

# Matched filter: detect a known pattern in noise
pattern = np.array([1., -1., 1., -1., 1.])   # ±1 template
noisy_signal = np.concatenate([rng.normal(0,1,50), pattern, rng.normal(0,1,50)])
mf_output = correlate(noisy_signal, pattern, mode='valid')
detected_pos = np.argmax(mf_output)
print(detected_pos)   # 50 — where the pattern is embedded

# correlation_lags: generate the lag array for a known pair of lengths
lags_arr = correlation_lags(100, 80, mode='full')
print(lags_arr[0], lags_arr[-1])  # -79  99

##--------------##
## convolve2d() ##
##--------------##
'''
convolve2d(in1, in2, mode='full', boundary='fill', fillvalue=0)

2-D convolution with boundary condition control.

boundary:
  'fill'  : pad with fillvalue (default 0). Same as convolve().
  'wrap'  : periodic / toroidal boundary. For circular convolution.
  'symm'  : mirror-symmetric padding. Avoids edge artefacts in image processing.

Compared to convolve(in1, in2):
  - convolve2d is faster for 2-D arrays.
  - Supports 'symm' and 'wrap' boundaries.
  - Output is always 2-D.
'''

img_gray = rng.integers(0, 256, (64, 64)).astype(float)

# Sobel edge detection: horizontal gradient
sobel_x = np.array([[-1., 0., 1.],
                     [-2., 0., 2.],
                     [-1., 0., 1.]])
edges_x = convolve2d(img_gray, sobel_x, mode='same', boundary='symm')
print(edges_x.shape)  # (64, 64)

# Gaussian blur
def gaussian_kernel(size, sigma):
    k = np.arange(size) - size // 2
    g = np.exp(-k**2 / (2*sigma**2))
    g /= g.sum()
    return np.outer(g, g)

gauss = gaussian_kernel(7, 1.5)
blurred = convolve2d(img_gray, gauss, mode='same', boundary='symm')
print(blurred.shape)  # (64, 64)

# Wrap (circular) convolution for periodic data
y_wrap = convolve2d(img_gray, sobel_x, mode='same', boundary='wrap')

##----------------------##
## choose_conv_method() ##
##----------------------##
'''
choose_conv_method(in1, in2, mode='full', measure=False)

Returns 'direct' or 'fft' — whichever is predicted to be faster.
measure=True : actually time both methods and return the faster one.

Useful for understanding the crossover point, or building adaptive pipelines.
'''

method_choice = choose_conv_method(x_noisy, np.ones(51), mode='same')
print(method_choice)   # 'direct' or 'fft' depending on lengths

method_timed, times = choose_conv_method(x_long, h_long, mode='same', measure=True)
print(method_timed)    # 'fft' for long signals


# =========================================================================================
#══════════════════════════════  PART B — FILTER APPLICATION  ════════════════════════════════════#
# =========================================================================================

##----------------------##
## lfilter / lfilter_zi ##
##----------------------##
'''
lfilter(b, a, x, axis=-1, zi=None)

Filter data with an IIR or FIR digital filter in CAUSAL (one-pass) direction.

b, a : numerator and denominator polynomial coefficients (BA representation).
       For FIR: a = [1.0].
       For IIR: both b and a have multiple terms.
x    : input signal array. Filtered along axis=-1 by default.
zi   : initial filter conditions (state). If provided, also returns zf (final state).

Returns:
  y : filtered output (same shape as x).
  zf: final filter state (only if zi is provided).

CAUTION: lfilter introduces group delay (phase shift). For zero-phase filtering use filtfilt.
CAUTION: BA representation can be numerically unstable for high-order IIR filters.
         Use SOS format (sosfilt) for anything above ~4th-order IIR.

lfilter_zi(b, a) : compute the initial state zi for step-response steady-state.
                   Use when filtering segments of a long signal to avoid edge transients.
'''

# Design a simple 4th-order Butterworth lowpass (BA form)
b_lp, a_lp = butter(4, 100.0, btype='low', fs=fs)

# Basic filtering
y_lfilter = lfilter(b_lp, a_lp, x_multi)
print(y_lfilter.shape)  # (1000,)

# Note: energy at 50 Hz is preserved; 150 Hz and 300 Hz are attenuated
from scipy.fft import rfft, rfftfreq
def peak_amp(y, freq, fs=1000):
    '''Return amplitude at a given frequency (rough estimate via DFT peak).'''
    Y = np.abs(rfft(y)) * 2 / len(y)
    freqs = rfftfreq(len(y), 1/fs)
    idx = np.argmin(np.abs(freqs - freq))
    return Y[idx]

print(f"50 Hz (passband):  {peak_amp(y_lfilter, 50):.3f}")   # 0.994 (~1.0)
print(f"150 Hz (stopband): {peak_amp(y_lfilter, 150):.3f}")  # 0.082 <<0.5

# Streaming: initialise state for step-response steady-state (no initial transient)
zi_lp = lfilter_zi(b_lp, a_lp) * x_multi[0]   # scale zi by first sample value
y_zi, zf = lfilter(b_lp, a_lp, x_multi, zi=zi_lp)
# Segment processing: continue filtering the next chunk from where we left off
x_chunk2 = np.sin(2*np.pi*50*t + 0.5)   # second segment
y_chunk2, _ = lfilter(b_lp, a_lp, x_chunk2, zi=zf)

# lfiltic: compute initial conditions from known past inputs and outputs
from scipy.signal import lfiltic
zi_from_ic = lfiltic(b_lp, a_lp, y=[y_lfilter[-1]], x=[x_multi[-1]])
print(zi_from_ic.shape)  # (max(len(b),len(a))-1,)

##------------##
## filtfilt() ##
##------------##
'''
filtfilt(b, a, x, axis=-1, padtype='odd', padlen=None, method='pad', irlen=None)

Apply a digital filter FORWARD then BACKWARD to produce zero-phase output.
Phase distortion is eliminated; effective order is doubled (4th-order -> 8th-order rolloff).

padtype : padding at edges before filtering:
  'odd'   : odd extension (default, best for signals that don't start/end at zero).
  'even'  : even extension.
  'constant': extend with the edge value.
  None    : no padding.
padlen  : number of samples to pad (default ~3 * max(len(b), len(a))).
irlen   : approximate length of IR (for very long IIR impulse responses).

Use filtfilt when phase matters: ECG peak detection, envelope following, etc.
Use lfilter when causality is required (real-time processing, recursive feedback).
'''

y_filtfilt = filtfilt(b_lp, a_lp, x_multi)
print(y_filtfilt.shape)   # (1000,)

# Zero-phase: compare phase shift of lfilter vs filtfilt
# filtfilt peaks align with input; lfilter peaks are delayed
print(f"lfilter  50 Hz amp: {peak_amp(y_lfilter, 50):.3f}")    # ~1.0
print(f"filtfilt 50 Hz amp: {peak_amp(y_filtfilt, 50):.3f}")   # ~1.0

# Quantify phase delay of lfilter at 50 Hz
w, gd = group_delay((b_lp, a_lp), fs=fs)
idx_50 = np.argmin(np.abs(w - 50))
print(f"lfilter group delay at 50 Hz: {gd[idx_50]:.1f} samples") # 4.7 samples
# filtfilt has zero group delay by construction

# Edge handling: padtype='odd' is robust for signals with non-zero start/end
y_odd   = filtfilt(b_lp, a_lp, x_multi, padtype='odd')
y_const = filtfilt(b_lp, a_lp, x_multi, padtype='constant')
print(np.abs(y_odd[:10] - y_const[:10]).max().round(4))  # 0.3309 differs at edges

##------------------------------------##
## sosfilt / sosfilt_zi / sosfiltfilt ##
##------------------------------------##
'''
sosfilt(sos, x, axis=-1, zi=None)

Filter using Second-Order Sections (SOS) representation.
Numerically more stable than BA representation for high-order IIR filters.

SOS format: (N_sections, 6) array, each row = [b0 b1 b2 a0 a1 a2] for one biquad.
Cascades second-order sections instead of implementing the filter as one high-order polynomial.

sosfilt_zi(sos)    : initial conditions for step steady-state (analogous to lfilter_zi).
sosfiltfilt(sos,x) : forward-backward zero-phase filtering in SOS form.

BEST PRACTICE: always design IIR filters directly in SOS form (output='sos')
and filter with sosfilt / sosfiltfilt. Avoid BA form for order > 4.
'''

# Design in SOS form directly (most stable)
sos_lp = butter(8, 100.0, btype='low', fs=fs, output='sos')  # 8th-order SOS
print(sos_lp.shape)   # (4, 6) — 4 second-order sections

# Apply causal SOS filter
y_sos = sosfilt(sos_lp, x_multi)
print(f"150 Hz SOS attenuated: {peak_amp(y_sos, 150):.4f}") # 0.0125 very small

# Zero-phase SOS (preferred for offline processing)
y_sosfiltfilt = sosfiltfilt(sos_lp, x_multi)
print(f"50 Hz preserved: {peak_amp(y_sosfiltfilt, 50):.3f}")  # ~1.0

# Initial conditions for segment processing
zi_sos = sosfilt_zi(sos_lp) * x_multi[0]
y_sos_zi, zf_sos = sosfilt(sos_lp, x_multi, zi=zi_sos)

# High-order filter: show SOS is stable while BA is not
sos_hi  = butter(20, 100.0, btype='low', fs=fs, output='sos')
b_hi, a_hi = butter(20, 100.0, btype='low', fs=fs)   # BA form — numerically bad

y_sos_hi   = sosfilt(sos_hi, x_multi)
y_ba_hi    = lfilter(b_hi, a_hi, x_multi)   # may be NaN/Inf for very high order
print(f"SOS stable: {np.isfinite(y_sos_hi).all()}")   # True
print(f"BA stable:  {np.isfinite(y_ba_hi).all()}")    # True (False for order >= ~15+)

##-----------------##
## savgol_filter() ##
##-----------------##
'''
savgol_filter(x, window_length, polyorder, deriv=0, delta=1.0, axis=-1, mode='interp')

Savitzky-Golay filter: fits a polynomial of degree polyorder to window_length consecutive
samples, and returns the polynomial value (or its derivative) at the centre.

window_length : number of samples in each fitting window (must be odd).
polyorder     : polynomial degree (must be < window_length).
deriv         : 0 = smoothing; 1 = first derivative; 2 = second derivative; etc.
delta         : sample spacing (used to scale derivatives correctly).
mode          : boundary handling ('interp', 'mirror', 'nearest', 'constant', 'wrap').

Advantages over moving average:
  - Preserves peaks and troughs better (polynomial fitting, not just averaging).
  - Can differentiate without separate smoothing step.

savgol_coeffs(window_length, polyorder, deriv=0) : returns the FIR coefficients
  corresponding to the SG filter — can then be applied with lfilter.
'''

# Smooth noisy data
y_sg = savgol_filter(x_noisy, window_length=51, polyorder=3)
print(f"SG smoothed noise std: {(y_sg - np.sin(2*np.pi*50*t)).std():.4f}")  # 0.8101 < original noise std

# First derivative: d/dt sin(2*pi*50*t) = 2*pi*50*cos(2*pi*50*t)
dy_dt = savgol_filter(x_noisy, window_length=51, polyorder=3, deriv=1, delta=1/fs)
true_deriv = 2*np.pi*50 * np.cos(2*np.pi*50*t)
print(f"Derivative error: {np.abs(dy_dt[100:-100] - true_deriv[100:-100]).mean():.4f}") # 223.3455

# Second derivative
d2y_dt2 = savgol_filter(x_noisy, window_length=51, polyorder=3, deriv=2, delta=1/fs)

# Window vs polyorder trade-off:
# Larger window = more smoothing (more noise reduction, more peak distortion).
# Higher polyorder = better peak preservation but less smoothing.
for wl, po in [(11,2), (51,2), (51,4), (101,4)]:
    y_sg_cmp = savgol_filter(x_noisy, wl, po)
    err = (y_sg_cmp - np.sin(2*np.pi*50*t)).std()
    print(f"  window={wl:3d} poly={po}  noise_std={err:.4f}")

# savgol_coeffs: get the FIR coefficients
coeffs_sg = savgol_coeffs(window_length=51, polyorder=3, deriv=0)
print(coeffs_sg.shape)   # (51,)
y_sg_fir = np.convolve(x_noisy, coeffs_sg, mode='same')
print(np.allclose(y_sg_fir[25:-25], y_sg[25:-25], atol=1e-10))  # True (interior)

##---------------------------------##
## medfilt / wiener / order_filter ##
##---------------------------------##
'''
medfilt(volume, kernel_size=3) : N-D median filter. Removes salt-and-pepper noise.
medfilt2d(input, kernel_size=3): 2-D median filter (faster for images).
wiener(im, mysize=None, noise=None): adaptive Wiener denoising based on local statistics.
order_filter(a, domain, rank): general order filter (rank 0=min, rank N-1=max, rank N//2=median).
'''

# medfilt: good for impulse (spike) noise
x_spike = x_noisy.copy()
x_spike[::100] = 5.0   # inject spike noise
y_med = medfilt(x_spike, kernel_size=5)   # median over 5-sample window
print(f"Spike noise removed: {np.abs(y_med[::100] - np.sin(2*np.pi*50*t[::100])).max():.3f}")  # 0.711 small

# Compare: moving average smears spikes; median completely removes them
y_ma = np.convolve(x_spike, np.ones(5)/5, mode='same')
print(f"MA spike error:      {np.abs(y_ma[::100]).max():.3f}")   # 1.210 still visible

# wiener: adaptive denoising — estimates local noise and suppresses it
y_wiener = wiener(x_noisy, mysize=11)
print(y_wiener.shape)   # (1000,)

# order_filter (2-D example): erosion (min) and dilation (max)
img_bin = (rng.uniform(0, 1, (10, 10)) > 0.5).astype(float)
domain = np.ones((3, 3))
img_erode  = sig.order_filter(img_bin, domain, rank=0)   # min filter
img_dilate = sig.order_filter(img_bin, domain, rank=8)   # max filter (3*3-1=8)

##--------------------##
## hilbert / envelope ##
##--------------------##
'''
hilbert(x, N=None, axis=-1)

Computes the analytic signal z(t) = x(t) + j*H{x(t)} where H is the Hilbert transform.

z = hilbert(x) is complex:
  np.real(z)    : original signal x(t).
  np.imag(z)    : Hilbert transform of x(t).
  np.abs(z)     : instantaneous amplitude (envelope).
  np.unwrap(np.angle(z)) : instantaneous phase.
  np.diff(np.unwrap(np.angle(z))) * fs / (2*pi) : instantaneous frequency.

N : FFT length (pad/truncate x). Default = len(x).

envelope(z, bp_in, n_out, squared) : more general envelope computation (new in 1.15).
'''

# Amplitude-modulated signal: carrier 200 Hz, modulated by 10 Hz envelope
am_carrier = np.sin(2*np.pi*200*t)
am_modulator = 1 + 0.5*np.cos(2*np.pi*10*t)
am_signal = am_modulator * am_carrier

# Extract envelope via Hilbert transform
z_analytic = hilbert(am_signal)
env_hilbert = np.abs(z_analytic)   # instantaneous amplitude

print(f"Envelope error: {np.abs(env_hilbert - am_modulator).max():.4f}")  # 0.0000 should be small

# Instantaneous frequency
inst_phase = np.unwrap(np.angle(z_analytic))
inst_freq  = np.diff(inst_phase) * fs / (2*np.pi)
print(f"Inst freq (should be ~200): {inst_freq[400:600].mean():.2f} Hz") # 200.00 Hz

# envelope() function: smoother API — returns shape (2, N): row 0 is upper, row 1 is lower envelope
env_new = envelope(am_signal)
print(env_new.shape)   # (2, 1000)
print(np.allclose(env_new[0], env_hilbert, atol=1e-3))  # True (upper envelope ~= hilbert envelope)

# Practical use: compute envelope of speech signal (same principle)
x_speech_sim = np.sin(2*np.pi*440*t) * (1 + np.sin(2*np.pi*5*t))
env_speech = np.abs(hilbert(x_speech_sim))

##-----------------------------------------------##
## decimate / resample / resample_poly / upfirdn ##
##-----------------------------------------------##
'''
decimate(x, q, n=None, ftype='iir', axis=-1, zero_phase=True)
  Downsample by factor q after anti-aliasing lowpass filter.
  ftype : 'iir' (Chebyshev I, default) or 'fir'.
  zero_phase=True : use filtfilt internally to avoid phase shift.

resample(x, num, t=None, axis=0, window=None, domain='time')
  Resample x to num samples using the FFT method (ideal sinc interpolation).
  Best for stationary signals; can introduce Gibbs ringing near discontinuities.

resample_poly(x, up, down, axis=0, window=('kaiser',5.0), padtype='constant', cval=0)
  Resample by rational factor up/down using polyphase FIR filtering.
  Cleaner than resample() for most practical signals; no FFT artifacts.
  up, down : integers; sample rate ratio = up/down. GCD is reduced automatically.

upfirdn(h, x, up=1, down=1, axis=-1)
  Low-level: upsample by up, apply FIR h, downsample by down.
  Building block for resample_poly and custom polyphase filter banks.
'''

# decimate: downsample by 4 (1000 Hz -> 250 Hz)
x_dec = decimate(x_multi, q=4, zero_phase=True)
print(f"Decimated: {len(x_dec)} samples at {fs/4:.0f} Hz")  # 250 samples at 250 Hz
# After decimation, 50 Hz should be preserved; 150 Hz is now above Nyquist (125 Hz)
# so it is correctly filtered out by the anti-aliasing filter before decimation

# resample: sinc-based, output exactly num samples
num_out = 750   # resample 1000 -> 750 (3/4 rate)
x_res = resample(x_multi, num_out)
print(f"Resampled to: {len(x_res)} samples")  # 750

# resample_poly: rational ratio up/down
# Resample 1000 Hz to 400 Hz: up=2, down=5 (factor = 2/5 = 0.4)
x_poly = resample_poly(x_multi, up=2, down=5)
print(f"Polyphase resampled: {len(x_poly)} samples at {fs*2/5:.0f} Hz")  # 400 samples at 400 Hz

# upfirdn: upsample by 3, apply FIR, downsample by 2 (net factor 3/2)
h_fir = firwin(31, 0.4)   # lowpass anti-aliasing FIR
x_updn = upfirdn(h_fir, x_noisy[:100], up=3, down=2)
print(x_updn.shape)   # ceil(100*3/2) + transient ≈ 150 + filter delay

# detrend: remove DC offset or linear trend
x_drift = x_noisy + np.linspace(0, 2, len(t))   # add linear drift
x_detrend_lin = detrend(x_drift, type='linear')   # remove linear trend
x_detrend_dc  = detrend(x_drift, type='constant') # remove mean only
print(f"After detrend: mean={x_detrend_lin.mean():.4f}")  # ~0.0


# =========================================================================================
#══════════════════════════════════  PART C — FIR FILTER DESIGN  ═════════════════════════════════#
# =========================================================================================
'''
FIR vs IIR summary:
  FIR (Finite Impulse Response):
    - Always stable (no poles except at z=0).
    - Can have exactly linear phase (constant group delay) — no distortion.
    - Higher filter order needed for same transition width.
    - a = [1.0] always; only b coefficients.
    - Preferred for: audio, communications, when phase matters.

  IIR (Infinite Impulse Response):
    - More efficient (lower order for same frequency response).
    - Can have nonlinear phase (must use filtfilt for zero-phase offline).
    - Both b and a coefficients; risk of numerical instability (use SOS).
    - Preferred for: high-order anti-aliasing, real-time processing.
'''

##----------##
## firwin() ##
##----------##
'''
firwin(numtaps, cutoff, width=None, window='hamming', pass_zero=True,
       scale=True, fs=None)

FIR filter design using the window method.

numtaps : filter length (number of taps). Must be odd for lowpass/highpass.
          Larger = sharper transition but more computation / group delay.
cutoff  : cutoff frequency in Hz (if fs given) or normalised [0, 1] (= Nyquist).
          Single value: lowpass or highpass.
          Two values: bandpass or bandstop (depends on pass_zero).
pass_zero:
  True  : DC is in the passband -> lowpass (1 cutoff) or bandstop (2 cutoffs).
  False : DC is in the stopband -> highpass (1 cutoff) or bandpass (2 cutoffs).
window  : window function name (string) or (name, param) tuple.
          'hamming' (default), 'hann', 'blackman', 'kaiser', etc.
          Wider main lobe window -> more transition width but lower sidelobes.
width   : transition width (Hz or normalised). If given, auto-selects Kaiser window with
          appropriate beta to meet stopband attenuation.
scale   : normalise so filter has unity gain at DC (lowpass) or Nyquist (highpass).
fs      : sample rate. If given, cutoff/width in Hz; else normalised 0..1.

Returns b (FIR coefficients); a = [1.0] always.
'''

# Lowpass: keep <= 100 Hz, attenuate > 100 Hz
b_firwin_lp = firwin(101, 100.0, window='hamming', fs=fs)
print(b_firwin_lp.shape)   # (101,)  — 101 taps
print(np.isclose(b_firwin_lp.sum(), 1.0))   # True — DC gain = 1

# Highpass: keep >= 200 Hz
b_firwin_hp = firwin(101, 200.0, pass_zero=False, window='hamming', fs=fs)

# Bandpass: keep 80–120 Hz (50 Hz passband)
b_firwin_bp = firwin(201, [80., 120.], pass_zero=False, window='hamming', fs=fs)

# Bandstop (notch region 80–120 Hz): keep 0–80 and 120+ Hz
b_firwin_bs = firwin(201, [80., 120.], pass_zero=True, window='hamming', fs=fs)

# Verify lowpass: check frequency response at key points
_, H_lp = freqz(b_firwin_lp, fs=fs)
w_lp    = np.linspace(0, fs/2, len(H_lp))
print(f"LP gain at 50 Hz:  {np.abs(H_lp[50]).round(4)}")    # ~1.0
print(f"LP gain at 150 Hz: {np.abs(H_lp[150]).round(4)}")   # << 1

# Kaiser window: auto-design with specified attenuation
# Rule: kaiserord gives numtaps and beta for a given ripple and transition width
numtaps_ksr, beta_ksr = kaiserord(ripple=60, width=20/(fs/2))  # 60 dB, 20 Hz transition
b_firwin_kaiser = firwin(numtaps_ksr, 100.0, window=('kaiser', beta_ksr), fs=fs)
print(f"Kaiser filter: {numtaps_ksr} taps, beta={beta_ksr:.2f}") # 183 taps, beta=5.65

# width= shortcut: automatically selects Kaiser window
b_firwin_auto = firwin(101, 100.0, width=20.0, fs=fs)   # 20 Hz transition width

##-----------##
## firwin2() ##
##-----------##
'''
firwin2(numtaps, freq, gain, nfreqs=None, window='hamming', antisymmetric=False, fs=None)

FIR filter with arbitrary frequency-response specification.

freq : frequency array (normalised 0..1 or Hz if fs given). Must start at 0 and end at 1 (or fs/2).
gain : desired gain at each frequency in freq. Piecewise-linear interpolation in between.
nfreqs: number of frequencies for interpolation (default 512). More = finer approximation.
antisymmetric=True : design Type III/IV FIR (odd symmetry; useful for Hilbert transformers).

Use when: you need a non-standard frequency response (shelving, multi-band, etc.).
'''

# Shelving EQ: boost below 200 Hz, cut above 400 Hz
freq_eq = [0., 200., 400., fs/2]
gain_eq = [2.,   2.,  0.5,  0.5]
b_fw2   = firwin2(201, freq_eq, gain_eq, fs=fs)
_, H_fw2 = freqz(b_fw2, fs=fs)
freqs_fw2 = np.linspace(0, fs/2, len(H_fw2))
print(f"Gain at 100 Hz (shelf boost): {np.abs(H_fw2[100]):.2f}")  # ~2.0
print(f"Gain at 450 Hz (shelf cut):   {np.abs(H_fw2[450]):.2f}")  # ~0.5

# Differentiator (Type III FIR): gain rises from 0 at DC, peaks at midband, back to 0 at Nyquist
# Type III requires gain=0 at both DC (0 Hz) and Nyquist (fs/2)
freq_diff = [0., fs/4, fs/2]   # three control points
gain_diff = [0., 1., 0.]       # 0 at DC, peak at quarter-Nyquist, 0 at Nyquist
b_diff = firwin2(101, freq_diff, gain_diff, antisymmetric=True, fs=fs)

# Multi-band: 0-100 Hz pass, 100-200 Hz roll-off, 200-400 Hz stop, 400-500 Hz pass
freq_mb = [0., 100., 200., 400., 500.]
gain_mb = [1.,   1.,   0.,   0.,   1.]
b_mb    = firwin2(301, freq_mb, gain_mb, fs=fs)

##---------------##
## firls / remez ##
##---------------##
'''
firls(numtaps, bands, desired, weight=None, fs=None)
  FIR design by least-squares minimisation of the weighted integrated squared error.
  bands  : 1-D array of band edges in pairs: [f0_start, f0_stop, f1_start, f1_stop, ...]
  desired: desired gain at each band edge (must be same length as bands).
  weight : relative weighting of each band (default all 1).
  Returns b (FIR coefficients).

remez(numtaps, bands, desired, weight=None, Hz=None, type='bandpass', maxiter=25, grid_density=16, fs=None)
  Parks-McClellan equiripple FIR via the Remez exchange algorithm.
  Minimises the maximum (Chebyshev) error -> equiripple passband and stopband.
  Compared to firls: smaller maximum error for same numtaps; firls has smaller RMS error.
  Returns b (FIR coefficients).
'''

# firls: weighted least-squares lowpass
# bands: [pass start, pass end, stop start, stop end]
bands_ls = [0., 90., 110., fs/2]   # 0-90 Hz pass, 110-500 Hz stop
desired_ls = [1., 1., 0., 0.]       # gain in each band
b_firls = firls(101, bands_ls, desired_ls, fs=fs)
_, H_firls = freqz(b_firls, fs=fs)
freqs_resp = np.linspace(0, fs/2, len(H_firls))
print(f"firls at 50 Hz:  {np.abs(H_firls[50]):.4f}")   # ~1.0
print(f"firls at 200 Hz: {np.abs(H_firls[200]):.4f}")  # ~0.0

# firls with unequal band weighting: emphasise stopband
w_ls = [1., 10.]   # stopband 10x more important than passband
b_firls_w = firls(101, bands_ls, desired_ls, weight=w_ls, fs=fs)

# remez: equiripple (Parks-McClellan) — same spec as firls
bands_rm  = [0., 90., 110., 500.]   # in Hz
desired_rm = [1., 0.]               # one gain per band (not per edge for remez)
b_remez = remez(101, bands_rm, desired_rm, fs=fs)
_, H_remez = freqz(b_remez, fs=fs)
print(f"remez at 50 Hz:  {np.abs(H_remez[50]):.4f}")   # ~1.0
print(f"remez at 200 Hz: {np.abs(H_remez[200]):.4f}")  # ~0.0

# Compare max stopband ripple
stop_firls  = np.abs(H_firls[220:]).max()
stop_remez  = np.abs(H_remez[220:]).max()
print(f"Max stopband: firls={stop_firls:.4f}  remez={stop_remez:.4f}")
# remez equiripple: max error spread equally; firls has lower RMS but higher max

# minimum_phase: convert linear-phase FIR to minimum-phase (causal, shorter group delay)
b_min_phase = minimum_phase(b_firwin_lp, method='homomorphic')
print(b_min_phase.shape)   # same length as b_firwin_lp
# Minimum-phase: all zeros inside unit circle; causal; less group delay at cost of phase linearity

##-------------------------##
## kaiserord / kaiser_beta ##
##-------------------------##
'''
kaiserord(ripple, width) -> (numtaps, beta)
  Compute Kaiser window FIR order and beta from desired attenuation specs.
  ripple : stopband attenuation in dB (positive number, e.g. 60 for 60 dB).
  width  : normalised transition width (Hz / Nyquist). Use width_hz / (fs/2).

kaiser_beta(a) -> beta
  Compute Kaiser beta from attenuation a (dB). Used in firwin window=('kaiser', beta).

kaiser_atten(numtaps, width) -> attenuation
  Compute the attenuation achieved by a Kaiser window filter.
'''

# Design Kaiser lowpass for 60 dB stopband, 20 Hz transition at fs=1000 Hz
ripple_db = 60.0
trans_hz  = 20.0
numtaps_k, beta_k = kaiserord(ripple_db, trans_hz / (fs/2))
print(f"Kaiser: {numtaps_k} taps, beta={beta_k:.4f}") # 183 taps, beta=5.6533

b_kaiser = firwin(numtaps_k, 100.0, window=('kaiser', beta_k), fs=fs)
_, H_kaiser = freqz(b_kaiser, fs=fs)
freqs_k = np.linspace(0, fs/2, len(H_kaiser))
# Verify stopband attenuation
stop_mask = freqs_k > 120
atten_kaiser = -20*np.log10(np.abs(H_kaiser[stop_mask]).max())
print(f"Actual stopband attenuation: {atten_kaiser:.1f} dB")  # 66.1 dB

# kaiser_beta: directly compute beta from attenuation requirement
beta_direct = kaiser_beta(60)   # beta for 60 dB attenuation
print(f"beta for 60 dB: {beta_direct:.4f}")

# kaiser_atten: what attenuation does a given design achieve?
atten = kaiser_atten(numtaps_k, trans_hz / (fs/2))
print(f"Predicted attenuation: {atten:.1f} dB") # 60.2 dB


# =========================================================================================
#════════════════════════════════  PART D — IIR FILTER DESIGN  ═══════════════════════════════════#
# =========================================================================================

'''
IIR filter design workflow (recommended):
  1. Determine filter type (butter/cheby1/cheby2/ellip/bessel) and requirements.
  2. Optionally use *ord functions (buttord, cheb1ord, etc.) to find minimum order.
  3. Design directly in SOS form: output='sos'.
  4. Apply with sosfilt (causal) or sosfiltfilt (zero-phase offline).

Filter type comparison (for same order N):
  Butterworth : maximally flat in passband; monotone rolloff; no ripple anywhere.
  Chebyshev I : equiripple in passband; steeper rolloff than Butterworth.
  Chebyshev II: equiripple in stopband; monotone passband; steeper than Butterworth.
  Elliptic    : equiripple in BOTH bands; steepest rolloff for given N.
  Bessel      : maximally flat GROUP DELAY (linear phase); less sharp rolloff.

All design functions support:
  btype   : 'lowpass' (default), 'highpass', 'bandpass', 'bandstop'.
  analog  : True = analog filter (rad/s), False = digital (default).
  output  : 'ba' (default), 'zpk', or 'sos'.
  fs      : sample rate (Hz). If None, Wn is normalised 0..1 (relative to Nyquist).
'''

##------------------##
## butter / buttord ##
##------------------##
'''
butter(N, Wn, btype='lowpass', analog=False, output='ba', fs=None)

Butterworth filter: maximally flat magnitude in passband (no ripple).
Monotonically decreasing response. At Wn: -3 dB attenuation.

buttord(wp, ws, gpass, gstop, analog=False, fs=None) -> (N, Wn)
  Compute minimum order and cutoff Wn for Butterworth given passband/stopband specs:
  wp    : passband edge (Hz or normalised). Max attenuation here: gpass dB.
  ws    : stopband edge (Hz or normalised). Min attenuation here: gstop dB.
  gpass : max passband ripple (dB), e.g. 3.0 for -3 dB.
  gstop : min stopband attenuation (dB), e.g. 40.0 for 40 dB.

Use Butterworth when: no ripple allowed in passband; flat phase response preferred.
'''

# Direct order specification
sos_butt = butter(6, 100.0, btype='low', fs=fs, output='sos')
y_butt = sosfiltfilt(sos_butt, x_multi)
print(f"Butterworth LP at 50 Hz:  {peak_amp(y_butt, 50):.4f}")   # ~1.0
print(f"Butterworth LP at 300 Hz: {peak_amp(y_butt, 300):.4f}")  # ~0.0

# Automatic order selection via buttord
N_butt, Wn_butt = buttord(wp=100., ws=150., gpass=1., gstop=40., fs=fs)
print(f"buttord: N={N_butt}, Wn={Wn_butt:.2f} Hz") # N=12, Wn=105.39 Hz
sos_butt_auto = butter(N_butt, Wn_butt, btype='low', fs=fs, output='sos')

# Bandpass Butterworth: 80-120 Hz
sos_butt_bp = butter(4, [80., 120.], btype='bandpass', fs=fs, output='sos')
y_bp = sosfiltfilt(sos_butt_bp, x_multi)
print(f"BP at 50 Hz (stop):  {peak_amp(y_bp, 50):.4f}") # 0.0008
print(f"BP at 100 Hz (pass): {peak_amp(y_bp, 100):.4f}")  # 0.0032

# ZPK form: more numerically stable for very high orders than BA
z_bp, p_bp, k_bp = butter(4, [80., 120.], btype='bandpass', fs=fs, output='zpk')
print(f"Poles inside unit circle: {np.all(np.abs(p_bp) < 1)}")  # True (stable)

##--------------------##
## cheby1 / cheb1ord  ##
##--------------------##
'''
cheby1(N, rp, Wn, btype='lowpass', analog=False, output='ba', fs=None)

Chebyshev Type I: equiripple in passband, monotone in stopband.
rp   : maximum passband ripple (dB). Smaller rp -> flatter passband, less stopband attenuation.
Wn   : passband edge frequency.

Sharper rolloff than Butterworth for same N, at the cost of passband ripple.

cheb1ord(wp, ws, gpass, gstop, analog=False, fs=None) -> (N, Wn)
'''

sos_cheb1 = cheby1(6, 1., 100., btype='low', fs=fs, output='sos')  # 1 dB ripple
y_cheb1 = sosfiltfilt(sos_cheb1, x_multi)
print(f"Cheby1 at 50 Hz:  {peak_amp(y_cheb1, 50):.4f}") # 0.7959
print(f"Cheby1 at 150 Hz: {peak_amp(y_cheb1, 150):.4f}") # 0.0015 steeper than Butterworth

N_c1, Wn_c1 = cheb1ord(wp=100., ws=150., gpass=1., gstop=40., fs=fs)
print(f"cheb1ord: N={N_c1} (vs buttord N={N_butt})")   # cheb1ord: N=6 (vs buttord N=12) - Cheby I needs fewer stages

##--------------------##
## cheby2 / cheb2ord  ##
##--------------------##
'''
cheby2(N, rs, Wn, btype='lowpass', analog=False, output='ba', fs=None)

Chebyshev Type II: monotone in passband, equiripple in stopband.
rs   : minimum stopband attenuation (dB). E.g. rs=40 -> 40 dB minimum stopband.
Wn   : stopband edge frequency (not passband edge — note different convention!).

Flat passband (like Butterworth) but better stopband attenuation.
Use when: passband flatness matters AND sharp stopband cutoff is needed.

cheb2ord(wp, ws, gpass, gstop, analog=False, fs=None) -> (N, Wn)
'''

sos_cheb2 = cheby2(6, 40., 150., btype='low', fs=fs, output='sos')  # Wn is stopband edge
y_cheb2 = sosfiltfilt(sos_cheb2, x_multi)
print(f"Cheby2 at 50 Hz (pass):  {peak_amp(y_cheb2, 50):.4f}")   # ~1.0 (flat passband)
print(f"Cheby2 at 200 Hz (stop): {peak_amp(y_cheb2, 200):.4f}")  # very small (equiripple stop)

N_c2, Wn_c2 = cheb2ord(wp=100., ws=150., gpass=1., gstop=40., fs=fs)
print(f"cheb2ord: N={N_c2}") # N=6

##------------------##
## ellip / ellipord ##
##------------------##
'''
ellip(N, rp, rs, Wn, btype='lowpass', analog=False, output='ba', fs=None)

Elliptic (Cauer) filter: equiripple in BOTH passband and stopband.
Steepest possible rolloff for given N, rp, and rs.
rp : maximum passband ripple (dB).
rs : minimum stopband attenuation (dB).

Elliptic is optimal (narrowest transition band for given N, rp, rs).
Use when: filter order is critical and some passband and stopband ripple is acceptable.
'''

sos_ellip = ellip(4, 1., 40., 100., btype='low', fs=fs, output='sos')
y_ellip = sosfiltfilt(sos_ellip, x_multi)
print(f"Ellip at 50 Hz:  {peak_amp(y_ellip, 50):.4f}") # 0.9846
print(f"Ellip at 150 Hz: {peak_amp(y_ellip, 150):.4f}") # 0.0017 very sharp transition

N_el, Wn_el = ellipord(wp=100., ws=130., gpass=1., gstop=40., fs=fs)
print(f"ellipord: N={N_el} vs buttord N={N_butt}") # ellipord: N=5 vs buttord N=12 - ellip needs fewest stages

# Compare sharpness for same N=4
print("=== Order 4, lowpass 100 Hz, stopband at 150 Hz ===")
for name, sos_cmp in [("Butterworth", butter(4, 100., fs=fs, output='sos')),
                       ("Cheby1 1dB", cheby1(4, 1., 100., fs=fs, output='sos')),
                       ("Cheby2 40dB", cheby2(4, 40., 150., fs=fs, output='sos')),
                       ("Elliptic",   ellip(4, 1., 40., 100., fs=fs, output='sos'))]:
    w_cmp, H_cmp = freqz_sos(sos_cmp, worN=1000, fs=fs)
    atten_cmp = -20*np.log10(np.abs(H_cmp[150:]).max() + 1e-16)
    print(f"  {name:15s}: attenuation at 150+ Hz = {atten_cmp:.1f} dB")

# === Order 4, lowpass 100 Hz, stopband at 150 Hz ===
#   Butterworth    : attenuation at 150+ Hz = 0.4 dB
#   Cheby1 1dB     : attenuation at 150+ Hz = 0.0 dB
#   Cheby2 40dB    : attenuation at 150+ Hz = 2.1 dB
#   Elliptic       : attenuation at 150+ Hz = 0.0 dB

##--------##
## bessel ##
##--------##
'''
bessel(N, Wn, btype='lowpass', analog=False, output='ba', norm='phase', fs=None)

Bessel/Thomson filter: maximally flat GROUP DELAY in the passband.
Linear phase in the passband -> minimum waveform distortion.

norm : normalisation type:
  'phase'  : -3 dB at Wn (default).
  'delay'  : group delay at DC = 1/Wn seconds.
  'mag'    : maximally flat magnitude at DC.

Trade-off: very gentle rolloff (much less sharp than Butterworth/Chebyshev).
Use when: preserving waveform shape is critical (e.g. pulse signals, group delay sensitive).
'''

sos_bessel = bessel(6, 100., btype='low', fs=fs, output='sos', norm='phase')
y_bessel = sosfiltfilt(sos_bessel, x_multi)
print(f"Bessel at 50 Hz:  {peak_amp(y_bessel, 50):.4f}") # 0.6182

# Bessel has nearly constant group delay in the passband
w_bes, gd_bes = group_delay(bessel(6, 100., fs=fs), fs=fs)
pass_mask = w_bes < 80
print(f"Bessel group delay variation in passband: {gd_bes[pass_mask].std():.4f} samples") # 0.1222 samples
# Compare with Butterworth
w_but, gd_but = group_delay(butter(6, 100., fs=fs), fs=fs)
print(f"Butterworth group delay variation:       {gd_but[pass_mask].std():.4f} samples") # 0.8739 samples

##-----------------------##
## iirdesign / iirfilter ##
##-----------------------##
'''
iirfilter(N, Wn, rp=None, rs=None, btype='lowpass', analog=False, ftype='butter',
          output='ba', fs=None)
  General IIR filter design for given order N and filter type ftype.
  ftype : 'butter', 'cheby1', 'cheby2', 'ellip', 'bessel'.

iirdesign(wp, ws, gpass, gstop, analog=False, ftype='butter', output='ba', fs=None)
  Complete design: automatically computes minimum order from spec.
  wp    : passband edge (Hz or normalised).
  ws    : stopband edge.
  gpass : max passband ripple (dB).
  gstop : min stopband attenuation (dB).
'''

# iirfilter: design any type in one call
sos_gen = iirfilter(6, 100., btype='low', ftype='butter', output='sos', fs=fs)
print(np.allclose(sos_gen, butter(6, 100., fs=fs, output='sos')))  # True

# iirdesign: all-in-one with automatic order selection
sos_iird = iirdesign(wp=100., ws=150., gpass=1., gstop=40.,
                     ftype='ellip', output='sos', fs=fs)
print(f"iirdesign elliptic: {sos_iird.shape[0]} sections") # 2 sections

##------------------------------##
## iirnotch / iirpeak / iircomb ##
##------------------------------##
'''
iirnotch(w0, Q, fs=1.0)
  Second-order IIR notch filter at frequency w0 with quality factor Q.
  w0 : notch frequency (Hz if fs given; normalised 0..1 if fs=1).
  Q  : quality factor. Higher Q -> narrower notch.
  Returns (b, a) BA coefficients (always 2nd-order, stable).

iirpeak(w0, Q, fs=1.0)
  Second-order IIR peaking (resonant) filter. Passband around w0.

iircomb(w0, Q, ftype='notch', fs=1.0, pass_zero=False)
  IIR comb filter: periodic notches (or peaks) at w0, 2*w0, 3*w0, ...
  ftype='notch' : notch comb (attenuates harmonics of w0).
  ftype='peak'  : peak comb (boosts harmonics).
  pass_zero     : whether DC is in the passband.
'''

# 50 Hz notch (e.g. remove power-line interference)
b_notch, a_notch = iirnotch(50., Q=30., fs=fs)
x_noise50 = x_noisy + np.sin(2*np.pi*50*t) * 2   # add 50 Hz interference
y_notch = filtfilt(b_notch, a_notch, x_noise50)
print(f"50 Hz notch output: {peak_amp(y_notch, 50):.4f}")   # 0.2812
print(f"100 Hz preserved:   {peak_amp(y_notch, 100):.4f}")  # 0.0048

# iirpeak: parametric EQ-style peak filter at 200 Hz
b_peak, a_peak = iirpeak(200., Q=5., fs=fs)
_, H_peak = freqz(b_peak, a_peak, fs=fs)
w_peak = np.linspace(0, fs/2, len(H_peak))
print(f"Peak gain at 200 Hz: {np.abs(H_peak[200]):.4f}")   # 0.9736

# iircomb: notch at 50 Hz and all harmonics (50, 100, 150, 200, ...)
b_comb, a_comb = iircomb(50., Q=30., ftype='notch', fs=fs)
y_comb = filtfilt(b_comb, a_comb, x_noise50)
# All harmonics of 50 Hz are suppressed


# =========================================================================================
#════════════════════  PART E — FREQUENCY RESPONSE & FILTER REPRESENTATIONS  ═════════════════════#
# =========================================================================================

##-------------------------------##
## freqz / freqz_zpk / freqz_sos ##
##-------------------------------##
'''
freqz(b, a=1, worN=512, whole=False, plot=None, fs=2*pi, include_nyquist=False)

Compute the frequency response H(e^{jw}) of a digital filter.

b, a   : filter numerator and denominator coefficients (BA form).
worN   : number of frequencies (int) or specific frequency array (rad/sample or Hz if fs given).
whole  : False = compute [0, pi]; True = compute [0, 2*pi].
fs     : sample rate (Hz). Defaults to 2*pi -> output w in rad/sample.

Returns (w, H):
  w : frequencies (rad/sample or Hz).
  H : complex frequency response. |H| = magnitude, angle(H) = phase.

freqz_zpk(z, p, k, worN=512, whole=False, fs=2*pi)
  Same but takes ZPK form. More numerically stable for high-order filters.

freqz_sos(sos, worN=512, whole=False, fs=2*pi)
  Same but takes SOS form. Most stable.
'''

# BA form (low-order OK)
b4, a4 = butter(4, 100., fs=fs)
w_ba, H_ba = freqz(b4, a4, worN=1000, fs=fs)

# ZPK form
z_4, p_4, k_4 = butter(4, 100., fs=fs, output='zpk')
w_zpk, H_zpk = freqz_zpk(z_4, p_4, k_4, worN=1000, fs=fs)

# SOS form
sos_4 = butter(4, 100., fs=fs, output='sos')
w_sos, H_sos = freqz_sos(sos_4, worN=1000, fs=fs)

print(np.allclose(np.abs(H_ba), np.abs(H_sos), atol=1e-6))  # True (same filter)

# Magnitude in dB and phase
mag_db  = 20 * np.log10(np.abs(H_sos) + 1e-16)
phase   = np.unwrap(np.angle(H_sos))  # unwrapped phase in radians

idx_100 = np.argmin(np.abs(w_sos - 100))
print(f"Butterworth at 100 Hz: {mag_db[idx_100]:.2f} dB")  # ~-3.0 dB

# freqs: ANALOG frequency response
b_analog, a_analog = butter(4, 2*np.pi*100, analog=True)   # analog filter at 100 rad/s
w_analog = np.logspace(1, 4, 200)   # rad/s
_, H_analog = freqs(b_analog, a_analog, worN=w_analog)
print(f"Analog Butterworth at 100 rad/s: {20*np.log10(np.abs(H_analog[100])):.2f} dB") # -0.02 dB

##---------------##
## group_delay() ##
##---------------##
'''
group_delay(system, w=512, whole=False, fs=2*pi)

Compute the group delay: tau(w) = -d(phase)/dw [in samples].

system : (b, a) tuple for BA form. For SOS use sos2tf() first.
w      : frequencies (int for evenly-spaced, or array).
fs     : sample rate.

Returns (w, gd) where gd is in samples.

Group delay interpretation:
  Constant gd -> linear phase -> all frequencies delayed equally -> no waveform distortion.
  Variable gd -> phase distortion -> FIR or use Bessel filter.
'''

# FIR: linear phase -> constant group delay = (N-1)/2
b_fir_gd = firwin(101, 100., fs=fs)
w_gd, gd_fir = group_delay((b_fir_gd, [1.0]), fs=fs)
gd_pass = gd_fir[w_gd < 80]
print(f"FIR group delay: {gd_pass.mean():.2f} ± {gd_pass.std():.4f} samples")  # ~50 ± tiny

# IIR Butterworth: nonlinear group delay
w_gd_iir, gd_iir = group_delay((b4, a4), fs=fs)
print(f"IIR group delay at 50 Hz:  {gd_iir[50]:.2f} samples")   # 4.63 samples
print(f"IIR group delay at 95 Hz:  {gd_iir[95]:.2f} samples")   # 6.52 samples (larger near cutoff)

##------------------------------------##
## tf2zpk / tf2sos / zpk2sos / sos2tf ##
##------------------------------------##
'''
Representation conversions:

BA  -> ZPK: tf2zpk(b, a)             returns (z, p, k)
ZPK -> BA : zpk2tf(z, p, k)          returns (b, a)
BA  -> SOS: tf2sos(b, a)             returns sos array (N, 6)
SOS -> BA : sos2tf(sos)              returns (b, a)
ZPK -> SOS: zpk2sos(z, p, k)        returns sos
SOS -> ZPK: sos2zpk(sos)            returns (z, p, k)
BA  -> SS : tf2ss(b, a)             returns (A, B, C, D) state-space matrices
SS  -> BA : ss2tf(A, B, C, D)       returns (b, a)
ZPK -> SS : zpk2ss(z, p, k)         returns (A, B, C, D)
SS  -> ZPK: ss2zpk(A, B, C, D)      returns (z, p, k)

Numerical stability ranking: SOS ≥ ZPK > BA > SS (for high-order filters)
Recommended workflow: design -> ZPK or SOS -> never convert back to BA.
'''

# BA -> ZPK
b_ex, a_ex = butter(6, 100., fs=fs)
z_ex, p_ex, k_ex = tf2zpk(b_ex, a_ex)
print(f"Zeros: {len(z_ex)}, Poles: {len(p_ex)}")  # 6 zeros, 6 poles

# All poles inside unit circle = stable
print(f"Max pole magnitude: {np.abs(p_ex).max():.6f}")  # 0.857855 (< 1.0)

# ZPK -> BA (round-trip)
b_rt, a_rt = zpk2tf(z_ex, p_ex, k_ex)
print(np.allclose(b_ex, b_rt, atol=1e-8))  # True

# BA -> SOS (always prefer this for IIR > 4th order)
sos_ex = tf2sos(b_ex, a_ex)
print(sos_ex.shape)   # (3, 6) — 3 second-order sections for 6th-order filter

# SOS -> ZPK
z_sos_ex, p_sos_ex, k_sos_ex = sos2zpk(sos_ex)
# Sorted absolute values should match (small rounding differs)
print(np.allclose(sorted(np.abs(z_ex)), sorted(np.abs(z_sos_ex)), atol=1e-6))  # True

# bilinear transform: convert analog prototype to digital
# (used internally by butter etc. when analog=False, with pre-warping)
b_a_analog, a_a_analog = butter(4, 2*np.pi*100, analog=True)
b_digital, a_digital = bilinear(b_a_analog, a_a_analog, fs=fs)
# Note: bilinear without frequency pre-warping differs slightly from butter(analog=False)
# which applies pre-warping to match the exact digital cutoff.
b_direct, a_direct = butter(4, 100., fs=fs)
print(np.abs(b_digital - b_direct).max() < 0.01)  # True — close but not identical (pre-warp diff)

##------------------##
## residue / invres ##
##------------------##
'''
residue(b, a, tol=1e-3, rtype='avg') -> (r, p, k)
  Partial fraction expansion of B(s)/A(s) (continuous-time / s-domain).
  r : residues.  p : poles.  k : polynomial remainder (direct terms).
  B(s)/A(s) = sum(r[i] / (s - p[i])) + k[0] + k[1]*s + ...

invres(r, p, k) -> (b, a)
  Reconstruct transfer function from partial fraction expansion.

residuez(b, a) / invresz(r, p, k)
  Same for z-domain (discrete-time) filters.

Use for:
  - System analysis: identify poles and partial fractions.
  - Inverse Laplace / z-transform: convert from pole-residue to time domain.
  - Stability analysis (poles inside/outside unit circle).
'''

# Partial fraction of a simple analog TF: H(s) = 1/(s^2 + 3s + 2) = 1/((s+1)(s+2))
b_pf = np.array([1.])
a_pf = np.array([1., 3., 2.])   # (s+1)(s+2)

r_pf, p_pf, k_pf = residue(b_pf, a_pf)
print(f"Poles: {p_pf}")   # Poles: [-1. -2.]
print(f"Residues: {r_pf}")  # [ 1. -1.]  -> 1/(s+2) - 1/(s+1) -> inverse Laplace: e^{-2t} - e^{-t}

# Reconstruct: invres should give back b, a (may have leading zero)
b_rt_pf, a_rt_pf = invres(r_pf, p_pf, k_pf)
print(np.allclose(np.real(b_rt_pf[-len(b_pf):]), b_pf, atol=1e-8))  # True (trailing matches)

# Z-domain partial fractions of a digital filter
b_z = np.array([1., 0.5])
a_z = np.array([1., -1.5, 0.5])   # poles at z=1 and z=0.5
r_z, p_z, k_z = residuez(b_z, a_z)
print(f"Z-domain poles: {p_z.round(4)}")   # [0.5 1. ]
b_rtz, a_rtz = invresz(r_z, p_z, k_z)
print(np.allclose(np.real(b_rtz), b_z, atol=1e-8))  # True


# =========================================================================================
#═════════════════════════════════  PART F — WINDOW FUNCTIONS  ═══════════════════════════════════#
# =========================================================================================
'''
Windows are used in spectral analysis (reduce spectral leakage) and FIR filter design.

Key properties:
  Main lobe width   : narrower -> better frequency resolution.
  Sidelobe level    : lower -> less spectral leakage (can't see weak nearby tones).
  Coherent gain     : sum(w) / N — affects spectral amplitude calibration.

Trade-off: narrower main lobe <-> higher sidelobes. No window is optimal for all purposes.

sym=True  (default): symmetric window (for FIR filter design; window peaks at centre).
sym=False          : periodic window (for spectral analysis / DFT; avoids duplicate endpoint).

Common choice:
  Rectangular (boxcar) : highest leakage; best frequency resolution. Only use for FFT of known
                          periodic stationary signals.
  Hann                  : good all-purpose window; -31 dB sidelobes; standard default.
  Hamming               : similar to Hann; slightly better sidelobes (-43 dB).
  Blackman              : wider main lobe but very low sidelobes (-58 dB).
  Blackman-Harris       : even lower sidelobes (-92 dB); best for dynamic range.
  Kaiser(beta)          : tunable; trade main-lobe width vs sidelobe level via beta.
  Flat-top              : designed for accurate amplitude measurement; wide main lobe.
  DPSS (Slepian)        : optimal for concentration of energy; used in multitaper spectral analysis.
'''

N_win = 64

# get_window: retrieve any window by name
w_hann    = get_window('hann', N_win)
w_hamming = get_window('hamming', N_win)
w_kaiser  = get_window(('kaiser', 8.6), N_win)   # beta=8.6 ~ 60 dB sidelobes
w_tukey   = get_window(('tukey', 0.5), N_win)    # alpha=0.5 cosine taper fraction
w_dpss, dpss_ratios = win.dpss(N_win, NW=4, Kmax=7, sym=True, return_ratios=True)  # 7 DPSS tapers

# Direct construction from windows submodule
w_boxcar    = win.boxcar(N_win, sym=False)      # rectangular
w_blackman  = win.blackman(N_win, sym=False)    # spectral analysis
w_blkharris = win.blackmanharris(N_win, sym=False)
w_flattop   = win.flattop(N_win, sym=False)     # amplitude measurement
w_gaussian  = win.gaussian(N_win, std=N_win/6)  # Gaussian

# Coherent gain (for amplitude correction in spectral analysis)
def coherent_gain(w):
    return w.sum() / len(w)

for name, w in [('boxcar', w_boxcar), ('hann', w_hann),
                ('hamming', w_hamming), ('blackman', w_blackman),
                ('flattop', w_flattop), ('kaiser8.6', w_kaiser)]:
    print(f"  {name:15s}  coherent_gain={coherent_gain(w):.4f}")
  # boxcar           coherent_gain=1.0000
  # hann             coherent_gain=0.5000
  # hamming          coherent_gain=0.5400
  # blackman         coherent_gain=0.4200
  # flattop          coherent_gain=0.2156
  # kaiser8.6        coherent_gain=0.4208

# Hann window (sym=False) for FFT: avoids double-counting the end point
w_hann_periodic = win.hann(N_win, sym=False)
print(f"Periodic Hann: w[0]={w_hann_periodic[0]:.4f}  w[-1]={w_hann_periodic[-1]:.4f}")
# Periodic Hann: w[0]=0.0000  w[-1]=0.0024
# For FIR design, use sym=True (default); for FFT analysis, use sym=False

# Kaiser: tune sidelobe level via beta
for beta, sll_approx in [(0, 13), (5, 40), (8.6, 60), (14, 100)]:
    w_k = win.kaiser(N_win, beta=beta, sym=False)
    print(f"  Kaiser beta={beta:.1f}: approx sidelobe level ~ {sll_approx} dB")
  # Kaiser beta=0.0: approx sidelobe level ~ 13 dB
  # Kaiser beta=5.0: approx sidelobe level ~ 40 dB
  # Kaiser beta=8.6: approx sidelobe level ~ 60 dB
  # Kaiser beta=14.0: approx sidelobe level ~ 100 dB

# DPSS: optimal concentration of energy in a bandwidth of NW/N Hz (per half-sample)
print(f"DPSS tapers: {w_dpss.shape}")   # (7, 64) — 7 tapers of length 64
print(f"Concentration ratios: {dpss_ratios.round(6)}")
# Concentration ratios: [1.       1.       0.999999 0.99997  0.999437 0.99271  0.937469]
# near 1 for first few

# Nuttall, Parzen, Lanczos
w_nuttall = win.nuttall(N_win, sym=False)
w_parzen  = win.parzen(N_win, sym=False)
w_lanczos = win.lanczos(N_win, sym=False)   # sinc window; good for image resampling


# =========================================================================================
#═════════════════════════════  PART G — SPECTRAL ANALYSIS  ══════════════════════════════════════#
# =========================================================================================

##---------------##
## periodogram() ##
##---------------##
'''
periodogram(x, fs=1.0, window='boxcar', nfft=None, detrend='constant',
            return_onesided=True, scaling='density')

Estimate power spectral density (PSD) using a single unaveraged DFT.

fs      : sample rate (Hz).
window  : window function (default 'boxcar'). Use 'hann' for better leakage control.
nfft    : FFT length. Default = len(x). Zero-padding increases frequency resolution display
          but does NOT add new information.
detrend : 'constant' (remove mean), 'linear' (remove linear trend), False (no detrend).
scaling : 'density' -> PSD [V^2/Hz]; 'spectrum' -> power spectrum [V^2].
return_onesided: True = one-sided (real signal, 0..fs/2).

Returns (f, Pxx):
  f   : frequency array (Hz).
  Pxx : PSD or power spectrum estimate.

Variance: periodogram has high variance (not useful alone for noisy signals).
          Use welch() for averaged PSD with lower variance.
'''

# Simple PSD of multi-tone signal
f_per, Pxx_per = periodogram(x_multi, fs=fs, window='hann', scaling='density')
# Peaks should be at 50, 150, 300 Hz
peak_freqs = f_per[np.argsort(Pxx_per)[-4:]]
print(f"Periodogram peaks at: {np.sort(peak_freqs).astype(int)}")  # [ 49  50  51 150]

# Power spectrum: integrate density over df to get total power
df = f_per[1] - f_per[0]
total_power = np.sum(Pxx_per) * df
print(f"Total power: {total_power:.4f}") # should be sum(A^2/2) = 0.5 + 0.125 + 0.045 = 0.67

# Effect of zero-padding (interpolates spectral display, doesn't add resolution)
f_nfft, Pxx_nfft = periodogram(x_multi[:100], fs=fs, window='hann', nfft=4096, scaling='density')
print(f"Zero-padded: {len(f_nfft)} frequency bins vs {100} data points")
# Zero-padded: 2049 frequency bins vs 100 data points

##---------##
## welch() ##
##---------##
'''
welch(x, fs=1.0, window='hann', nperseg=256, noverlap=None, nfft=None,
      detrend='constant', return_onesided=True, scaling='density', axis=-1)

Welch's method: average periodograms from overlapping segments to reduce variance.

nperseg   : segment length (samples). Default 256.
noverlap  : overlap between segments. Default nperseg//2 (50% overlap).
nfft      : FFT length (zero-pad each segment). Default = nperseg.
window    : window applied to each segment (default 'hann').
scaling   : 'density' (PSD in V^2/Hz) or 'spectrum' (power spectrum in V^2).

Trade-off: longer nperseg -> better frequency resolution but fewer averages.
           shorter nperseg -> more averages (lower variance) but coarser resolution.

Returns (f, Pxx): same as periodogram.
'''

f_welch, Pxx_welch = welch(x_multi, fs=fs, nperseg=256, noverlap=128,
                             window='hann', scaling='density')
print(f"Welch frequency resolution: {f_welch[1]-f_welch[0]:.2f} Hz")  # = fs/nperseg = 3.9 Hz

# PSD in dB
Pxx_db = 10 * np.log10(Pxx_welch + 1e-16)
for f_tone in [50, 150, 300]:
    idx_t = np.argmin(np.abs(f_welch - f_tone))
    print(f"  Welch PSD at {f_tone} Hz: {Pxx_db[idx_t]:.1f} dBW/Hz")
  # Welch PSD at 50 Hz: -10.9 dBW/Hz
  # Welch PSD at 150 Hz: -17.6 dBW/Hz
  # Welch PSD at 300 Hz: -21.4 dBW/Hz

# Longer segment: higher resolution but more variance
f_long, Pxx_long = welch(x_multi, fs=fs, nperseg=512, scaling='density')
print(f"Long-segment Welch: {f_long[1]-f_long[0]:.2f} Hz resolution") # 1.95 Hz resolution

# Apply to noisy signal: Welch reliably finds buried 50 Hz tone
f_n, Pxx_n = welch(x_noisy, fs=fs, nperseg=256, scaling='density')
snr_db = 10*np.log10(Pxx_n[np.argmin(np.abs(f_n-50))] / np.median(Pxx_n))
print(f"SNR of 50 Hz in noise: {snr_db:.1f} dB")
# SNR of 50 Hz in noise: 26.8 dB

##-------------------##
## csd / coherence() ##
##-------------------##
'''
csd(x, y, fs=1.0, window='hann', nperseg=256, noverlap=None, nfft=None,
    detrend='constant', return_onesided=True, scaling='density', axis=-1)

Cross Power Spectral Density: Pxy(f) = E[X(f)* Y(f)] (complex).
|Pxy| -> magnitude of cross-spectrum; angle(Pxy) -> phase difference at each frequency.

coherence(x, y, fs=1.0, ...) -> (f, Cxy)
  Magnitude Squared Coherence: Cxy = |Pxy|^2 / (Pxx * Pyy)
  Range: 0..1. Cxy(f)=1 means x and y are linearly related at frequency f.
  Cxy(f)=0 means no linear relationship.

Applications:
  - Identify which frequencies are shared between two signals.
  - Noise estimation / coherence-based enhancement.
  - System identification.
'''

# Construct x and y that share a 50 Hz component but differ elsewhere
x_csd = np.sin(2*np.pi*50*t) + rng.normal(0, 0.5, len(t))
y_csd = 0.8*np.sin(2*np.pi*50*t + 0.3) + rng.normal(0, 0.5, len(t))

# Cross-spectral density
f_csd, Pxy = csd(x_csd, y_csd, fs=fs, nperseg=256, window='hann')
print(f"CSD phase at 50 Hz: {np.angle(Pxy[np.argmin(np.abs(f_csd-50))], deg=True):.1f} deg")  # 23.7 deg

# Coherence: high at 50 Hz (shared), low elsewhere (independent noise)
f_coh, Cxy = coherence(x_csd, y_csd, fs=fs, nperseg=256)
idx_50_coh = np.argmin(np.abs(f_coh - 50))
print(f"Coherence at 50 Hz: {Cxy[idx_50_coh]:.4f}")   # 0.9917 (high ~0.8+)
print(f"Coherence at 200 Hz: {Cxy[np.argmin(np.abs(f_coh-200))]:.4f}")  # 0.2905 low ~0.0

##----------------------------##
## ShortTimeFFT (modern STFT) ##
##----------------------------##
'''
ShortTimeFFT(win, hop, fs, fft_mode='onesided', mfft=None, dual_win=None,
             scale_to=None, phase_shift=None)

Modern class-based STFT (and inverse STFT) interface. Introduced in SciPy 1.11.

win  : window array or name.
hop  : hop size (samples between consecutive frames).
fs   : sample rate.
fft_mode : 'onesided' (default, real signal), 'twosided', 'centered'.
scale_to : 'magnitude' or 'psd'. Normalises the STFT output.

Methods:
  SFT.stft(x)       : compute STFT, returns (f, t, Zxx).
  SFT.istft(Zxx)    : inverse STFT, returns reconstructed signal.
  SFT.spectrogram(x): squared magnitude |STFT|^2.

SFT.f  : frequency array.
SFT.t(n): time array for signal of length n.

Compared to legacy stft/istft:
  - More flexible and correct boundary handling.
  - Explicit control over synthesis window (dual window).
  - Class interface reuses the same window/hop setup.
'''

# Create STFT object: 50 ms window, 25 ms hop
win_stft = win.hann(M=int(0.05 * fs), sym=True)   # 50-sample window
hop_stft = int(0.025 * fs)                          # 25-sample hop

SFT = ShortTimeFFT(win_stft, hop=hop_stft, fs=fs, scale_to='magnitude')

# Compute STFT of chirp signal (frequency increases with time)
t_chirp = np.linspace(0, 1, int(fs))
x_chirp = chirp(t_chirp, f0=10, f1=400, t1=1.0, method='linear')

Zxx = SFT.stft(x_chirp)   # complex STFT, shape (n_freqs, n_frames)
print(f"STFT shape: {Zxx.shape}") # (26, 41)
print(f"Frequencies: {SFT.f[:5].round(1)} ... {SFT.f[-5:].round(1)}") # [ 0. 20. 40. 60. 80.] ... [420. 440. 460. 480. 500.]

# Time-frequency representation: time vs frequency magnitude
spectrogram_tf = np.abs(Zxx)

# Inverse STFT: reconstruct the original signal
x_reconstructed = SFT.istft(Zxx, k1=len(x_chirp))
print(f"Reconstruction error: {np.abs(x_reconstructed - x_chirp).max():.2e}")  # 4.44e-16 very small

# check_NOLA: verify reconstruction is possible (nonzero overlap)
print(check_NOLA(win_stft, len(win_stft), len(win_stft) - hop_stft))  # True

# spectrogram method directly
S = SFT.spectrogram(x_chirp)   # |STFT|^2; shape (n_freqs, n_frames)
print(S.shape) # (26, 41)

##-----------------------##
## stft / istft (legacy) ##
##-----------------------##
'''
stft(x, fs=1.0, window='hann', nperseg=256, noverlap=None, nfft=None,
     detrend=False, return_onesided=True, boundary='zeros', padded=True, axis=-1)

Legacy STFT: functionally correct but the class-based ShortTimeFFT is preferred for new code.

Returns (f, t, Zxx):
  f   : frequency array (Hz).
  t   : time array (seconds) at centre of each frame.
  Zxx : complex STFT, shape (n_freqs, n_frames).

istft(Zxx, fs=1.0, window='hann', nperseg=None, noverlap=None, nfft=None,
      input_onesided=True, boundary=True, time_axis=-1, freq_axis=-2)
  Inverse STFT. Requires COLA or NOLA conditions to reconstruct exactly.
'''

f_stft, t_stft, Zxx_stft = stft(x_chirp, fs=fs, window='hann', nperseg=50, noverlap=25)
print(f"Legacy STFT: {Zxx_stft.shape}")   # (26, 41) freq bins x frames

# Reconstruct
_, x_rec_stft = istft(Zxx_stft, fs=fs, window='hann', nperseg=50, noverlap=25)
x_rec_stft = x_rec_stft[:len(x_chirp)]
print(f"Legacy STFT reconstruction error: {np.abs(x_rec_stft - x_chirp).max():.2e}") # 5.55e-16

##---------------##
## lombscargle() ##
##---------------##
'''
lombscargle(x, y, freqs, precenter=False, normalize=False)

Lomb-Scargle periodogram: estimates PSD for UNEVENLY SAMPLED data.

x     : observation times (not required to be uniform).
y     : observed values.
freqs : angular frequencies (rad/s) to evaluate. Use 2*pi*f for Hz -> rad/s.
precenter=True  : subtract mean of y (reduces aliasing artefacts).
normalize=True  : normalise to chi-square distribution.

Returns PSD estimate at each frequency in freqs.
Essential for astronomy, geoscience, medical data with irregular sampling.
'''

# Simulate unevenly-sampled 10 Hz sinusoid
t_irr = np.sort(rng.uniform(0, 5, 200))   # 200 random times in [0, 5] s
y_irr = np.sin(2*np.pi*10 * t_irr) + rng.normal(0, 0.2, 200)

freqs_ls = np.linspace(1, 50, 500)   # 1-50 Hz in angular freq
ang_freqs = 2 * np.pi * freqs_ls

pgram_ls = lombscargle(t_irr, y_irr, ang_freqs, precenter=True)
peak_f = freqs_ls[np.argmax(pgram_ls)]
print(f"Lomb-Scargle detected frequency: {peak_f:.2f} Hz")  # ~10.0 Hz

##-----------##
## detrend() ##
##-----------##
'''
detrend(data, axis=-1, type='linear', bp=0, overwrite_data=False)

Remove linear trend ('linear') or constant mean ('constant') from data.

type : 'linear'   — subtract best-fit line (removes slope and DC).
       'constant' — subtract the mean (DC removal only).
bp   : breakpoints — indices where linear fit is pieced together.

Use before FFT analysis to reduce spectral leakage from DC and trend.
Also available via np.detrend() with same interface.
'''

x_trend = np.sin(2*np.pi*50*t) + np.linspace(0, 5, len(t))  # signal + ramp
x_dt_lin  = detrend(x_trend, type='linear')
x_dt_dc   = detrend(x_trend, type='constant')

print(f"After linear detrend: slope ~ {np.polyfit(t, x_dt_lin, 1)[0]:.4f}")  # ~0
print(f"After constant detrend: mean = {x_dt_dc.mean():.4f}")               # ~0


# =========================================================================================
#══════════════════════════════════  PART H — LTI SYSTEMS  ═══════════════════════════════════════#
# =========================================================================================
'''
LTI system representations:
  TransferFunction(b, a)         : H(s) = B(s)/A(s) (continuous) or H(z) (discrete).
  ZerosPolesGain(z, p, k)        : H(s) = k * prod(s-zi) / prod(s-pi).
  StateSpace(A, B, C, D)         : x'(t) = Ax + Bu;  y(t) = Cx + Du.

All three are interconvertible.
Continuous-time: time in seconds, frequency in rad/s.
Discrete-time:   add dt=... to make dlti.
'''

##-----------------------------##
## Continuous-time LTI systems ##
##-----------------------------##

# Define a 2nd-order underdamped system: natural frequency wn=10 rad/s, zeta=0.1
wn = 10.0     # natural frequency (rad/s)
zeta = 0.1   # damping ratio (0=undamped, 1=critically damped)
b_ct = [wn**2]
a_ct = [1., 2*zeta*wn, wn**2]

# TransferFunction object
sys_tf = TransferFunction(b_ct, a_ct)
print(f"System poles: {sys_tf.poles.round(4)}")  # [-1.+9.9499j -1.-9.9499j]

# ZerosPolesGain object
z_ct, p_ct, k_ct = tf2zpk(b_ct, a_ct)
sys_zpk = ZerosPolesGain(z_ct, p_ct, k_ct)

# StateSpace object
A_ss, B_ss, C_ss, D_ss = tf2ss(b_ct, a_ct)
sys_ss = StateSpace(A_ss, B_ss, C_ss, D_ss)

# Impulse response: response to delta input
T_ir, h_ir = impulse(sys_tf, T=np.linspace(0, 5, 500))
print(f"Impulse response peak: {h_ir.max():.4f} at t={T_ir[np.argmax(h_ir)]:.3f} s")
# Impulse response peak: 8.6233 at t=0.150 s

# Step response: response to unit step input
T_step, y_step = step(sys_tf, T=np.linspace(0, 5, 500))
print(f"Step response final value: {y_step[-1]:.4f}")   # should -> 1.0 (DC gain = 1)

# Simulate arbitrary input
T_sim   = np.linspace(0, 5, 5000)
U_sim   = np.sin(wn * T_sim)   # excite at natural frequency
T_out, y_sim, x_sim = lsim(sys_tf, U=U_sim, T=T_sim)
print(f"Simulation output shape: {y_sim.shape}")   # (5000,)

# Bode plot data
w_bode = np.logspace(-1, 3, 500)   # rad/s
w_mag, mag_db_bode, phase_bode = bode(sys_tf, w=w_bode)
print(f"Resonance peak: {mag_db_bode.max():.2f} dB at {w_bode[np.argmax(mag_db_bode)]:.2f} rad/s")
# Resonance peak: 14.02 dB at 9.91 rad/s

# Frequency response
w_fr, H_fr = freqresp(sys_tf, w=w_bode)
print(np.allclose(mag_db_bode, 20*np.log10(np.abs(H_fr)), atol=1e-8))  # True

# cont2discrete: convert continuous-time to discrete-time (for digital implementation)
dt = 1/fs   # sampling period at 1000 Hz
sys_d = cont2discrete((b_ct, a_ct), dt, method='bilinear')
print(f"Discrete TF: b={sys_d[0].round(6)}, a={sys_d[1].round(6)}")
# Discrete TF: b=[[2.5e-05 5.0e-05 2.5e-05]], a=[ 1.       -1.997902  0.998002]

##---------------------------##
## Discrete-time LTI systems ##
##---------------------------##
'''
dlti(*system, dt=1) : discrete-time LTI system.
  Same representations: TransferFunction(b,a,dt=...), ZerosPolesGain(z,p,k,dt=...), StateSpace(A,B,C,D,dt=...).

dlsim(system, u, t=None, x0=None): simulate output of discrete system.
dimpulse(system, x0=None, t=None, n=None): impulse response.
dstep(system, x0=None, t=None, n=None): step response.
dbode(system, w=None, n=100): Bode plot (frequency in rad/sample).
'''

# Discrete-time version of the same system
b_disc, a_disc = sys_d[0], sys_d[1]   # from cont2discrete
sys_dlti = dlti(b_disc, a_disc, dt=dt)

# Discrete impulse response
_, h_dimp = dimpulse(sys_dlti, n=500)
print(f"Discrete impulse response shape: {h_dimp[0].shape}")  # (500, 1)

# Discrete step response
_, y_dstep = dstep(sys_dlti, n=500)
print(f"Discrete step final value: {y_dstep[0][-1][0]:.4f}")   # 0.9044 (~1)

# Discrete simulation
n_sim = np.arange(500)
u_disc = np.sin(wn * n_sim * dt)
tout_d, y_disc = dlsim(sys_dlti, u=u_disc)
print(f"Discrete simulation output shape: {y_disc.shape}")  # (500, 1)

# Discrete Bode
w_dbode, mag_d, phase_d = dbode(sys_dlti, n=200)
print(f"Max gain: {mag_d.max():.2f} dB") # 0.00 dB


# =========================================================================================
#═════════════════════════════════  PART I — PEAK FINDING  ═══════════════════════════════════════#
# =========================================================================================

##------------##
## find_peaks ##
##------------##
'''
find_peaks(x, height=None, threshold=None, distance=None, prominence=None,
           width=None, wlen=None, rel_height=0.5, plateau_size=None)

Find all local maxima in a 1-D array, then filter by properties.

height       : minimum (or min/max range) height of peaks.
threshold    : minimum difference from neighbours (vertical threshold).
distance     : minimum horizontal distance (samples) between peaks.
prominence   : minimum prominence (how much a peak stands out from surrounding valleys).
width        : minimum peak width (at rel_height fraction of prominence).
wlen         : window length for prominence calculation (avoids searching the whole signal).

Returns (peaks, properties):
  peaks      : indices of peaks in x.
  properties : dict containing 'peak_heights', 'prominences', 'widths', etc.
               (only keys explicitly requested via the arguments are populated).

Peak prominence: height above the highest of the two surrounding valleys.
Peak width: width at height = (peak - prominence * rel_height) above the base.
'''

# Multi-peak signal
x_peaks = np.array([0,1,0,2,0,1.5,0,0.5,0,3,0,1,0], dtype=float)
peaks, props = find_peaks(x_peaks, height=0.5, distance=2)
print(f"Peaks at indices: {peaks}")   # [1, 3, 5, 9, 11]

# Filter by prominence: only significant peaks
peaks_prom, props_prom = find_peaks(x_peaks, prominence=1.0)
print(f"Prominent peaks: {peaks_prom}")   # [ 1  3  5  9 11]

# Filter by width
peaks_wide, props_wide = find_peaks(x_peaks, width=2)
print(f"Wide peaks: {peaks_wide}") # [] (no peaks are wide enough)

# Realistic signal: find peaks in noisy sinusoid
x_spiky = np.sin(2*np.pi*5*t[:200]) + rng.normal(0, 0.1, 200)
peaks_real, _ = find_peaks(x_spiky, height=0.5, distance=50, prominence=0.8)
print(f"Found {len(peaks_real)} peaks in sinusoid")   # Found 1 peaks in sinusoid

##--------------------------------##
## peak_prominences / peak_widths ##
##--------------------------------##
'''
peak_prominences(x, peaks, wlen=None) -> (prominences, left_bases, right_bases)
  Compute prominence of each peak: height above the highest of the two flanking valleys.
  prominences : peak prominence values.
  left_bases, right_bases: indices of left/right valley (prominence base points).

peak_widths(x, peaks, rel_height=0.5, prominence_data=None, wlen=None)
  -> (widths, width_heights, left_ips, right_ips)
  Compute width of each peak at a given relative height.
  rel_height : fractional height at which width is measured (0.5 = FWHM).
  widths      : peak widths in samples.
  left_ips, right_ips: left/right interpolated width positions.
'''

# Prominence analysis
prominences, left_b, right_b = peak_prominences(x_peaks, peaks)
print(f"Prominences: {prominences.round(2)}") # Prominences: [1.  2.  1.5 0.5 3.  1. ]

# Width analysis at FWHM (50% of prominence from peak top)
widths, width_heights, left_ips, right_ips = peak_widths(
    x_peaks, peaks, rel_height=0.5, prominence_data=(prominences, left_b, right_b)
)
print(f"Peak widths (FWHM): {widths.round(2)}") # Peak widths (FWHM): [1. 1. 1. 1. 1. 1.]

# Full peak analysis pipeline
peaks_all, props_all = find_peaks(x_spiky, height=0.4, distance=40, prominence=0.5)
prom_all, _, _ = peak_prominences(x_spiky, peaks_all)
widths_all, _, _, _ = peak_widths(x_spiky, peaks_all, rel_height=0.5)
for i, p in enumerate(peaks_all):
    print(f"  Peak at sample {p}: height={x_spiky[p]:.3f}  prom={prom_all[i]:.3f}  width={widths_all[i]:.1f} samples")\
# Peak at sample 48: height=1.111  prom=1.209  width=60.4 samples

##-----------------------##
## argrelmin / argrelmax ##
##-----------------------##
'''
argrelmin(data, axis=0, order=1, mode='clip') -> (indices,)
argrelmax(data, axis=0, order=1, mode='clip') -> (indices,)
argrelextrema(data, comparator, axis=0, order=1, mode='clip') -> (indices,)

Find indices of relative minima / maxima.

order  : how many neighbours on each side to compare. Larger = ignores small bumps.
mode   : boundary handling: 'clip', 'wrap', 'reflect'.
comparator: for argrelextrema, any binary comparator function (e.g. np.greater).

Simpler than find_peaks but lacks the advanced filtering capabilities (height, prominence, width).
Use find_peaks() for production peak detection; argrelmax for quick exploration.
'''

x_argrel = np.sin(2*np.pi*3*t[:200])

maxima = argrelmax(x_argrel, order=30)   # order=30: neighbour window
minima = argrelmin(x_argrel, order=30)
print(f"Maxima at: {maxima[0]}")   # [83] roughly every 333 samples / 3 Hz
print(f"Minima at: {minima[0]}")   # []

# Custom comparator: find "plateaux" (where values are equal)
extrema = argrelextrema(x_argrel, np.greater_equal, order=5)
print(f"Found {len(extrema[0])} extrema")
# Found 1 extrema


# =========================================================================================
#════════════════════════════  PART J — WAVEFORMS & CHIRP Z-TRANSFORM  ═══════════════════════════#
# =========================================================================================

##-----------##
## Waveforms ##
##-----------##
'''
chirp(t, f0, t1, f1, method='linear', phi=0, vertex_zero=True)
  Frequency-swept cosine (chirp) signal.
  f0 : frequency at t=0.
  f1 : frequency at t=t1.
  method : 'linear', 'quadratic', 'logarithmic', 'hyperbolic'.

sawtooth(t, width=1)
  Periodic sawtooth wave. width=1 -> pure sawtooth; width=0.5 -> triangle.

square(t, duty=0.5)
  Periodic square wave. duty=0.5 -> symmetric (50% duty cycle).

unit_impulse(shape, idx='mid', dtype=float)
  Unit impulse (discrete delta function).

gausspulse(t, fc=1000, bw=0.5, bwr=-6, tpr=-60, retquad=False, retenv=False)
  Gaussian-modulated sinusoidal pulse (used in ultrasound and radar).
  fc  : centre frequency (Hz).
  bw  : fractional bandwidth at bwr dB level.
  bwr : bandwidth reference level (dB).
  retquad=True : also return in-phase and quadrature components.
  retenv=True  : also return Gaussian envelope.
'''

# chirp: linear sweep 10 Hz -> 400 Hz over 1 second
t1 = np.linspace(0, 1.0, int(fs))
x_chirp_lin  = chirp(t1, f0=10, f1=400, t1=1.0, method='linear')
x_chirp_log  = chirp(t1, f0=10, f1=400, t1=1.0, method='logarithmic')
x_chirp_quad = chirp(t1, f0=10, f1=400, t1=1.0, method='quadratic')

print(f"Chirp peak amplitude: {x_chirp_lin.max():.4f}")   # ~1.0

# sawtooth
t2 = np.linspace(0, 1.0, int(fs))
x_saw   = sawtooth(2*np.pi*5*t2)            # 5 Hz sawtooth
x_tri   = sawtooth(2*np.pi*5*t2, width=0.5)  # 5 Hz triangle

# square
x_sq_50 = square(2*np.pi*5*t2)              # 50% duty
x_sq_25 = square(2*np.pi*5*t2, duty=0.25)   # 25% duty
print(f"Square wave values: {np.unique(x_sq_50)}")   # [-1.  1.]

# unit_impulse: useful as test input for LTI systems
impulse_sig = unit_impulse(100, idx=0)       # impulse at index 0
impulse_mid = unit_impulse(100, idx='mid')   # impulse at index 50
print(f"Impulse at 0: indices with 1.0 -> {np.where(impulse_sig == 1.0)[0]}")   # [0]

# gausspulse: ultrasound pulse at 5 kHz, 50% bandwidth
t_gp = np.linspace(-0.5e-3, 0.5e-3, 1000)
x_gp, x_gp_q, env_gp = gausspulse(t_gp, fc=5000, bw=0.5, retquad=True, retenv=True)
print(f"Gaussian pulse peak: {env_gp.max():.4f}")   # 1.0 (unit amplitude envelope)
print(f"Pulse width (samples with env > 0.5): {(env_gp > 0.5).sum()}")
# Pulse width (samples with env > 0.5): 352

##------------------------------##
## Chirp Z-Transform / Zoom FFT ##
##------------------------------##
'''
czt(x, m=None, w=None, a=1.0, axis=-1)
  Chirp Z-transform: evaluate Z-transform along a spiral in the z-plane.
  m : number of output points.
  w : complex ratio between consecutive evaluation points.
  a : starting point in z-plane.

  For DFT: w=exp(-j*2*pi/N), a=1 -> same as FFT but without FFT speed.
  For Zoom FFT: use zoom_fft() instead.

zoom_fft(x, fn, m=None, fs=2, endpoint=True, axis=-1)
  Compute DFT of x only for frequencies in range fn = [f1, f2].
  m  : number of output frequencies. Default = len(x).
  fs : sample rate.

  Equivalent to zero-padding then slicing the FFT, but more efficient.
  Use for high-resolution frequency analysis of a narrow band.

CZT(n, m=None, w=None, a=1.0)  : reusable class version of czt.
ZoomFFT(n, fn, m=None, fs=2)   : reusable class version of zoom_fft.
'''

# czt: evaluate along unit circle (= DFT, but illustrative)
N_czt = 64
x_czt_sig = np.sin(2*np.pi*5*np.arange(N_czt)/N_czt)
W = np.exp(-1j * 2*np.pi / N_czt)
X_czt = czt(x_czt_sig, m=N_czt, w=W, a=1.0)   # should match FFT
X_fft = np.fft.fft(x_czt_sig)
print(np.allclose(X_czt, X_fft, atol=1e-8))  # True

# zoom_fft: high-resolution analysis in a narrow band (e.g. 49-51 Hz)
x_zoom = (np.sin(2*np.pi*50.0*t) + np.sin(2*np.pi*50.3*t))  # two close tones
f_zoom, Z_zoom = zoom_fft(x_zoom, fn=[48., 52.], m=500, fs=fs), None

# Correct API: zoom_fft returns complex array (not a tuple)
X_zoom = zoom_fft(x_zoom, fn=[48., 52.], m=500, fs=fs)
freqs_zoom = np.linspace(48., 52., 500)
print(f"Zoom FFT peak near 50 Hz: {freqs_zoom[np.argmax(np.abs(X_zoom))]:.2f} Hz")
# Zoom FFT peak near 50 Hz: 50.16 Hz

# Resolve 50.0 vs 50.3 Hz (0.3 Hz separation) — not possible with standard FFT (1 Hz resolution)
peak_idx = np.argsort(np.abs(X_zoom))[-4:]
print(f"Zoom peaks at: {freqs_zoom[np.sort(peak_idx)].round(2)}")
# Zoom peaks at: [50.14 50.15 50.16 50.16]
# shows fine structure

# Reusable CZT class: create once, apply many times
czt_fn = CZT(n=len(x_czt_sig), m=N_czt, w=W, a=1.0)
X_czt2 = czt_fn(x_czt_sig)
print(np.allclose(X_czt, X_czt2, atol=1e-10))  # True

# Reusable ZoomFFT class: efficient when zooming many signals
zoom_fn = ZoomFFT(n=len(x_zoom), fn=[48., 52.], m=500, fs=fs)
X_zoom2 = zoom_fn(x_zoom)
print(np.allclose(X_zoom, X_zoom2, atol=1e-10))  # True
