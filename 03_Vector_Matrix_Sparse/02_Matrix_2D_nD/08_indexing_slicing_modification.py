'''
1. Basic Indexing: matrix[row, col]

2. Fancy Indexing matrix[list_of_rows, list_of_cols]

3. Slicing: matrix[row_start:row_stop:row_step, col_start:col_stop:col_step]

4. Advance Indexing (using methods):
   + arr.item(row, col)
   + arr.take(indices, axis)
   + np.take_along_axis(arr, indices, axis)

5. Modifying Elements:
   + matrix[row, col] = new_value
   + arr.put(flat_indices, list_of_new_values)

6. Examples for 3D and 4D matrices

7. Elipsis for skipping elements: arr[..., indices]: useful for higher-dimensional arrays
'''

import numpy as np

# Create a sample 2D matrix for demonstration
matrix = np.array([[10, 11, 12, 13, 14, 15],
                   [20, 21, 22, 23, 24, 25],
                   [30, 31, 32, 33, 34, 35],
                   [40, 41, 42, 43, 44, 45],
                   [50, 51, 52, 53, 54, 55],
                   [60, 61, 62, 63, 64, 65],
                   [70, 71, 72, 73, 74, 75],
                   [80, 81, 82, 83, 84, 85]])

print(matrix)
# [[10 11 12 13 14 15]
#  [20 21 22 23 24 25]
#  [30 31 32 33 34 35]
#  [40 41 42 43 44 45]
#  [50 51 52 53 54 55]
#  [60 61 62 63 64 65]
#  [70 71 72 73 74 75]
#  [80 81 82 83 84 85]]

print(matrix.shape)
# (8, 6)
# (8 rows, 6 columns)


#--------------------------------------------------------------------------------------------------------#
#---------------------------------- 1. Basic indexing: matrix[row, col] ---------------------------------#
#--------------------------------------------------------------------------------------------------------#

print(matrix[0, 0])
# 10
# (Element at row 0, column 0)

print(matrix[2, 3])
# 33
# (Element at row 2, column 3)

print(matrix[7, 5])
# 85
# (Element at row 7, column 5) (last row, last column)

print(matrix[-1, -1])
# 85
# (Last row, last column)
'''equivalent to matrix[7, 5] =  matrix[rows-1, cols-1]'''

print(matrix[-2, -3])
# 73
# (2nd row from the end, 3rd column from the end)
'''equivalent to matrix[6, 3] = matrix[rows-2, cols-3]'''

print(matrix[1])
# [20 21 22 23 24 25]
# (Entire row at index 1, i.e the 2nd row)

print(matrix[:, 2])
# [12 22 32 42 52 62 72 82]
# (Entire column at index 2, i.e the 3rd column)


#--------------------------------------------------------------------------------------------------------#
#-------------------------- 2. Fancy indexing: matrix[list_of_rows, list_of_cols] -----------------------#
#--------------------------------------------------------------------------------------------------------#

row_indices = [0, 2, 4]
col_indices = [1, 3, 5]

print(matrix[row_indices, col_indices])
# [11 33 55]
# (Elements at (0,1), (2,3), and (4,5))

print(matrix[[1, 3], [2, 4]])
# [22 44]
# (Elements at (1,2) and (3,4))

print(matrix[[0, 1, 2], :])
# [[10 11 12 13 14 15]
#  [20 21 22 23 24 25]
#  [30 31 32 33 34 35]]
# (Rows 0, 1, and 2 with all columns)

print(matrix[:, [0, 2, 4]])
# [[10 12 14]
#  [20 22 24]
#  [30 32 34]
#  [40 42 44]
#  [50 52 54]
#  [60 62 64]
#  [70 72 74]
#  [80 82 84]]
# (All rows with columns 0, 2, and 4)


#--------------------------------------------------------------------------------------------------------#
#--------------- 3. Slicing: matrix[row_start:row_stop:row_step, col_start:col_stop:col_step] -----------#
#--------------------------------------------------------------------------------------------------------#

