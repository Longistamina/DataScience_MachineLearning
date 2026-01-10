'''
1. Stack: np.stack(arrays, axis=0)
   + Concatenates a sequence of arrays along a NEW dimension.

2. Vertical Stack: np.vstack(arrays) / np.row_stack(arrays)
   + Stacks arrays vertically (row-wise).

3. Horizontal Stack: np.hstack(arrays)
   + Stacks arrays horizontally (column-wise).

4. Column Stack: np.column_stack(arrays)
   + Specifically stacks 1D arrays as columns in a 2D result.

5. Depth Stack: np.dstack(arrays)
   + Stacks arrays along the third dimension (depth).

6. Concatenate: np.concatenate(arrays, axis=0)
   + Joins a sequence of arrays along an EXISTING dimension.
   + All arrays must have the same shape except in the dimension being concatenated.
'''

import numpy as np

# Create sample 1D vectors
a1 = np.array([1, 2, 3])
a2 = np.array([4, 5, 6])

# Create sample 2D matrices
m1 = np.array([[1, 1, 1],
               [1, 1, 1]])

m2 = np.array([[2, 2, 2],
               [2, 2, 2]])


#-----------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 1. Stack ----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
np.stack() joins arrays along a NEW dimension.
All arrays must be the same size.
'''

print(np.stack((a1, a2), axis=0))
# [[1 2 3]
#  [4 5 6]]
# Result shape: (2, 3)

print(np.stack((a1, a2), axis=1))
# [[1 4]
#  [2 5]
#  [3 6]]
# Result shape: (3, 2)

###############

print(np.stack((m1, m2), axis=0))
# [[[1 1 1]
#   [1 1 1]]

#  [[2 2 2]
#   [2 2 2]]]
# Shape: (2, 2, 3)

print(np.stack((m1, m2), axis=1))
# [[[1 1 1]
#   [2 2 2]]

#  [[1 1 1]
#   [2 2 2]]]
# Shape: (2, 2, 3)


#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------- 2. Vertical & Row Stack --------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
np.vstack() stacks arrays on top of each other.
np.row_stack() is an alias for vstack ().

- 1D arrays (size N) become a matrix (2 x N).
- 2D arrays (M x N) become a larger matrix ((M+M) x N).
'''

print(np.vstack((a1, a2)))
# [[1 2 3]
#  [4 5 6]]

print(np.row_stack((m1, m2)))
# [[1 1 1]
#  [1 1 1]
#  [2 2 2]
#  [2 2 2]]
# Shape: (4, 3)
'''<stdin>:1: DeprecationWarning: `row_stack` alias is deprecated. Use `np.vstack` directly.'''


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------- 3. Horizontal Stack -------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
np.hstack() stacks arrays side-by-side.
- 1D arrays (size N) are concatenated into a longer 1D array (size 2N).
- 2D arrays (M x N) become a wider matrix (M x (N+N)).
'''

print(np.hstack((a1, a2)))
# [1 2 3 4 5 6]

print(np.hstack((m1, m2)))
# [[1 1 1 2 2 2]
#  [1 1 1 2 2 2]]
# Shape: (2, 6)


#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------- 4. Column Stack ----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
np.column_stack() is similar to hstack, but it behaves differently for 1D arrays.
It ensures 1D arrays are treated as COLUMNS (vertical) of a 2D matrix.
'''

print(np.column_stack((a1, a2)))
# [[1 4]
#  [2 5]
#  [3 6]]
# Result shape: (3, 2) (Compare this to hstack which stayed 1D)


#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------- 5. Depth Stack ---------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
np.dstack() stacks arrays along the third dimension (depth).
- 1D arrays (N) become (1 x N x 2).
- 2D arrays (M x N) become (M x N x 2).
'''

print(np.dstack((a1, a2)))
# [[[1 4]
#   [2 5]
#   [3 6]]]
# Result shape: (1, 3, 2)

print(np.dstack((m1, m2)))
# [[[1 2]
#   [1 2]
#   [1 2]]

#  [[1 2]
#   [1 2]
#   [1 2]]]
# Shape: (2, 3, 2)


#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------- 6. Concatenate: np.concatenate() -----------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
np.concatenate(arrays, axis=0)
- Joins a sequence of arrays along an EXISTING dimension.
- All arrays must have the same shape except in the dimension being concatenated.
'''

# 1D Concatenation
print(np.concatenate((a1, a2), axis=0))
# [1 2 3 4 5 6] -> Stays 1D (Size 6)


# 2D Concatenation (m1, m2 are 2x3)
# Vertically (axis=0)
print(np.concatenate((m1, m2), axis=0))
# [[1 1 1]
#  [1 1 1]
#  [2 2 2]
#  [2 2 2]] -> Shape (4, 3)

# Horizontally (axis=1)
print(np.concatenate((m1, m2), axis=1))
# [[1 1 1 2 2 2]
#  [1 1 1 2 2 2]] -> Shape (2, 6)
