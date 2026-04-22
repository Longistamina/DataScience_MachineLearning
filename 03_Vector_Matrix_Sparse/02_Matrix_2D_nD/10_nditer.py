'''
np.nditer() - A Simple Guide for 2-D Matrices

1. Basic Loop: Just iterate through values

2. Get Index While Looping: Know the row and column position

3. Modify Values: Change matrix elements

4. Process in Chunks: Faster for large matrices

5. Real-World Examples: Practical 2D operations

6. Examples with 3D and 4D matrices
'''

import numpy as np


#-------------------------------------------------------------------------------------------------------#
#------------------------------------- 1. Basic Loop (READ ONLY) ---------------------------------------#
#-------------------------------------------------------------------------------------------------------#

matrix = np.array([[10, 20, 30],
                   [40, 50, 60]])

# Simple iteration
for value in np.nditer(matrix):
    print(value)
# 10 20 30 40 50 60

############################

print(matrix.flat) 
# <numpy.flatiter object at 0x3065500>
'''
A flatiter object is an iterator that allows you to iterate over a NumPy array 
as if it were a flat (1D) array, regardless of its original shape.
'''

# For simple cases, you can flatten and loop:
for value in matrix.flat:
    print(value)
# 10 20 30 40 50 60

# Or nested loops for maintaining 2D structure:
for row in matrix:
    for value in row:
        print(value, end=' ')
    print()
# 10 20 30 
# 40 50 60


#--------------------------------------------------------------------------------------------------------#
#---------------------------------- 2. Get Index While Looping ------------------------------------------#
#--------------------------------------------------------------------------------------------------------#

# When you need both value AND position (row, col)
matrix2 = np.array([[100, 200],
                    [300, 400],
                    [500, 600]])

it = np.nditer(matrix2, flags=['multi_index'])
for value in it:
    print(f"Position {it.multi_index}: value = {value}")
# Position (0, 0): value = 100
# Position (0, 1): value = 200
# Position (1, 0): value = 300
# Position (1, 1): value = 400
# Position (2, 0): value = 500
# Position (2, 1): value = 600

############################

# Regular nested enumerate is often clearer:
for i, row in enumerate(matrix2):
    for j, value in enumerate(row):
        print(f"Position ({i}, {j}): value = {value}")
# Position (0, 0): value = 100
# Position (0, 1): value = 200
# Position (1, 0): value = 300
# Position (1, 1): value = 400
# Position (2, 0): value = 500
# Position (2, 1): value = 600


#--------------------------------------------------------------------------------------------------------#
#----------------------------------------- 3. Modify Values ---------------------------------------------#
#--------------------------------------------------------------------------------------------------------#

# This is where nditer becomes useful for 2D matrices!
matrix3 = np.array([[1.0, 2.0, 3.0],
                    [4.0, 5.0, 6.0]])

print("Before:\n", matrix3)
# Before:
#  [[1. 2. 3.]
#  [4. 5. 6.]]

# MUST use 'with' statement when modifying
with np.nditer(matrix3, op_flags=['readwrite']) as it:
    for x in it:
        x[...] = x * 2  # Double each value
'''"x[...] = something" is used to modify the value in-place.'''

print("After:\n", matrix3)
# After:
#  [[ 2.  4.  6.]
#  [ 8. 10. 12.]]

############################

# With multi_index-based modification:
matrix4 = np.zeros((3, 4))
with np.nditer(matrix4, flags=['multi_index'], op_flags=['writeonly']) as it:
    for x in it:
        row, col = it.multi_index
        #print(f"it.multi_index ({row}, {col})")
        x[...] = row + col  # Set to sum of indices

print("\nRow + Col index:\n", matrix4)
# Row + Col index:
#  [[0. 1. 2. 3.]
#  [1. 2. 3. 4.]
#  [2. 3. 4. 5.]]

############################