print(matrix[0:3, 1:4])
# [[11 12 13]
#  [21 22 23]
#  [31 32 33]]
# (Rows 0-2, columns 1-3)

print(matrix[:2, :3])
# [[10 11 12]
#  [20 21 22]]
# (First 2 rows, first 3 columns)

print(matrix[4:, 3:])
# [[53 54 55]
#  [63 64 65]
#  [73 74 75]
#  [83 84 85]]
# (Rows from index 4 to end, columns from index 3 to end)

print(matrix[::2, ::2])
# [[10 12 14]
#  [30 32 34]
#  [50 52 54]
#  [70 72 74]]
# (Every 2nd row, every 2nd column)

print(matrix[1:6:2, 0:5:2])
# [[20 22 24]
#  [40 42 44]
#  [60 62 64]]
# (Rows 1, 3, 5 and columns 0, 2, 4)

print(matrix[-3:, -4:])
# [[62 63 64 65]
#  [72 73 74 75]
#  [82 83 84 85]]
# (Last 3 rows, last 4 columns)

print(matrix[::-1, :])
'''Returns the matrix with rows reversed'''
# [[80 81 82 83 84 85]
#  [70 71 72 73 74 75]
#  [60 61 62 63 64 65]
#  [50 51 52 53 54 55]
#  [40 41 42 43 44 45]
#  [30 31 32 33 34 35]
#  [20 21 22 23 24 25]
#  [10 11 12 13 14 15]]

print(matrix[:, ::-1])
'''Returns the matrix with columns reversed'''
# [[15 14 13 12 11 10]
#  [25 24 23 22 21 20]
#  [35 34 33 32 31 30]
#  [45 44 43 42 41 40]
#  [55 54 53 52 51 50]
#  [65 64 63 62 61 60]
#  [75 74 73 72 71 70]
#  [85 84 83 82 81 80]]

print(matrix[::-1, ::-1])
'''Returns the matrix with both rows and columns reversed'''
# [[85 84 83 82 81 80]
#  [75 74 73 72 71 70]
#  [65 64 63 62 61 60]
#  [55 54 53 52 51 50]
#  [45 44 43 42 41 40]
#  [35 34 33 32 31 30]
#  [25 24 23 22 21 20]
#  [15 14 13 12 11 10]]


#--------------------------------------------------------------------------------------------------------#
#-------------------------------- 4. Advanced indexing (using methods) ----------------------------------#
#--------------------------------------------------------------------------------------------------------#

########################
## arr.item(row, col) ##
########################

print(matrix.item(0, 0))
# 10

print(matrix.item(3, 4))
# 44

print(matrix.item(-1, -2))
# 84

print(matrix.item(10))
# 22
# (Flat index 10 - treats matrix as 1D array)

#############################
## arr.take(indices, axis) ##
#############################

print(matrix.take([0, 2, 4], axis=0))
# [[10 11 12 13 14 15]
#  [30 31 32 33 34 35]
#  [50 51 52 53 54 55]]
# (Take rows 0, 2, and 4)

print(matrix.take([1, 3, 5], axis=1))
# [[11 13 15]
#  [21 23 25]
#  [31 33 35]
#  [41 43 45]
#  [51 53 55]
#  [61 63 65]
#  [71 73 75]
#  [81 83 85]]
# (Take columns 1, 3, and 5)

print(matrix.take(np.arange(0, 12, 3)))
# [10 13 22 25 34 37 46 49 62 65 74 77]
# (Take elements at flat indices 0, 3, 6, 9 using np.arange())

print(matrix.take(np.arange(matrix.shape[0] - 1, -1, -1), axis=0))
# [[80 81 82 83 84 85]
#  [70 71 72 73 74 75]
#  [60 61 62 63 64 65]
#  [50 51 52 53 54 55]
#  [40 41 42 43 44 45]
#  [30 31 32 33 34 35]
#  [20 21 22 23 24 25]
#  [10 11 12 13 14 15]]
# (Take all rows in reverse order using np.arange())

