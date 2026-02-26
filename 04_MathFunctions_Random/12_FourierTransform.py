'''
1. Standard FFTs
   + np.fft.fft()             : 1-D discrete Fourier Transform (complex input/output).
   + np.fft.ifft()            : 1-D inverse discrete Fourier Transform.
   + np.fft.fft2()            : 2-D discrete Fourier Transform.
   + np.fft.ifft2()           : 2-D inverse discrete Fourier Transform.
   + np.fft.fftn()            : N-D discrete Fourier Transform.
   + np.fft.ifftn()           : N-D inverse discrete Fourier Transform.

2. Real FFTs  (exploit Hermitian symmetry for real input → ~2x faster / half output size)
   + np.fft.rfft()            : 1-D FFT for real input; returns n//2+1 complex coefficients.
   + np.fft.irfft()           : inverse of rfft(); reconstructs real signal.
   + np.fft.rfft2()           : 2-D FFT for real input.
   + np.fft.irfft2()          : inverse of rfft2().
   + np.fft.rfftn()           : N-D FFT for real input.
   + np.fft.irfftn()          : inverse of rfftn().

3. Hermitian FFTs  (input is Hermitian-symmetric → output is real)
   + np.fft.hfft()            : FFT of a Hermitian-symmetric signal (real spectrum output).
   + np.fft.ihfft()           : inverse of hfft(); returns Hermitian-symmetric coefficients.
   [scipy.fft] hfft2()        : 2-D FFT of a Hermitian complex array.
   [scipy.fft] ihfft2()       : 2-D inverse FFT of a real spectrum.
   [scipy.fft] hfftn()        : N-D FFT of a Hermitian-symmetric signal.
   [scipy.fft] ihfftn()       : N-D inverse FFT of a real spectrum.

4. Helper routines
   + np.fft.fftfreq()         : DFT sample frequencies for fft/ifft output.
   + np.fft.rfftfreq()        : DFT sample frequencies for rfft/irfft output.
   + np.fft.fftshift()        : shift zero-frequency component to center of spectrum.
   + np.fft.ifftshift()       : inverse of fftshift().
   [scipy.fft] next_fast_len(): find next efficient FFT length for zero-padding.
   [scipy.fft] prev_fast_len(): find previous efficient FFT length.

5. Discrete Cosine / Sine Transforms  (scipy.fft — not in numpy.fft)
   + spfft.dct()              : 1-D Discrete Cosine Transform (types I-IV).
   + spfft.idct()             : inverse DCT.
   + spfft.dctn()             : N-D DCT along specified axes.
   + spfft.idctn()            : N-D inverse DCT.
   + spfft.dst()              : 1-D Discrete Sine Transform.
   + spfft.idst()             : inverse DST.
   + spfft.dstn()             : N-D DST along specified axes.
   + spfft.idstn()            : N-D inverse DST.

6. Fast Hankel Transforms  (scipy.fft — not in numpy.fft)
   + spfft.fht()              : fast Hankel transform using logarithmic convolution.
   + spfft.ifht()             : inverse fast Hankel transform.
   + spfft.fhtoffset()        : compute optimal offset for a fast Hankel transform.

7. Workers & backend control  (scipy.fft — not in numpy.fft)
   + spfft.set_workers()      : context manager to set the default number of parallel workers.
   + spfft.get_workers()      : return current default worker count.
   + spfft.set_backend()      : context manager to set a custom FFT backend (e.g. PyFFTW).
   + spfft.set_global_backend(): set a persistent global FFT backend.
'''

import numpy as np
import scipy.fft as spfft

# ── Sample signals ──────────────────────────────────────────────────────────────────────────────
N  = 8                               # number of samples (small — easy to read output)
Fs = 8.0                             # sampling frequency (Hz)
t  = np.arange(N) / Fs              # time axis: [0, 1/8, 2/8, ..., 7/8] seconds

# Pure 1-Hz cosine (real signal)
x_real = np.cos(2 * np.pi * 1.0 * t)
# [ 1.      0.7071  0.     -0.7071 -1.     -0.7071  0.      0.7071]

# Complex-valued signal (1-Hz + i·1-Hz sine)
x_cplx = np.exp(1j * 2 * np.pi * 1.0 * t)  # e^{i·2π·f·t}
# [1.+0.j  0.707+0.707j  0.+1.j  ...]

