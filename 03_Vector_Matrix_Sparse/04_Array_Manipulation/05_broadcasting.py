'''
Broadcasting is NumPy's mechanism for performing arithmetic between
arrays of different shapes without making explicit copies of data.
NumPy "stretches" the smaller array across the larger one so that
they have compatible shapes, then applies the operation element-wise.

##---------------------------##

Broadcasting Rules (applied dimension by dimension, right-to-left):
  1. If arrays have different numbers of dimensions, prepend 1s to the
     shape of the smaller array until both shapes have the same length.
  2. Dimensions are compatible if they are equal OR one of them is 1.
  3. If neither condition holds, NumPy raises a ValueError.
  4. The output shape is the element-wise maximum of the two shapes.

##---------------------------##

Flow of contents:

0. The Broadcasting Rules — shape alignment examples

1. 1D Array Broadcasting
   + scalar  op  1D
   + 1D      op  1D  (same shape)
   + 1D      op  1D  (one has size-1 dimension)

2. 2D Array (Matrix) Broadcasting
   + scalar  op  2D
   + 1D (row-vector) op 2D
   + column-vector   op 2D
   + 2D      op  2D  (compatible shapes)

3. 3D Array Broadcasting
   + scalar  op  3D
   + 1D      op  3D
   + 2D      op  3D

4. 4D Array Broadcasting
   + scalar  op  4D
   + 1D      op  4D
   + 3D      op  4D

5. Mixed-dimension Broadcasting
   + 1D op 2D
   + 1D op 3D
   + 2D op 3D
   + 2D op 4D
   + 3D op 4D

6. NumPy broadcasting functions:
   + np.broadcast_to
   + np.broadcast_arrays
   + np.broadcast_shapes

7. Practical Examples
   + Row-wise normalisation (zero-mean, unit-variance)
   + Column-wise normalisation
   + Pairwise Euclidean distance matrix
   + Outer product via broadcasting
   + Additive bias in a neural-network layer
'''

import numpy as np

# =========================================================================================
# 0. The Broadcasting Rules — shape alignment 
# =========================================================================================
'''
NumPy compares shapes right-to-left and applies the two rules:
  Rule A: if lengths differ, pad the shorter shape on the LEFT with 1s.
  Rule B: in each position, sizes must be equal or one must be 1.

Examples of shape compatibility:

  A:       (3,)    =>   (1, 3)   after padding   compatible with (4, 3)  -> out (4, 3)
  B:    (4, 1)     vs    (3,)    =>  (4, 1) vs (1, 3)                   -> out (4, 3)
  C: (2, 1, 5)     vs   (3, 5)   =>  (2, 1, 5) vs (1, 3, 5)            -> out (2, 3, 5)
  D:    (3, 4)     vs   (4, 4)   -> incompatible! 3 != 4, neither is 1  -> ValueError
'''

# Helper to show shape rules clearly
def show_broadcast(a, b, op=np.add):
    try:
        result = op(a, b)
        print(f"  {a.shape}  {op.__name__}  {b.shape}  =>  {result.shape}")
    except ValueError as e:
        print(f"  {a.shape}  {op.__name__}  {b.shape}  =>  ERROR: {e}")

print("Shape compatibility check:")
show_broadcast(np.ones((4, 3)),    np.ones((3,)))          # (4,3) + (3,)   => (4,3)
show_broadcast(np.ones((4, 1)),    np.ones((3,)))          # (4,1) + (3,)   => (4,3)
show_broadcast(np.ones((2, 1, 5)), np.ones((3, 5)))        # (2,1,5)+(3,5)  => (2,3,5)
show_broadcast(np.ones((3, 4)),    np.ones((4, 4)))        # ERROR: 3 != 4
show_broadcast(np.ones((1, 1, 4)), np.ones((3, 2, 4)))    # (1,1,4)+(3,2,4)=> (3,2,4)


