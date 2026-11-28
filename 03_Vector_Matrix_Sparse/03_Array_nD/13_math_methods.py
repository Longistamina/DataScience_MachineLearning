'''
1. Reductions: sum, mean, prod, max, min, ptp, var, std.
2. Cumulative methods: cumsum, cumprod.
3. Element-wise methods: round, clip.
4. Complex arrays: real, imag, conj / conjugate.
5. Matrix multiplication and transpose: @, dot, T, swapaxes.
'''

import numpy as np

arr = np.arange(1, 361, dtype=float).reshape(3, 4, 5, 6)
print(arr.shape)
# (3, 4, 5, 6)

# =========================================================================================
# 1. Statistical reductions
# =========================================================================================
'''
axis=None reduces all elements to a scalar.
axis=k removes axis k; a tuple reduces several axes at once.
keepdims=True keeps reduced axes with length 1 for broadcasting.
'''

print(arr.sum())
# 64980.0

print(arr.sum(axis=0).shape)
# (4, 5, 6)

print(arr.sum(axis=-1).shape)
# (3, 4, 5)

print(arr.mean(axis=(2, 3)).shape)
# (3, 4): one mean per last-two-axis matrix

print(arr.mean(axis=(2, 3), keepdims=True).shape)
# (3, 4, 1, 1)

print(arr.prod(axis=-1).shape)
# (3, 4, 5)

print(arr.max(axis=1).shape)
# (3, 5, 6)

print(arr.min(axis=(0, 2)).shape)
# (4, 6)

print(np.ptp(arr, axis=-1)[0, 0, :])
# [5. 5. 5. 5. 5.]: range = max - min

print(arr.var(axis=-1).shape)
# (3, 4, 5)

print(arr.std(axis=(2, 3)).shape)
# (3, 4)
# var/std default to ddof=0 (divide by N); ddof=1 divides by N-1.

# Broadcast each matrix's mean back over its elements.
centered = arr - arr.mean(axis=(-2, -1), keepdims=True)
print(centered.shape)
# (3, 4, 5, 6)

# =========================================================================================
# 2. Cumulative methods
# =========================================================================================
# A specified axis preserves the shape; axis=None (default) flattens.
# cumsum/cumprod accept a single axis or None, not a tuple.

print(arr.cumsum(axis=1).shape)
# (3, 4, 5, 6)

print(arr.cumsum(axis=-1)[0, 0, 0, :])
# [ 1.  3.  6. 10. 15. 21.]

print(arr.cumprod(axis=-1)[0, 0, 0, :])
# [  1.   2.   6.  24. 120. 720.]

print(arr.cumsum().shape)
# (360,)

print((1 + arr / 360).cumprod().shape)
# (360,): smaller factors keep this flattened-product example finite

# =========================================================================================
# 3. Rounding and clipping (element-wise; shape unchanged)
# =========================================================================================

scaled = arr / 7
print(scaled.round(decimals=2)[0, 0, 0, :])
# [0.14 0.29 0.43 0.57 0.71 0.86]

print(arr.clip(3, 5)[0, 0, 0, :])
# [3. 3. 3. 4. 5. 5.]

print(scaled.round(2).shape, arr.clip(3, 5).shape)
# (3, 4, 5, 6) (3, 4, 5, 6)

# =========================================================================================
# 4. Complex number methods (element-wise)
# =========================================================================================

arr_complex = arr + 2j
print(arr_complex.real.shape, arr_complex.imag.shape)
# (3, 4, 5, 6) (3, 4, 5, 6)
# real/imag are views of the complex array, not independent copies.

print(arr_complex.conj()[0, 0, 0, :3])
# [1.-2.j 2.-2.j 3.-2.j]

print(arr_complex.conjugate().shape)
# (3, 4, 5, 6): same as conj()

# =========================================================================================
# 5. Matrix multiplication and transpose
# =========================================================================================
'''
For @ / np.matmul: (..., m, k) @ (..., k, n) -> (..., m, n).
The last two axes are matrix axes; leading batch axes broadcast.
For nD arrays, dot() behaves differently from @.
'''

a = np.ones((3, 4, 5, 6))
b = np.ones((3, 4, 6, 2))

print((a @ b).shape)
# (3, 4, 5, 2)

print(np.matmul(a, b)[0, 0, 0, :])
# [6. 6.]

print((a @ np.ones((6, 2))).shape)
# (3, 4, 5, 2): one (6, 2) matrix broadcasts across all batches

print(a.dot(b).shape)
# (3, 4, 5, 3, 4, 2)
# dot contracts a's last axis with b's second-last axis,
# retaining BOTH sets of leading axes instead of broadcasting them.

print(arr.T.shape)
# (6, 5, 4, 3): reverses ALL axes; same as arr.transpose()

print(arr.transpose(0, 1, 3, 2).shape)
# (3, 4, 6, 5)

print(arr.swapaxes(-1, -2).shape)
# (3, 4, 6, 5): transpose each last-two-axis matrix

print(arr_complex.conj().swapaxes(-1, -2).shape)
# (3, 4, 6, 5): conjugate transpose of each matrix
