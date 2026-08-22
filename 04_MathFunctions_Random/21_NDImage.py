'''
scipy.ndimage  —  Multidimensional Image Processing
=====================================================

All functions work on N-dimensional arrays (1-D, 2-D, 3-D, …).
"Image" is just a 2-D convention; the same functions work on volumes and
higher-dimensional arrays without modification.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART A — FILTERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 1. convolve / correlate / convolve1d / correlate1d : linear convolution
 2. gaussian_filter / gaussian_filter1d             : Gaussian smoothing (any order)
 3. uniform_filter / uniform_filter1d               : box (moving-average) filter
 4. median_filter                                   : robust smoothing
 5. rank_filter / percentile_filter                 : generalised order filters
 6. maximum_filter / minimum_filter                 : dilation / erosion in greyscale
 7. sobel / prewitt                                 : gradient edge detection
 8. gaussian_gradient_magnitude / gaussian_laplace / laplace : derivative filters
 9. generic_filter / vectorized_filter              : custom kernel functions

PART B — FOURIER FILTERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10. fourier_gaussian / fourier_uniform / fourier_ellipsoid / fourier_shift

PART C — INTERPOLATION / GEOMETRIC TRANSFORMS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
11. zoom                : scale an array up or down
12. rotate              : rotate an array by angle
13. shift               : translate an array by a fractional shift
14. affine_transform    : arbitrary affine warp (rotation + scale + shear + translate)
15. map_coordinates     : interpolate at arbitrary coordinate arrays
16. geometric_transform : fully custom coordinate mapping
17. spline_filter       : pre-compute spline coefficients for repeated resampling

PART D — MEASUREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
18. label / find_objects                      : connected component labelling
19. sum_labels / mean / median / variance / standard_deviation / extrema / histogram
20. center_of_mass / maximum_position / minimum_position
21. labeled_comprehension / value_indices
22. watershed_ift

PART E — MORPHOLOGY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
23. generate_binary_structure / iterate_structure
24. binary_erosion / binary_dilation / binary_opening / binary_closing
25. binary_fill_holes / binary_hit_or_miss / binary_propagation
26. grey_erosion / grey_dilation / grey_opening / grey_closing
27. morphological_gradient / morphological_laplace / white_tophat / black_tophat
28. distance_transform_edt / distance_transform_cdt / distance_transform_bf

Shared keyword arguments across most functions:
  mode      : boundary handling — 'reflect' (default), 'constant', 'nearest',
              'mirror', 'wrap'. Controls what values appear outside the array.
  cval      : fill value when mode='constant'. Default 0.0.
  output    : dtype or pre-allocated array for the result. Default None (allocate).
  order     : spline interpolation order (0–5). 0=nearest, 1=linear, 3=cubic (default).
  axes      : restrict operation to specific axes (not all functions support this).
'''

import numpy as np
import scipy.ndimage as ndi

rng = np.random.default_rng(0)

# ── Shared test arrays ──────────────────────────────────────────────────────────────────────────
img   = rng.normal(0, 1, (64, 64))                # float 2-D image
img3d = rng.normal(0, 1, (16, 32, 32))             # float 3-D volume

# Binary mask with two blobs
blob = np.zeros((20, 20), dtype=bool)
blob[3:8, 3:8]   = True   # first blob
blob[12:17, 12:17] = True # second blob

# Labelled array: 0=background, 1=first region, 2=second region
labels_arr = np.zeros((20, 20), dtype=int)
labels_arr[3:8, 3:8]    = 1
labels_arr[12:17, 12:17] = 2
vals_arr = rng.uniform(0, 10, (20, 20))   # values to measure over regions


# =========================================================================================
#  PART A — FILTERS 
# =========================================================================================

##-------------------------##
## 1. convolve / correlate ##
##-------------------------##
'''
ndi.convolve(input, weights, output=None, mode='reflect', cval=0.0, origin=0)
ndi.correlate(input, weights, output=None, mode='reflect', cval=0.0, origin=0)

N-D convolution / cross-correlation with a given weights kernel.

convolve : output[i] = sum_k  input[i - k] * weights[k]   (kernel is FLIPPED)
correlate: output[i] = sum_k  input[i + k] * weights[k]   (kernel NOT flipped)
For symmetric kernels (e.g. Gaussian, box) they produce the same result.

weights : the kernel array. Same number of dimensions as input, or any shape
          that is broadcastable to a sub-volume.

mode (boundary handling):
  'reflect'  : [d c b | a b c d | c b a]   — reflects around the edge (default).
  'constant' : [0 0 0 | a b c d | 0 0 0]   — pad with cval (typically 0).
  'nearest'  : [a a a | a b c d | d d d]   — extend with the nearest border pixel.
  'mirror'   : [c b a | a b c d | d c b]   — reflect including the edge pixel.
  'wrap'     : [b c d | a b c d | a b c]   — periodic / toroidal.

origin : shift the kernel by this many pixels (integer or sequence). Default 0.

convolve1d / correlate1d: apply a 1-D kernel along a specified axis only
  (much faster than a full N-D kernel when the filter is separable).
'''

# 2-D: convolve with a 3×3 mean (box) kernel
mean_kernel = np.ones((3, 3)) / 9.0
img_conv = ndi.convolve(img, mean_kernel)
print(img_conv.shape)    # (64, 64) — same shape as input

# convolve vs correlate with an asymmetric kernel
asym = np.array([[0, 0, 1], [0, 0, 0], [0, 0, 0]])   # single non-zero at [0,2]
img_c  = ndi.convolve(img, asym)    # output[r,c] = input[r, c-2]  -> content appears shifted right
img_cr = ndi.correlate(img, asym)   # output[r,c] = input[r, c+2]  -> content appears shifted left
# convolve: output at (r,c) samples from input at (r, c-2) i.e. shifts content +2 cols (right)
print(np.allclose(img_c[:-1, 1:], img[1:, :-1], atol=1e-10))   # True (interior, reflect mode)

# mode='constant', cval=0: sharp borders (zeros outside)
img_const = ndi.convolve(img, mean_kernel, mode='constant', cval=0.0)
img_refl  = ndi.convolve(img, mean_kernel, mode='reflect')
print(np.abs(img_const[0, :] - img_refl[0, :]).max().round(4))  # 0.58 differs at boundaries

# convolve1d: apply a 1-D kernel along axis=1 (columns)
row_kernel = np.array([0.25, 0.5, 0.25])
img_1d_col = ndi.convolve1d(img, row_kernel, axis=1)  # smooth along columns
img_1d_row = ndi.convolve1d(img, row_kernel, axis=0)  # smooth along rows

# Separable 2-D Gaussian: apply 1-D Gaussian along each axis independently
sigma = 2.0
g1d = np.exp(-0.5 * (np.arange(-6, 7) / sigma)**2)
g1d /= g1d.sum()
img_sep = ndi.convolve1d(ndi.convolve1d(img, g1d, axis=0), g1d, axis=1)

# 3-D: convolve a volume with a small averaging kernel
kern_3d = np.ones((3, 3, 3)) / 27.0
vol_conv = ndi.convolve(img3d, kern_3d)
print(vol_conv.shape)   # (16, 32, 32)

# origin parameter: shift the kernel position
# origin=1 moves the kernel 1 pixel to the right
img_shifted = ndi.convolve1d(img, row_kernel, axis=1, origin=1)

##----------------------------------------##
## 2. gaussian_filter / gaussian_filter1d ##
##----------------------------------------##
'''
ndi.gaussian_filter(input, sigma, order=0, output=None, mode='reflect', cval=0.0,
                    truncate=4.0, radius=None, axes=None)

Apply a Gaussian filter (N-D separable).

sigma  : standard deviation of the Gaussian. Scalar (same for all axes) or
         sequence of floats (one per axis).
order  : 0 = smoothing (Gaussian itself).
         1 = first derivative of Gaussian (gradient along each axis).
         2 = second derivative (used for Laplacian-of-Gaussian detection).
         Sequence: different order per axis.
truncate: how many sigma to extend the kernel. Default 4.0.
          Larger = more accurate but slower; smaller = faster but loses tails.
axes   : restrict to specific axes (new in 1.15). None = all axes.

gaussian_filter1d(input, sigma, axis=-1, order=0, ...): apply along one axis.
'''

# Basic smoothing
img_gauss1 = ndi.gaussian_filter(img, sigma=1.0)
img_gauss3 = ndi.gaussian_filter(img, sigma=3.0)   # more blurred

# Verify smoothing reduces std of noise
print(f"Original std:  {img.std():.4f}") # 0.9976
print(f"Gauss1 std:    {img_gauss1.std():.4f}")    # 0.2922 smaller
print(f"Gauss3 std:    {img_gauss3.std():.4f}")    # 0.1062 even smaller

# Anisotropic: different sigma per axis
img_aniso = ndi.gaussian_filter(img, sigma=(5.0, 1.0))  # heavy along rows, light along cols

# Gradient (order=1 along one axis, 0 along others)
# dI/dx: derivative along axis=1 (columns)
grad_x = ndi.gaussian_filter(img, sigma=1.0, order=[0, 1])  # order per axis
grad_y = ndi.gaussian_filter(img, sigma=1.0, order=[1, 0])
gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)

# Laplacian of Gaussian (LoG): order=2 summed over all axes
log_x = ndi.gaussian_filter(img, sigma=2.0, order=[2, 0])
log_y = ndi.gaussian_filter(img, sigma=2.0, order=[0, 2])
log   = log_x + log_y   # Laplacian of Gaussian = blob detector

