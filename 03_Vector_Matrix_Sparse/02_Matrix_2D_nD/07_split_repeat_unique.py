'''
1. split:
   + np.split(): by "number of sections", by "indices"
   + np.array_split()
   + np.hsplit()
   + np.vsplit()
   + np.dsplit()

2. np.repeat(arr, repeats): repeat elements of an array
   + Repeating with same count
   + Repeating with different counts

3. np.unique(arr): find the unique elements of an array
   + np.unique()
   + np.unique(return_counts=True)
'''

import numpy as np


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 1. Split Operations -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

np.random.seed(0)
matrix = np.random.randint(1, 10, size=(4, 6))
print(matrix)
# [[6 1 4 4 8 4]
#  [6 3 5 8 7 9]
#  [9 2 7 7 9 9]
#  [8 6 9 3 7 7]]
# shape: (4, 6)

###################################################
## np.split(): Splitting by "number of sections" ##
###################################################

# Split along axis 0 (vertical)
split_matrices = np.split(ary=matrix, indices_or_sections=2, axis=0)
print(split_matrices)
# [array([[6, 1, 4, 4, 8, 4],
#         [6, 3, 5, 8, 7, 9]]),
#  array([[9, 2, 7, 7, 9, 9],
#         [8, 6, 9, 3, 7, 7]])]
'''Returns a list of 2 arrays, each with shape (2, 6).'''

for i, mat in enumerate(split_matrices):
    print(f"Matrix {i+1}:\n{mat}")
# Matrix 1:
# [[6 1 4 4 8 4]
#  [6 3 5 8 7 9]]
# Matrix 2:
# [[9 2 7 7 9 9]
#  [8 6 9 3 7 7]]

'''NOTE: If the array cannot be split evenly, a ValueError will be raised.'''

# Split along axis 1 (horizontal)
split_matrices = np.split(ary=matrix, indices_or_sections=3, axis=1)
print(split_matrices)
# [array([[6, 1],
#         [6, 3],
#         [9, 2],
#         [8, 6]]),
#  array([[4, 4],
#         [5, 8],
#         [7, 7],
#         [9, 3]]),
#  array([[8, 4],
#         [7, 9],
#         [9, 9],
#         [7, 7]])]
'''Returns a list of 3 arrays, each with shape (4, 2).'''

########################################
## np.split(): Splitting by "indices" ##
########################################

split_matrices = np.split(ary=matrix, indices_or_sections=[1, 3], axis=0) # arr[:1], arr[1:3], arr[3:]
print(split_matrices)
# [array([[6, 1, 4, 4, 8, 4]]),
#  array([[6, 3, 5, 8, 7, 9],
#         [9, 2, 7, 7, 9, 9]]),
#  array([[8, 6, 9, 3, 7, 7]])]

for i, mat in enumerate(split_matrices):
    print(f"Matrix {i+1} shape: {mat.shape}")
# Matrix 1 shape: (1, 6)
# Matrix 2 shape: (2, 6)
# Matrix 3 shape: (1, 6)
'''Using specified indices allows unequal splits.'''

######################
## np.array_split() ##
######################
'''
np.array_split() is similar to np.split(), but allows unequal splits.
If the array cannot be split evenly, it will not raise an error.
'''

np.random.seed(1)
matrix_uneven = np.random.randint(1, 10, size=(5, 4))
print(matrix_uneven)
# [[6 9 6 1]
#  [1 2 8 7]
#  [3 5 6 3]
#  [5 3 5 8]
#  [8 2 8 1]]

split_matrices = np.array_split(ary=matrix_uneven, indices_or_sections=3, axis=0)
for i, mat in enumerate(split_matrices):
    print(f"Matrix {i+1} shape: {mat.shape}\n{mat}")
# Matrix 1 shape: (2, 4)
# [[6 9 6 1]
#  [1 2 8 7]]
# Matrix 2 shape: (2, 4)
# [[3 5 6 3]
#  [5 3 5 8]]
# Matrix 3 shape: (1, 4)
# [[8 2 8 1]]
'''np.array_split() automatically handles unequal division.'''

#################
## np.hsplit() ##
#################
'''
np.hsplit() splits an array horizontally (column-wise).
Equivalent to np.split(axis=1).
'''

hsplit_matrices = np.hsplit(matrix, 3)
print(hsplit_matrices)
# [array([[6, 1],
#         [6, 3],
#         [9, 2],
#         [8, 6]]),
#  array([[4, 4],
#         [5, 8],
#         [7, 7],
#         [9, 3]]),
#  array([[8, 4],
#         [7, 9],
#         [9, 9],
#         [7, 7]])]
'''Splits the (4, 6) matrix into 3 matrices of shape (4, 2).'''

