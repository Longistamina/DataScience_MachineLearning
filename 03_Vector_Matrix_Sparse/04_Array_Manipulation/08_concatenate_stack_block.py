'''
1. np.concatenate(arrays, axis=0)
   + Joins a sequence of arrays along an EXISTING axis.

2. np.concat(arrays, axis=0)
   + Alias for np.concatenate introduced in NumPy 2.0 (Array API compatible).

3. np.stack(arrays, axis=0)
   + Joins a sequence of arrays along a NEW axis.

4. np.vstack(arrays)
   + Stacks arrays vertically (row-wise). Alias: np.row_stack() [deprecated].

5. np.hstack(arrays)
   + Stacks arrays horizontally (column-wise).

6. np.dstack(arrays)
   + Stacks arrays depth-wise (along the third axis).

7. np.column_stack(arrays)
   + Stacks 1D arrays as columns into a 2D array.

8. np.block(arrays)
   + Assembles an nd-array from nested lists of blocks (like MATLAB bracket stacking).
'''

import numpy as np

# ── Sample arrays ──────────────────────────────────────────────────────────────

a1 = np.array([1, 2, 3])           # 1D, shape (3,)
a2 = np.array([4, 5, 6])           # 1D, shape (3,)

m1 = np.array([[1, 1, 1],          # 2D, shape (2, 3)
               [1, 1, 1]])

m2 = np.array([[2, 2, 2],          # 2D, shape (2, 3)
               [2, 2, 2]])

t1 = np.array([[[1, 2],            # 3D, shape (2, 2, 2)
                [3, 4]],
               [[5, 6],
                [7, 8]]])

t2 = np.array([[[9, 10],           # 3D, shape (2, 2, 2)
                [11, 12]],
               [[13, 14],
                [15, 16]]])


#-----------------------------------------------------------------------------------------------------------#
#----------------------------------------- 1. np.concatenate() ---------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
np.concatenate(arrays, axis=0)
- Joins a sequence of arrays along an EXISTING axis (not generate new dimension)
- All arrays must have the same shape except along the concatenation axis.
- axis=None flattens all arrays before joining.
'''

# 1D: both arrays are merged into one longer 1D array
print(np.concatenate((a1, a2)))
# [1 2 3 4 5 6]
# Shape: (6,)

print(np.concatenate((a1, a2), axis=0))   # axis=0 is the default for 1D
# [1 2 3 4 5 6]

# 2D axis=0: stack rows → taller matrix
print(np.concatenate((m1, m2), axis=0))
# [[1 1 1]
#  [1 1 1]
#  [2 2 2]
#  [2 2 2]]
# Shape: (4, 3)

# 2D axis=1: stack columns → wider matrix
print(np.concatenate((m1, m2), axis=1))
# [[1 1 1 2 2 2]
#  [1 1 1 2 2 2]]
# Shape: (2, 6)

# axis=None: flattens all arrays, then concatenates into one 1D array
print(np.concatenate((m1, m2), axis=None))
# [1 1 1 1 1 1 2 2 2 2 2 2]
# Shape: (12,)

# 3D axis=0: stack along depth (new "batch" of matrices)
print(np.concatenate((t1, t2), axis=0))
# Shape: (4, 2, 2)

# 3D axis=1: stack along rows within each depth slice
print(np.concatenate((t1, t2), axis=1))
# Shape: (2, 4, 2)

# 3D axis=2: stack along columns within each row
print(np.concatenate((t1, t2), axis=2))
# Shape: (2, 2, 4)


#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 2. np.concat() -----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
np.concat(arrays, axis=0)
- Introduced in NumPy 2.0 as part of the Array API standard.
- Functionally identical to np.concatenate().
- Prefer np.concat() in new code for Array API compatibility.
'''

# 1D
print(np.concat((a1, a2)))
# [1 2 3 4 5 6]

# 2D axis=0
print(np.concat((m1, m2), axis=0))
# [[1 1 1]
#  [1 1 1]
#  [2 2 2]
#  [2 2 2]]
# Shape: (4, 3)