# =========================================================================================
# 1. 1D Array Broadcasting
# =========================================================================================

v = np.array([10, 20, 30, 40, 50])   # shape (5,)

##----------------##
## scalar  op  1D ##
##----------------##
'''
A Python scalar is treated as a 0-D array of shape ().
Rule A pads it to (1,) then (1,) broadcasts to (5,).
Every element gets the same scalar applied.
'''

print(v + 5)
# [15 25 35 45 55]

print(v * 2)
# [20 40 60 80 100]

print(v ** 2)
# [ 100  400  900 1600 2500]

print(v / 10)
# [1. 2. 3. 4. 5.]

print(v % 3)
# [1 2 0 1 2]

##----------------------##
## 1D op 1D (same size) ##
##----------------------##
'''
When both 1D arrays have the same length, broadcasting is trivially element-wise.
Shape (5,) op (5,) => (5,). No stretching needed.
'''

a = np.array([1, 2, 3, 4, 5])   # shape (5,)
b = np.array([5, 4, 3, 2, 1])   # shape (5,)

print(a + b)   # [6 6 6 6 6]
print(a * b)   # [5 8 9 8 5]
print(a - b)   # [-4 -2  0  2  4]

##--------------------------##
## 1D op 1D (one is size-1) ##
##--------------------------##
'''
Shape (5,) op (1,): the size-1 array stretches to (5,) — equivalent to a scalar.
'''

c = np.array([100])   # shape (1,)

print(a + c)    # [101 102 103 104 105]
print(a * c)    # [100 200 300 400 500]


# =========================================================================================
# 2. 2D Array (Matrix) Broadcasting
# =========================================================================================

matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9],
                   [10,11,12]])   # shape (4, 3)

##--------------##
## scalar op 2D ##
##--------------##
'''
Scalar () pads left to (1,1) then broadcasts to (4,3).
'''

print(matrix + 100)
# [[101 102 103]
#  [104 105 106]
#  [107 108 109]
#  [110 111 112]]

print(matrix * 2)
# [[ 2  4  6]
#  [ 8 10 12]
#  [14 16 18]
#  [20 22 24]]

##-----------------------##
## 1D (row-vector) op 2D ##
##-----------------------##
'''
row = shape (3,) => padded to (1, 3) => broadcast to (4, 3).
The same row is applied to every row of the matrix.
'''

row = np.array([10, 20, 30])   # shape (3,)

print(matrix + row)
# [[11 22 33]
#  [14 25 36]
#  [17 28 39]
#  [20 31 42]]

print(matrix * row)
# [[ 10  40  90]
#  [ 40 100 180]
#  [ 70 160 270]
#  [100 220 360]]

##---------------------##
## column-vector op 2D ##
##---------------------##
'''
col = shape (4,) is 1D, so we must reshape to (4, 1) first.
(4, 1) broadcasts to (4, 3): the same scalar is applied across each row.
'''

col = np.array([10, 20, 30, 40]).reshape(4, 1)   # shape (4, 1)

print(matrix + col)
# [[11 12 13]
#  [24 25 26]
#  [37 38 39]
#  [50 51 52]]

print(matrix * col)
# [[ 10  20  30]
#  [ 80 100 120]
#  [210 240 270]
#  [400 440 480]]

# Alternatively using np.newaxis / None
col_v2 = np.array([10, 20, 30, 40])[:, np.newaxis]   # shape (4, 1)  — same result
print(np.array_equal(matrix + col, matrix + col_v2))   # True

##-----------------------##
## 2D op 2D (compatible) ##
##-----------------------##
'''
(4, 3) op (4, 1): column of 1s stretches right to (4, 3).
(4, 3) op (1, 3): row of 1s stretches down to (4, 3).
'''

col_2d = np.array([[1], [2], [3], [4]])   # shape (4, 1)
# Broadcasts to (4, 3)
# [[1 1 1]
#  [2 2 2]
#  [3 3 3]
#  [4 4 4]]

