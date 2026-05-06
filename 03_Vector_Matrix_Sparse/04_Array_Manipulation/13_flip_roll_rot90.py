"""
1. np.flip(): Reverses the order of elements along a given axis.
2. np.fliplr(): Flips an array (2D or more) left-to-right (along axis 1).
3. np.flipud(): Flips an array (2D or more) up-to-down (along axis 0).
4. np.roll(): Shifts elements along a specified axis by a given number of steps.
5. np.rot90(): Rotates an array by 90 degrees in the plane specified by axes.

NOTE:
    + np.flip(arr, axis=None) -> If axis is None, reverses all axes.
    + np.roll(arr, shift, axis) -> Elements that roll off the end are re-introduced at the beginning.
    + np.rot90(arr, k=1, axes=(0, 1)) -> k is the number of times the array is rotated by 90 degrees.
"""

import numpy as np

vector = np.array([1, 2, 3, 4, 5])

matrix = np.arange(12).reshape(3, 4)
print("Original Matrix:")
print(matrix)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

tensor = np.arange(24).reshape(2, 3, 4)
print("\nOriginal Tensor Shape:", tensor.shape)
# (2, 3, 4)


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 1. np.flip() --------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
np.flip() reverses the order of elements.
If no axis is specified, it reverses all dimensions.
'''

# Flip 1D vector
print("Flip Vector:", np.flip(vector))
# [5, 4, 3, 2, 1]

# Flip 2D matrix (All axes)
print("Flip Matrix (All axes):\n", np.flip(matrix))
# [[11, 10,  9,  8],
#  [ 7,  6,  5,  4],
#  [ 3,  2,  1,  0]]

# Flip 2D matrix (Along axis 0 - Vertical flip)
print("Flip Matrix (Axis 0):\n", np.flip(matrix, axis=0))
# [[ 8,  9, 10, 11],
#  [ 4,  5,  6,  7],
#  [ 0,  1,  2,  3]]

# Flip 2D matrix (Along axis 1 - Horizontal flip)
print("Flip Matrix (Axis 1):\n", np.flip(matrix, axis=1))
# [[ 3,  2,  1,  0],
#  [ 7,  6,  5,  4],
#  [11, 10,  9,  8]]


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 2. np.fliplr() ------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
np.fliplr() stands for "Flip Left-Right".
It is a convenience function for np.flip(arr, axis=1).
Works on 2D arrays or higher.
'''

print("Flip Matrix Left-to-Right:\n", np.fliplr(matrix))
# [[ 3,  2,  1,  0],
#  [ 7,  6,  5,  4],
#  [11, 10,  9,  8]]


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 3. np.flipud() -----------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
np.flipud() stands for "Flip Up-Down".
It is a convenience function for np.flip(arr, axis=0).
Works on 2D arrays or higher.
'''

print("Flip Matrix Up-to-Down:\n", np.flipud(matrix))
# [[ 8,  9, 10, 11],
#  [ 4,  5,  6,  7],
#  [ 0,  1,  2,  3]]


#-----------------------------------------------------------------------------------------------------------#
#--------------------------------------------------- 4. np.roll() ------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
np.roll() shifts elements.
The elements that "fall off" one end are wrapped around to the other end.
'''

# Roll 1D vector by 2 positions
print("Roll Vector (shift=2):", np.roll(vector, 2))
# [4, 5, 1, 2, 3]

# Roll 2D matrix along axis 0 (Vertical shift)
print("Roll Matrix (axis 0, shift=1):\n", np.roll(matrix, shift=1, axis=0))
# [[ 8,  9, 10, 11],
#  [ 0,  1,  2,  3],
#  [ 4,  5,  6,  7]]

# Roll 2D matrix along axis 1 (Horizontal shift)
print("Roll Matrix (axis 1, shift=1):\n", np.roll(matrix, shift=1, axis=1))
# [[ 3,  0,  1,  2],
#  [ 7,  4,  5,  6],
#  [11,  8,  9, 10]]

# Roll 2D matrix with multiple shifts (tuple)
# Shift axis 0 by 1 and axis 1 by 1
print("Roll Matrix (axis 0 by 1, axis 1 by 1):\n", np.roll(matrix, shift=(1, 1)))
# [[11,  8,  9, 10],
#  [ 7,  4,  5,  6],
#  [ 3,  0,  1,  2]]


#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------------- 5. np.rot90() ------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
np.rot90() rotates an array by 90 degrees.
k: number of times to rotate (default 1).
axes: the plane of rotation (default (0, 1)).
'''

# Rotate 90 degrees (k=1)
print("Rotate Matrix 90 deg (k=1):\n", np.rot90(matrix, k=1))
# [[ 3,  7, 11],
#  [ 2,  6, 10],
#  [ 1,  5,  9],
#  [ 0,  4,  8]]

# Rotate 180 degrees (k=2)
print("Rotate Matrix 180 deg (k=2):\n", np.rot90(matrix, k=2))
# [[11, 10,  9,  8],
#  [ 7,  6,  5,  4],
#  [ 3,  2,  1,  0]]

# Rotate 270 degrees (k=3)
print("Rotate Matrix 270 deg (k=3):\n", np.rot90(matrix, k=3))
 # [[ 8  4  0]
 # [ 9  5  1]
 # [10  6  2]
 # [11  7  3]]
