'''
0. Masks: conditions produce boolean arrays with the same shape.
1. Single conditions: >, <, >=, <=, ==, !=, np.isin().
2. Negation: ~ reverses a boolean mask.
3. Multiple conditions: & (and), | (or); parenthesize comparisons.
4. Compression: arr.compress(mask, axis) selects along one axis.
5. np.any() / np.all(): reduce conditions to filter whole slices.
'''

import numpy as np

arr = np.arange(360).reshape(3, 4, 5, 6)

print(arr.shape)
# (3, 4, 5, 6)

# =========================================================================================
# 0. Masks and boolean indexing
# =========================================================================================

mask = arr > 350
print(mask.shape)
# (3, 4, 5, 6)

print(arr[mask])
# [351 352 353 354 355 356 357 358 359]
# A full-shape boolean mask selects elements into a 1D copy.

# A 1D mask selects whole slices along its matching axis.
axis_mask = np.array([True, False, True, False])
print(arr[:, axis_mask, :, :].shape)
# (3, 2, 5, 6): selects indices 0 and 2 on axis 1

# =========================================================================================
# 1. Single conditions and np.isin()
# =========================================================================================

print(arr[arr < 5])
# [0 1 2 3 4]

print(arr[arr >= 355])
# [355 356 357 358 359]

print(arr[arr == 42])
# [42]

print(arr[arr != 42].shape)
# (359,)

mask_isin = np.isin(arr, [10, 150, 300])
print(mask_isin.shape)
# (3, 4, 5, 6): np.isin() preserves the input shape

print(arr[mask_isin])
# [ 10 150 300]

print(arr[np.isin(arr, [10, 150, 300], invert=True)].shape)
# (357,): elements NOT in the list

# =========================================================================================
# 2. Negation: ~ (tilde)
# =========================================================================================

print(arr[~(arr >= 5)])
# [0 1 2 3 4]

print(arr[~np.isin(arr, [10, 150, 300])].shape)
# (357,): equivalent to np.isin(..., invert=True)

# =========================================================================================
# 3. Multiple conditions: &, |
# =========================================================================================

print(arr[(arr > 150) & (arr < 155)])
# [151 152 153 154]

print(arr[(arr < 3) | (arr > 356)])
# [  0   1   2 357 358 359]

print(arr[((arr >= 150) & (arr <= 153)) | (arr == 42)])
# [ 42 150 151 152 153]
# Use &, |, ~ for element-wise logic; parenthesize each comparison.

# =========================================================================================
# 4. Boolean compression: arr.compress(mask, axis)
# =========================================================================================
'''
compress() requires a 1D mask. For whole-axis filtering, use a mask whose
length equals arr.shape[axis]. Only that axis changes size.
With axis=None, compress() flattens the input array automatically.
'''

print(arr.compress([True, False, True, False], axis=1).shape)
# (3, 2, 5, 6): equivalent to arr[:, axis_mask, :, :]

# Reduce all axes except axis 1 to obtain one mean per axis-1 slice.
axis_mask = arr.mean(axis=(0, 2, 3)) > 180
print(axis_mask)
# [False False  True  True]

print(arr.compress(axis_mask, axis=1).shape)
# (3, 2, 5, 6)

print(arr.compress((arr > 355).ravel()))
# [356 357 358 359]: flatten the MASK; arr is flattened automatically

# =========================================================================================
# 5. Filtering whole slices with np.any() and np.all()
# =========================================================================================
'''
any(): at least one True; all(): every value is True.
To filter axis k, reduce ALL OTHER axes to get a 1D mask for axis k.
The reduced axes disappear unless keepdims=True.
'''

##---------------------##
## Filter axis 0       ##
##---------------------##

mask_any = np.any(arr > 250, axis=(1, 2, 3))
print(mask_any)
# [False False  True]

print(arr[mask_any].shape)
# (1, 4, 5, 6)

mask_all = np.all(arr >= 120, axis=(1, 2, 3))
print(mask_all)
# [False  True  True]

print(arr[mask_all].shape)
# (2, 4, 5, 6)

##---------------------##
## Filter last axis    ##
##---------------------##

mask_last = np.any(arr > 356, axis=(0, 1, 2))
print(mask_last)
# [False False False  True  True  True]

print(arr[..., mask_last].shape)
# (3, 4, 5, 3)

mask_last_all = np.all(arr >= 3, axis=(0, 1, 2))
print(arr[..., mask_last_all].shape)
# (3, 4, 5, 3)

##------------------------------------##
## Reduce only the last axis          ##
##------------------------------------##

mask_slices = np.any(arr > 350, axis=-1)
print(mask_slices.shape)
# (3, 4, 5): one boolean per last-axis slice

print(arr[mask_slices].shape)
# (2, 6): selects two complete last-axis slices
# A mask matching the leading axes combines those axes; trailing axes remain.

print(np.any(arr > 350, axis=-1, keepdims=True).shape)
# (3, 4, 5, 1): useful for broadcasting, but NOT a full-shape indexing mask

print(np.any(arr > 350), np.all(arr > 350))
# True False: omitting axis reduces the entire array