################################
## Using np.take_along_axis() ##
################################

'''
np.take_along_axis() takes values from an array by matching indices along a specified axis.
Unlike np.take(), this function works with 2D index arrays and can select different indices 
for each row or column.

Syntax: np.take_along_axis(arr, indices, axis)
- arr: input array
- indices: array of indices (must have same shape as arr, or broadcastable)
- axis: axis along which to take values
'''

# Create index arrays for demonstration
row_indices = np.array([[0, 2, 4],    # For row 0, take columns 0, 2, 4
                        [1, 3, 5],    # For row 1, take columns 1, 3, 5
                        [5, 4, 3],    # For row 2, take columns 5, 4, 3
                        [2, 1, 0]])   # For row 3, take columns 2, 1, 0

print(row_indices.shape)
# (4, 3)

#-----
## Taking along axis=1 (columns)
#-----

result_axis1 = np.take_along_axis(matrix[:4], row_indices, axis=1)
print(result_axis1)
# [[10 12 14]
#  [21 23 25]
#  [35 34 33]
#  [42 41 40]]

print(f"Original matrix[0]: {matrix[0]}")
print(f"Indices for row 0: {row_indices[0]}")
print(f"Result for row 0: {result_axis1[0]}")
# Original matrix[0]: [10 11 12 13 14 15]
# Indices for row 0: [0 2 4]
# Result for row 0: [10 12 14]

#-----
## Taking along axis=0 (rows)
#-----

col_indices = np.array([[0, 1, 2, 3, 4, 5],    # For col 0, take row 0
                        [7, 6, 5, 4, 3, 2],    # For col 1, take row 7
                        [2, 2, 2, 2, 2, 2]])   # For col 2, take row 2

print(col_indices.shape)
# (3, 6)

result_axis0 = np.take_along_axis(matrix, col_indices, axis=0)
print(result_axis0)
# [[10 21 32 43 54 65]
#  [80 71 62 53 44 35]
#  [30 31 32 33 34 35]]

print(f"Column 0 values: {matrix[:, 0]}")
print(f"Indices for col 0: {col_indices[:, 0]}")
print(f"Result for col 0: {result_axis0[:, 0]}")
# Column 0 values: [10 20 30 40 50 60 70 80]
# Indices for col 0: [0 7 2]
# Result for col 0: [10 80 30]

#-----
## Using with custom index patterns
#-----

# Create indices to select specific elements from each row
# For rows that have values > 40, select columns 0, 1, 2
# For rows that don't, select column 0 three times
sample_indices = np.array([[0, 0, 0],     # Row 0: values <= 40, repeat column 0
                           [0, 0, 0],     # Row 1: values <= 40, repeat column 0
                           [0, 0, 0],     # Row 2: values <= 40, repeat column 0
                           [0, 1, 2],     # Row 3: select columns 0, 1, 2
                           [0, 1, 2]])    # Row 4: select columns 0, 1, 2

result_sample = np.take_along_axis(matrix[3:, :], sample_indices, axis=1)
print(result_sample)
# [[40 40 40]
#  [50 50 50]
#  [60 60 60]
#  [70 71 72]
#  [80 81 82]]

# This shows how each row uses its corresponding index array
print(f"Row 3 (matrix[3]): {matrix[3]}")
print(f"Indices [0, 0, 0]: {matrix[3][[0, 0, 0]]}")
# Row 3 (matrix[3]): [40 41 42 43 44 45]
# Indices [0, 0, 0]: [40 40 40]

print(f"Row 7 (matrix[7]): {matrix[7]}")
print(f"Indices [0, 1, 2]: {matrix[7][[0, 1, 2]]}")
# Row 7 (matrix[7]): [80 81 82 83 84 85]
# Indices [0, 1, 2]: [80 81 82]

#-----
## Practical example: combine with argsort to get sorted elements
#-----

