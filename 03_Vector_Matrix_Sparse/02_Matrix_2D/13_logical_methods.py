'''
1. arr.all(axis=...) ||| np.all(arr, axis=...): Check if all elements along the specified axis are True (non-zero).

2. arr.any(axis=...) ||| np.any(arr, axis=...): Check if any element along the specified axis is True (non-zero).

3. arr.nonzero() ||| np.nonzero(arr): Return the indices of the elements that are non-zero (True).

4. Examples for 3D and 4D matrices.
'''

import numpy as np

np.random.seed(42)

matrix_True = np.array([[True, True, True], 
                        [True, True, True]])

matrix_False = np.array([[False, False, False], 
                         [False, False, False]])

matrix_mixed = np.array([[True, False, True], 
                         [False, True, False]])

matrix_ones = np.ones((2, 3))  # array([[1., 1., 1.], [1., 1., 1.]])

matrix_zeros = np.zeros((2, 3))  # array([[0., 0., 0.], [0., 0., 0.]])

matrix_mixed_num = np.array([[0, 1, 2], 
                             [3, 0, 4]])


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------ 1. arr.all() ||| np.all(arr) --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
arr.all() and np.all(): check if all elements (or along a specific axis) are True (or non-zero).

(True if all are True/non-zero, False otherwise)

Can use them to verify if a boolean mask (array) is entirely True, 
or if all numerical values in an array are non-zero.

With axis parameter:
- axis=None (default): check all elements in the entire matrix
- axis=0: check along rows (returns result for each column)
- axis=1: check along columns (returns result for each row)
'''

######################
## arr.all() method ##
######################

#-----
## arr.all(): all elements are True (or non-zero)
#-----

print(matrix_True.all())
# True
# Returns True since all elements are True

print(matrix_False.all())
# False
# Returns False since not all elements are True

print(matrix_mixed.all())
# False
# Returns False since not all elements are True

print(matrix_ones.all())
# True
# Returns True since all elements are non-zero

print(matrix_zeros.all())
# False
# Returns False since not all elements are non-zero

print(matrix_mixed_num.all())
# False
# Returns False since not all elements are non-zero

#-----
## arr.all(axis=0): check along rows (result for each column)
#-----

print(matrix_mixed_num)
# [[0 1 2]
#  [3 0 4]]

print(matrix_mixed_num.all(axis=0))
# [False False  True]
'''
Column 0: [0, 3] -> False (not all are non-zero)
Column 1: [1, 0] -> False (not all are non-zero)
Column 2: [2, 4] -> True (all are non-zero)
'''

#-----
## arr.all(axis=1): check along columns (result for each row)
#-----

print(matrix_mixed_num.all(axis=1))
# [False False]
'''
Row 0: [0, 1, 2] -> False (not all are non-zero)
Row 1: [3, 0, 4] -> False (not all are non-zero)
'''

#-----
## Logical array (mask) checking
#-----

print(matrix_mixed_num > -1)
# [[ True  True  True]
#  [ True  True  True]]

print((matrix_mixed_num > -1).all())
# True
# Returns True since all elements are greater than -1 (all are True)

print((matrix_mixed_num == 2))
# [[False False  True]
#  [False False False]]

print((matrix_mixed_num == 2).all())
# False
# Returns False since not all elements are equal to 2 (not all are True)

print((matrix_mixed_num > 0).all(axis=0))
# [False False  True]
# Column-wise check: only column 2 has all elements > 0

print((matrix_mixed_num > 0).all(axis=1))
# [False False]
# Row-wise check: neither row has all elements > 0

#######################
## np.all() function ##
#######################

#-----
## np.all(): all elements are True (or non-zero)
#-----

print(np.all(matrix_True))  # True

print(np.all(matrix_False))  # False

print(np.all(matrix_mixed))  # False

print(np.all(matrix_ones))  # True

print(np.all(matrix_zeros))  # False

print(np.all(matrix_mixed_num))  # False

#-----
## np.all() with axis parameter
#-----

print(np.all(matrix_mixed_num, axis=0))  # [False False  True]

print(np.all(matrix_mixed_num, axis=1))  # [False False]

#-----
## Logical array (mask) checking
#-----

print(np.all(matrix_mixed_num > -1))  # True

print(np.all(matrix_mixed_num == 2))  # False

print(np.all(matrix_mixed_num > 0, axis=0))  # [False False  True]

print(np.all(matrix_mixed_num > 0, axis=1))  # [False False]


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------ 2. arr.any() ||| np.any(arr) --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
arr.any() and np.any(): check if any element (or along a specific axis) is True (or non-zero).

(False if all are False/zero, True otherwise)

Can use them to verify if a boolean mask (array) has at least one True, 
or if any numerical value in an array is non-zero.

With axis parameter:
- axis=None (default): check all elements in the entire matrix
- axis=0: check along rows (returns result for each column)
- axis=1: check along columns (returns result for each row)
'''

