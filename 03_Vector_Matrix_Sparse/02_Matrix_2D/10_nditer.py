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

# Simple iteration - flattens and iterates through all values
for value in np.nditer(matrix):
    print(value, end=' ')
# 10 20 30 40 50 60

print("\n")

############################

# For simple cases, you can flatten and loop:
for value in matrix.flat:
    print(value, end=' ')
# 10 20 30 40 50 60

print("\n")

# Or nested loops for maintaining 2D structure:
for row in matrix:
    for value in row:
        print(value, end=' ')
# 10 20 30 40 50 60

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

#------------------------------------ 3. Modify Values --------------------------------------------------#

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

#------------------------------- 5. Real-World Examples ------------------------------------------------- #

#--------------------------------------------------------------------------------------------------------#

# Example 1: Normalize each element by its distance from center
print("\n\nExample 1 - Distance-based normalization:")
data = np.array([[1, 2, 3, 4],
                 [5, 6, 7, 8],
                 [9, 10, 11, 12]], dtype=float)

result = np.zeros_like(data)
center_row, center_col = data.shape[0] / 2, data.shape[1] / 2

with np.nditer(data, flags=['multi_index']) as it:
    for val in it:
        row, col = it.multi_index
        distance = np.sqrt((row - center_row)**2 + (col - center_col)**2)
        result[row, col] = val / (distance + 1)  # +1 to avoid division by zero

print("Original:\n", data)
print("Normalized:\n", result)

############################

# Example 2: Apply boundary-aware smoothing (edge handling)
print("\n\nExample 2 - 2D smoothing with neighbors:")
image = np.array([[10, 20, 30],
                  [40, 50, 60],
                  [70, 80, 90]], dtype=float)

smoothed = np.zeros_like(image)

with np.nditer(image, flags=['multi_index']) as it:
    for val in it:
        row, col = it.multi_index
        neighbors = []
        
        # Collect valid neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                r, c = row + dr, col + dc
                if 0 <= r < image.shape[0] and 0 <= c < image.shape[1]:
                    neighbors.append(image[r, c])
        
        smoothed[row, col] = np.mean(neighbors)

print("Original:\n", image)
print("Smoothed:\n", smoothed)

#--------------------------------------------------------------------------------------------------------#

#-------------------------- 6. Examples with 3D and 4D Matrices ----------------------------------------- #

#--------------------------------------------------------------------------------------------------------#

print("\n\n=== 3D ARRAY EXAMPLES ===")

# Example: 3D array (like RGB image or video frame)
arr_3d = np.arange(24).reshape(2, 3, 4)
print("3D array shape:", arr_3d.shape)
print(arr_3d)

# Iterate with 3D indices
print("\nIterating 3D with multi_index:")
it_3d = np.nditer(arr_3d, flags=['multi_index'])
count = 0
for value in it_3d:
    if count < 5:  # Show first 5 to avoid clutter
        print(f"Position {it_3d.multi_index}: value = {value}")
    count += 1

# Modify 3D array based on position
arr_3d_mod = np.zeros((2, 3, 4))
with np.nditer(arr_3d_mod, flags=['multi_index'], op_flags=['writeonly']) as it:
    for x in it:
        i, j, k = it.multi_index
        x[...] = i * 100 + j * 10 + k  # Encode position

print("\n3D array with encoded positions:\n", arr_3d_mod)

############################

print("\n\n=== 4D ARRAY EXAMPLES ===")

# Example: 4D array (like batch of RGB images or video)
arr_4d = np.ones((2, 2, 3, 3))  # (batch, channel, height, width)
print("4D array shape:", arr_4d.shape)

# Set different values for each batch
with np.nditer(arr_4d, flags=['multi_index'], op_flags=['readwrite']) as it:
    for x in it:
        b, c, h, w = it.multi_index
        x[...] = b * 10 + c  # Different value per batch and channel

print("\n4D array slice [0, :, :, :]:\n", arr_4d[0])
print("\n4D array slice [1, :, :, :]:\n", arr_4d[1])

############################

# Example: Processing 4D with external_loop for performance
print("\n\nProcessing 4D array in chunks:")
arr_4d_large = np.arange(120, dtype=float).reshape(2, 3, 4, 5)

with np.nditer(arr_4d_large, flags=['external_loop', 'buffered'], 
               op_flags=['readwrite'], buffersize=20) as it:
    chunk_count = 0
    for chunk in it:
        chunk[...] = np.sqrt(chunk)  # Apply sqrt to entire chunk
        chunk_count += 1
    print(f"Processed {chunk_count} chunks")

print("First slice after sqrt:\n", arr_4d_large[0, 0])

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