row_2d = np.array([[100, 200, 300]]) # shape (1, 3)
# Broadcasts to (4, 3)
# [[100 200 300]
#  [100 200 300]
#  [100 200 300]
#  [100 200 300]

print(matrix + col_2d)
# [[ 2  3  4]
#  [ 6  7  8]
#  [10 11 12]
#  [14 15 16]]

print(matrix + row_2d)
# [[101 202 303]
#  [104 205 306]
#  [107 208 309]
#  [110 211 312]]

# Both together: (4,1) + (1,3) => (4,3)  — outer-product-like addition
print(col_2d + row_2d)
# [[101 201 301]
#  [102 202 302]
#  [103 203 303]
#  [104 204 304]]


# =========================================================================================
# 3. 3D Array Broadcasting
# =========================================================================================

T = np.arange(24).reshape(2, 3, 4)   # shape (2, 3, 4)
# [[[ 0  1  2  3]
#   [ 4  5  6  7]
#   [ 8  9 10 11]]
#  [[12 13 14 15]
#   [16 17 18 19]
#   [20 21 22 23]]]

##--------------##
## scalar op 3D ##
##--------------##

print((T + 10).shape)   # (2, 3, 4)
print(T + 10)
# [[[ 10 11 12 13]
#   [ 14 15 16 17]
#   [ 18 19 20 21]]
#  [[ 22 23 24 25]
#   [ 26 27 28 29]
#   [ 30 31 32 33]]]

##----------##
## 1D op 3D ##
##----------##
'''
shape (4,) => padded to (1, 1, 4) => broadcast to (2, 3, 4).
Applied identically across the two "depth" slices and the 3 rows.
'''

v_1d = np.array([1, 2, 3, 4])   # shape (4,)
# Broadcasts to (2, 3, 4):
# [[[1 2 3 4]
#   [1 2 3 4]
#  [1 2 3 4]]
#
# [[1 2 3 4]
#  [1 2 3 4]
#  [1 2 3 4]]]

print((T + v_1d).shape)   # (2, 3, 4)
print(T + v_1d)
# [[[ 1  3  5  7]
#   [ 5  7  9 11]
#   [ 9 11 13 15]]
#  [[13 15 17 19]
#   [17 19 21 23]
#   [21 23 25 27]]]

# # 
# Stretch along axis-1 (rows): shape (3,) => (1, 3, 1) => (2, 3, 4)
v_rows = np.array([10, 20, 30]).reshape(1, 3, 1)   # shape (1, 3, 1)
# Broadcasts to (2, 3, 4):
# [[[10 10 10 10]
#   [20 20 20 20]
#   [30 30 30 30]]
#  [[10 10 10 10]
#   [20 20 20 20]
#   [30 30 30 30]]]

print((T + v_rows).shape)   # (2, 3, 4)
print(T + v_rows)
# [[[ 10 11 12 13]
#   [ 24 25 26 27]
#   [ 38 39 40 41]]
#  [[ 22 23 24 25]
#   [ 36 37 38 39]
#   [ 50 51 52 53]]]

# Stretch along axis-0 (depth): shape (2,) => (2, 1, 1) => (2, 3, 4)
v_depth = np.array([100, 200]).reshape(2, 1, 1)   # shape (2, 1, 1)

print((T + v_depth).shape)   # (2, 3, 4)
print(T + v_depth)
# [[[100 101 102 103]
#   [104 105 106 107]
#   [108 109 110 111]]
#  [[212 213 214 215]
#   [216 217 218 219]
#   [220 221 222 223]]]

##----------##
## 2D op 3D ##
##----------##
'''
shape (3, 4) => padded to (1, 3, 4) => broadcast to (2, 3, 4).
The same 2D "slice" is applied to every depth layer.
'''