matrix_scores = np.array([
    [85, 92, 78, 95, 88],
    [76, 88, 91, 84, 79],
    [93, 81, 87, 90, 85],
    [88, 79, 94, 77, 92]
])

# Get the indices that would sort each row (horizontally)
sorted_indices = np.argsort(matrix_scores, axis=1)
print(np.take_along_axis(matrix_scores, sorted_indices, axis=1))
# [[78 85 88 92 95]
#  [76 79 84 88 91]
#  [81 85 87 90 93]
#  [77 79 88 92 94]]

# Get the indices of argmax each column (vertically)
argmax_indices = np.argmax(matrix_scores, axis=0)
print(np.take_along_axis(matrix_scores, argmax_indices[np.newaxis, :], axis=0))
# [[93 92 94 95 92]]
'''np.newaxis is used to convert 1D array argmax_indices to 2D for proper broadcasting'''

#---------------------------------------------------------------------------------------------------------#
#-------------------------- 5. Modifying elements: matrix[row, col] = new_value --------------------------#
#---------------------------------------------------------------------------------------------------------#

##################################
## matrix[row, col] = new_value ##
##################################

matrix_demo = matrix.copy() # Create a copy to avoid modifying the original matrix

matrix_demo[0, 0] = 999
print(f"Modified: {matrix_demo[0, 0]}\nOriginal: {matrix[0, 0]}")
# Modified: 999
# Original: 10

matrix_demo[2, 1:4] = [111, 222, 333]
print(f"Modified slice: {matrix_demo[2, 1:4]}\nOriginal slice: {matrix[2, 1:4]}")
# Modified slice: [111 222 333]
# Original slice: [31 32 33]

matrix_demo[1:3, 2] = 0
print(f"Modified column slice: {matrix_demo[1:3, 2]}\nOriginal column slice: {matrix[1:3, 2]}")
# Modified column slice: [0 0]
# Original column slice: [22 32]

matrix_demo[[0, 2, 4], [1, 3, 5]] = [500, 501, 502]
print(f"Modified indices: {matrix_demo[[0, 2, 4], [1, 3, 5]]}\nOriginal indices: {matrix[[0, 2, 4], [1, 3, 5]]}")
# Modified indices: [500 501 502]
# Original indices: [11 33 55]

matrix_demo[-2:, -2:] = 88
print(f"Modified last 2x2 block:\n{matrix_demo[-2:, -2:]}\nOriginal last 2x2 block:\n{matrix[-2:, -2:]}")
# Modified last 2x2 block:
# [[88 88]
#  [88 88]]
# Original last 2x2 block:
# [[74 75]
#  [84 85]]

###############################################
## arr.put(flat_indices, list_of_new_values) ##
###############################################

matrix_demo = matrix.copy() # Create a copy to avoid modifying the original matrix

matrix_demo.put([0, 7, 14], [111, 222, 333])

print(f"Modified flat indices: {matrix_demo.flat[[0, 7, 14]]}\nOriginal flat indices: {matrix.flat[[0, 7, 14]]}")
# Modified flat indices: [111 222 333]
# Original flat indices: [10 21 32]

matrix_demo.put(np.arange(6, 12), 0)
print(f"Modified slice (flat): {matrix_demo.flat[6:12]}\nOriginal slice (flat): {matrix.flat[6:12]}")
# Modified slice (flat): [0 0 0 0 0 0]
# Original slice (flat): [20 21 22 23 24 25]


#---------------------------------------------------------------------------------------------------------#
#----------------------------- 6. Examples for 3D and 4D matrices ----------------------------------------#
#---------------------------------------------------------------------------------------------------------#

########################
## 3D Matrix (Tensor) ##
########################

# Create a 3D array with shape (3, 4, 5) - 3 layers, 4 rows, 5 columns
tensor_3d = np.arange(60).reshape(3, 4, 5)