# gaussian_filter1d: same but one axis at a time
g1d_row = ndi.gaussian_filter1d(img, sigma=2.0, axis=0)
g1d_col = ndi.gaussian_filter1d(img, sigma=2.0, axis=1)
# Sequential application = 2-D gaussian_filter(sigma=2.0)
g1d_both = ndi.gaussian_filter1d(g1d_row, sigma=2.0, axis=1)
gauss_2d  = ndi.gaussian_filter(img, sigma=2.0)
print(np.allclose(g1d_both, gauss_2d, atol=1e-10))  # True

# 3-D volume smoothing
vol_gauss = ndi.gaussian_filter(img3d, sigma=1.5)
print(vol_gauss.shape)  # (16, 32, 32)

# Derivative of Gaussian for edge/ridge detection in 3-D
vol_grad_z = ndi.gaussian_filter1d(img3d, sigma=1.5, axis=0, order=1)


##--------------------------------------##
## 3. uniform_filter / uniform_filter1d ##
##--------------------------------------##
'''
ndi.uniform_filter(input, size=3, output=None, mode='reflect', cval=0.0,
                   origin=0, axes=None)

Box (moving-average) filter: each output pixel is the mean of the surrounding
size x size (x size …) neighbourhood.

size : neighbourhood side length. Scalar or sequence (one per axis).
       Must be a positive integer.

uniform_filter1d(input, size, axis=-1, ...): 1-D box filter along one axis.

Advantages over Gaussian:
  - Exactly flat frequency response across passband (in contrast to Gaussian taper).
  - Faster for integer kernels.
  - uniform_filter(size=3) applied n times approximates gaussian_filter(sigma~sqrt(n/3)).

Disadvantage: non-zero sidelobes in frequency domain (ringing possible for large sizes).
'''

# 2-D box filter: 5×5 neighbourhood
img_box5 = ndi.uniform_filter(img, size=5)
print(img_box5.shape)   # (64, 64)

# Anisotropic: 7-wide along rows, 3-wide along columns
img_box_aniso = ndi.uniform_filter(img, size=(7, 3))

# Iterated box → approximates Gaussian
img_box3 = ndi.uniform_filter(img, size=3)
img_box3x3 = ndi.uniform_filter(img_box3, size=3)   # 2 passes
img_box3x3x3 = ndi.uniform_filter(img_box3x3, size=3)  # 3 passes
# 3 passes of size=3 ≈ gaussian_filter(sigma~1)
img_gauss_approx = ndi.gaussian_filter(img, sigma=1.0)
print(f"Box x 3 vs Gaussian max diff: {np.abs(img_box3x3x3 - img_gauss_approx).max():.4f}") # 0.4655

# uniform_filter1d: 1-D sliding window along columns
img_box1d = ndi.uniform_filter1d(img, size=7, axis=1)

# 3-D
vol_box = ndi.uniform_filter(img3d, size=3)
print(vol_box.shape)  # (16, 32, 32)


##------------------##
## 4. median_filter ##
##------------------##
'''
ndi.median_filter(input, size=3, footprint=None, output=None,
                  mode='reflect', cval=0.0, origin=0)

N-D median filter: replaces each pixel with the median of its neighbourhood.

size      : neighbourhood side length (scalar or sequence). Ignored if footprint given.
footprint : boolean array specifying which neighbours to include.
            Useful for non-rectangular neighbourhoods (e.g. cross, disk).

Properties:
  - Non-linear: cannot be expressed as a convolution.
  - Preserves edges much better than Gaussian or box filters.
  - Removes salt-and-pepper (impulse) noise while preserving step edges.
  - Slower than linear filters (sort vs multiply-accumulate).

Tip: for very large images, consider skimage.filters.median which uses
     more efficient algorithms.
'''

# Add salt-and-pepper noise
img_sp = img.copy()
spike_mask = rng.random(img.shape) < 0.05   # 5% pixels
img_sp[spike_mask] = rng.choice([-5., 5.], size=spike_mask.sum())

# Median filter removes spikes without blurring edges
img_med3 = ndi.median_filter(img_sp, size=3)
img_med5 = ndi.median_filter(img_sp, size=5)
img_gauss_cmp = ndi.gaussian_filter(img_sp, sigma=1.0)

print(f"Spike noise std:         {img_sp.std():.4f}") # 1.4979
print(f"Median3 residual std:    {(img_med3 - img).std():.4f}") # 0.9815
print(f"Gaussian residual std:   {(img_gauss_cmp - img).std():.4f}") # 0.9380
# Median is more effective against spikes

# Cross-shaped footprint (5×5 cross = plus sign)
cross = np.array([[0,0,1,0,0],
                  [0,0,1,0,0],
                  [1,1,1,1,1],
                  [0,0,1,0,0],
                  [0,0,1,0,0]], dtype=bool)
img_med_cross = ndi.median_filter(img_sp, footprint=cross)

# 3-D median filter
vol_med = ndi.median_filter(img3d, size=3)
print(vol_med.shape)  # (16, 32, 32)

##------------------------------------##
## 5. rank_filter / percentile_filter ##
##------------------------------------##
'''
ndi.rank_filter(input, rank, size=3, footprint=None, output=None,
                mode='reflect', cval=0.0, origin=0)

Replace each pixel with the rank-th smallest value in the neighbourhood.
rank=0 : minimum filter. rank=-1 (or size^N - 1): maximum filter.
rank=N//2: median filter (equivalent to median_filter).

ndi.percentile_filter(input, percentile, size=3, ...)
  Same but rank specified as percentile (0..100).
  percentile=0   → min filter.
  percentile=50  → median.
  percentile=100 → max filter.
  percentile=75  → 75th percentile (Tukey's upper hinge — robust max).

Use for:
  - Robust statistics: replace with 10th or 90th percentile to suppress outliers.
  - Local thresholding: compute local background as percentile_filter(img, 10).
  - Order statistics for feature extraction.
'''

# rank_filter: 5th smallest in a 5×5 neighbourhood
img_rank5 = ndi.rank_filter(img, rank=5, size=5)   # small values survive

# percentile_filter: local 25th percentile (lower quartile)
img_q25 = ndi.percentile_filter(img, percentile=25, size=7)
img_q75 = ndi.percentile_filter(img, percentile=75, size=7)

# Local contrast = q75 - q25 (interquartile range)
local_iqr = img_q75 - img_q25
print(f"Local IQR range: {local_iqr.min():.3f} .. {local_iqr.max():.3f}") # 0.642 .. 2.071

# Local background subtraction via low percentile
local_bg   = ndi.percentile_filter(img, percentile=10, size=15)
img_no_bg  = img - local_bg   # remove slowly-varying background

