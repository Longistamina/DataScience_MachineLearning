'''
scipy.sparse - Sparse Array Indexing and Slicing

1. Single Element Access:
   + Getting single elements: A[i, j]
   + Setting single elements: A[i, j] = value
   + Format requirements for indexing

2. Row and Column Slicing:
   + Row slicing: A[i, :]
   + Column slicing: A[:, j]
   + Multiple rows/columns: A[i:j, :]
   + CSR efficient for rows, CSC efficient for columns

3. Fancy Indexing:
   + Integer array indexing: A[[0, 2], :]
   + Multiple indices: A[rows, cols]

4. Boolean Indexing:
   + Boolean masks
   + Conditional selection

5. Assignment Operations:
   + Assigning to elements
   + Assigning to slices
   + Adding new non-zero elements
   + Format considerations

6. Best Practices:
   + When to convert formats
   + Efficient indexing patterns
'''

import numpy as np
from scipy.sparse import csr_array, csc_array, coo_array, lil_array, dok_array


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 1. Single Element Access ----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

#############################
## Getting single elements ##
#############################
'''
Most formats support single element access: A[i, j]
Exceptions: COO and DIA formats do not support indexing
'''

A = csr_array([[1, 0, 2, 0],
               [0, 3, 0, 4],
               [5, 0, 6, 0]])

# Access elements
print("\nA[0, 0] =", A[0, 0])  # 1
print("A[1, 1] =", A[1, 1])  # 3
print("A[0, 1] =", A[0, 1])  # 0 (sparse zero)
print("A[2, 2] =", A[2, 2])  # 6

# Type of returned element
print("\nType of A[0, 0]:", type(A[0, 0]))  # numpy scalar or matrix
                                            # <class 'numpy.int64'>

#######################################
## COO arrays don't support indexing ##
#######################################
'''
COO format does not support element access
Must convert to CSR, CSC, or other formats first
'''

A_coo = coo_array([[1, 0, 2],
                   [0, 3, 0]])

try:
    element = A_coo[0, 0]
except TypeError as e:
    print(f"Error accessing COO element: {e}")
# Error accessing COO element: 'coo_array' object is not subscriptable

# Solution: convert to CSR
A_csr = A_coo.tocsr()
print(f"After converting to CSR: A_csr[0, 0] = {A_csr[0, 0]}") # 1

#############################
## Setting single elements ##
#############################
'''
Some formats support element assignment
LIL and DOK are best for element-wise construction
CSR/CSC support assignment but less efficient
'''

# Using DOK (best for element-wise construction)
A_dok = dok_array((3, 4), dtype=float)
A_dok[0, 0] = 1.0
A_dok[0, 2] = 2.0
A_dok[1, 1] = 3.0
A_dok[2, 3] = 4.0
print(A_dok.toarray())
# [[1. 0. 2. 0.]
#  [0. 3. 0. 0.]
#  [0. 0. 0. 4.]]

# Using LIL
A_lil = lil_array((3, 4), dtype=float)
A_lil[0, 0] = 5.0
A_lil[1, 1] = 6.0
A_lil[2, 2] = 7.0
print(A_lil.toarray())
# [[5. 0. 0. 0.]
#  [0. 6. 0. 0.]
#  [0. 0. 7. 0.]]

# CSR supports assignment but creates explicit zeros
A_csr_set = csr_array([[1, 0, 2],
                       [0, 3, 0]])
A_csr_set[0, 1] = 5  # Modifying a zero element
print(A_csr_set.toarray())
# [[1 5 2]
#  [0 3 0]]


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 2. Row and Column Slicing --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

####################################
## Row slicing (efficient in CSR) ##
####################################
'''
CSR format is optimized for row access
Returns a sparse matrix (row vector)
'''

A_row = csr_array([[1, 0, 2, 0, 3],
                   [0, 4, 0, 5, 0],
                   [6, 0, 7, 0, 8],
                   [0, 9, 0, 10, 0]])

# Single row
row_1 = A_row[1, :]
print(row_1.toarray())
# [0 4 0 5 0]

# Multiple rows
rows_0_2 = A_row[0:3, :]
print(rows_0_2.toarray())
# [[1 0 2 0 3]
#  [0 4 0 5 0]
#  [6 0 7 0 8]]

# Specific rows (fancy indexing)
rows_select = A_row[[0, 2], :]
print(rows_select.toarray())
# [[1 0 2 0 3]
#  [6 0 7 0 8]]

#######################################
## Column slicing (efficient in CSC) ##
#######################################
'''
CSC format is optimized for column access
Convert CSR to CSC for efficient column operations
'''

A_col = csc_array(A_row.toarray())  # Convert to CSC

# Single column
col_2 = A_col[:, 2]
print(col_2.toarray())
# [2 0 7 0]

# Multiple columns
cols_1_3 = A_col[:, 1:4]
print(cols_1_3.toarray())
# [[ 0  2  0]
#  [ 4  0  5]
#  [ 0  7  0]
#  [ 9  0 10]]

# Specific columns
cols_select = A_col[:, [0, 2, 4]]
print(cols_select.toarray())
# [[1 2 3]
#  [0 0 0]
#  [6 7 8]
#  [0 0 0]]