# 2-D image-like array (4×4)
img = np.array([[1., 2., 3., 4.],
                [5., 6., 7., 8.],
                [9., 10., 11., 12.],
                [13., 14., 15., 16.]])
# array([[ 1.,  2.,  3.,  4.],
#        [ 5.,  6.,  7.,  8.],
#        [ 9., 10., 11., 12.],
#        [13., 14., 15., 16.]])

# Hermitian-symmetric spectrum (designed so its IFFT is real)
# For N=8 real signal, the spectrum has the form [A0, A1, ..., A_{N/2}, conj(A_{N/2-1}), ...]
spectrum_h = np.array([8.+0.j, 4.+0.j, 0.+0.j, 0.+0.j, 0.+0.j])  # one-sided (for irfft)


#-------------------------------------------------------------------------------------------------#
#---------------------------------------- 1. Standard FFTs ---------------------------------------#
#-------------------------------------------------------------------------------------------------#

##################
## np.fft.fft() ##
##################
'''
np.fft.fft() computes the 1-D discrete Fourier Transform (DFT) of a sequence.

Definition: A[k] = Σ_{m=0}^{n-1}  a[m] · exp(-2πi·mk/n)

- Input can be real or complex.
- Output is always complex with length n (or the specified n parameter).
- A[0] is the DC (zero-frequency) component = sum of all samples.
- A[1 : n//2] are positive frequencies; A[n//2+1 :] are negative frequencies (mirrored).
- norm='backward' (default): forward transform unscaled; 'ortho': both scaled by 1/√n.

Amplitude spectrum : np.abs(fft(x))
Power spectrum     : np.abs(fft(x))**2
Phase spectrum     : np.angle(fft(x))
'''

X = np.fft.fft(x_real)

print(X)
# [ 2.22e-16+0.j  4.00+0.j  2.22e-16+0.j  0.+0.j  2.22e-16+0.j
#   0.+0.j  2.22e-16+0.j  4.00-0.j ]
# DC≈0 (cosine has no offset); spike at k=1 and k=7 (positive/negative 1 Hz) with magnitude 4

print(np.abs(X).round(4))
# [0. 4. 0. 0. 0. 0. 0. 4.]
# amplitude spectrum: two spikes at bins 1 and 7 (1 Hz and its mirror)

print(np.fft.fft(x_real, n=16).shape)
# (16,)  — zero-padded to length 16 (interpolates spectrum, does NOT add resolution)

print(np.fft.fft(x_cplx))
# [~0.+0.j  8.+0.j  ~0.+0.j  ...]  spike only at k=1 (single positive frequency, no mirror)

###################
## np.fft.ifft() ##
###################
'''
np.fft.ifft() computes the 1-D inverse DFT.

Definition: a[m] = (1/n) Σ_{k=0}^{n-1} A[k] · exp(2πi·mk/n)

The default 1/n normalization is applied to the inverse (not the forward) transform.
np.fft.ifft(np.fft.fft(x)) ≈ x  (round-trip up to floating-point error).
'''

X = np.fft.fft(x_real)
x_rec = np.fft.ifft(X)

print(x_rec.real.round(4))
# [ 1.      0.7071  0.     -0.7071 -1.     -0.7071  0.      0.7071]
# recovers x_real exactly (imaginary part is ≈ 0 for real input)

print(np.allclose(x_rec.real, x_real))
# True

print(np.fft.ifft(X, norm='ortho'))
# with ortho norm both fft and ifft are scaled by 1/√n

###################
## np.fft.fft2() ##
###################
'''
np.fft.fft2() computes the 2-D DFT of a 2-D array (row-wise, then column-wise).

A[k,l] = Σ_m Σ_n  a[m,n] · exp(-2πi·mk/M) · exp(-2πi·nl/N)

Common use: image frequency analysis, 2-D convolution via multiplication in frequency domain.
'''

IMG = np.fft.fft2(img)

print(IMG.shape)
# (4, 4)  — same shape as input

print(IMG[0, 0])
# (136+0j)  — DC component = sum of all pixels

