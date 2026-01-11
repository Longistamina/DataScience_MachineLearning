'''
Boolean Indexing Boolean Filtering for 2D Matrices is a powerful technique
that allows you to filter data based on specific conditions.

###############################

Flow of contents:

0. Mask: a boolean array created using a condition

1. Single Condition Examples:
   + Logic Operators: >, <, >=, <=, ==, !=
   + np.isin()

2. Negation of Condition: ~ (tilde) operator

3. Combine Multiple Conditions:
   + & (and),
   + | (or)
   + Combine & and |

4. Boolean Compression: arr.compress(mask, axis)

5. Row and Column Filtering (using np.any() and np.all())

6. Examples for 3D and 4D matrices
'''

import numpy as np

np.random.seed(42)
matrix = np.random.randint(40, 80, size=(6, 8))

print(matrix)
# [[78 68 54 47 60 78 58 62]
#  [50 50 63 75 79 63 42 61]
#  [41 63 69 77 41 60 72 51]
#  [61 64 66 67 55 54 42 76]
#  [46 60 48 78 57 43 64 53]
#  [48 65 41 59 67 46 47 74]]


#--------------------------------------------------------------------------------------------------------#
#-------------------------- 0. Mask: a boolean array created using a condition --------------------------#
#--------------------------------------------------------------------------------------------------------#

mask = matrix > 70
print(mask)
# [[ True False False False False  True False False]
#  [False False False  True  True False False False]
#  [False False False  True False False  True False]
#  [False False False False False False False  True]
#  [False False False  True False False False False]
#  [False False False False False False False  True]]

print(matrix <= 50)
# [[False False False  True False False False False]
#  [ True  True False False False False  True False]
#  [ True False False False  True False False False]
#  [False False False False False False  True False]
#  [ True False  True False False  True False False]
#  [ True False  True False False  True  True False]]

'''
So Mask is a boolean 2D array where each element indicates whether the corresponding
element in the original matrix satisfies the given condition (True) or not (False).

NOTE: When used for indexing, it flattens the result into a 1D array.
'''


#--------------------------------------------------------------------------------------------------------#
#------------------------------ 1. Single Condition Examples: np.isin() ---------------------------------#
#--------------------------------------------------------------------------------------------------------#

######################
## > (greater than) ##
######################

mask_gt_70 = matrix > 70
print(matrix[mask_gt_70])
# [78 78 75 79 77 72 76 78 74]

print(matrix[matrix > 70])
# [78 78 75 79 77 72 76 78 74]

###################
## < (less than) ##
###################

print(matrix[matrix < 50])
# [48 43 42 48 44 42 43 46 41]

'''
>= (greater than or equal to)
<= (less than or equal to)

They work similarly to > and < but include equality.
'''

################
## == (equal) ##
################

print(matrix[matrix == 78])
# [78 78 78]

####################
## != (not equal) ##
####################

print(matrix[matrix != 51][:20])
# [78 68 54 47 60 78 58 62 50 50 63 75 79 63 42 61 41 63 69 77]

###############
## np.isin() ##
###############
'''
np.isin() checks whether each element in your 2D matrix is present in a test array,
returning a boolean 2D array with the same shape

Key Parameters for 2D Arrays
# element: Your 2D numeric array to check
# test_elements: Values to search for (can be list, array, or other iterable)
# assume_unique: Set True if both arrays have unique values for faster computation
# invert: Set True to find elements NOT in test_elements
'''

test_values = [51, 77, 42]

mask_isin = np.isin(element=matrix, test_elements=test_values)
print(mask_isin)
# [[False False False False False False False False]
#  [False False False False False False  True False]
#  [False False False  True False False False  True]
#  [False False False False False False  True False]
#  [False False False False False False False False]
#  [False False False False False False False False]]

print(matrix[mask_isin])
# [42 77 51 42]

# Use invert=True to get elements NOT in test_values
print(matrix[np.isin(matrix, [51, 77, 70], invert=True)][:20])
# [78 68 54 47 60 78 58 62 50 50 63 75 79 63 42 61 41 63 69 41]


#--------------------------------------------------------------------------------------------------------#
#--------------------------- 2. Negation of Condition: ~ (tilde) operator -------------------------------#
#--------------------------------------------------------------------------------------------------------#

print(matrix[~(matrix >= 60)])
# [54 47 58 50 50 42 41 41 51 55 54 42 46 48 57 43 53 48 41 59 46 47]
'''Values that are NOT greater than or equal to 60'''

