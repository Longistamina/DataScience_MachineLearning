'''
1. arr.transpose() or arr.T: Transpose the array (swap rows and columns)
   + np.transpose(arr) or np.T(arr): similar to arr.transpose() or arr.T

2. swapaxes:
   + np.swapaxes(arr, axis1, axis2): swap two axes of an array; for 2D, swapping 0 and 1 is equivalent to transpose
   + arr.swapaxes(axis1, axis2): similar to np.swapaxes(arr, axis1, axis2)

3. permute_dims:
   + np.permute_dims(arr, axes): permute (reorder) all axes according to axes
                                 Works conceptually like torch.permute (available in newer NumPy / array API)
   + arr.transpose(axes): do the same thing
'''

import numpy as np

# =========================================================================================
# 1. arr.transpose() or arr.T: Transpose the array
# =========================================================================================

np.random.seed(4)
matrix1 = np.random.randint(1, 21, size=(3, 4))

print(matrix1)
# [[15  6  2  9]
#  [ 9 19 10  8]
#  [14  9  5 19]]
# shape: (3, 4)

##-----------------##
## arr.transpose() ##
##-----------------##

print(matrix1.transpose())
# [[15  9 14]
#  [ 6 19  9]
#  [ 2 10  5]
#  [ 9  8 19]]
# shape: (4, 3)

##-------##
## arr.T ##
##-------##

print(matrix1.T)
# [[15  9 14]
#  [ 6 19  9]
#  [ 2 10  5]
#  [ 9  8 19]]
# shape: (4, 3)

##-------------------##
## np.transpose(arr) ##
##-------------------##

print(np.transpose(matrix1))
# [[15  9 14]
#  [ 6 19  9]
#  [ 2 10  5]
#  [ 9  8 19]]
# same result as arr.T or arr.transpose()

# =========================================================================================
# 2. np.swapaxes(): swap two axes
# =========================================================================================
'''
np.swapaxes(arr, axis1, axis2):

For 2D (m, n):
   + np.swapaxes(arr, 0, 1) is equivalent to transpose: shape becomes (n, m)

For higher dimensions:
   + only the two specified axes are swapped, others stay in place
'''

np.random.seed(6)
matrix2 = np.random.randint(1, 21, size=(3, 4))

print(matrix2)
# [[11 10  4 11]
#  [14 16 11 17]
#  [ 2 12 14 16]]

print(matrix2.shape)   # (3, 4)

##----##
## 2D ##
##----##

swapped_2d = np.swapaxes(matrix2, 0, 1)
print(swapped_2d)
# [[11 14  2]
#  [10 16 12]
#  [ 4 11 14]
#  [11 17 16]]

print(swapped_2d.shape)  # (4, 3), same as transpose

##----##
## 3D ##
##----##

np.random.seed(0)
tensor3d = np.random.randint(1, 10, size=(2, 3, 4))

print(tensor3d)
# [[[6 7 4 6]
#   [2 3 4 7]
#   [9 1 4 8]]

#  [[5 9 2 3]
#   [5 2 6 6]
#   [7 2 1 6]]]

print(tensor3d.shape)
# (2, 3, 4)

# =========================================================================================

swapped_3d = np.swapaxes(tensor3d, 0, 2)

print(swapped_3d)
# [[[6 5]
#   [2 5]
#   [9 7]]

#  [[7 9]
#   [3 2]
#   [1 2]]

#  [[4 2]
#   [4 6]
#   [4 1]]

#  [[6 3]
#   [7 6]
#   [8 6]]]

print(swapped_3d.shape)
# (4, 3, 2)

##----------------------##
## using arr.swapaxes() ##
##----------------------##

swapped_3d_method = tensor3d.swapaxes(1, 2)
print(swapped_3d_method)
# [[[6 8 5]
#   [1 4 8]
#   [4 6 7]
#   [4 3 9]]

#  [[9 8 9]
#   [2 9 5]
#   [7 2 4]
#   [8 6 1]]]

print(swapped_3d_method.shape)
# (2, 4, 3)
'''from (2, 3, 4) to (2, 4, 3), only axes 1 and 2 are swapped.'''

# =========================================================================================
# 3. np.permute_dims(): permute axes
# =========================================================================================
'''
np.permute_dims(arr, axes):
(arr.transpose(axes))

   + Permute (reorder) all axes according to axes
   + For a 3D tensor with shape (d0, d1, d2):

        np.permute_dims(arr, (1, 0, 2)) -> shape (d1, d0, d2)
        np.permute_dims(arr, (2, 0, 1)) -> shape (d2, d0, d1)

   + In newer NumPy / array API, permute_dims is available; if not, np.transpose(arr, axes) does the same thing.
'''

'''NOTE: when use np.permute_dims(), must specify ALL axes in the new order.'''

np.random.seed(7)
tensor3d_2 = np.random.randint(1, 10, size=(2, 3, 4))

print(tensor3d_2)
# [[[5 7 4 4]
#   [8 8 8 9]
#   [9 8 7 5]]

#  [[1 8 1 8]
#   [7 4 6 9]
#   [9 8 6 1]]]

print(tensor3d_2.shape)
# (2, 3, 4)

##-----------------------##
## (1, 0, 2) permutation ##
##-----------------------##

perm_1 = np.permute_dims(tensor3d_2, (1, 0, 2))

print(perm_1)
# [[[5 7 4 4]
#   [1 8 1 8]]

#  [[8 8 8 9]
#   [7 4 6 9]]

#  [[9 8 7 5]
#   [9 8 6 1]]]

print(perm_1.shape)
# (3, 2, 4)

##-----------------------##
## (2, 0, 1) permutation ##
##-----------------------##

perm_2 = np.permute_dims(tensor3d_2, (2, 0, 1))

print(perm_2)
# [[[5 8 9]
#   [1 7 9]]

#  [[7 8 8]
#   [8 4 8]]

#  [[4 8 7]
#   [1 6 6]]

#  [[4 9 5]
#   [8 9 1]]]

print(perm_2.shape)
# (4, 2, 3)

##---------------------##
## arr.transpose(axes) ##
##---------------------##

print(
    tensor3d_2.transpose(1, 0, 2)
    .shape
)
# (3, 2, 4)
