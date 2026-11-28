'''
Chain methods by calling each on the previous result.
Each step may change the shape; it need not return the same object.
'''

import numpy as np

arr = np.arange(360, dtype=float).reshape(3, 4, 5, 6)

# =========================================================================================
# 1. One-line chaining
# =========================================================================================

mean_arr = arr.mean(axis=(2, 3)).round(2)
print(mean_arr.shape)
# (3, 4): reduce the last two axes, then round element-wise

print(mean_arr[0])
# [ 14.5  44.5  74.5 104.5]

# =========================================================================================
# 2. Multi-line chaining
# =========================================================================================

result = (
    arr                         # (3, 4, 5, 6)
    .transpose(0, 2, 1, 3)       # (3, 5, 4, 6)
    .mean(axis=-1)              # (3, 5, 4)
    .round(2)                   # (3, 5, 4)
)
print(result.shape)
# (3, 5, 4)

# Keep reduced axes so the result broadcasts back over arr.
centered = arr - arr.mean(axis=(-2, -1), keepdims=True)
print(centered.shape)
# (3, 4, 5, 6)

print(np.allclose(centered.mean(axis=(-2, -1)), 0))
# True

# =========================================================================================
# 3. In-place methods return None: use a separate statement
# =========================================================================================

arr_demo = arr.copy()
arr_demo.sort(axis=-1)
print(arr_demo.shape)
# (3, 4, 5, 6)
# arr.copy().sort(axis=-1).round(2) would fail: sort() returns None.
# Other examples returning None: arr.resize(...), arr.fill(...), arr.put(...).

# Use np.sort() when you need an array result to continue a chain.
print(
    np.sort(arr, axis=-1)
    .mean(axis=1)
    .round(2)
    .shape
)
# (3, 5, 6)