M_2d = np.array([[1, 0, 1, 0],
                 [0, 1, 0, 1],
                 [1, 1, 0, 0]])   # shape (3, 4)

print((T + M_2d).shape)   # (2, 3, 4)
print(T + M_2d)
# [[[ 1  1  3  3]
#   [ 4  6  6  8]
#   [ 9 10 10 11]]
#  [[13 13 15 15]
#   [16 18 18 20]
#   [21 22 22 23]]]

# (2,1,4) op (2,3,4): stretches the middle axis
M_rows_only = np.ones((2, 1, 4), dtype=int) * np.array([[[10, 20, 30, 40]]])
print((T + M_rows_only).shape)   # (2, 3, 4)


# =========================================================================================
# 4. 4D Array Broadcasting
# =========================================================================================

F = np.arange(48).reshape(2, 3, 4, 2)   # shape (2, 3, 4, 2)  — e.g. batch of images

##--------------##
## scalar op 4D ##
##--------------##

print((F * 0.5).shape)   # (2, 3, 4, 2)

##----------##
## 1D op 4D ##
##----------##
'''
shape (2,) => padded to (1, 1, 1, 2) => broadcast to (2, 3, 4, 2).
Applied identically to the last axis (e.g. 2 colour channels).
'''

channel_bias = np.array([10, 20])   # shape (2,)

print((F + channel_bias).shape)   # (2, 3, 4, 2)
print((F + channel_bias)[0, 0])
# [[10 21]
#  [12 23]
#  [14 25]
#  [16 27]]

##----------##
## 3D op 4D ##
##----------##
'''
shape (3, 4, 2) => padded to (1, 3, 4, 2) => broadcast to (2, 3, 4, 2).
The same (3,4,2) block applies to every element along the first (batch) axis.
'''

filter_3d = np.ones((3, 4, 2), dtype=int)   # shape (3, 4, 2)

print((F + filter_3d).shape)   # (2, 3, 4, 2)
print(np.array_equal(F + filter_3d,
                     np.stack([F[0] + filter_3d, F[1] + filter_3d])))   # True


# =========================================================================================
# 5. Mixed-dimension Broadcasting
# =========================================================================================

##----------##
## 1D op 2D ##
##----------##
'''
Shape alignment (right-to-left):
  (5,)   vs   (4, 5)   =>   (1, 5)  vs  (4, 5)   =>  out (4, 5)
The row-vector is added to every row of the matrix.
'''

v5  = np.array([1, 2, 3, 4, 5])              # shape (5,)
M45 = np.arange(20).reshape(4, 5)            # shape (4, 5)

print((M45 + v5).shape)   # (4, 5)
print(M45 + v5)
# [[ 1  3  5  7  9]
#  [ 6  8 10 12 14]
#  [11 13 15 17 19]
#  [16 18 20 22 24]]

# Column-wise: reshape v to (4,1) so it broadcasts across columns
v4 = np.array([10, 20, 30, 40])[:, None]     # shape (4, 1)
print(M45 + v4)
# [[10 11 12 13 14]
#  [25 26 27 28 29]
#  [32 33 34 35 36]
#  [49 50 51 52 53]]

##----------##
## 1D op 3D ##
##----------##
'''
  (4,)   vs   (2, 3, 4)   =>   (1, 1, 4)  vs  (2, 3, 4)   =>  out (2, 3, 4)
Applied along the last axis (innermost dimension).
'''

v4_  = np.array([100, 200, 300, 400])         # shape (4,)
T234 = np.arange(24).reshape(2, 3, 4)         # shape (2, 3, 4)

print((T234 + v4_).shape)   # (2, 3, 4)
print(T234 + v4_)
# [[[100 201 302 403]
#   [104 205 306 407]
#   [108 209 310 411]]
#  [[112 213 314 415]
#   [116 217 318 419]
#   [120 221 322 423]]]