##########################
## Submatrix extraction ##
##########################
'''
Extract rectangular submatrix
Works with both row and column slices
'''

submatrix = A_row[1:3, 1:4]
print(submatrix.toarray())
# [[4 0 5]
#  [0 7 0]]

# Using fancy indexing
submat_fancy = A_row[[0, 2], :][:, [1, 3]]
print(submat_fancy.toarray())
# [[0 0]
#  [0 0]]

########################################
## Comparison: CSR vs CSC performance ##
########################################
'''Demonstrate efficiency difference'''

import time
from tldm import tldm

# Large matrix
n = 1000
A_large = csr_array(np.random.rand(n, n) < 0.01)  # 1% density

#-----
## CSR benchmack
#-----

# Row access in CSR (fast)
start = time.time()
for i in tldm(range(100), desc="CSR benchmark"):
    row = A_large[i, :]
csr_row_time = time.time() - start

# Column access in CSR (slower)
start = time.time()
for i in tldm(range(100), desc="CSR benchmark"):
    col = A_large[:, i]
csr_col_time = time.time() - start

#-----
## CSC benchmack
#-----

# Convert to CSC
A_large_csc = A_large.tocsc()

# Column access in CSC (fast)
start = time.time()
for i in tldm(range(100), desc="CSC benchmark"):
    col = A_large_csc[:, i]
csc_col_time = time.time() - start

print(f"CSR row access: {csr_row_time*1000:.2f} ms") # 31.51 ms
print(f"CSR column access: {csr_col_time*1000:.2f} ms") # 16.42 ms
print(f"CSC column access: {csc_col_time*1000:.2f} ms") # 12.76 ms
print(f"\nSpeedup (CSR col vs CSC col): {csr_col_time/csc_col_time:.1f}x") # 1.3x


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 3. Fancy Indexing ------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

############################
## Integer array indexing ##
############################
'''
Use arrays of integers to select rows/columns
Similar to NumPy fancy indexing but more limited
'''

A_fancy = csr_array([[1, 0, 2, 0],
                     [0, 3, 0, 4],
                     [5, 0, 6, 0],
                     [0, 7, 0, 8]])

# Select specific rows
row_indices = [0, 2, 3]
rows_fancy = A_fancy[row_indices, :]
print(rows_fancy.toarray())
# [[1 0 2 0]
#  [5 0 6 0]
#  [0 7 0 8]]

# Select specific columns (more efficient in CSC)
col_indices = [1, 3]
cols_fancy = A_fancy[:, col_indices]
print(cols_fancy.toarray())
# [[0 0]
#  [3 4]
#  [0 0]
#  [7 8]]

# Boolean array indexing for rows
bool_mask = np.array([True, False, True, False])
rows_bool = A_fancy[bool_mask, :]
print(rows_bool.toarray())
# [[1 0 2 0]
#  [5 0 6 0]]


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 4. Boolean Indexing --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

###################
## Boolean masks ##
###################
'''
Use boolean arrays to select rows or columns
More limited than NumPy dense arrays
'''

A_bool = csr_array([[1, 0, 2, 0],
                    [0, 3, 0, 4],
                    [5, 0, 6, 0],
                    [0, 7, 0, 8]])

# Boolean mask for rows
row_mask = np.array([True, False, True, False])
rows_masked = A_bool[row_mask, :]
print(rows_masked.toarray())
# [[1 0 2 0]
#  [5 0 6 0]]

# Boolean mask for columns
col_mask = np.array([False, True, False, True])
cols_masked = A_bool[:, col_mask]
print(cols_masked.toarray())
# [[0 0]
#  [3 4]
#  [0 0]
#  [7 8]]

###########################
## Conditional selection ##
###########################
'''
Select elements based on conditions
Returns sparse matrix with True/False (as 1/0)
'''

# Find elements > 3
mask_gt3 = A_bool > 3
print(mask_gt3.toarray())
# [[False False False False]
#  [False False False  True]
#  [ True False  True False]
#  [False  True False  True]]

# Find non-zero elements
mask_nonzero = A_bool != 0
print(mask_nonzero.toarray())
# [[ True False  True False]
#  [False  True False  True]
#  [ True False  True False]
#  [False  True False  True]]

# Use mask to select rows with any element > 5
has_large = np.array((A_bool > 5).sum(axis=1)).flatten() > 0 # array([False, False,  True,  True])
rows_with_large = A_bool[has_large, :]
print(rows_with_large.toarray())
# [[5 0 6 0]
#  [0 7 0 8]]

#################
## Limitations ##
#################
'''
Boolean indexing on elements (not rows/cols) usually produces dense output
Avoid: A[A > 3] = 0  # This doesn't work as in NumPy
'''

print("Element-wise boolean indexing is limited in sparse arrays")
print("Use comparison operations to create boolean sparse matrices instead")


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 5. Assignment Operations ----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

###########################
## Assigning to elements ##
###########################
'''
Best formats for assignment: DOK and LIL
CSR/CSC allow assignment but may be slower
'''

