'''
1. arr.transpose() or arr.T: Transpose the array
   + np.transpose(arr) or np.T(arr): similar to arr.transpose() or arr.T

2. swapaxes:
   + np.swapaxes(arr, axis1, axis2): swap two axes of an array
   + arr.swapaxes(axis1, axis2): similar to np.swapaxes(arr, axis1, axis2)

3. permute_dims:
   + np.permute_dims(arr, axes): permute (reorder) all axes according to axes
                                 Works conceptually like torch.permute (available in newer NumPy / array API)
   + arr.transpose(axes): do the same thing
'''

import numpy as np

np.random.seed(42)
arr = np.random.rand(2, 3, 4, 5)

print(arr.shape)
# (2, 3, 4, 5)

# =========================================================================================
# 1. arr.transpose() or arr.T: Transpose the array
# =========================================================================================
'''
For high-dimensional array, tranpose will reverse the dimension orders:
    (d1, d2, ..., dn) -> (dn, ..., d2, d1)

To transpose the 2 last dimension only, should use swapaxes
    arr.swapaxes(-1, -2)
'''

##-----------------##
## arr.transpose() ##
##-----------------##

print(
    arr.transpose()
    .shape
)
# (5, 4, 3, 2)

##-------##
## arr.T ##
##-------##

print(
    arr.T
    .shape
)
# (5, 4, 3, 2)

##-------------------##
## np.transpose(arr) ##
##-------------------##

print(
    np.transpose(arr)
    .shape
)
# (5, 4, 3, 2)

# =========================================================================================
# 2. np.swapaxes(): swap two axes
# =========================================================================================
'''
arr.swapaxes(axis1, axis2)
np.swapaxes(arr, axis1, axis2):

For 2D (m, n):
   + np.swapaxes(arr, 0, 1) is equivalent to transpose: shape becomes (n, m)

For higher dimensions:
   + only the two specified axes are swapped, others stay in place

Can use swapaxes to transpose the 2 last dimensions.
    arr.swapaxes(-1, -2)
'''

##--------------##
## arr.swapaxes ##
##--------------##

print(
    arr.swapaxes(1, 3)
    .shape
)
# (2, 5, 4, 3)

##---------------##
## np.swapaxes() ##
##---------------##

print(
    np.swapaxes(arr, 0, 3)
    .shape
)
# (5, 3, 4, 2)

##----------------------##
## arr.swapaxes(-1, -2) ##
##----------------------##

print(
    arr.swapaxes(-1, -2)
    .shape
)
# (2, 3, 5, 4)

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

##-------------------##
## np.permute_dims() ##
##-------------------##

print(
    np.permute_dims(arr, (3, 0, 2, 1))
    .shape
)
# (5, 2, 4, 3)

##---------------------##
## arr.transpose(axes) ##
##---------------------##

print(
    arr.transpose(3, 0, 2, 1)
    .shape
)
# (5, 2, 4, 3)