# Stretch along axis-0: reshape to (2,1,1) for depth-wise bias
v2_ = np.array([0, 1000]).reshape(2, 1, 1)    # shape (2, 1, 1)
print((T234 + v2_).shape)   # (2, 3, 4)
print((T234 + v2_)[0, 0])   # [0 1 2 3]
print((T234 + v2_)[1, 0])   # [1012 1013 1014 1015]

##----------##
## 2D op 3D ##
##----------##
'''
  (3, 4)   vs   (2, 3, 4)   =>   (1, 3, 4)  vs  (2, 3, 4)   =>  out (2, 3, 4)
The 2D matrix is broadcast across the leading dimension (batch/depth axis).
'''

M34  = np.array([[1, 0, 1, 0],
                 [0, 1, 0, 1],
                 [1, 1, 0, 0]])   # shape (3, 4)
T234b = np.arange(24).reshape(2, 3, 4)

print((T234b * M34).shape)   # (2, 3, 4)
print(T234b * M34)
# [[[ 0  0  2  0]
#   [ 0  5  0  7]
#   [ 8  9  0  0]]
#  [[12  0 14  0]
#   [ 0 17  0 19]
#   [20 21  0  0]]]

# (2, 1, 4) op (2, 3, 4): row-wise broadcast within each depth slice
M214 = np.array([[[10, 20, 30, 40]],
                 [[50, 60, 70, 80]]])   # shape (2, 1, 4)

print((T234b + M214).shape)   # (2, 3, 4)
print(T234b + M214)
# [[[ 10 21 32 43]
#   [ 14 25 36 47]
#   [ 18 29 40 51]]
#  [[ 62 73 84 95]
#   [ 66 77 88 99]
#   [ 70 81 92 103]]]

##----------##
## 2D op 4D ##
##----------##
'''
  (3, 2)   vs   (2, 3, 4, 2)
  padded:   (1, 1, 3, 2)  vs  (2, 3, 4, 2)  =>  ERROR (3 != 4 at axis -2)

  To broadcast (3,2) across axis-1 and axis-3 of a (2,3,4,2) tensor we need
  shape (1, 3, 1, 2) — always think right-to-left and pad to the same ndim.
'''

F2342 = np.arange(48).reshape(2, 3, 4, 2)
M_1312 = np.ones((1, 3, 1, 2), dtype=int) * np.array([[[[10, 20]],
                                                         [[30, 40]],
                                                         [[50, 60]]]])
# shape (1, 3, 1, 2) => (2, 3, 4, 2)

print((F2342 + M_1312).shape)   # (2, 3, 4, 2)
print((F2342 + M_1312)[0])
# [[[10 21]
#   [12 23]
#   [14 25]
#   [16 27]]
#  [[38 49]
#   [40 51]
#   [42 53]
#   [44 55]]
#  [[58 71]
#   [60 73]
#   [62 75]
#   [64 77]]]

##----------##
## 3D op 4D ##
##----------##
'''
  (3, 4, 2)   vs   (2, 3, 4, 2)
  padded:   (1, 3, 4, 2)  vs  (2, 3, 4, 2)   =>  out (2, 3, 4, 2)
The 3D block is applied identically to each element of the batch (axis 0).
'''

block_3d = np.ones((3, 4, 2), dtype=int)   # shape (3, 4, 2)

print((F2342 + block_3d).shape)   # (2, 3, 4, 2)
# equivalent: np.stack([F2342[i] + block_3d for i in range(2)])
print(np.array_equal(F2342 + block_3d,
                     np.stack([F2342[0] + block_3d,
                                F2342[1] + block_3d])))   # True


# =========================================================================================
# 6. NumPy broadcasting functions 
# =========================================================================================

##-------------------##
## np.broadcast_to() ##
##-------------------##
'''Broadcast an array to a new shape.'''

x = np.array([1, 2, 3])   # shape (3,)