print(matrix[~np.isin(matrix, [51, 72, 77])][:20])
# [78 68 54 47 60 78 58 62 50 50 63 75 79 63 42 61 41 63 69 41]
'''Values that are NOT in the list [51, 72, 77]'''


#--------------------------------------------------------------------------------------------------------#
#----------------------- 3. Combine Multiple Conditions: & (and), | (or) --------------------------------#
#--------------------------------------------------------------------------------------------------------#

######################
## & (and) operator ##
######################

print(matrix[(matrix > 60) & (matrix < 70)])
# [68 62 63 63 61 63 69 61 64 66 67 64 65 67]

#####################
## | (or) operator ##
#####################

print(matrix[(matrix < 45) | (matrix > 75)])
# [78 78 79 42 41 77 41 42 76 78 43 41]

#####################
## Combine & and | ##
#####################

print(matrix[((matrix >= 70) & (matrix <= 75)) | (matrix == 42)])
# [75 42 72 42 74]


#--------------------------------------------------------------------------------------------------------#
#----------------------------- 4. Boolean Compression: arr.compress(mask) -------------------------------#
#--------------------------------------------------------------------------------------------------------#

'''
For 2D arrays, compress() works along a specified axis

axis=0: compress rows based on boolean array of length = number of rows
axis=1: compress columns based on boolean array of length = number of columns

NOTE: for 2D arrays, cannot use axis=None directly with compress(), but can flatten first
'''

#############################
## Compress with axis=None ##
#############################

matrix_flat = matrix.flatten()

print(matrix_flat.compress(matrix_flat > 70, axis=None))
# [78 78 75 79 77 72 76 78 74]

##########################
## Compress with axis=0 ##
##########################
'''axis=0 goes vertically, meaning column-wise'''

col_mask = matrix.mean(axis=0) > 60
print("Column means:", matrix.mean(axis=0).round(2))
print("Column mask:", col_mask)
print(matrix.compress(col_mask, axis=1))
# Column means: [54.   61.67 56.83 67.17 59.83 57.33 54.17 62.83]
# Column mask: [False  True False  True False False False  True]
# [[68 47 62]
#  [50 75 61]
#  [63 77 51]
#  [64 67 76]
#  [60 78 53]
#  [65 59 74]]
'''These are the 3 columns where the vertical mean value is greater than 60.'''

##########################
## Compress with axis=0 ##
##########################

row_mask = matrix.sum(axis=1) > 460
print("Row sums:", matrix.sum(axis=1))
print("Row mask:", row_mask)
print(matrix.compress(row_mask, axis=0))

# Row sums: [505 483 474 485 449 447]
# Row mask: [ True  True  True  True False False]
# [[78 68 54 47 60 78 58 62]
#  [50 50 63 75 79 63 42 61]
#  [41 63 69 77 41 60 72 51]
#  [61 64 66 67 55 54 42 76]]
'''These are the 4 rows where the horizontal sum is greater than 460.'''


#--------------------------------------------------------------------------------------------------------#
#------------------------- 5. Row and Column Filtering (np.any() and np.all()) --------------------------#
#--------------------------------------------------------------------------------------------------------#
'''
Can youse np.any() and np.all() along specific axes to filter rows or columns
=> results in a 2D array with selected rows or columns based on the condition.
'''

#############################
## Column Filtering axis=0 ##
#############################
'''NOTE: must use matrix[:, condition] to get all the rows for selected columns, keep 2D structure'''

#------
## with np.any()
#------

col_condition = np.any(matrix < 45, axis=0) # Filter columns where ANY element < 45
print("Column condition:", col_condition)
# Column condition: [ True False  True False  True  True  True False]

print(matrix[:, col_condition])
# [[78 54 60 78 58]
#  [50 63 79 63 42]
#  [41 69 41 60 72]
#  [61 66 55 54 42]
#  [46 48 57 43 64]
#  [48 41 67 46 47]]

print(matrix[:, np.any(matrix < 50, axis=0)]) # same outcome
# [[78 54 47 60 78 58]
#  [50 63 75 79 63 42]
#  [41 69 77 41 60 72]
#  [61 66 67 55 54 42]
#  [46 48 78 57 43 64]
#  [48 41 59 67 46 47]]

#-----
## with np.all()
#-----

col_condtion = np.all(matrix > 45, axis=0) # Filter columns where ALL elements > 45
print("Column condition:", col_condtion)
# Column condition: [False  True False  True False False False  True]