print(np.abs(IMG).round(2))
# [[136.    11.31   8.    11.31]
#  [ 45.25   0.     0.     0.  ]
#  [ 32.     0.     0.     0.  ]
#  [ 45.25   0.     0.     0.  ]]

print(np.allclose(np.fft.ifft2(IMG), img))
# True  (round-trip)

# s parameter: specify output shape (zero-pads or crops each axis before transform)
IMG_padded = np.fft.fft2(img, s=(8, 8))
print(IMG_padded.shape)
# (8, 8)  — zero-padded to 8×8

####################
## np.fft.ifft2() ##
####################
'''
np.fft.ifft2() computes the 2-D inverse DFT.

Reconstructs the spatial-domain array from its 2-D frequency-domain representation.
ifft2(fft2(a)) ≈ a  (up to floating-point precision).
'''

img_rec = np.fft.ifft2(IMG)

print(img_rec.real.round(4))
# [[ 1.  2.  3.  4.]
#  [ 5.  6.  7.  8.]
#  [ 9. 10. 11. 12.]
#  [13. 14. 15. 16.]]

print(np.allclose(img_rec.real, img))
# True

###################
## np.fft.fftn() ##
###################
'''
np.fft.fftn() computes the N-D DFT of an array.

Applies FFT along each of the specified axes (default: all axes).
fft2 is equivalent to fftn(a, axes=(-2, -1)).

Use: volumetric data (3-D imaging, fluid simulations), tensor signal processing.
'''

vol = np.random.default_rng(0).random((4, 4, 4))  # 3-D volume

VOL = np.fft.fftn(vol)
print(VOL.shape)
# (4, 4, 4)

# Transform only along last two axes (treat first axis as batch)
VOL_2d = np.fft.fftn(vol, axes=(-2, -1))
print(np.allclose(VOL_2d[0], np.fft.fft2(vol[0])))
# True  (same as applying fft2 to each slice)

print(np.allclose(np.fft.ifftn(VOL), vol))
# True  (round-trip)

####################
## np.fft.ifftn() ##
####################
'''
np.fft.ifftn() computes the N-D inverse DFT.

ifftn(fftn(a)) ≈ a  (up to floating-point precision).
axes and norm parameters work the same as fftn.
'''

vol_rec = np.fft.ifftn(VOL)
print(np.allclose(vol_rec.real, vol))
# True


#-------------------------------------------------------------------------------------------------#
#------------------------------------------ 2. Real FFTs -----------------------------------------#
#-------------------------------------------------------------------------------------------------#

###################
## np.fft.rfft() ##
###################
'''
np.fft.rfft() computes the 1-D DFT for real-valued input, exploiting Hermitian symmetry.

For a real signal of length n, the spectrum satisfies A[-k] = conj(A[k]),
so only the non-redundant positive-frequency half is returned:
  output length = n//2 + 1  (includes DC at index 0 and Nyquist at index n//2)

Advantage: ~2x faster than fft() and uses half the memory.
Use rfft whenever the input is real (audio, sensor data, image rows, etc.).
'''

XR = np.fft.rfft(x_real)

print(XR.shape)
# (5,)  — n=8 → 8//2+1 = 5 coefficients (DC, 1 Hz, 2 Hz, 3 Hz, Nyquist)

print(np.abs(XR).round(4))
# [0. 4. 0. 0. 0.]
# only the 1-Hz bin (index 1) is non-zero (amplitude 4 = N/2 for a unit cosine)

print(XR[1])
# (4+0j)  — positive 1-Hz component (cosine → purely real coefficient)

####################
## np.fft.irfft() ##
####################
'''
np.fft.irfft() is the inverse of rfft(); reconstructs a real-valued signal.

Input: complex array of length n//2 + 1.
Output: real array of length n (must specify n explicitly if original length was odd).

irfft assumes the input has Hermitian symmetry; the output is guaranteed real.
'''

x_rec_r = np.fft.irfft(XR, n=N)

print(x_rec_r.round(4))
# [ 1.      0.7071  0.     -0.7071 -1.     -0.7071  0.      0.7071]
# identical to x_real

print(np.allclose(x_rec_r, x_real))
# True

# irfft(rfft(x)) round-trip
print(np.allclose(np.fft.irfft(np.fft.rfft(x_real), n=N), x_real))
# True

