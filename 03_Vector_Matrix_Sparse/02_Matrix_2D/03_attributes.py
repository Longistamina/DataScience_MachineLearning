"""
Matrix (2D array) attributes in NumPy.

Core attributes (same idea as the vector example):
- arr.ndim: number of dimensions (axes) of the array.
- arr.shape: tuple representing the size of the array along each dimension.
- arr.size: total number of elements in the array.
- arr.dtype: data type of the elements in the array.
- arr.itemsize: size (in bytes) of each element in the array.
- arr.nbytes: total number of bytes consumed by the array's elements.

Extra attributes that are especially informative for 2D matrices:
- arr.T: transpose view of the array (swap axes).
- arr.strides: step (in bytes) to move along each axis (important for memory layout).
- arr.flags: memory layout / mutability info (C_CONTIGUOUS, F_CONTIGUOUS, WRITEABLE, etc.).
- arr.base: reference to the original array if this is a view (e.g., transpose).
"""

import numpy as np

np.random.seed(0)
matrix = np.random.uniform(1, 11, size=(3, 4)).astype(np.float16)

print(matrix)
# [[ 6.49   8.15   7.027  6.45 ]
#  [ 5.24   7.457  5.375  9.914]
#  [10.63   4.836  8.914  6.29 ]]

##############
## arr.ndim ##
##############

print(matrix.ndim)
# 2
# (2 dimensions, i.e., a 2D matrix)

###############
## arr.shape ##
###############

print(matrix.shape)
# (3, 4)
# (3 rows, 4 columns)

# Row/column counts are just shape components
n_rows, n_cols = matrix.shape
print(n_rows, n_cols)
# 3 4

print(matrix.shape[0])  # n_rows
# 3

print(matrix.shape[1])  # n_cols
# 4

##############
## arr.size ##
##############

print(matrix.size)
# 12
# (Total number of elements = 3 * 4 = 12)

###############
## arr.dtype ##
###############

print(matrix.dtype)
# float16
# (Data type of the elements in the array)

##################
## arr.itemsize ##
##################

print(matrix.itemsize)
# 2
# (Each float16 element takes 2 bytes)

################
## arr.nbytes ##
################

print(matrix.nbytes)
# 24
# (Total bytes = 12 elements * 2 bytes/element = 24 bytes)

#######################
## Transpose (arr.T) ##
#######################

print(matrix.T)
# [[ 6.49   5.24  10.63 ]
#  [ 8.15   7.457  4.836]
#  [ 7.027  5.375  8.914]
#  [ 6.45   9.914  6.29 ]]

print(matrix.T.shape)
# (4, 3)

##################
## arr.strides  ##
##################

print(matrix.strides)
# (8, 2)
'''
Meaning:
- To move to the next row (first axis), move 8 bytes (4 columns * 2 bytes/element).
- To move to the next column (second axis), move 2 bytes (1 element * 2 bytes/element).
'''

print(matrix.T.strides)
# (2, 8)

###############
## arr.flags ##
###############

print(matrix.flags)
# Shows memory layout and other properties (C_CONTIGUOUS, F_CONTIGUOUS, WRITEABLE, etc.)
'''
  C_CONTIGUOUS : True
  F_CONTIGUOUS : False
  OWNDATA : True
  WRITEABLE : True
  ALIGNED : True
  WRITEBACKIFCOPY : False
'''

################################
## Views vs copies (arr.base) ##
################################

print(matrix.base)
# None  (typically None because this is an owning array)

print(matrix.T.base is matrix)
# True  (transpose is typically a view backed by the same data buffer)
