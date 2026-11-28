'''
1. Basic iteration: nditer() visits scalar elements of an nD array.
2. Indices: multi_index gives one coordinate per axis.
3. Modification: readwrite / writeonly and x[...] assignment.
4. Chunks: external_loop yields 1D chunks.
5. Multiple arrays: iterate together with broadcasting.
'''

import numpy as np

arr = np.arange(360).reshape(3, 4, 5, 6)
print(arr.shape)
# (3, 4, 5, 6)

# =========================================================================================
# 1. Basic iteration (read only)
# =========================================================================================

# order='C': last axis varies fastest. Default order='K' follows memory layout.
with np.nditer(arr, order='C') as it:
    for value in it:
        if value < 5:
            print(value, end=' ')
print()
# 0 1 2 3 4

# flat always visits elements in C order, regardless of ndim.
print(list(arr.flat)[:5])
# First five values: [0, 1, 2, 3, 4]

print(next(iter(arr)).shape)
# (4, 5, 6): ordinary iteration yields slices along axis 0

# =========================================================================================
# 2. Get indices while looping
# =========================================================================================

with np.nditer(arr, flags=['multi_index'], order='C') as it:
    for value in it:
        if value < 3:
            print(it.multi_index, value)
# (0, 0, 0, 0) 0
# (0, 0, 0, 1) 1
# (0, 0, 0, 2) 2

# Simpler alternative when you only need coordinates and values:
for index, value in np.ndenumerate(arr):
    if value < 3:
        print(index, value)
# Same three lines as above

# =========================================================================================
# 3. Modify values
# =========================================================================================

arr_demo = arr.copy()
with np.nditer(arr_demo, op_flags=['readwrite']) as it:
    for x in it:
        x[...] = x * 2
# x is a 0D array view; x[...] writes through to the original element.
# A context manager ensures any buffered writes are completed on exit.

print(arr_demo[0, 0, 0, :])
# [ 0  2  4  6  8 10]

# multi_index works for any ndim: no need to unpack fixed row/column indices.
positions = np.empty_like(arr)
with np.nditer(positions, flags=['multi_index'], op_flags=['writeonly']) as it:
    for x in it:
        x[...] = sum(it.multi_index)

print(positions[1, 2, 3, :])
# [ 6  7  8  9 10 11]

# =========================================================================================
# 4. Process in chunks
# =========================================================================================

arr_demo = arr.copy()
chunk_sizes = []
with np.nditer(arr_demo, flags=['external_loop', 'buffered'],
               op_flags=['readwrite'], order='C', buffersize=60) as it:
    for chunk in it:
        chunk_sizes.append(chunk.size)
        chunk[...] = chunk ** 2

print(chunk_sizes)
# [60, 60, 60, 60, 60, 60]

print(arr_demo.shape)
# (3, 4, 5, 6): chunk iteration does not change the array shape

print(arr_demo[0, 0, 0, :])
# [ 0  1  4  9 16 25]
# Without buffering, chunk sizes depend on memory layout.
# external_loop cannot be combined with multi_index.

# =========================================================================================
# 5. Iterate over multiple arrays with broadcasting
# =========================================================================================

weights = np.arange(1, 7)  # (6,) broadcasts over the leading axes
result = np.empty_like(arr)

with np.nditer([arr, weights, result],
               op_flags=[['readonly'], ['readonly'], ['writeonly']]) as it:
    for value, weight, out in it:
        out[...] = value * weight

print(result.shape)
# (3, 4, 5, 6)

print(result[0, 0, 0, :])
# [ 0  2  6 12 20 30]

# Prefer vectorized operations for ordinary element-wise math:
# arr * 2, arr ** 2, arr * weights.
# Use nditer when custom iteration, memory order, or buffering is needed.