####################
## np.fft.rfft2() ##
####################
'''
np.fft.rfft2() computes the 2-D FFT of a real array.

The transform is full along the second-to-last axis and half along the last axis:
  output shape = (..., M, N//2+1)

Use: 2-D image processing, convolution with real filters.
'''

IMG_R = np.fft.rfft2(img)

print(IMG_R.shape)
# (4, 3)  — last axis: 4//2+1 = 3 (not 4)

print(np.allclose(np.fft.irfft2(IMG_R, s=img.shape), img))
# True  (must pass original shape s to irfft2 because length is ambiguous)

#####################
## np.fft.irfft2() ##
#####################
'''
np.fft.irfft2() is the inverse of rfft2(); reconstructs a real 2-D array.

Requires the target output shape s (the original spatial dimensions) to reconstruct correctly.
'''

img_rec_r = np.fft.irfft2(IMG_R, s=(4, 4))

print(img_rec_r.round(4))
# [[ 1.  2.  3.  4.]
#  [ 5.  6.  7.  8.]
#  [ 9. 10. 11. 12.]
#  [13. 14. 15. 16.]]

print(np.allclose(img_rec_r, img))
# True

####################
## np.fft.rfftn() ##
####################
'''
np.fft.rfftn() computes the N-D FFT for real input.

Like rfft2 but generalizes to arbitrary dimensions.
Output is full along all axes except the last, which has size n[-1]//2 + 1.
'''

VOL_R = np.fft.rfftn(vol)
print(VOL_R.shape)
# (4, 4, 3)  — last axis halved: 4//2+1 = 3

print(np.allclose(np.fft.irfftn(VOL_R, s=vol.shape, axes=(0, 1, 2)), vol))
# True

#####################
## np.fft.irfftn() ##
#####################
'''
np.fft.irfftn() is the inverse of rfftn(); reconstructs a real N-D array.

The original shape s must be provided for unambiguous reconstruction.
'''

vol_rec_r = np.fft.irfftn(VOL_R, s=vol.shape, axes=(0, 1, 2))
print(np.allclose(vol_rec_r, vol))
# True


#-------------------------------------------------------------------------------------------------#
#--------------------------------------- 3. Hermitian FFTs ----------------------------------------#
#-------------------------------------------------------------------------------------------------#

##################
## np.fft.hfft() ##
##################
'''
np.fft.hfft() computes the FFT of a signal that is Hermitian-symmetric in the time domain,
producing a real-valued output spectrum.

Input: complex array of length n//2+1 representing a Hermitian half-sequence.
Output: real array of length n (default n = 2*(len(input)-1)).

Key distinction from rfft:
  rfft  : real time-domain signal    → complex half-spectrum  (input real, output complex)
  hfft  : complex Hermitian half-seq → real full spectrum     (input complex, output real)

The Hermitian half-representation of any real signal x is: ihfft(x).
Reconstruct the original signal from it with: hfft(ihfft(x)) ≈ x.

Use: signal reconstruction when you hold only the Hermitian half of the time-domain data.
'''

# ihfft gives the Hermitian half-representation of a real time-domain sequence
half_seq = np.fft.ihfft(x_real)   # shape (5,) complex

print(half_seq.round(4))
# [-0.+0.j  0.5-0.j  0.+0.j  0.+0.j  0.+0.j]
# compact Hermitian description of x_real (only n//2+1 points needed)

x_from_hfft = np.fft.hfft(half_seq)  # reconstruct x_real from its Hermitian half

print(x_from_hfft.round(4))
# [ 1.      0.7071  0.     -0.7071 -1.     -0.7071  0.      0.7071]
# recovers x_real exactly

print(x_from_hfft.shape)
# (8,)  — output length = 2*(5-1) = 8

print(np.allclose(x_from_hfft, x_real))
# True

###################
## np.fft.ihfft() ##
###################
'''
np.fft.ihfft() is the inverse of hfft().

Takes a real spectrum (output of hfft) and returns a complex Hermitian half-spectrum.
ihfft(hfft(a)) ≈ a.

ihfft is numerically equivalent to np.conj(rfft(a)) / n.
'''

half_seq_rec = np.fft.ihfft(x_from_hfft)