######################
## arr.any() method ##
######################

#-----
## arr.any(): any element is True (or non-zero)
#-----

print(matrix_True.any())
# True
# Returns True since at least one element is True

print(matrix_False.any())
# False
# Returns False since no elements are True

print(matrix_mixed.any())
# True
# Returns True since at least one element is True

print(matrix_ones.any())
# True
# Returns True since at least one element is non-zero

print(matrix_zeros.any())
# False
# Returns False since no elements are non-zero

print(matrix_mixed_num.any())
# True
# Returns True since at least one element is non-zero

#-----
## arr.any(axis=0): check along rows (result for each column)
#-----

print(matrix_mixed_num)
# [[0 1 2]
#  [3 0 4]]

print(matrix_mixed_num.any(axis=0))
# [ True  True  True]
'''
Column 0: [0, 3] -> True (at least one is non-zero)
Column 1: [1, 0] -> True (at least one is non-zero)
Column 2: [2, 4] -> True (at least one is non-zero)
'''

#-----
## arr.any(axis=1): check along columns (result for each row)
#-----

print(matrix_mixed_num.any(axis=1))
# [ True  True]
'''
Row 0: [0, 1, 2] -> True (at least one is non-zero)
Row 1: [3, 0, 4] -> True (at least one is non-zero)
'''

#-----
## Logical array (mask) checking
#-----

print(matrix_mixed_num > 1)
# [[False False  True]
#  [ True False  True]]

print((matrix_mixed_num > 1).any())
# True
# Returns True since at least one element is greater than 1 (at least one is True)

print((matrix_mixed_num < -1))
# [[False False False]
#  [False False False]]

print((matrix_mixed_num < -1).any())
# False
# Returns False since no elements are less than -1 (none are True)

print((matrix_mixed_num > 2).any(axis=0))
# [False False  True]
# Column-wise check: only column 2 has at least one element > 2

print((matrix_mixed_num > 2).any(axis=1))
# [False  True]
# Row-wise check: only row 1 has at least one element > 2

#######################
## np.any() function ##
#######################

#-----
## np.any(): any element is True (or non-zero)
#-----

print(np.any(matrix_True))  # True

print(np.any(matrix_False))  # False

print(np.any(matrix_mixed))  # True

print(np.any(matrix_ones))  # True

print(np.any(matrix_zeros))  # False

print(np.any(matrix_mixed_num))  # True

#-----
## np.any() with axis parameter
#-----

print(np.any(matrix_mixed_num, axis=0))  # [ True  True  True]

print(np.any(matrix_mixed_num, axis=1))  # [ True  True]

#-----
## Logical array (mask) checking
#-----

print(np.any(matrix_mixed_num > 1))  # True

print(np.any(matrix_mixed_num < -1))  # False

print(np.any(matrix_mixed_num > 2, axis=0))  # [False False  True]

print(np.any(matrix_mixed_num > 2, axis=1))  # [False  True]


