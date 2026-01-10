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
   
6. Concatenate: np.concatenate((arr1, arr2, ...)): 
   + concatenate many vectors into one vector
'''

import numpy as np

# Create sample 1D vectors
a1 = np.array([1, 2, 3])
a2 = np.array([4, 5, 6])


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


#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------- 2. Vertical & Row Stack --------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
np.vstack() stacks arrays on top of each other.
np.row_stack() is an alias for vstack ().

- 1D arrays (size N) become a matrix (2 x N).
'''

print(np.vstack((a1, a2)))
# [[1 2 3]
#  [4 5 6]]

print(np.row_stack((a1, a2)))
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
'''

print(np.hstack((a1, a2)))
# [1 2 3 4 5 6]


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
'''

print(np.dstack((a1, a2)))
# [[[1 4]
#   [2 5]
#   [3 6]]]
# Result shape: (1, 3, 2)


#---------------------------------------------------------------------------------------------------------#
#------------------------------------------ 6. Concatenate -----------------------------------------------#
#---------------------------------------------------------------------------------------------------------#

vector_1 = np.array([1, 5, 3])
vector_2 = np.array([4, 2, 6])
vector_3 = np.array([7, 9, 8])

###################
## Concatenating ##
###################

print(np.concatenate((vector_1, vector_2, vector_3), axis=0))
# [1 5 3 4 2 6 7 9 8]
# axis=0 by default (joins all elements into one long vector)

print(np.concatenate((vector_1, vector_2, vector_3))) # can omit axis
# [1 5 3 4 2 6 7 9 8]

print(np.concatenate((vector_1, vector_2, vector_3), axis=1))
'''numpy.exceptions.AxisError: axis 1 is out of bounds for array of dimension 1'''
# Error: 1D arrays only have axis 0