print(half_seq_rec.round(4))
# [-0.+0.j  0.5-0.j  0.+0.j  0.+0.j  0.+0.j]

print(np.allclose(half_seq_rec, half_seq))
# True

# [scipy.fft] hfft2 / ihfft2 / hfftn / ihfftn — 2-D and N-D extensions
# hfft2(x)  : 2-D FFT of Hermitian complex array → real output
# ihfft2(x) : 2-D inverse; input is a real spectrum, output is complex Hermitian
# hfftn(x)  : N-D version of hfft2
# ihfftn(x) : N-D version of ihfft2
# These mirror the rfft2/irfft2 family but for the "transposed" Hermitian case.

half_spec_2d = spfft.ihfft2(img)     # real image → Hermitian half-spectrum
img_from_hfft2 = spfft.hfft2(half_spec_2d, s=img.shape)

print(np.allclose(img_from_hfft2, img))
# True


#-------------------------------------------------------------------------------------------------#
#--------------------------------------- 4. Helper routines --------------------------------------#
#-------------------------------------------------------------------------------------------------#

#####################
## np.fft.fftfreq() ##
#####################
'''
np.fft.fftfreq() returns the DFT sample frequencies corresponding to fft/ifft output bins.

fftfreq(n, d=1.0) returns an array of length n:
  - bins 0 to n//2-1    : positive frequencies  [0, 1/nd, 2/nd, ...]
  - bin  n//2            : Nyquist frequency (negative for even n in standard convention)
  - bins n//2+1 to n-1  : negative frequencies  [..., -2/nd, -1/nd]

d : sample spacing (seconds). freq unit = 1/d (Hz if d is in seconds).
Use: labeling the x-axis of a spectrum plot, frequency-domain filtering.
'''

freqs = np.fft.fftfreq(N, d=1.0/Fs)

print(freqs)
# [ 0.  1.  2.  3. -4. -3. -2. -1.]
# frequencies in Hz: 0, ±1, ±2, ±3, and Nyquist −4 (=+4 Hz)

# Amplitude spectrum with correct frequency labels
X_full = np.fft.fft(x_real)
for f, a in zip(freqs, np.abs(X_full).round(2)):
    print(f"{f:+.0f} Hz : {a}")
#  +0 Hz : 0.0
#  +1 Hz : 4.0   ← 1-Hz cosine component
#  +2 Hz : 0.0
#  +3 Hz : 0.0
#  -4 Hz : 0.0
#  -3 Hz : 0.0
#  -2 Hz : 0.0
#  -1 Hz : 4.0   ← mirror (negative frequency)

######################
## np.fft.rfftfreq() ##
######################
'''
np.fft.rfftfreq() returns the DFT sample frequencies for rfft/irfft output.

Returns only the non-negative frequencies (length n//2 + 1).
rfftfreq(n, d) = fftfreq(n, d)[:n//2 + 1]

Use: labeling the x-axis of rfft amplitude spectra (always non-negative).
'''

rfreqs = np.fft.rfftfreq(N, d=1.0/Fs)

print(rfreqs)
# [0. 1. 2. 3. 4.]  — DC through Nyquist, no negatives

XR = np.fft.rfft(x_real)
for f, a in zip(rfreqs, np.abs(XR).round(2)):
    print(f"{f:.0f} Hz : {a}")
# 0 Hz : 0.0
# 1 Hz : 4.0   ← the 1-Hz cosine component (amplitude = N/2 = 4)
# 2 Hz : 0.0
# 3 Hz : 0.0
# 4 Hz : 0.0

#####################
## np.fft.fftshift() ##
#####################
'''
np.fft.fftshift() shifts the zero-frequency component to the center of the array.

Without fftshift: [DC, pos_freqs..., neg_freqs...]
After  fftshift:  [neg_freqs..., DC, pos_freqs...]

Useful for displaying a centered spectrum (standard in signal processing plots).
For 2-D arrays, the shift is applied along all axes by default.
'''

X_shifted = np.fft.fftshift(np.fft.fft(x_real))
freqs_shifted = np.fft.fftshift(freqs)

print(freqs_shifted)
# [-4. -3. -2. -1.  0.  1.  2.  3.]  — centered, monotonically increasing