print(tensor_3d)
# [[[ 0  1  2  3  4]
#   [ 5  6  7  8  9]
#   [10 11 12 13 14]
#   [15 16 17 18 19]]
#
#  [[20 21 22 23 24]
#   [25 26 27 28 29]
#   [30 31 32 33 34]
#   [35 36 37 38 39]]
#
#  [[40 41 42 43 44]
#   [45 46 47 48 49]
#   [50 51 52 53 54]
#   [55 56 57 58 59]]]

print(f"Shape: {tensor_3d.shape}")
# Shape: (3, 4, 5)

#------
## Basic indexing: tensor_3d[layer, row, col]
#------

print(tensor_3d[0, 1, 2])
# 7
# (Layer 0, row 1, column 2)

print(tensor_3d[1, 2, 3])
# 33
# (Layer 1, row 2, column 3)

print(tensor_3d[-1, -1, -1])
# 59
# (Last layer, last row, last column)

# Slicing along different axes
print(tensor_3d[0, :, :])
# [[ 0  1  2  3  4]
#  [ 5  6  7  8  9]
#  [10 11 12 13 14]
#  [15 16 17 18 19]]
# (First layer - entire 2D slice)

print(tensor_3d[:, 1, :])
# [[ 5  6  7  8  9]
#  [25 26 27 28 29]
#  [45 46 47 48 49]]
# (All layers, row 1, all columns)

print(tensor_3d[:, :, 2])
# [[ 2  7 12 17]
#  [22 27 32 37]
#  [42 47 52 57]]
# (All layers, all rows, column 2)
'''The columns become rows in the output'''

print(tensor_3d[0:2, 1:3, 2:5])
# [[[ 7  8  9]
#   [12 13 14]]
#
#  [[27 28 29]
#   [32 33 34]]]
# (Layers 0-1, rows 1-2, columns 2-4)

print(tensor_3d[::2, ::2, ::2])
# [[[ 0  2  4]
#   [10 12 14]]
#
#  [[40 42 44]
#   [50 52 54]]]
# (Every 2nd layer, every 2nd row, every 2nd column)

# Using take() on specific axis
print(tensor_3d.take([0, 2], axis=0))
# [[[ 0  1  2  3  4]
#   [ 5  6  7  8  9]
#   [10 11 12 13 14]
#   [15 16 17 18 19]]
#
#  [[40 41 42 43 44]
#   [45 46 47 48 49]
#   [50 51 52 53 54]
#   [55 56 57 58 59]]]
# (Take layers 0 and 2)

#------
## Modifying 3D tensor
#------

tensor_3d_demo = tensor_3d.copy()
tensor_3d_demo[1, 2, 3] = 999

print(f"Modified: {tensor_3d_demo[1, 2, 3]}\nOriginal: {tensor_3d[1, 2, 3]}")
# Modified: 999
# Original: 33

tensor_3d_demo[0, :, 2] = 0
print(f"Modified column: {tensor_3d_demo[0, :, 2]}\nOriginal column: {tensor_3d[0, :, 2]}")
# Modified column: [0 0 0 0]
# Original column: [ 2  7 12 17]

########################
## 4D Matrix (Tensor) ##
########################

# Create a 4D array with shape (2, 3, 4, 5) - 2 batches, 3 channels, 4 rows, 5 columns
tensor_4d = np.arange(120).reshape(2, 3, 4, 5)

print(f"Shape: {tensor_4d.shape}")
# Shape: (2, 3, 4, 5)

#------
## Basic indexing: tensor_4d[batch, channel, row, col]
#------

print(tensor_4d[0, 0, 0, 0])
# 0
# (Batch 0, channel 0, row 0, column 0)

print(tensor_4d[1, 2, 3, 4])
# 119
# (Batch 1, channel 2, row 3, column 4)

print(tensor_4d[-1, -1, -1, -1])
# 119
# (Last batch, last channel, last row, last column)