print(np.broadcast_to(array=x, shape=(4, 3)))
# [[1 2 3]
#  [1 2 3]
#  [1 2 3]
#  [1 2 3]]

print(np.broadcast_to(x, (3, 2, 3)))
# [[[1 2 3]
#   [1 2 3]]

#  [[1 2 3]
#   [1 2 3]]

#  [[1 2 3]
#   [1 2 3]]]

##-----------------------##
## np.broadcast_arrays() ##
##-----------------------##
'''
Broadcast multiple arrays against each other and return views.
NOTE: the returned arrays are in tuple.
'''

a1 = np.array([1, 2, 3])   # shape (3,)
a2 = np.array([[10], [20], [30], [40]])   # shape (4, 1)

print(np.broadcast_arrays(a1, a2))
# (array([[1, 2, 3],
#        [1, 2, 3],
#        [1, 2, 3],
#        [1, 2, 3]]), array([[10, 10, 10],
#        [20, 20, 20],
#        [30, 30, 30],
#        [40, 40, 40]]))

b1, b2 = np.broadcast_arrays(a1, a2)

print(b1)
# [[1 2 3]
#  [1 2 3]
#  [1 2 3]
#  [1 2 3]]

print(b2)
# [[10 10 10]
#  [20 20 20]
#  [30 30 30]
#  [40 40 40]]

##-----------------------##
## np.broadcast_shapes() ##
##-----------------------##
'''Determine the shape of the broadcast result from multiple shapes.'''

shape1 = (3,)      # -> (1, 1, 3)
shape2 = (4, 1)    # -> (1, 4, 1)
shape3 = (2, 4, 1) # -> (2, 4, 1)
                   # => (2, 4, 3) MAX

print(np.broadcast_shapes(shape1, shape2, shape3))
# (2, 4, 3)


# =========================================================================================
# 7. Practical Examples
# =========================================================================================

data = np.array([[ 2., 4., 6., 8.],
                 [ 1., 3., 5., 7.],
                 [10.,20.,30.,40.],
                 [ 5., 5., 5., 5.]])   # shape (4, 4)

##----------------------------------##
## Row-wise normalisation (z-score) ##
##----------------------------------##
'''
Subtract each row's mean and divide by its std.
mean/std have shape (4,) => reshape to (4,1) so they broadcast column-wise.
'''

row_mean = data.mean(axis=1)[:, np.newaxis]   # shape (4, 1)
row_std  = data.std(axis=1)[:, np.newaxis]    # shape (4, 1)

z_rows = (data - row_mean) / (row_std + 1e-6)          # (4,4) - (4,1) / (4,1) => (4,4)
print("Row-wise z-score:")
print(z_rows.round(4))
# [[-1.3416 -0.4472  0.4472  1.3416]
#  [-1.3416 -0.4472  0.4472  1.3416]
#  [-1.3416 -0.4472  0.4472  1.3416]
#  [ 0.      0.      0.      0.    ]]

print("Row means after normalisation:", z_rows.mean(axis=1).round(10))
# [0. 0. 0. 0.]

##-------------------------------------##
## Column-wise normalisation (z-score) ##
##-------------------------------------##
'''
Subtract each column's mean (shape (4,) = (1,4)) and divide by column std.
These already broadcast naturally across rows without any reshape.
'''

col_mean = data.mean(axis=0)   # shape (4,)  — treated as (1, 4)
col_std  = data.std(axis=0)    # shape (4,)

z_cols = (data - col_mean) / (col_std + 1e-6)   # (4,4) - (4,) / (4,) => (4,4)
print("Column-wise z-score:")
print(z_cols.round(4))
# [[-0.2132  -0.2132  -0.2132  -0.2132]
#  [-0.5345  -0.5345  -0.5345  -0.5345]
#  [ 1.3736   1.3736   1.3736   1.3736]
#  [-0.6259  -0.6259  -0.6259  -0.6259]]

print("Column means after normalisation:", z_cols.mean(axis=0).round(10))
# [0. 0. 0. 0.]