print(np.abs(X_shifted).round(2))
# [0. 0. 0. 4. 0. 4. 0. 0.]  — symmetric around center (bin 3 → -1 Hz, bin 5 → +1 Hz)

# 2-D example: shift image spectrum to center
IMG_shifted = np.fft.fftshift(np.fft.fft2(img))
print(IMG_shifted[2, 2])  # DC at center
# (136+0j)

######################
## np.fft.ifftshift() ##
######################
'''
np.fft.ifftshift() undoes fftshift — moves the zero-frequency component back to index 0.

Must be applied before calling fft/ifft if the array has been fftshifted.
ifftshift(fftshift(x)) == x (exactly, not just approximately).
'''

X_unshifted = np.fft.ifftshift(X_shifted)

print(np.allclose(X_unshifted, np.fft.fft(x_real)))
# True  — restored to standard fft output order

# Common workflow: display centered, then unshift before ifft
x_recovered = np.fft.ifft(np.fft.ifftshift(X_shifted))
print(np.allclose(x_recovered.real, x_real))
# True

# [scipy.fft] next_fast_len() / prev_fast_len()
# FFT is most efficient when n is a product of small prime factors (2, 3, 5, 7, 11, 13).
# next_fast_len(n) finds the smallest such number >= n for zero-padding.

print(spfft.next_fast_len(100))
# 100  (100 = 4 × 25 = 2^2 × 5^2 — already fast)

print(spfft.next_fast_len(101))
# 105  (= 3 × 5 × 7, next fast length above 101)

print(spfft.next_fast_len(1000))
# 1000  (= 8 × 125 = 2^3 × 5^3)

print(spfft.next_fast_len(1001))
# 1008  (= 2^4 × 3^2 × 7)

# Practical zero-padding workflow for fast convolution
x_long = np.random.default_rng(1).random(997)   # awkward prime-ish length
n_fft = spfft.next_fast_len(len(x_long))
X_fast = spfft.rfft(x_long, n=n_fft)            # padded to fast length before FFT
print(n_fft)
# 1000


#-------------------------------------------------------------------------------------------------#
#--------------------- 5. Discrete Cosine / Sine Transforms  (scipy.fft) ------------------------#
#-------------------------------------------------------------------------------------------------#

################
## spfft.dct() ##
################
'''
spfft.dct() computes the Discrete Cosine Transform (DCT) of a real sequence.

Four types (type=1..4); type-II is the default and most widely used:
  DCT-II: X[k] = 2 Σ_{n=0}^{N-1} x[n] cos(π·k·(2n+1) / (2N))   k=0..N-1

Key properties:
  - Works on real input, output is real.
  - Energy compaction: most energy concentrated in a few low-frequency coefficients.
  - Widely used in lossy compression: JPEG (2-D DCT-II on 8×8 blocks), MP3, AAC.
  - DCT-II and DCT-III are inverses of each other (up to a normalization factor).
  - norm='ortho' produces an orthonormal DCT useful for whitening / PCA analogy.
'''

x_dc = np.array([1., 2., 3., 4., 5., 6., 7., 8.])

X_dct = spfft.dct(x_dc)

print(X_dct.round(4))
# [ 72.     -25.7693   0.      -2.6938   0.      -0.8036   0.      -0.2028]
# Large DC coefficient (X[0] = 2*sum(x) = 72) dominates; energy compaction

X_dct_ortho = spfft.dct(x_dc, norm='ortho')
print(X_dct_ortho.round(4))
# [12.7279  -6.4423   0.      -0.6735   0.      -0.2009   0.      -0.0507]

# DCT-I (type=1): both endpoints included in the sum
print(spfft.dct(x_dc, type=1).round(4))
# [ 63.     -20.1957   0.      -2.5724   0.      -1.2319   0.      -1.    ]

# Verify energy compaction: most power in first few coefficients
print((X_dct_ortho**2).round(2))
# [162.     41.5     0.       0.45    0.       0.04    0.       0.  ]  — concentrated at low k

#################
## spfft.idct() ##
#################
'''
spfft.idct() computes the inverse DCT.

idct(dct(x, type=2), type=2) ≈ x  (up to floating-point error).
DCT-III is the inverse of DCT-II when both use the default (unnormalized) convention.
Using norm='ortho' makes dct and idct exactly each other's inverse.
'''