# Slicing 4D tensor
print(tensor_4d[0, 0, :, :])
# [[ 0  1  2  3  4]
#  [ 5  6  7  8  9]
#  [10 11 12 13 14]
#  [15 16 17 18 19]]
# (Batch 0, channel 0, all rows and columns - a 2D slice)

print(tensor_4d[:, 1, 2, 3])
# [28 88]
# (All batches, channel 1, row 2, column 3)

print(tensor_4d[0, :, 1, :])
# [[ 5  6  7  8  9]
#  [25 26 27 28 29]
#  [45 46 47 48 49]]
# (Batch 0, all channels, row 1, all columns)

print(tensor_4d[::1, ::2, ::2, ::2])
# [[[[ 0  2  4]
#    [10 12 14]]
#
#   [[40 42 44]
#    [50 52 54]]]
#
#
#  [[[60 62 64]
#    [70 72 74]]
#
#   [[100 102 104]
#    [110 112 114]]]]
# (All batches, every 2nd channel, every 2nd row, every 2nd column)

#------
## Modifying 4D tensor
#------

tensor_4d_demo = tensor_4d.copy()
tensor_4d_demo[1, 1, 2, 3] = 777

print(f"Modified: {tensor_4d_demo[1, 1, 2, 3]}\nOriginal: {tensor_4d[1, 1, 2, 3]}")
# Modified: 777
# Original: 93

tensor_4d_demo[0, 0, :, :] = 0
print(f"Modified 2D slice shape: {tensor_4d_demo[0, 0, :, :].shape}")
# Modified 2D slice shape: (4, 5)
# (Entire first channel of first batch set to 0)

# Using take() on specific axis
print(tensor_4d.take([0], axis=0).shape)
# (1, 3, 4, 5)
# (Take only first batch)

print(tensor_4d.take([1, 3], axis=2).shape)
# (2, 3, 2, 5)
# (Take rows 1 and 3 from all batches and channels)


#---------------------------------------------------------------------------------------------------------#
#---------------------- 7. Elipsis for skipping elements: arr[..., indices] ------------------------------#
#---------------------------------------------------------------------------------------------------------#

########################
## 3D Matrix (Tensor) ##
########################

# Create a 3D array with shape (3, 4, 5) - 3 layers, 4 rows, 5 columns
tensor_3d = np.arange(60).reshape(3, 4, 5)

print(tensor_3d)
# [[[ 0  1  2  3  4]
#   [ 5  6  7  8  9]
#   [10 11 12 13 14]
#   [15 16 17 18 19]]
#
#  [[20 21 22 23 24]
#   [25 26 27 28 29]
#   [30 31 32 33 34]
#   [35 36 37 38 39]]
#
#  [[40 41 42 43 44]
#   [45 46 47 48 49]
#   [50 51 52 53 54]
#   [55 56 57 58 59]]]

print(tensor_3d[..., 2])
# [[ 2  7 12 17]
#  [22 27 32 37]
#  [42 47 52 57]]
'''
All layers, all rows, column 2
Equivalent to tensor_3d[:, :, 2]
'''

print(tensor_3d[1, ...])
# [[20 21 22 23 24]
#  [25 26 27 28 29]
#  [30 31 32 33 34]
#  [35 36 37 38 39]]
'''
Layer 1, all rows and columns
Equivalent to tensor_3d[1, :, :]
'''

print(tensor_3d[..., 1:4])
# [[[ 1  2  3]
#   [ 6  7  8]
#   [11 12 13]
#   [16 17 18]]

#  [[21 22 23]
#   [26 27 28]
#   [31 32 33]
#   [36 37 38]]

#  [[41 42 43]
#   [46 47 48]
#   [51 52 53]
#   [56 57 58]]]
'''
All layers, all rows, columns 1 to 3
Equivalent to tensor_3d[:, :, 1:4]
'''

print(tensor_3d[1, ..., 3])
# [23 28 33 38]
'''
Layer 1, all rows, column 3
Equivalent to tensor_3d[1, :, 3]
'''