# 2D axis=1
print(np.concat((m1, m2), axis=1))
# [[1 1 1 2 2 2]
#  [1 1 1 2 2 2]]
# Shape: (2, 6)

# axis=None: flatten then concatenate
print(np.concat((m1, m2), axis=None))
# [1 1 1 1 1 1 2 2 2 2 2 2]


#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 3. np.stack() ----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
np.stack(arrays, axis=0)
- Joins arrays along a NEW axis (increases dimensionality by 1).
- All input arrays must have exactly the same shape.
- axis controls where the new dimension is inserted.
'''

# 1D → 2D
print(np.stack((a1, a2), axis=0))
# [[1 2 3]
#  [4 5 6]]
# Shape: (2, 3)  ← new axis inserted at position 0 (rows)

print(np.stack((a1, a2), axis=1))
# [[1 4]
#  [2 5]
#  [3 6]]
# Shape: (3, 2)  ← new axis inserted at position 1 (columns)

# 2D → 3D
print(np.stack((m1, m2), axis=0))
# [[[1 1 1]
#   [1 1 1]]
#  [[2 2 2]
#   [2 2 2]]]
# Shape: (2, 2, 3)  ← new axis at front

print(np.stack((m1, m2), axis=1))
# [[[1 1 1]
#   [2 2 2]]
#  [[1 1 1]
#   [2 2 2]]]
# Shape: (2, 2, 3)  ← new axis interleaves rows

print(np.stack((m1, m2), axis=2))
# [[[1 2]
#   [1 2]
#   [1 2]]
#  [[1 2]
#   [1 2]
#   [1 2]]]
# Shape: (2, 3, 2)  ← new axis at the end (depth)


#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 4. np.vstack() ---------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
np.vstack(arrays)
- Stacks arrays vertically (row-wise), i.e. along axis=0.
- 1D arrays (N,) are treated as (1, N) rows before stacking → result is (k, N).
- 2D arrays (M, N) are stacked on top of each other → result is (k*M, N).
- Equivalent to np.concatenate(arrays, axis=0) after promoting 1D→2D.
- np.row_stack() is a deprecated alias → use np.vstack() directly.
'''

# 1D → each becomes a row
print(np.vstack((a1, a2)))
# [[1 2 3]
#  [4 5 6]]
# Shape: (2, 3)

# 2D → stacked on top of each other
print(np.vstack((m1, m2)))
# [[1 1 1]
#  [1 1 1]
#  [2 2 2]
#  [2 2 2]]
# Shape: (4, 3)

# Mix of 1D and 2D (1D is promoted to 1-row 2D)
print(np.vstack((a1, m1)))
# [[1 2 3]
#  [1 1 1]
#  [1 1 1]]
# Shape: (3, 3)

# row_stack is deprecated:
# np.row_stack((a1, a2))
# DeprecationWarning: `row_stack` alias is deprecated. Use `np.vstack` directly.


#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 5. np.hstack() ---------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
np.hstack(arrays)
- Stacks arrays horizontally (column-wise), i.e. along axis=1 for 2D+.
- Exception: 1D arrays are joined along axis=0 (concatenated end-to-end).
- 2D arrays (M, N) become a wider matrix (M, k*N).
'''

# 1D → concatenated end-to-end (stays 1D)
print(np.hstack((a1, a2)))
# [1 2 3 4 5 6]
# Shape: (6,)

# 2D → columns appended side-by-side
print(np.hstack((m1, m2)))
# [[1 1 1 2 2 2]
#  [1 1 1 2 2 2]]
# Shape: (2, 6)

# 3D → joined along axis=1 (second axis)
print(np.hstack((t1, t2)))
# Shape: (2, 4, 2)


#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 6. np.dstack() ---------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
np.dstack(arrays)
- Stacks arrays depth-wise (along the third axis, axis=2).
- 1D arrays (N,)   are reshaped to (1, N, 1) before stacking → result is (1, N, k).
- 2D arrays (M, N) are reshaped to (M, N, 1) before stacking → result is (M, N, k).
- 3D arrays (M, N, P) are stacked along their existing third axis → result is (M, N, k*P).
'''