print(matrix[:, col_condtion])
# [[68 47 62]
#  [50 75 61]
#  [63 77 51]
#  [64 67 76]
#  [60 78 53]
#  [65 59 74]]

print(matrix[:, np.all(matrix > 45, axis=0)]) # same outcome
# [[68 47 62]
#  [50 75 61]
#  [63 77 51]
#  [64 67 76]
#  [60 78 53]
#  [65 59 74]]

'''
col_condition could be more complicated, like:
# np.all((matrix > 45) & (matrix < 75), axis=0)
# np.any((matrix < 50) | (matrix > 70), axis=0)
'''

#-----
## With custom boolean array for column filtering
#-----

custom_mask = np.array([True, False, True, False, True, False, True, False])

print(matrix[:, custom_mask])
# [[78 54 60 58]
#  [50 63 79 42]
#  [41 69 41 72]
#  [61 66 55 42]
#  [46 48 57 64]
#  [48 41 67 47]]

print(matrix[:, [True, False, True, False, True, False, True, False]]) # same outcome
# [[78 54 60 58]
#  [50 63 79 42]
#  [41 69 41 72]
#  [61 66 55 42]
#  [46 48 57 64]
#  [48 41 67 47]]

##########################
## Row Filtering axis=1 ##
##########################

#------
## with np.any()
#------

row_condition = np.any(matrix >= 78, axis=1) # Filter rows where ANY element >= 78
print("Row condition:", row_condition)
# Row condition: [ True  True False False  True False]

print(matrix[row_condition, :])
# [[78 68 54 47 60 78 58 62]
#  [50 50 63 75 79 63 42 61]
#  [46 60 48 78 57 43 64 53]]

print(matrix[np.any(matrix >= 78, axis=1)]) # Same outcome, no need to specify ":" for columns
# [[78 68 54 47 60 78 58 62]
#  [50 50 63 75 79 63 42 61]
#  [46 60 48 78 57 43 64 53]]

#-----
## with np.all()
#-----

row_condition = np.all(matrix <= 76, axis=1) # Filter rows where ALL elements <= 76
print("Row condition:", row_condition)
# Row condition: [False False False  True False  True]

print(matrix[row_condition, :])
# [[61 64 66 67 55 54 42 76]
#  [48 65 41 59 67 46 47 74]]

print(matrix[np.all(matrix <= 76, axis=1)]) # Same outcome, no need to specify ":" for columns
# [[61 64 66 67 55 54 42 76]
#  [48 65 41 59 67 46 47 74]]

'''
NOTE: row_condition could be more complicated, like:
# np.all((matrix >= 45) & (matrix <= 70), axis=1)
# np.any((matrix < 50) | (matrix > 75), axis=1
'''

#-----
## With custom boolean array for row filtering
#-----

custom_mask = np.array([True, False, True, False, True, False])

print(matrix[custom_mask, :])
# [[51 52 69 67 51 58 48 59]
#  [52 63 77 43 42 75 78 51]
#  [54 73 77 73 78 77 43 64]]

print(matrix[[True, False, True, False, True, False]]) # Same outcome, no need to specify ":" for columns
# [[78 68 54 47 60 78 58 62]
#  [41 63 69 77 41 60 72 51]
#  [46 60 48 78 57 43 64 53]]


#--------------------------------------------------------------------------------------------------------#
#---------------------------- 6. Examples for 3D and 4D matrices ----------------------------------------#
#--------------------------------------------------------------------------------------------------------#
'''
Boolean indexing works similarly for higher-dimensional arrays,
flattening the result into a 1D array when using element-wise conditions.
'''

################
## 3D Example ##
################

matrix_3d = np.random.randint(10, 50, size=(3, 4, 5))
print("\n3D Matrix shape:", matrix_3d.shape)
print("3D Matrix:\n", matrix_3d)

print("\n3D: Elements > 40:")
print(matrix_3d[matrix_3d > 40])

print("\n3D: Filter along axis (first dimension where mean of each 2D slice > 28):")
slice_means = matrix_3d.mean(axis=(1, 2))
print("Slice means:", slice_means)
print(matrix_3d[slice_means > 28])

################
## 4D Example ##
################

matrix_4d = np.random.randint(5, 25, size=(2, 3, 3, 4))
print("\n4D Matrix shape:", matrix_4d.shape)

print("\n4D: Elements in [10, 15, 20]:")
print(matrix_4d[np.isin(matrix_4d, [10, 15, 20])])

print("\n4D: Combined condition (< 10) | (> 20):")
print(matrix_4d[(matrix_4d < 10) | (matrix_4d > 20)])