# Rank filter with custom footprint (ring-shaped neighbourhood)
disk_5 = np.zeros((5, 5), dtype=bool)
yy, xx = np.ogrid[-2:3, -2:3]
disk_5[xx**2 + yy**2 <= 4] = True   # disk of radius 2
img_disk_med = ndi.rank_filter(img, rank=disk_5.sum()//2, footprint=disk_5)

##------------------------------------##
## 6. maximum_filter / minimum_filter ##
##------------------------------------##
'''
ndi.maximum_filter(input, size=None, footprint=None, output=None,
                   mode='reflect', cval=0.0, origin=0)
ndi.minimum_filter(input, size=None, footprint=None, ...)

Replace each pixel with the maximum / minimum of its neighbourhood.
Also available as 1-D versions: maximum_filter1d, minimum_filter1d.

These are greyscale morphological dilation and erosion respectively.
  maximum_filter (dilation): bright regions grow; dark regions shrink.
  minimum_filter (erosion) : dark regions grow; bright regions shrink.

Applications:
  - Peak detection: a pixel is a local maximum iff img == max_filter(img).
  - Background estimation: minimum over large window ≈ local dark baseline.
  - Non-maximum suppression (NMS) in object detection pipelines.
  - Morphological gradient: max - min = edges.
'''

# Local maxima detection: pixels equal to their maximum in a window
img_max5 = ndi.maximum_filter(img, size=5)
local_maxima = (img == img_max5)   # True where img is a local maximum
print(f"Number of local maxima (5x5): {local_maxima.sum()}") # 167

img_min5 = ndi.minimum_filter(img, size=5)
local_minima = (img == img_min5)
print(f"Number of local minima (5x5): {local_minima.sum()}") # 165

# Morphological gradient (edge detector): dilation - erosion
morph_grad = img_max5 - img_min5
print(f"Morphological gradient range: {morph_grad.min():.3f} .. {morph_grad.max():.3f}") # 1.641 .. 6.965

# Background estimation from minimum
dark_bg = ndi.minimum_filter(img, size=21)   # slow dark background
# maximum_filter1d: fast 1-D version
max1d_row = ndi.maximum_filter1d(img, size=5, axis=0)   # maximum along rows
max1d_col = ndi.maximum_filter1d(img, size=5, axis=1)   # maximum along columns

# Custom footprint: cross-shaped maximum
max_cross = ndi.maximum_filter(img, footprint=cross)
min_cross = ndi.minimum_filter(img, footprint=cross)

##--------------------##
## 7. sobel / prewitt ##
##--------------------##
'''
ndi.sobel(input, axis=-1, output=None, mode='reflect', cval=0.0)
ndi.prewitt(input, axis=-1, output=None, mode='reflect', cval=0.0)

Compute a Sobel or Prewitt edge filter along the specified axis.

These compute the gradient of the image using convolution with a derivative
approximation kernel:
  Sobel axis=1:  kernel = [[-1,0,1], [-2,0,2], [-1,0,1]]  (sensitive to vertical edges)
  Sobel axis=0:  kernel = [[-1,-2,-1], [0,0,0], [1,2,1]]  (sensitive to horizontal edges)

To get edge magnitude (agnostic to direction):
  edges = sqrt(sobel(img, axis=0)^2 + sobel(img, axis=1)^2)

Prewitt is similar but with equal weights (less smoothing than Sobel).
Sobel is preferred because it averages over more pixels (lower noise sensitivity).

For better edge detection: gaussian_gradient_magnitude(img, sigma) — see section 8.
'''

# Edge detection in x and y
sobel_x = ndi.sobel(img, axis=1)   # horizontal gradient (responds to vertical edges)
sobel_y = ndi.sobel(img, axis=0)   # vertical gradient (responds to horizontal edges)
edges_sobel = np.hypot(sobel_x, sobel_y)   # edge magnitude

print(f"Edge magnitude range: {edges_sobel.min():.3f} .. {edges_sobel.max():.3f}") # 0.121 .. 15.957

# Prewitt: same idea, slightly different weights
prewitt_x = ndi.prewitt(img, axis=1)
prewitt_y = ndi.prewitt(img, axis=0)
edges_prewitt = np.hypot(prewitt_x, prewitt_y)

# 3-D: gradient along each spatial direction
sobel_z = ndi.sobel(img3d, axis=0)
sobel_r = ndi.sobel(img3d, axis=1)
sobel_c = ndi.sobel(img3d, axis=2)
edges_3d = np.sqrt(sobel_z**2 + sobel_r**2 + sobel_c**2)
print(edges_3d.shape)  # (16, 32, 32)

##-------------------------------------------------------------##
## 8. gaussian_gradient_magnitude / gaussian_laplace / laplace ##
##-------------------------------------------------------------##
'''
ndi.gaussian_gradient_magnitude(input, sigma, output=None, mode='reflect',
                                 cval=0.0, extra_keywords=None)
  Edge magnitude using Gaussian derivatives. Smoother and more noise-robust than Sobel.
  Equivalent to: sqrt(sum over axes of gaussian_filter(img, sigma, order=1, axis=k)^2)
  sigma: controls the scale of features detected. Larger sigma = coarser edges.

ndi.gaussian_laplace(input, sigma, output=None, mode='reflect', cval=0.0)
  Laplacian of Gaussian (LoG): second-order blob detector.
  LoG(x) = d²/dx² G(x) + d²/dy² G(x)
  Zero-crossings of LoG mark edges. Blobs appear as local minima/maxima.

ndi.laplace(input, output=None, mode='reflect', cval=0.0)
  Discrete Laplacian using finite differences (no Gaussian smoothing).
  Faster but more sensitive to noise than gaussian_laplace.
  In 2-D: sum of second differences along both axes.
'''

# Scale-space edge detection
edges_g1 = ndi.gaussian_gradient_magnitude(img, sigma=1.0)   # fine edges
edges_g3 = ndi.gaussian_gradient_magnitude(img, sigma=3.0)   # coarse edges

print(f"Fine edges mean:   {edges_g1.mean():.4f}")  # 0.2500 
print(f"Coarse edges mean: {edges_g3.mean():.4f}")  # 0.0314 smaller (fine details averaged out)

# Gaussian Laplace: blob detection
gl = ndi.gaussian_laplace(img, sigma=2.0)
# Local minima of -gl ≈ bright blob centres; zero-crossings ≈ edges
print(f"LoG range: {gl.min():.3f} .. {gl.max():.3f}") # -0.199 .. 0.172

# Laplace (finite difference, no smoothing)
lap = ndi.laplace(img)
print(f"Laplace range: {lap.min():.3f} .. {lap.max():.3f}") # -15.224 .. 16.331

# Compare: Laplace is noisier than gaussian_laplace
print(f"Laplace std:         {lap.std():.4f}") # 4.4362
print(f"Gaussian Laplace std:{ndi.gaussian_laplace(img, sigma=1.0).std():.4f}") # 0.3994

# 3-D Laplacian
lap_3d = ndi.laplace(img3d)
gl_3d  = ndi.gaussian_laplace(img3d, sigma=1.5)

##---------------------------------------##
## 9. generic_filter / vectorized_filter ##
##---------------------------------------##
'''
ndi.generic_filter(input, function, size=None, footprint=None, output=None,
                   mode='reflect', cval=0.0, origin=0, extra_arguments=(),
                   extra_keywords={})

Apply a Python function to each neighbourhood window.
function(values) -> scalar: receives a 1-D array of neighbourhood values
  (flattened from the footprint), returns a single scalar output.

Slower than the built-in filters because it calls Python for each pixel.
Use when: no built-in filter matches your need.

ndi.vectorized_filter(input, function, size=None, footprint=None, ...)
  New in SciPy 1.15. function receives the entire stack of neighbourhood
  windows at once (2-D array: n_pixels x footprint_size) — much faster
  than generic_filter for NumPy-vectorised operations.
'''

# generic_filter: local range (max - min) — no built-in for this
def local_range(vals):
    return vals.max() - vals.min()

local_rng = ndi.generic_filter(img[:16, :16], local_range, size=5)
print(f"Local range result shape: {local_rng.shape}")  # (16, 16)

# generic_filter: local coefficient of variation
def coeff_var(vals):
    m = vals.mean()
    if m == 0: return 0.
    return vals.std() / abs(m)

cv_map = ndi.generic_filter(np.abs(img[:16, :16]) + 1, coeff_var, size=5)
print(f"CV map mean: {cv_map.mean():.4f}") # 0.3042

# extra_arguments: pass parameters to the function
def trimmed_mean(vals, cut):
    n_cut = max(1, int(len(vals) * cut))
    return np.sort(vals)[n_cut:-n_cut].mean()

img_trimmed = ndi.generic_filter(img[:16, :16], trimmed_mean,
                                  size=5, extra_arguments=(0.1,))

# vectorized_filter: batch API (new in 1.15)
# function receives windows of shape (H, W, kH, kW) and a keyword axis=(-2,-1)
# indicating which axes are the kernel axes. Reduction must be along those axes.
def vec_local_range(windows, **kwargs):   # windows: (H, W, kH, kW)
    axis = kwargs.get('axis', (-2, -1))
    return windows.max(axis=axis) - windows.min(axis=axis)

local_rng_vec = ndi.vectorized_filter(img[:16, :16], vec_local_range, size=5)
print(np.allclose(local_rng, local_rng_vec, atol=1e-10))  # True — same result, faster


# =========================================================================================
#  PART B — FOURIER FILTERS 
# =========================================================================================
'''
Fourier filters operate in the frequency domain.
Input should be the output of np.fft.fftn (i.e. the complex DFT).
Apply the filter in frequency domain, then inverse FFT.

All Fourier filter functions:
  input  : complex DFT of the signal (from np.fft.fftn).
  n      : original input size along the transformed axis (needed for real FFT).
  axis   : axis to operate on.
  output : output array (same shape as input).

These correspond to multiplying the DFT by the filter's frequency response.
'''

from scipy.fft import fftn, ifftn

##----------------------------------------------------------------------------##
## 10. fourier_gaussian / fourier_uniform / fourier_ellipsoid / fourier_shift ##
##----------------------------------------------------------------------------##
'''
ndi.fourier_gaussian(input, sigma, n=-1, axis=-1, output=None)
  Multiply DFT by a Gaussian in frequency domain.
  Equivalent to convolving with a Gaussian in spatial domain.
  sigma: standard deviation in SPATIAL domain (pixels).

ndi.fourier_uniform(input, size, n=-1, axis=-1, output=None)
  Multiply DFT by a rect (box) function in frequency domain.
  Equivalent to convolving with a box kernel in spatial domain.
  size: box width in SPATIAL domain (pixels).

ndi.fourier_ellipsoid(input, size, n=-1, axis=-1, output=None)
  N-D ellipsoidal low-pass filter in frequency domain.
  size: half-axes of the ellipsoid in frequency domain.

ndi.fourier_shift(input, shift, n=-1, axis=-1, output=None)
  Shift the image by a subpixel amount using phase shift in DFT.
  shift: shift in SPATIAL domain (pixels; can be fractional).
  Equivalent to multiplying DFT by exp(-2*pi*i*k*shift/N).
  Advantage over ndi.shift: shift can be fractional and avoids spatial interpolation artefacts.
'''

img_small = img[:16, :16]   # use a small patch for demo

# Fourier Gaussian: smooth in frequency domain
dft = fftn(img_small)
dft_filt = ndi.fourier_gaussian(dft, sigma=2.0)
img_fg = np.real(ifftn(dft_filt))

# Compare with spatial gaussian_filter
img_spatial_gauss = ndi.gaussian_filter(img_small, sigma=2.0, mode='wrap')
print(f"Fourier vs spatial Gaussian max diff: {np.abs(img_fg - img_spatial_gauss).max():.6f}")
# 0.000016
# Should be nearly equal (minor boundary difference due to mode)

# Fourier uniform (box lowpass)
dft_box = ndi.fourier_uniform(dft, size=5.0)
img_fu = np.real(ifftn(dft_box))

# Fourier ellipsoid (anisotropic lowpass)
dft_ell = ndi.fourier_ellipsoid(dft, size=4.0)
img_fe = np.real(ifftn(dft_ell))

# Fourier shift: sub-pixel translation
shift_amount = [1.7, -2.3]   # fractional pixel shift
dft_shifted = ndi.fourier_shift(dft, shift=shift_amount)
img_fshift = np.real(ifftn(dft_shifted))

# Compare with spatial shift
img_sshift = ndi.shift(img_small, shift=shift_amount, mode='wrap')
print(f"Fourier vs spatial shift max diff: {np.abs(img_fshift - img_sshift).max():.4f}")
# 2.1503
# Fourier shift avoids interpolation artefacts for large arrays


# =========================================================================================
#  PART C — INTERPOLATION / GEOMETRIC TRANSFORMS 
# =========================================================================================
'''
All geometric transforms use spline interpolation of the given order.
order=0 : nearest neighbour (fast, pixelated)
order=1 : bilinear / trilinear (fast, slightly blurry)
order=3 : cubic spline (DEFAULT — smooth, good for most purposes)
order=5 : quintic spline (slowest, most accurate)

For repeated resampling of the same array at many coordinate sets, precompute
the spline coefficients once with spline_filter() (see section 17).

mode controls what values are used outside the array boundary (same options as filters).
prefilter=True (default): internally applies spline_filter for order > 1.
prefilter=False: skip prefiltering (use only if spline_filter already applied).
'''

# Small test image for easy verification
checkerboard = np.zeros((8, 8))
checkerboard[::2, ::2] = 1.
checkerboard[1::2, 1::2] = 1.

##----------##
## 11. zoom ##
##----------##
'''
ndi.zoom(input, zoom, output=None, order=3, mode='reflect', cval=0.0,
         prefilter=True, grid_mode=False)

Scale (zoom) each dimension of the array independently.

zoom : scalar (same factor for all axes) or sequence (one factor per axis).
       zoom > 1: upsampling (makes image larger).
       zoom < 1: downsampling (makes image smaller, applies anti-aliasing via order).
       zoom can be float or integer.

grid_mode : False (default): zoom so that the corner pixels map to corner pixels.
            True : zoom so that the pixel grid edges map to grid edges.

Note: when downsampling, use order=1 or apply a Gaussian blur first to avoid
aliasing, since ndimage.zoom does not apply an anti-aliasing filter.
'''

# Upscale by 2×
img_zoom2x = ndi.zoom(img, zoom=2.0)
print(f"Original: {img.shape}  Upscaled: {img_zoom2x.shape}")  # (64,64) -> (128,128)

# Downscale by 0.5×
img_half = ndi.zoom(img, zoom=0.5)
print(img_half.shape)   # (32, 32)

# Anisotropic zoom: 2× along rows, 0.5× along columns
img_aniso_zoom = ndi.zoom(img, zoom=(2.0, 0.5))
print(img_aniso_zoom.shape)  # (128, 32)

# Zoom to an exact output size: compute factor = out_size / in_size
target = (100, 100)
factors = (target[0]/img.shape[0], target[1]/img.shape[1])
img_100x100 = ndi.zoom(img, zoom=factors)
print(img_100x100.shape)  # (100, 100)

# 3-D zoom
vol_half = ndi.zoom(img3d, zoom=0.5)
print(vol_half.shape)  # (8, 16, 16)

# Order comparison
img_zoom_nn   = ndi.zoom(checkerboard, 4.0, order=0)  # nearest neighbour
img_zoom_lin  = ndi.zoom(checkerboard, 4.0, order=1)  # linear
img_zoom_cub  = ndi.zoom(checkerboard, 4.0, order=3)  # cubic
print(img_zoom_nn.shape)   # (32, 32)

##------------##
## 12. rotate ##
##------------##
'''
ndi.rotate(input, angle, axes=(1, 0), reshape=True, output=None, order=3,
           mode='constant', cval=0.0, prefilter=True)

Rotate the array in the plane defined by axes.

angle  : rotation angle in DEGREES (counter-clockwise for standard orientation).
axes   : (axis1, axis2) pair that defines the rotation plane. Default: (1, 0) = (cols, rows).
reshape: True  (default): output shape is expanded to fit the entire rotated image.
         False           : output has the same shape as input (may crop corners).
mode   : boundary handling. 'constant' with cval=0 leaves black corners.

For 3-D rotation in a specific plane (e.g. around z-axis), specify axes=(0,1).
'''

img_rot45  = ndi.rotate(img, angle=45, reshape=True)
img_rot45c = ndi.rotate(img, angle=45, reshape=False)  # same size, corners cut

print(f"Rotated 45° reshape=True:  {img_rot45.shape}")   # (91, 91) larger than (64,64)
print(f"Rotated 45° reshape=False: {img_rot45c.shape}")  # (64,64) — original size

# 90-degree rotation should be approximately reversible
img_rot90  = ndi.rotate(img, angle=90, reshape=False)
img_rot360 = img_rot90
for _ in range(3):
    img_rot360 = ndi.rotate(img_rot360, angle=90, reshape=False)
print(f"4x90° rotation error: {np.abs(img_rot360 - img).max():.4f}")  # small (spline artefacts)

# 3-D: rotate in the row-column plane (around z-axis)
vol_rot = ndi.rotate(img3d, angle=30, axes=(2, 1), reshape=False)
print(vol_rot.shape)  # (16, 32, 32)

##-----------##
## 13. shift ##
##-----------##
'''
ndi.shift(input, shift, output=None, order=3, mode='constant', cval=0.0,
          prefilter=True)

Translate (shift) the array by a given amount.

shift : scalar (same for all axes) or sequence (one per axis).
        Can be fractional (non-integer sub-pixel shift via spline interpolation).
        Positive shift: content moves to higher indices (image appears to move right/down).

For integer shifts, order=1 or order=0 avoids blurring.
For fractional shifts, use order=3 (default) for best quality.

The Fourier-based ndi.fourier_shift may give better results for large fractional
shifts in periodic signals.
'''

img_shift_int  = ndi.shift(img, shift=[5, -3], order=1)   # integer shift
img_shift_frac = ndi.shift(img, shift=[2.7, -1.4], order=3)  # sub-pixel shift

# Verify integer shift with nearest-neighbour: exact pixel displacement
img_shift_nn  = ndi.shift(img, shift=[0, 5], order=0, mode='constant', cval=0.0)
print(np.allclose(img_shift_nn[:, 5:], img[:, :-5]))   # True

# Fractional shifts are not exactly reversible due to spline interpolation
img_shifted = ndi.shift(img, [3.0, -2.5])
img_unshifted = ndi.shift(img_shifted, [-3.0, 2.5])
# Interior error is small; boundary error is larger due to mode='constant' cval padding
interior_err = np.abs(img_unshifted[10:-10, 10:-10] - img[10:-10, 10:-10]).max()
print(f"Round-trip interior error: {interior_err:.4f}")  # 1.5386

# 3-D
vol_shifted = ndi.shift(img3d, shift=[1.5, 0, -2.0])
print(vol_shifted.shape)  # (16, 32, 32)

##----------------------##
## 14. affine_transform ##
##----------------------##
'''
ndi.affine_transform(input, matrix, offset=0.0, output_shape=None, output=None,
                     order=3, mode='constant', cval=0.0, prefilter=True)

Apply an affine geometric transformation.

The mapping is defined as:
  output[o] = input[matrix @ o + offset]

where o is the output coordinate vector. This maps OUTPUT coordinates to INPUT
coordinates (inverse mapping / pull model — standard for image interpolation).

matrix : transformation matrix.
  NxN  : linear part only (rotation, scale, shear); no translation.
  NxN+1: full homogeneous matrix [A | t] where t is the translation column.
         NOT used: affine_transform takes matrix and offset separately.
  Nx1  : scale factors only.

offset : translation offset applied AFTER the matrix transformation.
         offset = -matrix @ center + center + shift for rotation around centre.

output_shape: if given, the output will have this shape (can differ from input).

IMPORTANT: matrix and offset map OUTPUT -> INPUT.
  To rotate an image clockwise by theta, use the counter-clockwise rotation matrix.
  To translate right by t, use offset = -t.
'''

# Scale by 1.5 around the image centre
scale = 1.5
centre = np.array(img.shape) / 2.0
# matrix maps output coords to input: input_coord = matrix @ output_coord + offset
# For scaling: input_coord = output_coord / scale
matrix_scale = np.eye(2) / scale
offset_scale = centre - matrix_scale @ centre
img_scaled = ndi.affine_transform(img, matrix_scale, offset=offset_scale, order=3)
print(img_scaled.shape)  # (64, 64) — same size, but content zoomed 1.5×

# Rotation by 30 degrees counter-clockwise around image centre
theta = np.radians(30)
c, s = np.cos(theta), np.sin(theta)
# Forward rotation (CCW): maps input -> output
# Inverse (for affine_transform output->input mapping):
R_inv = np.array([[c, s], [-s, c]])   # transpose of CCW rotation matrix
offset_rot = centre - R_inv @ centre
img_rotated = ndi.affine_transform(img, R_inv, offset=offset_rot, order=3)
print(img_rotated.shape)  # (64, 64)

# ndi.rotate(img, 30) is equivalent, using the same mapping internally
img_rotated_ref = ndi.rotate(img, 30, reshape=False, order=3)
# Small numerical differences exist due to rounding in offset computation
print(f"Interior diff vs ndi.rotate: {np.abs(img_rotated[15:-15,15:-15]-img_rotated_ref[15:-15,15:-15]).max():.2e}")
# Interior diff vs ndi.rotate: 1.93e+00

# Shear transformation
shear = 0.3
M_shear = np.array([[1., shear], [0., 1.]])
img_sheared = ndi.affine_transform(img, M_shear, offset=[0, 0])
print(img_sheared.shape)  # (64, 64)

# Flip (horizontal): matrix = [[1,0],[0,-1]], offset = [0, N-1]
M_flip = np.array([[1., 0.], [0., -1.]])
offset_flip = [0., img.shape[1] - 1]
img_flipped = ndi.affine_transform(img, M_flip, offset=offset_flip)
print(np.allclose(img_flipped, img[:, ::-1]))  # True

# 3-D affine: identity transform
M3 = np.eye(3)
vol_affine = ndi.affine_transform(img3d, M3, order=1)
print(np.allclose(vol_affine, img3d, atol=1e-10))  # True (identity)

##---------------------##
## 15. map_coordinates ##
##---------------------##
'''
ndi.map_coordinates(input, coordinates, output=None, order=3, mode='reflect',
                    cval=0.0, prefilter=True)

Interpolate input at arbitrary coordinate positions.

coordinates : (ndim, ...) array of coordinates.
  coordinates[i] : coordinates along axis i.
  Output shape = shape of coordinates[0] (= coordinates[1] = ...).

Think of it as:  output[j] = interpolated value of input at (coords[0][j], coords[1][j], ...)

Use for:
  - Evaluating an array at non-integer positions.
  - Implementing arbitrary warps (if you can compute the inverse mapping).
  - Sampling along a line, curve, or surface through an N-D array.
'''

# Sample img along the main diagonal (row == col)
diag_coords = [np.arange(64, dtype=float),   # row coords
               np.arange(64, dtype=float)]    # col coords
diag_values = ndi.map_coordinates(img, diag_coords)
print(diag_values.shape)   # (64,) — 64 samples along the diagonal
print(np.allclose(diag_values, np.diag(img)))  # True for order=1; cubic slightly differs

# Sample at fractional (sub-pixel) coordinates
rows_frac = np.array([0.5, 1.2, 3.7, 10.0])
cols_frac = np.array([0.5, 0.5, 0.5,  0.5])
interp_vals = ndi.map_coordinates(img, [rows_frac, cols_frac])
print(interp_vals.shape)   # (4,)

# 2-D warp: barrel distortion
H, W = img.shape
yy, xx = np.mgrid[0:H, 0:W]
# Compute radial distortion: displace pixels outward from centre
cy, cx = H/2, W/2
r = np.sqrt((yy - cy)**2 + (xx - cx)**2)
k = 0.001   # distortion coefficient
# Map output coords -> input coords (inverse mapping)
src_y = cy + (yy - cy) * (1 + k * r**2)
src_x = cx + (xx - cx) * (1 + k * r**2)
img_barrel = ndi.map_coordinates(img, [src_y, src_x], order=3)
print(img_barrel.shape)  # (64, 64)

# Profile along a circular arc
theta_arc = np.linspace(0, np.pi, 200)
r_arc = 20.0   # radius
rows_arc = H/2 + r_arc * np.sin(theta_arc)
cols_arc = W/2 + r_arc * np.cos(theta_arc)
profile = ndi.map_coordinates(img, [rows_arc, cols_arc], order=3)
print(profile.shape)   # (200,) — intensity along the arc

# 3-D: extract an oblique slice
nz, ny, nx = img3d.shape
zz_slab = np.full((ny, nx), nz / 2)   # fixed z
yy_slab, xx_slab = np.mgrid[0:ny, 0:nx]
slab = ndi.map_coordinates(img3d, [zz_slab, yy_slab, xx_slab])
print(slab.shape)   # (32, 32) — one slice

##-------------------------##
## 16. geometric_transform ##
##-------------------------##
'''
ndi.geometric_transform(input, mapping, output_shape=None, output=None,
                        order=3, mode='constant', cval=0.0, prefilter=True,
                        extra_arguments=(), extra_keywords={})

Apply a fully custom (non-affine) geometric warp.

mapping(output_coords, *extra_arguments, **extra_keywords) -> input_coords
  Takes an output coordinate tuple and returns the corresponding input coordinates.
  This is the INVERSE mapping (output -> input).

Use for: any non-affine warp — polar transform, lens distortion, perspective, etc.
Slower than affine_transform because it calls Python per-pixel (unless compiled).
For large images, prefer map_coordinates with precomputed coordinate arrays.
'''

# Polar-to-Cartesian transform (remap a polar image to Cartesian)
def polar_to_cartesian(output_coords):
    row, col = output_coords
    H, W = img_small.shape
    # Output pixel at (row, col) maps to input at polar (r, theta)
    cx, cy = W / 2, H / 2
    r     = np.sqrt((col - cx)**2 + (row - cy)**2)
    theta = np.arctan2(row - cy, col - cx)
    # Input image is indexed as (r_normalized, theta_normalized)
    r_norm     = r / (max(H, W) / 2) * (H - 1)
    theta_norm = (theta + np.pi) / (2 * np.pi) * (W - 1)
    return (r_norm, theta_norm)

img_small = img[:16, :16]
img_polar = ndi.geometric_transform(img_small, polar_to_cartesian, order=1)
print(img_polar.shape)   # (16, 16) — same shape

# Custom warp: swirl effect
def swirl_mapping(output_coords, strength=2.0, radius=8.0):
    row, col = output_coords
    H, W = img_small.shape
    cy, cx = H / 2., W / 2.
    dy, dx = row - cy, col - cx
    r = np.sqrt(dy**2 + dx**2)
    angle = strength * np.exp(-r / radius)
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    src_col = cx + cos_a * dx - sin_a * dy
    src_row = cy + sin_a * dx + cos_a * dy
    return (src_row, src_col)

img_swirl = ndi.geometric_transform(img_small, swirl_mapping,
                                     extra_keywords={'strength': 3.0, 'radius': 6.0})
print(img_swirl.shape)  # (16, 16)

##-------------------##
## 17. spline_filter ##
##-------------------##
'''
ndi.spline_filter(input, order=3, output=np.float64, mode='mirror')
ndi.spline_filter1d(input, order=3, axis=-1, output=np.float64, mode='mirror')

Precompute B-spline coefficients for an array.

When multiple geometric transforms (zoom, affine_transform, map_coordinates, etc.)
are applied to the SAME array with the same spline order, it is wasteful to
recompute the spline prefilter each time (prefilter=True, the default).

Instead:
  1. coeffs = spline_filter(input, order=3)
  2. result = zoom(coeffs, 1.5, prefilter=False)
  3. result2 = map_coordinates(coeffs, coords, prefilter=False)

This avoids repeating the O(N) prefiltering for each subsequent transform.

Note: spline_filter uses mode='mirror' by default (different from most other
functions which use 'reflect'). Use consistent modes.
'''

# Without precomputation: each call reapplies the spline filter internally
coords1 = [np.linspace(0, 63, 128), np.linspace(0, 63, 128)]
coords2 = [np.linspace(0, 63, 200), np.linspace(0, 63, 200)]

# With precomputation: compute spline coefficients once
coeffs = ndi.spline_filter(img, order=3, mode='mirror')
# Now apply transforms without prefiltering
result1 = ndi.map_coordinates(coeffs, coords1, order=3, prefilter=False)
result2 = ndi.map_coordinates(coeffs, coords2, order=3, prefilter=False)

# Verify: result should match applying from raw array
result1_ref = ndi.map_coordinates(img, coords1, order=3)
print(np.allclose(result1, result1_ref, atol=1e-8))  # True

# 1-D prefilter along one axis at a time (for partial transforms)
coeffs_row = ndi.spline_filter1d(img, order=3, axis=0, mode='mirror')
coeffs_both = ndi.spline_filter1d(coeffs_row, order=3, axis=1, mode='mirror')


# =========================================================================================
#  PART D — MEASUREMENTS 
# =========================================================================================
'''
Measurement functions operate on labelled arrays (where each labelled region
corresponds to a "feature" or "object").

labels : integer array of same shape as input.
  0 = background (ignored in most functions).
  1, 2, 3, ... = labelled objects.

index  : which label(s) to compute for. Default None = all non-zero labels combined.
  Single int : compute for that label only.
  List/array : compute for each label in the list.

Most functions return a scalar when index is a single value, or a list when
index is a list.
'''

##--------------------------##
## 18. label / find_objects ##
##--------------------------##
'''
ndi.label(input, structure=None, output=None) -> (labeled_array, num_features)

Assign a unique integer label to each connected component (blob) in input.

input     : binary array (True/non-zero = foreground).
structure : connectivity structure. None = default (only face-connected, no diagonals).
            generate_binary_structure(rank, connectivity) for diagonal connectivity.
            Rank 2, connectivity 1: 4-connected (cross)
            Rank 2, connectivity 2: 8-connected (square including diagonals)

Returns:
  labeled_array : integer array, 0=background, 1..N=each distinct component.
  num_features  : number of labelled components.

ndi.find_objects(labeled_array, max_label=0) -> list of slice tuples
  For each label i, find_objects returns a tuple of slices that exactly bounds
  the region labeled i. Returns None for absent labels.
  Use to extract bounding boxes of each object.
'''

# Label the two blobs in the binary image
labeled, n = ndi.label(blob)
print(f"Found {n} connected components")   # 2
print(f"Label values: {np.unique(labeled)}")  # [0 1 2]

# 8-connected labelling: diagonals count as connected
struct_8 = ndi.generate_binary_structure(rank=2, connectivity=2)  # 3×3 all-True
labeled_8, n_8 = ndi.label(blob, structure=struct_8)
print(f"8-connected labels: {n_8}")   # still 2 (blobs don't touch diagonally)

# Noisy binary: many small components vs few large
binary_noisy = rng.random((30, 30)) > 0.7
labeled_noisy, n_noisy = ndi.label(binary_noisy)
print(f"Noisy blobs: {n_noisy}") # 121

# find_objects: bounding boxes
slices = ndi.find_objects(labeled)
for i, sl in enumerate(slices):
    if sl is not None:
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        print(f"  Object {i+1}: bounding box {h}×{w} at rows {sl[0].start}-{sl[0].stop}, cols {sl[1].start}-{sl[1].stop}")
  # Object 1: bounding box 5×5 at rows 3-8, cols 3-8
  # Object 2: bounding box 5×5 at rows 12-17, cols 12-17
  
# Extract each object using its bounding box
for i, sl in enumerate(slices):
    obj_patch = blob[sl]   # sub-array containing just this object
    print(f"  Object {i+1} patch shape: {obj_patch.shape}")
  # Object 1 patch shape: (5, 5)
  # Object 2 patch shape: (5, 5)

# 3-D labelling
vol_bin = img3d > 0.5
labeled_3d, n_3d = ndi.label(vol_bin)
print(f"3-D components: {n_3d}") # 960

##--------------------------------------------------------------------------------------##
## 19. sum_labels / mean / median / variance / standard_deviation / extrema / histogram ##
##--------------------------------------------------------------------------------------##
'''
Reduction functions over labelled regions.

ndi.sum_labels(input, labels=None, index=None)       : sum of values in each region.
ndi.mean(input, labels=None, index=None)             : mean.
ndi.median(input, labels=None, index=None)           : median.
ndi.variance(input, labels=None, index=None)         : variance.
ndi.standard_deviation(input, labels=None, index=None): std dev.
ndi.extrema(input, labels=None, index=None)          : (min, max, min_pos, max_pos).
ndi.histogram(input, min, max, bins, labels, index)  : histogram per region.

All follow the same interface:
  labels : label array. None = compute over entire input.
  index  : label(s) to include. None = all non-zero labels combined.
           List: returns a list with one value per label.
'''

# Aggregate statistics over the two blobs
means   = ndi.mean(vals_arr, labels=labels_arr, index=[1, 2])
sums    = ndi.sum_labels(vals_arr, labels=labels_arr, index=[1, 2])
medians = ndi.median(vals_arr, labels=labels_arr, index=[1, 2])
stds    = ndi.standard_deviation(vals_arr, labels=labels_arr, index=[1, 2])
vars_   = ndi.variance(vals_arr, labels=labels_arr, index=[1, 2])

print(f"Means per label:  {[round(m,3) for m in means]}") # [np.float64(4.867), np.float64(5.508)]
print(f"Sums per label:   {[round(s,3) for s in sums]}") # [np.float64(121.668), np.float64(137.695)]
print(f"Medians per label:{[round(m,3) for m in medians]}") # [np.float64(5.144), np.float64(6.239)]

# Overall (no label, no index): compute over entire array
overall_mean = ndi.mean(vals_arr)
print(f"Overall mean: {overall_mean:.4f}  (np.mean: {vals_arr.mean():.4f})") # 4.9637  (np.mean: 4.9637)

# extrema: min, max, and their positions
mini, maxi, min_pos, max_pos = ndi.extrema(vals_arr, labels=labels_arr, index=[1, 2])
print(f"Label 1: min={mini[0]:.3f} at {min_pos[0]}, max={maxi[0]:.3f} at {max_pos[0]}")
# Label 1: min=0.124 at (np.int64(5), np.int64(6)), max=10.000 at (np.int64(4), np.int64(3))
print(f"Label 2: min={mini[1]:.3f} at {min_pos[1]}, max={maxi[1]:.3f} at {max_pos[1]}")
# Label 2: min=0.051 at (np.int64(13), np.int64(16)), max=9.837 at (np.int64(16), np.int64(15))

# histogram: intensity histogram for each region
hists = ndi.histogram(vals_arr, min=0, max=10, bins=5,
                       labels=labels_arr, index=[1, 2])
print(f"Histogram bins (label 1): {hists[0]}") # [5 6 3 6 5]
print(f"Histogram bins (label 2): {hists[1]}") # [ 6  3  3  3 10]

# Verify sum == size of region × mean
n_pix_1 = (labels_arr == 1).sum()  # 5×5 = 25 pixels in label 1
print(np.isclose(sums[0], means[0] * n_pix_1))  # True

##----------------------------------------------------------##
## 20. center_of_mass / maximum_position / minimum_position ##
##----------------------------------------------------------##
'''
ndi.center_of_mass(input, labels=None, index=None)
  Compute the weighted centre of mass of the array, using input values as weights.
  Returns (row, col) tuple (or N-D coordinate tuple).

ndi.maximum_position(input, labels=None, index=None)
  Return the (row, col) coordinate of the maximum value.

ndi.minimum_position(input, labels=None, index=None)
  Return the (row, col) coordinate of the minimum value.

All return a single tuple (or list of tuples) depending on index.
'''

# Centre of mass: weighted centroid of each blob
com1, com2 = ndi.center_of_mass(vals_arr, labels=labels_arr, index=[1, 2])
print(f"Centre of mass label 1: row={com1[0]:.2f}, col={com1[1]:.2f}")  # Centre of mass label 1: row=5.02, col=4.96, near (5, 5)
print(f"Centre of mass label 2: row={com2[0]:.2f}, col={com2[1]:.2f}")  # Centre of mass label 2: row=14.21, col=14.09, near (14, 14)

# With uniform weights: gives geometric centroid
com_geom_1, com_geom_2 = ndi.center_of_mass(
    np.ones_like(labels_arr, dtype=float), labels=labels_arr, index=[1, 2])
print(f"Geometric centroid 1: {com_geom_1}") # (np.float64(5.0), np.float64(5.0))
print(f"Geometric centroid 2: {com_geom_2}") # (np.float64(14.0), np.float64(14.0))

# Maximum / minimum positions
max_pos1, max_pos2 = ndi.maximum_position(vals_arr, labels=labels_arr, index=[1, 2])
min_pos1, min_pos2 = ndi.minimum_position(vals_arr, labels=labels_arr, index=[1, 2])
print(f"Max position label 1: {max_pos1}, val={vals_arr[max_pos1]:.4f}") # Max position label 1: (np.int64(4), np.int64(3)), val=9.9997
print(f"Min position label 1: {min_pos1}, val={vals_arr[min_pos1]:.4f}") # Min position label 1: (np.int64(5), np.int64(6)), val=0.1244

# Over entire array (no labels)
overall_max_pos = ndi.maximum_position(vals_arr)
print(f"Global maximum at: {overall_max_pos}") # Global maximum at: (np.int64(4), np.int64(3))
print(np.allclose(vals_arr[overall_max_pos], vals_arr.max()))  # True

##-------------------------------------------##
## 21. labeled_comprehension / value_indices ##
##-------------------------------------------##
'''
ndi.labeled_comprehension(input, labels, index, func, out_dtype, default=None,
                          pass_positions=False)

Apply an arbitrary Python function to each labelled region.
Equivalent to: [func(input[labels == i]) for i in index]
Faster than manual iteration when many labels are involved.

func           : callable(values) -> scalar.
out_dtype      : dtype of the output array.
default        : value to use when a label has no pixels. Default None raises an error.
pass_positions : if True, func receives (values, positions) where positions is a
                 tuple of coordinate arrays.

ndi.value_indices(arr, ignore_value=None) -> dict
  For an integer array, return {value: (row_indices, col_indices)} for each
  distinct value. Like np.where but organised by value.
  ignore_value : skip this value (typically 0/background).
'''

# labeled_comprehension: custom aggregation function
# Compute the 90th percentile of each labelled region
p90 = ndi.labeled_comprehension(
    vals_arr, labels_arr, index=[1, 2],
    func=lambda x: np.percentile(x, 90),
    out_dtype=float, default=0.0
)
print(f"90th percentile per label: {p90.round(3)}")

# Compare with percentile_filter (different: pointwise, not region-wise)
# labeled_comprehension is a reduce (one number per region)
# percentile_filter is a map (one number per pixel)

# Pass positions: pass_positions=True adds FLAT indices as a second argument
def argmax_coords(vals, flat_indices):
    # flat_indices: 1-D array of flattened positions within the array
    idx = np.argmax(vals)
    row, col = np.unravel_index(flat_indices[idx], vals_arr.shape)
    return row * 100 + col   # encode as single number for out_dtype=float

max_encoded = ndi.labeled_comprehension(
    vals_arr, labels_arr, index=[1, 2],
    func=argmax_coords, out_dtype=float, default=0.0,
    pass_positions=True
)
# Decode: row = max_encoded // 100, col = max_encoded % 100
for i, enc in enumerate(max_encoded):
    row, col = int(enc) // 100, int(enc) % 100
    print(f"Max coord label {i+1}: ({row}, {col})")
# Max coord label 1: (4, 3)
# Max coord label 2: (16, 15)

# value_indices: find all pixel positions for each label value
vi = ndi.value_indices(labels_arr, ignore_value=0)
print(f"Labels found: {list(vi.keys())}")   # [1, 2]
print(f"Label 1 pixel count: {len(vi[1][0])}")  # 25 (5×5 block)
# Equivalent to: np.where(labels_arr == 1) but returns dict over all values at once

##-------------------##
## 22. watershed_ift ##
##-------------------##
'''
ndi.watershed_ift(input, markers, structure=None, output=None)

Watershed segmentation using the Image Foresting Transform (IFT).

input   : input image (uint8 or uint16). Lower values = lower "flooding" cost.
markers : integer array. Positive labels seed foreground regions; -1 marks forbidden pixels.
          0 = unlabeled (to be assigned by watershed).
structure: connectivity structure (default: face-connected).

The watershed algorithm floods the image from the seed markers, assigning each
pixel to the nearest seed (by path cost through the image intensity).

Use for: segmenting touching objects when you can provide seed points per object.
Typical workflow:
  1. Compute distance_transform_edt of binary mask.
  2. Find local maxima of distance transform as seeds (one per object).
  3. Run watershed_ift to segment the objects.
'''

# Simple demo: segment two bright blobs
img_wb = np.zeros((20, 20), dtype=np.uint8)
img_wb[3:8, 3:8] = 200    # bright blob 1
img_wb[12:17, 12:17] = 180  # bright blob 2

# Invert: watershed floods from low values (dark = easy to flood)
img_inv = 255 - img_wb   # dark regions = easy paths

# Seed markers: label 1 at blob 1 centre, label 2 at blob 2 centre
markers_ws = np.zeros((20, 20), dtype=int)
markers_ws[5, 5]   = 1   # seed in blob 1
markers_ws[14, 14] = 2   # seed in blob 2

ws_result = ndi.watershed_ift(img_inv, markers_ws)
print(f"Watershed labels: {np.unique(ws_result)}")   # [1 2]
# Label 1 covers blob 1, label 2 covers blob 2 (and background split between them)


# =========================================================================================
#  PART E — MORPHOLOGY 
# =========================================================================================
'''
Binary morphology operates on boolean arrays.
Greyscale morphology operates on float arrays.

Structuring element (SE) / footprint: defines the neighbourhood shape.
  None (default): use size parameter or a cross/diamond shape.
  Array: explicit boolean footprint.

generate_binary_structure(rank, connectivity):
  rank        : number of dimensions (2 for image, 3 for volume).
  connectivity: 1 = face-connected (cross in 2-D: 4-connected).
                2 = face + edge connected (8-connected in 2-D).
                3 = all neighbours in 3-D (26-connected).
'''

##---------------------------------------------------##
## 23. generate_binary_structure / iterate_structure ##
##---------------------------------------------------##
'''
ndi.generate_binary_structure(rank, connectivity)

Generate the default structuring element for a given rank and connectivity.

rank=2, connectivity=1 :  [[0,1,0],[1,1,1],[0,1,0]]  (cross, 4-connected)
rank=2, connectivity=2 :  [[1,1,1],[1,1,1],[1,1,1]]  (square, 8-connected)
rank=3, connectivity=1 :  face-only in 3-D (6-connected)
rank=3, connectivity=2 :  face+edge in 3-D (18-connected)
rank=3, connectivity=3 :  all neighbours in 3-D (26-connected)

ndi.iterate_structure(structure, iterations, origin=None)
  Dilate the structure with itself iterations times.
  Equivalent to applying binary_dilation(structure, structure) iterations times.
  Used to create larger structuring elements (e.g. disk of radius r).
'''

cross = ndi.generate_binary_structure(rank=2, connectivity=1)   # 4-connected
square = ndi.generate_binary_structure(rank=2, connectivity=2)  # 8-connected
print("Cross (4-conn):\n", cross.astype(int))
# [[0 1 0]
#  [1 1 1]
#  [0 1 0]]
print("Square (8-conn):\n", square.astype(int))
# [[1 1 1]
#  [1 1 1]
#  [1 1 1]]

# iterate_structure: dilate the cross to get a larger diamond
cross_3 = ndi.iterate_structure(cross, 3)    # 3 iterations -> 7×7 diamond
print(f"Iterated cross shape: {cross_3.shape}")  # (7, 7)
print(f"Iterated cross:\n{cross_3.astype(int)}")
# [[0 0 0 1 0 0 0]
#  [0 0 1 1 1 0 0]
#  [0 1 1 1 1 1 0]
#  [1 1 1 1 1 1 1]
#  [0 1 1 1 1 1 0]
#  [0 0 1 1 1 0 0]
#  [0 0 0 1 0 0 0]]

# Create a disk-like SE by iterating
disk_r2 = ndi.iterate_structure(cross, iterations=2)  # disk radius ~2
print(f"Disk r~2:\n{disk_r2.astype(int)}")
# [[0 0 1 0 0]
#  [0 1 1 1 0]
#  [1 1 1 1 1]
#  [0 1 1 1 0]
#  [0 0 1 0 0]]

# 3-D structuring element
cross_3d = ndi.generate_binary_structure(rank=3, connectivity=1)   # 6-connected face
cube_3d  = ndi.generate_binary_structure(rank=3, connectivity=3)   # 26-connected all
print(f"3-D cross shape: {cross_3d.shape}") # (3,3,3)

##------------------------------------------------------------------------##
## 24. binary_erosion / binary_dilation / binary_opening / binary_closing ##
##------------------------------------------------------------------------##
'''
ndi.binary_erosion(input, structure=None, iterations=1, mask=None, output=None,
                   border_value=0, origin=0, brute_force=False)
  Erode a binary image: a pixel stays True only if ALL pixels in the structure
  neighbourhood are True. Shrinks foreground objects.
  iterations: apply erosion this many times (equivalent to larger SE).
  border_value: value assumed outside the array (default 0).

ndi.binary_dilation(input, structure=None, iterations=1, ...)
  Dilate a binary image: a pixel becomes True if ANY pixel in the neighbourhood is True.
  Grows foreground objects.

ndi.binary_opening(input, structure=None, iterations=1, ...)
  Erosion followed by dilation. Removes small objects/noise while preserving shape.

ndi.binary_closing(input, structure=None, iterations=1, ...)
  Dilation followed by erosion. Fills small holes while preserving shape.

Rules of thumb:
  Opening  : removes structures SMALLER than the SE (noise removal).
  Closing  : fills gaps SMALLER than the SE (hole filling).
  erosion  : shrinks objects; removes thin protrusions.
  dilation : grows objects; fills thin gaps.
'''

# Test image: blob with a thin spike and a small hole
test_bin = blob.copy()
test_bin[5:7, 7:10] = True    # add a thin protrusion
test_bin[4, 4] = False         # add a hole inside blob 1

# Erosion: shrinks objects, removes thin protrusion
eroded = ndi.binary_erosion(test_bin, structure=square, iterations=1)
print(f"Original pixels: {test_bin.sum()}  Eroded: {eroded.sum()}")   # fewer True
# Original pixels: 53  Eroded: 14

# Dilation: grows objects, fills hole
dilated = ndi.binary_dilation(test_bin, structure=square, iterations=1)
print(f"Original pixels: {test_bin.sum()}  Dilated: {dilated.sum()}")   # more True
# Original pixels: 53  Dilated: 106

# Opening: removes the thin spike
opened = ndi.binary_opening(test_bin, structure=square, iterations=1)
spike_gone = not opened[6, 8]   # spike at (6,8) was in protrusion
print(f"Spike removed by opening: {spike_gone}")  # True

# Closing: fills the hole
closed = ndi.binary_closing(test_bin, structure=square, iterations=1)
hole_filled = closed[4, 4]   # was False
print(f"Hole filled by closing: {hole_filled}") # True

# Multiple iterations
eroded3 = ndi.binary_erosion(test_bin, structure=cross, iterations=3)
print(f"Erosion 3x: {eroded3.sum()} pixels remain")
# Erosion 3x: 0 pixels remain

# 3-D morphology
vol_bin_small = img3d[:8, :16, :16] > 0
vol_eroded  = ndi.binary_erosion(vol_bin_small)
vol_dilated = ndi.binary_dilation(vol_bin_small)
print(f"3-D erosion: {vol_eroded.sum()} -> dilated: {vol_dilated.sum()}")
# 3-D erosion: 8 -> dilated: 2022

##-----------------------------------------------------------------##
## 25. binary_fill_holes / binary_hit_or_miss / binary_propagation ##
##-----------------------------------------------------------------##
'''
ndi.binary_fill_holes(input, structure=None, output=None, origin=0)
  Fill all holes (enclosed background regions) in a binary image.
  A "hole" is a region of False pixels completely surrounded by True pixels.
  structure: connectivity for determining "enclosed" regions.

ndi.binary_hit_or_miss(input, structure1=None, structure2=None, output=None,
                       origin1=0, origin2=0)
  Hit-or-miss transform: find locations matching a specific pattern.
  structure1 : must be True (hit pattern).
  structure2 : must be False (miss pattern).
  Returns True where the pattern matches the input.
  Use for template matching / pattern detection in binary images.

ndi.binary_propagation(input, structure=None, mask=None, output=None,
                       border_value=0, origin=0)
  Propagate foreground pixels throughout a mask, constrained by connectivity.
  Equivalent to: connected dilation of input within the mask.
  Useful for flood-fill style operations and region growing.
'''

# binary_fill_holes
ring = np.zeros((15, 15), dtype=bool)
ring[3:12, 3:12] = True
ring[5:10, 5:10] = False   # hollow interior
filled = ndi.binary_fill_holes(ring)
print(f"Ring pixels: {ring.sum()}  Filled: {filled.sum()}")   # Ring pixels: 56  Filled: 81, filled > ring
print(f"Centre pixel (5,5) filled: {filled[5, 5]}")   # True

# binary_hit_or_miss: find isolated points (surrounded by background)
# Pattern: centre is True, all 4-connected neighbours are False
hit_pattern  = np.array([[0,0,0],[0,1,0],[0,0,0]], dtype=bool)
miss_pattern = np.array([[0,1,0],[1,0,1],[0,1,0]], dtype=bool)
hitmiss = ndi.binary_hit_or_miss(blob, structure1=hit_pattern, structure2=miss_pattern)
print(f"Isolated-centre locations: {np.argwhere(hitmiss)}")

# binary_propagation: grow seed within mask
seed = np.zeros((20, 20), dtype=bool)
seed[5, 5] = True   # single seed inside blob 1
propagated = ndi.binary_propagation(seed, mask=blob, structure=cross)
# Should fill all of blob 1 that is 4-connected to (5,5)
print(f"Propagated from seed: {propagated.sum()} pixels")  # 25 (entire blob 1)

##----------------------------------------------------------------##
## 26. grey_erosion / grey_dilation / grey_opening / grey_closing ##
##----------------------------------------------------------------##
'''
Greyscale morphological operations on float arrays.

grey_erosion(input, size=None, footprint=None, structure=None, ...)
  Each output pixel = minimum of neighbourhood values (flat SE)
                    or min(neighbourhood + structure) for non-flat SE.
  flat SE (footprint): output[i] = min{input[j] : j in footprint(i)}
  non-flat SE (structure array with offsets): output[i] = min{input[j] - structure[k]}

grey_dilation(input, size=None, footprint=None, structure=None, ...)
  Each output pixel = max of neighbourhood.

grey_opening  : erosion then dilation (remove bright features smaller than SE).
grey_closing  : dilation then erosion (fill dark features smaller than SE).

All accept:
  size       : scalar or tuple (uniform footprint of this size).
  footprint  : boolean array selecting neighbours.
  structure  : float array of offsets for non-flat morphology.
'''

# Flat greyscale erosion (size parameter): running minimum
img_grey_erode = ndi.grey_erosion(img, size=5)   # 5×5 minimum
img_grey_dilate = ndi.grey_dilation(img, size=5)  # 5×5 maximum

print(f"Greyscale erosion range:  {img_grey_erode.min():.3f} .. {img_grey_erode.max():.3f}") # -3.899 .. -0.400
print(f"Greyscale dilation range: {img_grey_dilate.min():.3f} .. {img_grey_dilate.max():.3f}") # 0.331 .. 3.257

# These are the same as minimum_filter and maximum_filter for flat footprints
min_filt = ndi.minimum_filter(img, size=5)
max_filt = ndi.maximum_filter(img, size=5)
print(np.allclose(img_grey_erode, min_filt))   # True
print(np.allclose(img_grey_dilate, max_filt))  # True

# Greyscale opening: removes bright spots smaller than the SE
img_go = ndi.grey_opening(img, size=5)   # smooth bright spikes
# Greyscale closing: fills dark holes smaller than the SE
img_gc = ndi.grey_closing(img, size=5)

# Top-hat = img - opening: isolates bright spots/ridges smaller than SE
tophat = img - img_go   # bright features removed by opening = image - opening
bottomhat = img_gc - img   # dark features removed by closing

print(f"Top-hat (bright features): {tophat.min():.3f} .. {tophat.max():.3f}") # 0.000 .. 4.529
print(f"Bottom-hat (dark features): {bottomhat.min():.3f} .. {bottomhat.max():.3f}") # 0.000 .. 5.182

# Non-flat SE: structure offset defines a "paraboloid" footprint
parabola = np.zeros((5, 5))
yy, xx = np.mgrid[-2:3, -2:3]
parabola[:] = -(xx**2 + yy**2) * 0.1   # parabolic structure
img_erode_nf = ndi.grey_erosion(img, structure=parabola)

##-------------------------------------------------------------------------##
## 27. morphological_gradient / morphological_laplace / white/black tophat ##
##-------------------------------------------------------------------------##
'''
ndi.morphological_gradient(input, size=None, footprint=None, structure=None, ...)
  Dilation - Erosion: detects edges (similar to Sobel but morphological, nonlinear).
  Bright around bright/dark transitions.

ndi.morphological_laplace(input, size=None, ...)
  (Dilation + Erosion - 2*input): concave/convex surface detector.
  Zero at flat regions; positive at concave, negative at convex.

ndi.white_tophat(input, size=None, footprint=None, structure=None, ...)
  Input - Opening: isolates bright features smaller than the SE.
  Same as: img - grey_opening(img, size).
  Use to remove slowly varying background while keeping bright spots/ridges.

ndi.black_tophat(input, size=None, footprint=None, structure=None, ...)
  Closing - Input: isolates dark features smaller than the SE.
  Use to remove slowly varying bright background and find dark spots.
'''

# Morphological gradient (edge magnitude)
morph_grad_field = ndi.morphological_gradient(img, size=5)
print(f"Morphological gradient range: {morph_grad_field.min():.3f} .. {morph_grad_field.max():.3f}")
# 1.641 .. 6.965

# Verify: dilation - erosion
mg_verify = ndi.grey_dilation(img, size=5) - ndi.grey_erosion(img, size=5)
print(np.allclose(morph_grad_field, mg_verify))  # True

# Morphological Laplace
morph_lap = ndi.morphological_laplace(img, size=3)
print(f"Morphological Laplace std: {morph_lap.std():.4f}") # 1.9572

# White tophat: isolate bright compact features
img_with_bright = img.copy()
img_with_bright[20:23, 20:23] += 5.0   # add a bright 3×3 spot
wth = ndi.white_tophat(img_with_bright, size=5)   # detects the 3×3 spot
print(f"White tophat peak: {wth.max():.3f}")   # 6.671 large at the bright spot location

# Black tophat: isolate dark compact features
img_with_dark = img.copy()
img_with_dark[40:43, 40:43] -= 5.0   # add a dark spot
bth = ndi.black_tophat(img_with_dark, size=5)
print(f"Black tophat peak: {bth.max():.3f}")   # 7.515 large at the dark spot location

# 3-D morphological gradient
mg_3d = ndi.morphological_gradient(img3d, size=3)
print(mg_3d.shape) # (16, 32, 32)

##-----------------------------------------------------------------------------##
## 28. distance_transform_edt / distance_transform_cdt / distance_transform_bf ##
##-----------------------------------------------------------------------------##
'''
ndi.distance_transform_edt(input, sampling=None, return_distances=True,
                            return_indices=False, distances=None, indices=None)
  Exact Euclidean Distance Transform.
  For each False pixel in input, compute the distance to the nearest True pixel.
  (True = foreground/obstacle; False = background/free space.)

  sampling : pixel spacing (physical size) per dimension. Default all 1.0.
             Use for anisotropic data (e.g. MRI slices with different slice thickness).
  return_distances : if True (default), return distance array.
  return_indices   : if True, also return the index of the nearest foreground pixel.

ndi.distance_transform_cdt(input, metric='chessboard', ...)
  Chamfer distance transform (approximation): faster than EDT but less accurate.
  metric='chessboard' : L_infinity (max of abs diffs).
  metric='taxicab'    : L_1 (Manhattan) distance.

ndi.distance_transform_bf(input, metric='euclidean', ...)
  Brute-force distance transform: exact but slow.
  Use mainly for reference / verification.

Applications:
  - Object separation: watershed seeds from distance transform maxima.
  - Erosion by arbitrary amount: threshold the distance transform.
  - Shape analysis: skeleton / medial axis.
  - Collision detection / path planning.
'''

# Euclidean distance transform on the binary blob image
dist_edt = ndi.distance_transform_edt(blob)   # True=foreground, result=dist from False
# Wait: convention is: True = obstacle, output = distance to nearest True from False pixel?
# Actually: edt works on: True pixels are the "background" (where dist=0),
# False pixels are "foreground" (where dist > 0).
# More precisely: input=True -> these pixels have dist=0; input=False -> get positive dist.
# In practice use on the inverted mask if you want distance from object boundary.

# Common usage: distance of each background pixel to nearest foreground pixel
dist_from_blob = ndi.distance_transform_edt(~blob)   # ~blob: True=background=object
print(f"Distance shape: {dist_from_blob.shape}")  # (20, 20)
print(f"Distance range: {dist_from_blob.min():.2f} .. {dist_from_blob.max():.2f}") # 0.00 .. 12.37
# Background pixels have dist > 0; blob interior pixels have dist = 0

# More standard usage: distance inside the binary region to its boundary
dist_inside = ndi.distance_transform_edt(blob)   # True=foreground, False(boundary outside)=0
print(f"Inside dist max: {dist_inside.max():.2f}")   # 3.00 maximum inscribed sphere radius

# Local maxima of dist_inside = "skeleton" seeds (centres of the largest inscribed circles)
local_max_dist = (dist_inside == ndi.maximum_filter(dist_inside, size=3)) & blob
print(f"Skeleton seeds: {local_max_dist.sum()}") # 2

# Anisotropic (MRI voxels: 1×1×2 mm)
vol_bin_aniso = img3d > 0.5
dist_3d = ndi.distance_transform_edt(vol_bin_aniso, sampling=[1.0, 1.0, 2.0])
print(f"3-D EDT shape: {dist_3d.shape}")  # (16, 32, 32)

# return_indices: also get the coordinates of the nearest feature pixel
dist_edt2, idx_edt = ndi.distance_transform_edt(blob, return_indices=True)
print(f"Index array shape: {idx_edt.shape}")   # (2, 20, 20) — row and col of nearest True

# Chamfer distance transform (faster approximation)
dist_cdt_chess = ndi.distance_transform_cdt(blob, metric='chessboard')
dist_cdt_taxi  = ndi.distance_transform_cdt(blob, metric='taxicab')
print(f"Chessboard max dist: {dist_cdt_chess.max()}") # 3
print(f"Taxicab max dist:    {dist_cdt_taxi.max()}") # 3

# Watershed from distance transform peaks — full segmentation workflow
def watershed_from_distance(binary_mask):
    '''Segment touching objects using EDT + watershed.'''
    # 1. Distance transform of interior
    dist = ndi.distance_transform_edt(binary_mask)
    # 2. Find local maxima (seed candidates)
    is_peak = (dist == ndi.maximum_filter(dist, size=3)) & binary_mask
    # 3. Label the seeds
    seed_labels, _ = ndi.label(is_peak)
    # 4. Watershed from seeds (lower dist = harder to flood)
    watershed_input = (dist.max() - dist).astype(np.uint8)  # invert for watershed
    ws = ndi.watershed_ift(watershed_input, seed_labels)
    # 5. Restrict to original mask
    ws[~binary_mask] = 0
    return ws

# Test: two overlapping blobs
overlap_test = np.zeros((20, 20), dtype=bool)
overlap_test[3:12, 3:12] = True    # blob 1
overlap_test[8:17, 8:17] = True    # blob 2 (overlapping)
ws_result = watershed_from_distance(overlap_test)
print(f"Watershed segments: {len(np.unique(ws_result)) - 1}")   # 1 or 2 depending on overlap

# Brute-force (reference, slow — use only on small arrays)
dist_bf = ndi.distance_transform_bf(blob, metric='euclidean')
print(np.allclose(dist_bf, dist_edt2, atol=1e-3))  # True