# Using indices
hsplit_matrices = np.hsplit(matrix, [2, 4]) # arr[:, :2], arr[:, 2:4], arr[:, 4:]
for i, mat in enumerate(hsplit_matrices):
    print(f"Matrix {i+1} shape: {mat.shape}")
# Matrix 1 shape: (4, 2)
# Matrix 2 shape: (4, 2)
# Matrix 3 shape: (4, 2)

#################
## np.vsplit() ##
#################
'''
np.vsplit() splits an array vertically (row-wise).
Equivalent to np.split(axis=0).
'''

vsplit_matrices = np.vsplit(matrix, 2)
print(vsplit_matrices)
# [array([[6, 1, 4, 4, 8, 4],
#         [6, 3, 5, 8, 7, 9]]),
#  array([[9, 2, 7, 7, 9, 9],
#         [8, 6, 9, 3, 7, 7]])]
'''Splits the (4, 6) matrix into 2 matrices of shape (2, 6).'''

# Using indices
vsplit_matrices = np.vsplit(matrix, [1, 3]) # arr[:1], arr[1:3], arr[3:]
for i, mat in enumerate(vsplit_matrices):
    print(f"Matrix {i+1} shape: {mat.shape}")
# Matrix 1 shape: (1, 6)
# Matrix 2 shape: (2, 6)
# Matrix 3 shape: (1, 6)

#################
## np.dsplit() ##
#################
'''
np.dsplit() splits an array along the third axis (depth).
Requires a 3D array.
'''

np.random.seed(2)
matrix_3d = np.random.randint(1, 10, size=(2, 3, 6))
print(f"3D Matrix shape: {matrix_3d.shape}")
# 3D Matrix shape: (2, 3, 6)

dsplit_matrices = np.dsplit(matrix_3d, 3)
for i, mat in enumerate(dsplit_matrices):
    print(f"Matrix {i+1} shape: {mat.shape}")
# Matrix 1 shape: (2, 3, 2)
# Matrix 2 shape: (2, 3, 2)
# Matrix 3 shape: (2, 3, 2)
'''Splits the (2, 3, 6) matrix into 3 matrices of shape (2, 3, 2).'''


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 2. np.repeat() ----------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

matrix = np.array([[1, 2, 3],
                   [4, 5, 6]])
print(matrix)
# [[1 2 3]
#  [4 5 6]]

###############################
## Repeating with same count ##
###############################

# Flatten and repeat each element
print(matrix.repeat(repeats=2))
# [1 1 2 2 3 3 4 4 5 5 6 6]

# Repeat along axis 0 (vertical)
print(matrix.repeat(repeats=2, axis=0))
# [[1 2 3]
#  [1 2 3]
#  [4 5 6]
#  [4 5 6]]

# Repeat along axis 1 (horizontal)
print(matrix.repeat(repeats=2, axis=1))
# [[1 1 2 2 3 3]
#  [4 4 5 5 6 6]]

#####################################
## Repeating with different counts ##
#####################################

# Repeat each row different number of times
print(matrix.repeat(repeats=[1, 3], axis=0))
# [[1 2 3]
#  [4 5 6]
#  [4 5 6]
#  [4 5 6]]
'''
The 1st row is repeated once,
the 2nd row is repeated three times.
'''

# Repeat each column different number of times
print(matrix.repeat(repeats=[1, 2, 3], axis=1))
# [[1 2 2 3 3 3]
#  [4 5 5 6 6 6]]
'''
The 1st column is repeated once,
the 2nd column is repeated twice,
the 3rd column is repeated three times.
'''


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 3. np.unique() ----------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

matrix = np.array([[5, 2, 8, 2],
                   [5, 7, 5, 8],
                   [2, 7, 8, 5]])
print(matrix)
# [[5 2 8 2]
#  [5 7 5 8]
#  [2 7 8 5]]

#################
## np.unique() ##
#################

unique_elements = np.unique(matrix)
print(unique_elements)
# [2 5 7 8]
'''Returns a sorted 1D array of unique elements from the matrix.'''

###################################
## np.unique(return_counts=True) ##
###################################

unique_elements, counts = np.unique(matrix, return_counts=True)

print(unique_elements)
# [2 5 7 8]

print(counts)
# [3 4 2 3]

'''
Element 2 appears 3 times,
Element 5 appears 4 times,
Element 7 appears 2 times,
Element 8 appears 3 times.
'''

# Create a count dictionary
count_dict = dict(zip(unique_elements, counts))
print(count_dict)
# {2: 3, 5: 4, 7: 2, 8: 3}