##------------------------------------##
## Pairwise Euclidean distance matrix ##
##------------------------------------##
'''
Given N points in D dimensions (shape N x D), compute the N x N distance matrix.
Key broadcast trick: expand rows to (N,1,D) and columns to (1,N,D).
Subtraction broadcasts to (N,N,D), then square + sum over D + sqrt.
No Python loops, no explicit copies.
'''

points = np.array([[0., 0.],
                   [3., 0.],
                   [0., 4.],
                   [3., 4.]])   # shape (4, 2)

diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]   # (4,1,2)-(1,4,2) => (4,4,2)
dist_matrix = np.sqrt((diff ** 2).sum(axis=-1))               # (4,4)

print("Pairwise distance matrix:")
print(dist_matrix.round(4))
# [[0. 3. 4. 5.]
#  [3. 0. 5. 4.]
#  [4. 5. 0. 3.]
#  [5. 4. 3. 0.]]

print("Symmetric:", np.allclose(dist_matrix, dist_matrix.T))   # True
print("Zero diagonal:", np.allclose(np.diag(dist_matrix), 0))  # True

##--------------------------------##
## Outer product via broadcasting ##
##--------------------------------##
'''
The outer product of two 1D arrays u (shape M,) and v (shape N,)
is the (M, N) matrix with out[i,j] = u[i] * v[j].
Classic approach: u[:,None] * v[None,:]  =>  (M,1) * (1,N) => (M,N)
'''

u = np.array([1, 2, 3, 4])   # shape (4,)
v = np.array([10, 20, 30])   # shape (3,)

outer = u[:, np.newaxis] * v[np.newaxis, :]   # (4,1) * (1,3) => (4,3)
print("Outer product (broadcast):")
print(outer)
# [[ 10  20  30]
#  [ 20  40  60]
#  [ 30  60  90]
#  [ 40  80 120]]

print(np.array_equal(outer, np.outer(u, v)))   # True

##-----------------------------------------##
## Additive bias in a neural-network layer ##
##-----------------------------------------##
'''
A dense (fully-connected) layer applies: output = input @ W + bias
  input : (batch, in_features)         e.g. (32, 128)
  W     : (in_features, out_features)  e.g. (128, 64)
  bias  : (out_features,)              e.g. (64,)

After matmul: (32, 64). Adding bias of shape (64,):
  (64,) => padded to (1, 64) => broadcast to (32, 64).
Each of the 32 samples gets the same bias added per neuron.
'''

batch      = 32
in_feat    = 128
out_feat   = 64

np.random.seed(0)
X    = np.random.randn(batch, in_feat)                           # (32, 128)
W    = np.random.randn(in_feat, out_feat) * 0.01                 # (128, 64)
bias = np.zeros(out_feat)                                        # (64,)

pre_activation = X @ W + bias   # (32,64) + (64,) => (32,64) via broadcast
print("pre_activation shape:", pre_activation.shape)   # (32, 64)

# Verify: each sample has the same bias added
row0 = X[0] @ W
row1 = X[1] @ W
print("Bias broadcast correct:",
      np.allclose(pre_activation[0], row0 + bias) and
      np.allclose(pre_activation[1], row1 + bias))   # True

# Batch normalisation: subtract per-feature mean across the batch
feat_mean = pre_activation.mean(axis=0)   # shape (64,)  — treated as (1,64)
feat_std  = pre_activation.std(axis=0)    # shape (64,)
normed = (pre_activation - feat_mean) / (feat_std + 1e-8)   # (32,64) broadcast

print("Batch-normed shape:", normed.shape)           # (32, 64)
print("Feature means ≈ 0:", np.allclose(normed.mean(axis=0), 0, atol=1e-6))   # True
print("Feature stds  ≈ 1:", np.allclose(normed.std(axis=0),  1, atol=1e-6))   # True