# Conditional modification based on position
matrix5 = np.ones((4, 4))
with np.nditer(matrix5, flags=['multi_index'], op_flags=['readwrite']) as it:
    for x in it:
        row, col = it.multi_index
        if row == col:  # Diagonal elements
            x[...] = 10

print("\nDiagonal matrix:\n", matrix5)
# Diagonal matrix:
#  [[10.  1.  1.  1.]
#  [ 1. 10.  1.  1.]
#  [ 1.  1. 10.  1.]
#  [ 1.  1.  1. 10.]]


#--------------------------------------------------------------------------------------------------------#
#----------------------------- 4. Process in Chunks (For Performance) -----------------------------------#
#--------------------------------------------------------------------------------------------------------#

# For large matrices, processing chunks is faster
matrix6 = np.arange(12, dtype=float).reshape(3, 4)
print("Original matrix:\n", matrix6)

with np.nditer(matrix6, flags=['external_loop'], op_flags=['readwrite']) as it:
    for chunk in it:
        print(f"Processing chunk of size {len(chunk)}")
        chunk[...] = chunk ** 2  # Square all values in chunk at once

print("Result:\n", matrix6)
# Processing chunk of size 4
# Processing chunk of size 4
# Processing chunk of size 4
# Result:
#  [[  0.   1.   4.   9.]
#  [ 16.  25.  36.  49.]
#  [ 64.  81. 100. 121.]]


#--------------------------------------------------------------------------------------------------------#
#-------------------------------------- 5. Real-World Examples ------------------------------------------#
#--------------------------------------------------------------------------------------------------------#

# Example 1: Normalize each element by its distance from center
data = np.array([[1, 2, 3, 4],
                 [5, 6, 7, 8],
                 [9, 10, 11, 12]], dtype=float)

result = np.zeros_like(data)
center_row, center_col = data.shape[0] / 2, data.shape[1] / 2
# center_row = 1.5, center_col = 2.0

with np.nditer(data, flags=['multi_index']) as it:
    for val in it:
        row, col = it.multi_index # Position in matrix, e.g., (0, 0), (0, 1), ...
        distance = np.sqrt((row - center_row)**2 + (col - center_col)**2)
        result[row, col] = val / (distance + 1)  # +1 to avoid division by zero

print("Normalized:\n", result)
# Normalized:
#  [[0.28571429 0.71357834 1.2        1.42715669]
#  [1.63315817 2.83281573 4.66666667 3.77708764]
#  [2.93968471 4.72135955 7.33333333 5.66563146]]

'''
Elements closer to the center position of the matrix are divided by smaller numbers (so they stay larger), 
while elements at the edges are divided by larger numbers (so they become smaller). 
=> This is a spatial/geometric normalization, 
   useful in image processing where you want to emphasize the center of an image or apply radial weighting.
'''


#--------------------------------------------------------------------------------------------------------#
#----------------------------- 6. Examples with 3D and 4D Matrices --------------------------------------#
#--------------------------------------------------------------------------------------------------------#

#######################
## 3D ARRAY EXAMPLES ##
#######################

# Example: 3D array (like RGB image or video frame)
arr_3d = np.arange(24).reshape(2, 3, 4)
print(arr_3d)
# [[[ 0  1  2  3]
#   [ 4  5  6  7]
#   [ 8  9 10 11]]

#  [[12 13 14 15]
#   [16 17 18 19]
#   [20 21 22 23]]]

# Iterate with 3D indices
it_3d = np.nditer(arr_3d, flags=['multi_index'])
count = 0
for value in it_3d:
    if count < 5:  # Show first 5 to avoid clutter
        print(f"Position {it_3d.multi_index}: value = {value}")
    count += 1
# Position (0, 0, 0): value = 0
# Position (0, 0, 1): value = 1
# Position (0, 0, 2): value = 2
# Position (0, 0, 3): value = 3
# Position (0, 1, 0): value = 4

#--------
## Modify 3D array based on position
#--------