# DOK: best for element assignment
A_assign = dok_array((4, 4), dtype=float)
print(A_assign.toarray())
# [[0. 0. 0. 0.]
#  [0. 0. 0. 0.]
#  [0. 0. 0. 0.]
#  [0. 0. 0. 0.]]

# Assign values
A_assign[0, 0] = 1
A_assign[1, 1] = 2
A_assign[2, 2] = 3
A_assign[3, 3] = 4
print(A_assign.toarray())
# [[1. 0. 0. 0.]
#  [0. 2. 0. 0.]
#  [0. 0. 3. 0.]
#  [0. 0. 0. 4.]]

# Assign to previously zero element
A_assign[0, 2] = 5
print(A_assign.toarray())
# [[1. 0. 5. 0.]
#  [0. 2. 0. 0.]
#  [0. 0. 3. 0.]
#  [0. 0. 0. 4.]]

# Change existing element
A_assign[1, 1] = 10
print(A_assign.toarray())
# [[ 1.  0.  5.  0.]
#  [ 0. 10.  0.  0.]
#  [ 0.  0.  3.  0.]
#  [ 0.  0.  0.  4.]]

#########################
## Assigning to slices ##
#########################
'''LIL format is efficient for row slicing assignment'''

A_slice = lil_array((4, 4), dtype=float)

# Assign to a row
A_slice[0, :] = [1, 2, 3, 4]
print(A_slice.toarray())
# [[1. 2. 3. 4.]
#  [0. 0. 0. 0.]
#  [0. 0. 0. 0.]
#  [0. 0. 0. 0.]]

# Assign to a column (less efficient in LIL)
A_slice[:, 1] = [[10], [20], [30], [40]]
print(A_slice.toarray())
# [[ 1. 10.  3.  4.]
#  [ 0. 20.  0.  0.]
#  [ 0. 30.  0.  0.]
#  [ 0. 40.  0.  0.]]

# Assign to submatrix
A_slice[2:4, 2:4] = [[50, 60], [70, 80]]
print(A_slice.toarray())
# [[ 1. 10.  3.  4.]
#  [ 0. 20.  0.  0.]
#  [ 0. 30. 50. 60.]
#  [ 0. 40. 70. 80.]]

##################################
## Adding new non-zero elements ##
##################################
'''
Adding elements to sparse arrays
Formats like DOK and LIL handle this efficiently
'''

A_add = lil_array((3, 3), dtype=int)
A_add[0, 0] = 1 # Add initial element
print(A_add.toarray())
# [[1 0 0]
#  [0 0 0]
#  [0 0 0]]

# Add more elements
A_add[0, 1] = 2
A_add[1, 2] = 3
A_add[2, 0] = 4
print(A_add.toarray())
# [[1 2 0]
#  [0 0 3]
#  [4 0 0]]

# Stored elements
print(f"Number of stored elements: {A_add.nnz}")  # 4

#############################
## Assignment with CSR/CSC ##
#############################
'''
CSR and CSC support assignment but it's slower
May need to convert format for many assignments
'''

#--------
## CSR assignment
#--------

A_csr_assign = csr_array(np.zeros((3, 3)))
print(A_csr_assign.toarray())
# [[0. 0. 0.]
#  [0. 0. 0.]
#  [0. 0. 0.]]

# Assign to existing zero (creates explicit zero or changes structure)
A_csr_assign[0, 0] = 5
A_csr_assign[1, 1] = 10
print(A_csr_assign.toarray())
# [[ 5.  0.  0.]
#  [ 0. 10.  0.]
#  [ 0.  0.  0.]]

# For many assignments, convert to LIL first
A_lil_temp = A_csr_assign.tolil()
A_lil_temp[0, 2] = 15
A_lil_temp[2, 0] = 20
A_csr_assign = A_lil_temp.tocsr()
print(A_csr_assign.toarray())
# [[ 5.  0. 15.]
#  [ 0. 10.  0.]
#  [20.  0.  0.]]


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 6. Best Practices ------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

#############################
## When to convert formats ##
#############################
'''
Choose format based on access pattern:
- Many row accesses -> CSR
- Many column accesses -> CSC  
- Building element-by-element -> DOK or LIL
- Arithmetic operations -> CSR or CSC
'''

print("\nFormat Selection Guidelines:")
print("1. Use DOK or LIL for construction")
print("2. Convert to CSR for row operations and arithmetic")
print("3. Convert to CSC for column operations")
print("4. Use COO for easy format conversion")

#################################
## Efficient indexing patterns ##
#################################

'''
Demonstrate efficient vs inefficient patterns
'''

A_pattern = csr_array(np.random.rand(100, 100) < 0.1)

# EFFICIENT: Slice entire rows in CSR
print("✓ Efficient: A[10:20, :]  # Row slices in CSR")

# LESS EFFICIENT: Individual element access in loop
print("✗ Less efficient: for i in range(n): x = A[i, j]  # Element-by-element")

# EFFICIENT: Vectorized operations
print("✓ Efficient: A @ v  # Matrix-vector product")

# EFFICIENT: Get multiple rows at once
print("✓ Efficient: A[[1,3,5], :]  # Multiple rows at once")
