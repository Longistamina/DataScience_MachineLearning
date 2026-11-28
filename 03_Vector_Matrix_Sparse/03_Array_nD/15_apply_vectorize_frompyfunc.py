'''
1. apply_along_axis: call a function on each 1D slice.
2. apply_over_axes: call a reduction repeatedly, preserving ndim.
3. vectorize: wrap a scalar Python function with broadcasting.
4. frompyfunc: create an object-output ufunc from a Python function.
'''

import numpy as np

arr = np.arange(1, 361).reshape(3, 4, 5, 6)
print(arr.shape)
# (3, 4, 5, 6)

# =========================================================================================
# 1. np.apply_along_axis(func, axis, arr)
# =========================================================================================
# func receives a 1D slice; it may return a scalar OR an array.
# The selected axis is replaced by the shape of func's result.

print(np.apply_along_axis(np.mean, axis=1, arr=arr).shape)
# (3, 5, 6): scalar output removes axis 1

print(np.apply_along_axis(lambda x: [x.min(), x.max()], 1, arr).shape)
# (3, 2, 5, 6): a (2,) output replaces axis 1 with length 2


def normalize(x):
    std = x.std()
    return (x - x.mean()) / (std if std != 0 else 1)


normalized = np.apply_along_axis(normalize, axis=-1, arr=arr)
print(normalized.shape)
# (3, 4, 5, 6): a length-6 output preserves the selected axis

print(np.allclose(normalized.mean(axis=-1), 0))
# True
# For built-in reductions prefer arr.mean(axis=1), np.ptp(arr, axis=...), etc.
# math.log2 expects scalars; use np.log2(arr) for element-wise logarithms.

# =========================================================================================
# 2. np.apply_over_axes(func, arr, axes)
# =========================================================================================
# func(a, axis) must return the same ndim or reduce ndim by exactly one.
# apply_over_axes restores a removed axis with length 1 after each call.

print(np.apply_over_axes(np.sum, arr, axes=[0, 2]).shape)
# (1, 4, 1, 6)

print(np.apply_over_axes(np.mean, arr, axes=[2, 3]).shape)
# (3, 4, 1, 1)

print(np.apply_over_axes(np.sum, arr, axes=[0, 1, 2, 3]).shape)
# (1, 1, 1, 1)
# Simpler equivalent for sum: arr.sum(axis=(0, 2), keepdims=True).
# This applies reductions sequentially; it is not a cumulative operation.

# =========================================================================================
# 3. np.vectorize(func)
# =========================================================================================


def categorize(x):
    return 'Low' if x < 120 else ('Medium' if x < 240 else 'High')


categorize_array = np.vectorize(categorize, otypes=[str])
labels = categorize_array(arr)
print(labels.shape)
# (3, 4, 5, 6)

print(labels[:, 0, 0, 0])
# ['Low' 'Medium' 'High']

# Multiple inputs broadcast just like ordinary NumPy operations.
scale = np.vectorize(lambda x, w: x * w, otypes=[float])
scaled = scale(arr, np.arange(1, 7))
print(scaled[0, 0, 0, :])
# [ 1.  4.  9. 16. 25. 36.]
# otypes specifies output dtypes rather than inferring them from the first call.
# vectorize is a convenience wrapper around Python calls, not a speed boost.

# =========================================================================================
# 4. np.frompyfunc(func, nin, nout)
# =========================================================================================
# Inputs broadcast; each output has the broadcast shape and dtype=object.

##-------------------------##
## One input, one output   ##
##-------------------------##

hex_func = np.frompyfunc(hex, 1, 1)
hex_values = hex_func(arr)
print(hex_values.shape, hex_values.dtype)
# (3, 4, 5, 6) object

print(hex_values[0, 0, 0, :3])
# ['0x1' '0x2' '0x3']

##----------------------------##
## Multiple inputs, one output ##
##----------------------------##

weighted_sum = np.frompyfunc(lambda a, b, c, w1, w2, w3:
                             a*w1 + b*w2 + c*w3, 6, 1)
result = weighted_sum(arr, arr + 10, arr + 20, 0.5, 0.3, 0.2)
print(result.astype(float)[0, 0, 0, :3])
# [ 8.  9. 10.]

##----------------------------##
## One input, multiple outputs ##
##----------------------------##

stats = np.frompyfunc(lambda x: (x, x**2, np.sqrt(x)), 1, 3)
values, squares, roots = stats(arr)
print([x.shape for x in (values, squares, roots)])
# [(3, 4, 5, 6), (3, 4, 5, 6), (3, 4, 5, 6)]

##----------------------------------##
## Multiple inputs, multiple outputs ##
##----------------------------------##

operations = np.frompyfunc(lambda x, y: (x + y, x - y, x * y, x / y), 2, 4)
sums, diffs, prods, divs = operations(arr, np.arange(1, 7))
print(divs.astype(float)[0, 0, 0, :])
# [1. 1. 1. 1. 1. 1.]
# Prefer built-in array expressions when possible: arr * weights, np.sqrt(arr).