arr_3d_mod = np.zeros((2, 3, 4))
with np.nditer(arr_3d_mod, flags=['multi_index'], op_flags=['writeonly']) as it:
    for x in it:
        i, j, k = it.multi_index
        x[...] = i * 100 + j * 10 + k  # Encode position

print("\n3D array with encoded positions:\n", arr_3d_mod)
#  [[[  0.   1.   2.   3.]
#   [ 10.  11.  12.  13.]
#   [ 20.  21.  22.  23.]]

#  [[100. 101. 102. 103.]
#   [110. 111. 112. 113.]
#   [120. 121. 122. 123.]]]

#######################
## 4D ARRAY EXAMPLES ##
#######################

# Example: 4D array (like batch of RGB images or video)
arr_4d = np.ones((2, 2, 3, 3))  # (batch, channel, height, width)

# Set different values for each batch
with np.nditer(arr_4d, flags=['multi_index'], op_flags=['readwrite']) as it:
    for x in it:
        b, c, h, w = it.multi_index
        x[...] = b * 10 + c  # Different value per batch and channel

print("\n4D array slice [0, :, :, :]:\n", arr_4d[0])
#  [[[0. 0. 0.]
#   [0. 0. 0.]
#   [0. 0. 0.]]

#  [[1. 1. 1.]
#   [1. 1. 1.]
#   [1. 1. 1.]]]

print("\n4D array slice [1, :, :, :]:\n", arr_4d[1])
#  [[[10. 10. 10.]
#   [10. 10. 10.]
#   [10. 10. 10.]]

#  [[11. 11. 11.]
#   [11. 11. 11.]
#   [11. 11. 11.]]]

#--------
## Example: Processing 4D with external_loop for performance
#--------

arr_4d_large = np.arange(120, dtype=float).reshape(2, 3, 4, 5) # A very large 4D array

# Process in chunks
with np.nditer(arr_4d_large, flags=['external_loop', 'buffered'], 
               op_flags=['readwrite'], buffersize=20) as it:
    chunk_count = 0
    for chunk in it:
        chunk[...] = np.sqrt(chunk)  # Apply sqrt to entire chunk
        chunk_count += 1
    print(f"Processed {chunk_count} chunks")

print("First slice after sqrt:\n", arr_4d_large[0, 0])
#  [[0.         1.         1.41421356 1.73205081 2.        ]
#  [2.23606798 2.44948974 2.64575131 2.82842712 3.        ]
#  [3.16227766 3.31662479 3.46410162 3.60555128 3.74165739]
#  [3.87298335 4.         4.12310563 4.24264069 4.35889894]]


#--------------------------------------------------------------------------------------------------------#
#--------------------------------- When to Actually Use nditer ------------------------------------------#
#--------------------------------------------------------------------------------------------------------#

'''
HONEST TRUTH FOR 2D MATRICES:

✓ USE nditer when:
  - You need to modify matrix while iterating with row/col indices
  - Working with non-contiguous or strided memory layouts
  - Processing multiple matrices together with broadcasting
  - Building custom operations that need fine-grained control
  - Working with 3D/4D arrays where nested loops get messy

✗ DON'T USE nditer for:
  - Simple loops → Just use: for row in matrix: for val in row
  - Element-wise math → Use: matrix * 2, matrix + 5, etc.
  - Getting indices → Use: for i, row in enumerate(matrix)
  - Most common tasks → NumPy has built-in functions!

SIMPLE ALTERNATIVES:
  matrix * 2                  instead of nditer with x[...] = x * 2
  np.sqrt(matrix)             instead of nditer with x[...] = sqrt(x)
  matrix[matrix > 0]          instead of nditer with conditions
  enumerate(matrix)           instead of nditer with multi_index
  np.apply_along_axis()       for row/column operations
  matrix.T                    for transposition
  np.mean(matrix, axis=0/1)   for row/column means

For 2D operations, vectorized NumPy functions are almost always faster!
Use nditer only when you truly need custom element-by-element logic
that can't be expressed with broadcasting or existing NumPy functions.
'''