x_rec_dct = spfft.idct(X_dct)

print(x_rec_dct.round(4))
# [1. 2. 3. 4. 5. 6. 7. 8.]  — exact recovery

print(np.allclose(x_rec_dct, x_dc))
# True

# ortho norm: perfect round-trip without any scaling
x_rec_ortho = spfft.idct(X_dct_ortho, norm='ortho')
print(np.allclose(x_rec_ortho, x_dc))
# True

#################
## spfft.dctn() ##
#################
'''
spfft.dctn() computes the N-D DCT along specified axes.

Applies 1-D DCT successively along each axis in axes (default: all axes).
Used in image/video compression: JPEG applies 2-D DCT-II to 8×8 pixel blocks.
'''

img_small = np.array([[1., 2., 3., 4.],
                      [5., 6., 7., 8.],
                      [9., 10., 11., 12.],
                      [13., 14., 15., 16.]])

DCT2D = spfft.dctn(img_small, norm='ortho')

print(DCT2D.round(4))
# [[68.       0.       0.       0.    ]
#  [-0.       0.       0.       0.    ]
#  [16.      -0.       0.      -0.    ]
#  [-0.       0.       0.       0.    ]]
# DC-dominated: most energy in top-left corner (JPEG compression exploits this)

print(np.allclose(spfft.idctn(DCT2D, norm='ortho'), img_small))
# True

# JPEG-style: process 8×8 blocks
block = np.random.default_rng(0).integers(0, 256, (8, 8)).astype(float) - 128  # center
DCT_block = spfft.dctn(block, norm='ortho')
# Zero small coefficients (lossy step)
DCT_block[np.abs(DCT_block) < 5] = 0
img_approx = spfft.idctn(DCT_block, norm='ortho')
print(img_approx.shape)
# (8, 8)  — reconstructed (lossy) block

#######################
## spfft.dst() / idst() ##
#######################
'''
spfft.dst() computes the Discrete Sine Transform (DST) of a real sequence.

DST-II (default): X[k] = 2 Σ_{n=0}^{N-1} x[n] sin(π·k·(2n+1) / (2N))  k=1..N

Key differences from DCT:
  - Uses sine basis functions instead of cosine.
  - Implicitly assumes odd symmetry at the boundaries (x[-1] = -x[0]).
  - Useful in solving PDEs with Dirichlet boundary conditions (zero endpoints).

idst() is the inverse of dst() (same type).
'''

X_dst = spfft.dst(x_dc, norm='ortho')
print(X_dst.round(4))
# [10.0022  -4.2761   0.8839  -0.3   ...] (sine-weighted coefficients)

x_rec_dst = spfft.idst(X_dst, norm='ortho')
print(np.allclose(x_rec_dst, x_dc))
# True

# dstn / idstn: N-D DST (same pattern as dctn / idctn)
DST2D = spfft.dstn(img_small, norm='ortho')
print(np.allclose(spfft.idstn(DST2D, norm='ortho'), img_small))
# True


#-------------------------------------------------------------------------------------------------#
#--------------------------- 6. Fast Hankel Transforms  (scipy.fft) ------------------------------#
#-------------------------------------------------------------------------------------------------#

################
## spfft.fht() ##
################
'''
spfft.fht() computes the Fast Hankel Transform (FHT) via logarithmic convolution.

The Hankel transform of order ν of f(r):
  F(k) = ∫_0^∞ f(r) J_ν(kr) r dr

where J_ν is the Bessel function of the first kind.

Parameters:
  a    : input array (samples of f(r) on logarithmically-spaced points)
  dln  : uniform logarithmic spacing Δ(ln r) between samples
  mu   : order ν of the Hankel transform (Bessel function order)
  offset: log-offset of the transform (related to the pivot point)
  bias : power-law bias parameter q (for biased FHT; default 0)

Use: 2-D radially-symmetric problems (cosmology power spectra, optics, radial Schrödinger eq.)
'''

# Gaussian example: Hankel transform of a Gaussian f(r) = exp(-r^2/2)
# Known analytically: F(k) = exp(-k^2/2) for order 0

n_pts = 64
dln = 0.1                                   # log-spacing
mu  = 0.0                                   # order-0 Hankel transform