# 1D → reshaped to (1, N, 1) then stacked
print(np.dstack((a1, a2)))
# [[[1 4]
#   [2 5]
#   [3 6]]]
# Shape: (1, 3, 2)

# 2D → reshaped to (M, N, 1) then stacked
print(np.dstack((m1, m2)))
# [[[1 2]
#   [1 2]
#   [1 2]]
#  [[1 2]
#   [1 2]
#   [1 2]]]
# Shape: (2, 3, 2)

# 3D → stacked along existing third axis
print(np.dstack((t1, t2)))
# Shape: (2, 2, 4)


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------- 7. np.column_stack() ------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
np.column_stack(arrays)
- Stacks 1D arrays as COLUMNS into a 2D matrix (treats each 1D array as a column vector).
- For 2D arrays: behaves identically to hstack (joins along axis=1).
- Key difference from hstack: 1D arrays become columns (N, 1) instead of staying 1D.
'''

# 1D → each array becomes a column (compare to hstack which stays 1D)
print(np.column_stack((a1, a2)))
# [[1 4]
#  [2 5]
#  [3 6]]
# Shape: (3, 2)   ← cf. hstack: [1 2 3 4 5 6], shape (6,)

# 2D → same as hstack for 2D arrays
print(np.column_stack((m1, m2)))
# [[1 1 1 2 2 2]
#  [1 1 1 2 2 2]]
# Shape: (2, 6)

# Mix: 2D array (2, 3) + 1D array (2,) → 1D is treated as a single column (2, 1)
# The 1D array length must match the number of rows in the 2D array.
col = np.array([9, 8])          # shape (2,) → matches m1's 2 rows
print(np.column_stack((m1, col)))
# [[1 1 1 9]
#  [1 1 1 8]]
# Shape: (2, 4)


#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 8. np.block() ----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
np.block(arrays)
- Assembles an nd-array from a NESTED LIST of blocks (like MATLAB [A, B; C, D]).
- Inner list  → concatenate along the LAST  axis  (horizontally for 2D)
- Outer list  → concatenate along the SECOND-LAST axis (vertically for 2D)
- Useful for constructing block matrices from components.
- Depth-1 list behaves like hstack; depth-2 list behaves like vstack/hstack combo.
'''

# Depth-1 list → behaves like hstack (horizontal join)
print(np.block([a1, a2]))
# [1 2 3 4 5 6]

print(np.block([m1, m2]))
# [[1 1 1 2 2 2]
#  [1 1 1 2 2 2]]
# Shape: (2, 6)

# Depth-2 list → behaves like vstack (vertical join)
print(np.block([[a1], [a2]]))
# [[1 2 3]
#  [4 5 6]]
# Shape: (2, 3)

print(np.block([[m1], [m2]]))
# [[1 1 1]
#  [1 1 1]
#  [2 2 2]
#  [2 2 2]]
# Shape: (4, 3)

# Classic block matrix construction (2×2 block layout):
A = np.eye(2) * 1          # 2×2 identity
B = np.ones((2, 3)) * 2    # 2×3 block of 2s
C = np.ones((3, 2)) * 3    # 3×2 block of 3s
D = np.eye(3) * 4          # 3×3 identity scaled

print(np.block([
    [A, B],
    [C, D]
]))
# [[1. 0. 2. 2. 2.]
#  [0. 1. 2. 2. 2.]
#  [3. 3. 4. 0. 0.]
#  [3. 3. 0. 4. 0.]
#  [3. 3. 0. 0. 4.]]
# Shape: (5, 5)

# Scalars are treated as 0D arrays and promoted automatically
print(np.block([[1, 2], [3, 4]]))
# [[1 2]
#  [3 4]]
