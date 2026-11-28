'''
1. Basic indexing: one index per axis; integer indices remove axes.
2. Fancy indexing: index lists select paired positions or whole slices.
3. Slicing: start:stop:step per axis; slices preserve axes.
4. Selection methods: item(), take(), np.take_along_axis().
5. Modifying elements: indexed assignment and put().
6. Ellipsis (...): fills in omitted axes with full slices (:).
'''

import numpy as np

arr = np.arange(360).reshape(3, 4, 5, 6)

print(arr.shape)
# (3, 4, 5, 6)

# =========================================================================================
# 1. Basic indexing: arr[i0, i1, i2, i3]
# =========================================================================================

print(arr[1, 2, 3, 4])
# 202

print(arr[-1, -1, -1, -1])
# 359

print(arr[1].shape)
# (4, 5, 6): equivalent to arr[1, :, :, :]

print(arr[:, 2, :, :].shape)
# (3, 5, 6): integer index removes axis 1

print(arr[:, 2:3, :, :].shape)
# (3, 1, 5, 6): slice keeps axis 1

# =========================================================================================
# 2. Fancy indexing
# =========================================================================================

# Lists select PAIRED coordinates, not every combination.
print(arr[[0, 2], [1, 3], [2, 4], [3, 5]])
# [ 45 359]: positions (0, 1, 2, 3) and (2, 3, 4, 5)

print(arr[:, [0, 2], :, :].shape)
# (3, 2, 5, 6)

# np.ix_ selects EVERY combination of the supplied indices.
print(arr[np.ix_([0, 2], [1, 3], [2, 4], [3, 5])].shape)
# (2, 2, 2, 2)

# =========================================================================================
# 3. Slicing: start:stop:step on each axis (stop is excluded)
# =========================================================================================

print(arr[:2, 1:4, 2:5, :3].shape)
# (2, 3, 3, 3)

print(arr[::2, ::2, ::2, ::2].shape)
# (2, 2, 3, 3)

print(arr[-2:, :, -3:, -4:].shape)
# (2, 4, 3, 4)

print(arr[:, :, :, ::-1].shape)
# (3, 4, 5, 6): reverses the last axis; shape stays the same

# Basic slices are views; fancy indexing returns copies.
# Use arr[...].copy() when you need an independent array.

# =========================================================================================
# 4. Selection methods
# =========================================================================================

##------------##
## arr.item() ##
##------------##

print(arr.item(1, 2, 3, 4))
# 202: returns a Python scalar

print(arr.item(10))
# 10: flat index in C order (last axis varies fastest)

##---------------------------##
## arr.take(indices, axis=) ##
##---------------------------##

print(arr.take([0, 2], axis=1).shape)
# (3, 2, 5, 6): same indices for every slice along axis 1

print(arr.take([1, 3, 5], axis=-1).shape)
# (3, 4, 5, 3)

print(arr.take([0, 7, 14]))
# [ 0  7 14]: omitting axis uses the flattened array

##----------------------##
## np.take_along_axis() ##
##----------------------##
'''
Select different indices for each slice along an axis.
Indices must have the same ndim as arr; sizes on other axes must broadcast.
The selected axis can have a different length.
'''

# One maximum per last-axis slice; keepdims preserves all 4 axes.
indices = np.argmax(arr, axis=-1, keepdims=True)
print(indices.shape)
# (3, 4, 5, 1)

selected = np.take_along_axis(arr, indices, axis=-1)
print(selected.shape)
# (3, 4, 5, 1)

print(selected[0, 0, :, 0])
# [ 5 11 17 23 29]

# argsort + take_along_axis sorts each last-axis slice.
indices = np.argsort(arr, axis=-1)
print(np.take_along_axis(arr, indices, axis=-1).shape)
# (3, 4, 5, 6)

# =========================================================================================
# 5. Modifying elements
# =========================================================================================

arr_demo = arr.copy()

arr_demo[1, 2, 3, 4] = 999
print(arr_demo[1, 2, 3, 4], arr[1, 2, 3, 4])
# 999 202

# A scalar broadcasts to every element of the selected block.
arr_demo[:, 1:3, :, :] = 0
print(arr_demo[:, 1:3, :, :].shape)
# (3, 2, 5, 6): all selected elements are now 0

# A (3,) array broadcasts across the leading selected axes.
arr_demo[..., :3] = [111, 222, 333]
print(arr_demo[0, 0, 0, :])
# [111 222 333   3   4   5]

arr_demo[[0, 2], [1, 3], [2, 4], [3, 5]] = [500, 501]
print(arr_demo[[0, 2], [1, 3], [2, 4], [3, 5]])
# [500 501]: direct fancy-index assignment updates arr_demo

##----------------------------------------##
## arr.put(flat_indices, new_values)      ##
##----------------------------------------##

arr_demo = arr.copy()
arr_demo.put([0, 7, 14], [111, 222, 333])
print(arr_demo.flat[[0, 7, 14]])
# [111 222 333]: put() uses flat indices in C order

# =========================================================================================
# 6. Ellipsis: ... represents as many full slices (:) as needed
# =========================================================================================

print(arr[..., 2].shape)
# (3, 4, 5): equivalent to arr[:, :, :, 2]

print(arr[1, ...].shape)
# (4, 5, 6): equivalent to arr[1, :, :, :]

print(arr[..., 1:4].shape)
# (3, 4, 5, 3): equivalent to arr[:, :, :, 1:4]

print(arr[1, ..., 3].shape)
# (4, 5): equivalent to arr[1, :, :, 3]