# Compute the optimal offset for this transform
offset = spfft.fhtoffset(dln, mu)
print(offset)
# 0.0  (or a small value depending on dln and mu)

# Log-spaced radius array
r = np.exp(offset + dln * np.arange(n_pts))

a = np.exp(-0.5 * r**2)                    # Gaussian in real space

A = spfft.fht(a, dln, mu)                  # Hankel transform

# k-space sampling points (same log-spacing, same offset)
k = np.exp(-offset + dln * (np.arange(n_pts) - (n_pts - 1)))
k = k[::-1]

print(A[:5].round(6))
# small values (edge of transform); center bins approximate exp(-k^2/2)

#################
## spfft.ifht() ##
#################
'''
spfft.ifht() is the inverse Fast Hankel Transform.

ifht(fht(a, dln, mu), dln, mu) ≈ a  (round-trip).
Same parameters as fht(); uses the same logarithmic convolution approach in reverse.
'''

a_rec = spfft.ifht(A, dln, mu)

print(np.allclose(a_rec, a, atol=1e-6))
# True  (round-trip recovery)

######################
## spfft.fhtoffset() ##
######################
'''
spfft.fhtoffset() returns the optimal offset for a Fast Hankel Transform.

The offset is chosen to minimize aliasing artefacts by centering the transform kernel.
Should always be used to construct the r/k grids before calling fht/ifht.

Parameters:
  dln     : logarithmic spacing
  mu      : Hankel transform order
  initial : starting guess for the offset (default 0)
  bias    : power-law bias exponent q (for biased FHT)
'''

for order in [0.0, 0.5, 1.0]:
    off = spfft.fhtoffset(dln=0.05, mu=order)
    print(f"mu={order}  offset={off:.6f}")
# mu=0.0  offset=-0.009496  (or similar small value depending on dln)
# mu=0.5  offset=0.002973
# mu=1.0  offset=0.015378


#-------------------------------------------------------------------------------------------------#
#------------------------- 7. Workers & backend control  (scipy.fft) ----------------------------#
#-------------------------------------------------------------------------------------------------#

######################
## spfft.set_workers() ##
######################
'''
spfft.set_workers() is a context manager that sets the default number of parallel workers
used internally by scipy.fft transforms.

workers > 0 : use that many threads.
workers = -1: use all available CPU cores.
workers = 1 : single-threaded (default behaviour).

Only scipy.fft (not numpy.fft) supports multi-threaded FFTs.
Use for large transforms where parallelism provides a meaningful speedup.
'''

print(spfft.get_workers())
# 1  (default: single-threaded)

# Temporarily use all available cores for a large transform
large_signal = np.random.default_rng(0).random(2**20)

with spfft.set_workers(-1):
    print(spfft.get_workers())   # number of logical CPUs on this machine
    X_large = spfft.rfft(large_signal)

print(spfft.get_workers())
# 1  (restored to default after the context block)

#######################
## spfft.set_backend() ##
#######################
'''
spfft.set_backend() is a context manager that sets a custom FFT backend (e.g. PyFFTW).

scipy.fft uses a UAF (uarray) dispatch system; any compliant backend can be plugged in.

Usage (requires pip install pyfftw):
  import pyfftw
  with spfft.set_backend(pyfftw.interfaces.scipy_fft):
      X = spfft.fft(x)   # uses PyFFTW instead of scipy internals

set_global_backend(backend) sets the backend permanently for the process.
register_backend(backend) registers a backend to be tried before the default.

Arguments:
  backend : a UAF-compatible backend object.
  coerce  : if True, coerce input arrays to the backend's native type.
  only    : if True, raise an error if the backend doesn't support the call.
'''

# Demonstrate the dispatch machinery (no external backend required)
print(type(spfft.fft(x_real)))
# <class 'numpy.ndarray'>  (scipy.fft returns numpy arrays by default)

# With a custom backend (illustrative — PyFFTW not necessarily installed):
# import pyfftw
# spfft.set_global_backend(pyfftw.interfaces.scipy_fft)
# X = spfft.fft(large_signal)   # now uses PyFFTW globally

# skip_backend: temporarily disable a specific backend within a scope
# with spfft.skip_backend(my_backend):
#     X = spfft.fft(x)   # falls through to next available backend