#--------------------------------------------------------------------------------------------------------------#
#------------------------------ 3. arr.nonzero() ||| np.nonzero(arr) ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
arr.nonzero() and np.nonzero(): return the indices of the elements that are non-zero (or True).

For 2D arrays, returns a tuple of two arrays:
- First array: row indices
- Second array: column indices

Can be used to filter elements based on a boolean mask or find positions of non-zero elements.
'''

matrix_mixed = np.array([[True, False, True], 
                         [False, True, False]])

matrix_mixed_num = np.array([[0, 1, 2], 
                             [3, 0, 4]])

##########################
## arr.nonzero() method ##
##########################

#-----
## arr.nonzero(): indices of non-zero (or True) elements
#-----

print(matrix_mixed.nonzero())
# (array([0, 0, 1]), array([0, 2, 1]))
'''
Returns (row_indices, column_indices)
Element [0, 0] is True
Element [0, 2] is True
Element [1, 1] is True
'''

print(matrix_mixed_num.nonzero())
# (array([0, 0, 1, 1]), array([1, 2, 0, 2]))
'''
Returns (row_indices, column_indices)
Element [0, 1] = 1 (non-zero)
Element [0, 2] = 2 (non-zero)
Element [1, 0] = 3 (non-zero)
Element [1, 2] = 4 (non-zero)
'''

#-----
## Extracting non-zero elements
#-----

row_idx, col_idx = matrix_mixed_num.nonzero()

print(row_idx)  # [0 0 1 1]

print(col_idx)  # [1 2 0 2]

print(matrix_mixed_num[row_idx, col_idx])
# [1 2 3 4]
# These are the non-zero elements

#-----
## Logical array (mask) checking
#-----

print(matrix_mixed_num % 2 == 0)
# [[ True False  True]
#  [False  True  True]]

print((matrix_mixed_num % 2 == 0).nonzero())
# (array([0, 0, 1, 1]), array([0, 2, 1, 2]))
'''
Returns indices of elements that are EVEN (True in the mask):
Element [0, 0] = 0 (even)
Element [0, 2] = 2 (even)
Element [1, 1] = 0 (even)
Element [1, 2] = 4 (even)
'''

###########################
## np.nonzero() function ##
###########################

#-----
## np.nonzero(): indices of non-zero (or True) elements
#-----

print(np.nonzero(matrix_mixed))
# (array([0, 0, 1]), array([0, 2, 1]))

print(np.nonzero(matrix_mixed_num))
# (array([0, 0, 1, 1]), array([1, 2, 0, 2]))

#-----
## Logical array (mask) checking
#-----

print(matrix_mixed_num > 0)
# [[False  True  True]
#  [ True False  True]]

print(np.nonzero(matrix_mixed_num > 0))
# (array([0, 0, 1, 1]), array([1, 2, 0, 2]))
'''
Returns indices of elements greater than 0 (True in the mask):
Element [0, 1] = 1
Element [0, 2] = 2
Element [1, 0] = 3
Element [1, 2] = 4
'''


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 4. Examples for 3D and 4D matrices ------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

#######################
## 3D Matrix Example ##
#######################

np.random.seed(100)
matrix_3d = np.random.randint(0, 3, size=(2, 3, 4))

print(matrix_3d)
# [[[0 0 0 2]
#   [2 0 2 1]
#   [2 2 2 2]]

#  [[1 0 0 0]
#   [0 2 0 1]
#   [1 2 2 0]]]

#----------
## all() and any() with axis parameter
#----------

print(matrix_3d.all())  # False (not all elements are non-zero)

print(matrix_3d.all(axis=0))  # Check if all elements along depth are non-zero
# [[False False False False]
#  [False False False  True]
#  [ True  True  True False]]

print(matrix_3d.all(axis=1))  # Check if all elements along rows are non-zero
# [[False False False  True]
#  [False False False False]]

print(matrix_3d.all(axis=2))  # Check if all elements along columns are non-zero
# [[False False  True]
#  [False False False]]

print(matrix_3d.any())  # True (at least one element is non-zero)

print(matrix_3d.any(axis=0))  # Check if any element along depth is non-zero
# [[ True False False  True]
#  [ True  True  True  True]
#  [ True  True  True  True]]

#-----------
## nonzero() for 3D arrays
#-----------

print(matrix_3d.nonzero())
# (array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]), array([0, 1, 1, 1, 2, 2, 2, 2, 0, 1, 1, 2, 2, 2]), array([3, 0, 2, 3, 0, 1, 2, 3, 0, 1, 3, 0, 1, 2]))
# Returns tuple of 3 arrays: (depth_indices, row_indices, column_indices)

depth_idx, row_idx, col_idx = matrix_3d.nonzero()

print(f"Depth indices: {depth_idx[:5]}")   #  First 5 depth indices
# [0 0 0 0 0]

print(f"Row indices: {row_idx[:5]}")       # First 5 row indices
# [0 1 1 1 2]

print(f"Column indices: {col_idx[:5]}")    # First 5 column indices
# [3 0 2 3 0]

print(f"Non-zero values: {matrix_3d[depth_idx[:5], row_idx[:5], col_idx[:5]]}")
# First 5 non-zero values: [2 2 2 1 2]

#######################
## 4D Matrix Example ##
#######################

np.random.seed(200)
matrix_4d = np.random.randint(0, 2, size=(2, 2, 3, 3))

print(matrix_4d)
# [[[[0 1 0]
#    [0 0 1]
#    [0 1 1]]

#   [[0 1 1]
#    [1 1 0]
#    [0 0 1]]]


#  [[[1 1 1]
#    [1 1 1]
#    [0 1 1]]

#   [[0 1 0]
#    [0 1 0]
#    [1 0 0]]]]

#----------
## all() and any() with axis parameter
#----------

print(matrix_4d.all())  # False (not all elements are non-zero)

print(matrix_4d.all(axis=0))  # Check along batches
# [[[False  True False]
#   [False False  True]
#   [False  True  True]]

#  [[False  True False]
#   [False  True False]
#   [False False False]]]

print(matrix_4d.any())  # True (at least one element is non-zero)

print(matrix_4d.any(axis=(2, 3)))  # Check if any element exists in each (3, 3) matrix
# [[ True  True]
#  [ True  True]]
'''All 4 matrices have at least one non-zero element'''

print(matrix_4d.all(axis=(2, 3)))  # Check if all elements are non-zero in each (3, 3) matrix
# [[False False]
#  [False False]]
'''None of the 4 matrices have all non-zero elements'''

#-----------
## nonzero() for 4D arrays
#-----------

print(matrix_4d.nonzero())
# (array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]), array([0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]), array([0, 1, 2, 2, 0, 0, 1, 1, 2, 0, 0, 0, 1, 1, 1, 2, 2, 0, 1, 2]), array([1, 2, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 1, 1, 0]))
# Returns tuple of 4 arrays: (batch_indices, depth_indices, row_indices, column_indices)

batch_idx, depth_idx, row_idx, col_idx = matrix_4d.nonzero()

print(f"Total non-zero elements: {len(batch_idx)}") # 20

print(f"First non-zero at position: [{batch_idx[0]}, {depth_idx[0]}, {row_idx[0]}, {col_idx[0]}]")
# First non-zero at position: [0, 0, 0, 1]

print(f"Value: {matrix_4d[batch_idx[0], depth_idx[0], row_idx[0], col_idx[0]]}")
# Value: 1

'''
Key insights for higher-dimensional arrays:
- axis parameter becomes increasingly important for controlling which dimension to check
- nonzero() returns a tuple with one array per dimension
- Can combine multiple axes: axis=(0, 1) or axis=(2, 3)
- all() and any() can reduce the dimensionality of the result
'''
