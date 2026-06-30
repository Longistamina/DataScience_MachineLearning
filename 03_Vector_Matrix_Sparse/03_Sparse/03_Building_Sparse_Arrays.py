'''
scipy.sparse - Building Sparse Arrays

1. From Dense Arrays:
   + Direct conversion: csr_array(dense_array)
   + All formats support this

2. From Coordinates (data, (row, col)):
   + Format: sparse_array((data, (row, col)), shape=shape)
   + Supported by: COO, CSR, CSC, BSR

3. Special Constructors:
   + eye_array(): Identity matrix
   + diags_array(): Diagonal matrices
   + random_array(): Random sparse arrays
   + block_array(): From sparse blocks

4. From Existing Sparse Arrays:
   + Format conversion: .tocsr(), .tocsc(), .tocoo(), etc.
   + Copying: .copy()

5. Specialized Building Functions:
   + block_diag(): Block diagonal matrices
   + hstack(), vstack(): Horizontal and vertical stacking
   + kron(): Kronecker product
'''

import numpy as np
from scipy import sparse
from scipy.sparse import (csr_array, csc_array, coo_array,
                          eye_array, diags_array, random_array, block_array)


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 1. From Dense Arrays -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
The simplest way to create sparse arrays
All sparse formats can be constructed from dense arrays
'''

########################
## Create dense array ##
########################

dense = np.array([[1, 0, 0, 2],
                  [0, 4, 1, 0],
                  [0, 0, 5, 0]])

print("Original dense array:")
print(dense)
# [[1 0 0 2]
#  [0 4 1 0]
#  [0 0 5 0]]

##################################
## Convert to different formats ##
##################################

csr = csr_array(dense)
csc = csc_array(dense)
coo = coo_array(dense)

print("\n--- Converted to Sparse Formats ---")
print("CSR:", csr)
print("CSC:", csc)
print("COO:", coo)

##################################
## From NumPy matrix operations ##
##################################

# Create larger sparse structure
n = 100
dense_small = np.zeros((n, n))
dense_small[0, 0] = 1
dense_small[n-1, n-1] = 5
# Add some diagonal elements
for i in range(0, n, 10):
    dense_small[i, i] = i + 1

sparse_large = csr_array(dense_small)

print(f"\nLarge sparse array: {sparse_large.shape}, {sparse_large.nnz} non-zeros")
# Large sparse array: (100, 100), 11 non-zeros


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 2. From Coordinates (data, (row, col)) -------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Most flexible construction method
Specify exactly which elements are non-zero

Format: sparse_array((data, (row, col)), shape=(m, n))
'''

###################################
## Basic coordinate construction ##
###################################

row = np.array([0, 0, 1, 1, 2])
col = np.array([0, 3, 1, 2, 2])
data = np.array([1, 2, 4, 1, 5])

coo_coords = coo_array((data, (row, col)), shape=(3, 4))

print("\nCOO from coordinates:")
print(coo_coords.toarray())
# [[1 0 0 2]
#  [0 4 1 0]
#  [0 0 5 0]]

#############################
## Direct CSR construction ##
#############################

csr_coords = csr_array((data, (row, col)), shape=(3, 4))

print(csr_coords.toarray())

###############################################
## Building a large sparse array efficiently ##
###############################################

# Create a sparse array with 1000x1000 shape but only 100 non-zeros
n_size = 1000
n_nonzero = 100

np.random.seed(42)
rows = np.random.randint(0, n_size, n_nonzero)
cols = np.random.randint(0, n_size, n_nonzero)
data_vals = np.random.randn(n_nonzero)

large_sparse = coo_array((data_vals, (rows, cols)), shape=(n_size, n_size))

print(f"\nLarge sparse array: {large_sparse.shape}") # (1000, 1000)
print(f"Non-zeros: {large_sparse.nnz}") # 100
print(f"Density: {100 * large_sparse.nnz / (n_size**2):.4f}%") # 0.0100%

###############################
## Automatic shape inference ##
###############################

# If shape not specified, inferred from max indices
row_auto = [0, 2, 4]
col_auto = [1, 3, 5]
data_auto = [10, 20, 30]

coo_auto = coo_array((data_auto, (row_auto, col_auto)))

print(f"\nAuto shape inference: {coo_auto.shape}")  # (5, 6) - max_row+1, max_col+1
print(coo_auto.toarray())
# [[ 0 10  0  0  0  0]
#  [ 0  0  0  0  0  0]
#  [ 0  0  0 20  0  0]
#  [ 0  0  0  0  0  0]
#  [ 0  0  0  0  0 30]]


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 3. Special Constructors ---------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

###################################
## eye_array() - Identity matrix ##
###################################
'''
Create sparse identity matrix
eye_array(n, m=None, k=0, format=None)
- n: number of rows
- m: number of columns (default: m=n)
- k: diagonal offset (0=main diagonal, 1=above, -1=below)
- format: sparse format (default: csr)
'''

# Standard identity matrix
identity = eye_array(5)
print(identity.toarray())
# [[1. 0. 0. 0. 0.]
#  [0. 1. 0. 0. 0.]
#  [0. 0. 1. 0. 0.]
#  [0. 0. 0. 1. 0.]
#  [0. 0. 0. 0. 1.]]

# Rectangular identity
rect_identity = eye_array(3, 5)
print(rect_identity.toarray())
# [[1. 0. 0. 0. 0.]
#  [0. 1. 0. 0. 0.]
#  [0. 0. 1. 0. 0.]]

# Off-diagonal identity
off_diag = eye_array(4, k=1)  # Upper diagonal
print(off_diag.toarray())
# [[0. 1. 0. 0.]
#  [0. 0. 1. 0.]
#  [0. 0. 0. 1.]
#  [0. 0. 0. 0.]]

off_diag_lower = eye_array(4, k=-1)  # Lower diagonal
print(off_diag_lower.toarray())
# [[0. 0. 0. 0.]
#  [1. 0. 0. 0.]
#  [0. 1. 0. 0.]
#  [0. 0. 1. 0.]]

#######################################
## diags_array() - Diagonal matrices ##
#######################################
'''
Create sparse matrix from diagonals
diags_array(diagonals, offsets=0, shape=None, format=None)
- diagonals: array or list of arrays (one per diagonal)
- offsets: diagonal positions (0=main, positive=above, negative=below)
- shape: output shape (auto-inferred if not provided)
'''

# Single diagonal
main_diag = [1, 2, 3, 4]
diag_main = diags_array(main_diag, offsets=0)
print(diag_main.toarray())
# [[1. 0. 0. 0.]
#  [0. 2. 0. 0.]
#  [0. 0. 3. 0.]
#  [0. 0. 0. 4.]]

# Multiple diagonals
diagonals = [[1, 2, 3, 4],     # Main diagonal
             [5, 6, 7],        # Upper diagonal
             [8, 9, 10]]       # Lower diagonal
offsets = [0, 1, -1]
multi_diag = diags_array(diagonals, offsets=offsets)
print(multi_diag.toarray())
# [[ 1.  5.  0.  0.]
#  [ 8.  2.  6.  0.]
#  [ 0.  9.  3.  7.]
#  [ 0.  0. 10.  4.]]

# Tridiagonal matrix (common in numerical methods)
n = 5
main = np.ones(n) * 2
upper = np.ones(n-1) * -1
lower = np.ones(n-1) * -1
tridiag = diags_array([lower, main, upper], offsets=[-1, 0, 1])
print(tridiag.toarray())
# [[ 2. -1.  0.  0.  0.]
#  [-1.  2. -1.  0.  0.]
#  [ 0. -1.  2. -1.  0.]
#  [ 0.  0. -1.  2. -1.]
#  [ 0.  0.  0. -1.  2.]]

###########################################
## random_array() - Random sparse arrays ##
###########################################
'''
Create random sparse array
random_array(shape, density=0.01, format=None, dtype=None, random_state=None)
- shape: tuple (m, n)
- density: fraction of non-zero elements
- format: sparse format
- random_state: for reproducibility
'''

# Small random sparse array
np.random.seed(42)
random_sparse = random_array((5, 5), density=0.3, random_state=42)
print(random_sparse.toarray().round(2))
# [[0.43 0.   0.   0.   0.  ]
#  [0.37 0.   0.61 0.52 0.  ]
#  [0.   0.   0.   0.   0.  ]
#  [0.   0.3  0.29 0.   0.29]
#  [0.   0.14 0.   0.   0.  ]]

# Large random sparse
np.random.seed(43)
large_random = random_array((1000, 1000), density=0.001, format='csr', random_state=42)
print(f"\nLarge random: {large_random.shape}, density={large_random.nnz/(1000*1000):.4f}")
# Large random: (1000, 1000), density=0.0010

########################################
## block_array() - From sparse blocks ##
########################################
'''
Build sparse array from smaller sparse blocks
block_array(blocks, format=None, dtype=None)
- blocks: 2D list/array of sparse arrays or None
'''

# Create small sparse blocks
A = csr_array([[1, 2], [3, 4]])
B = csr_array([[5], [6]])
C = csr_array([[7, 8]])
D = csr_array([[9]])

# Combine into larger block matrix
blocks = [[A, B],
          [C, D]]

block_mat = block_array(blocks)

print(block_mat.toarray())
# [[1 2 5]      # [1 2 5] = A [1, 2] | B [5]
#  [3 4 6]
#  [7 8 9]]

# Using None for zero blocks
block_with_zeros = block_array([[A, None],
                                [None, A]])
print(block_with_zeros.toarray())
# [[1 2 0 0]
#  [3 4 0 0]
#  [0 0 1 2]
#  [0 0 3 4]]


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------- 4. From Existing Sparse Arrays -----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

#######################
## Format conversion ##
#######################
'''Convert between sparse formats using .to<format>() methods'''

original_coo = coo_array(dense)
print(f"Original: {original_coo}")

# Convert to different formats
converted_csr = original_coo.tocsr()
converted_csc = original_coo.tocsc()
converted_dia = original_coo.todia()
converted_dok = original_coo.todok()
converted_lil = original_coo.tolil()

print(f"To CSR: {converted_csr}")
print(f"To CSC: {converted_csc}")
print(f"To DIA: {converted_dia}")

###########################
## Copying sparse arrays ##
###########################
'''Use .copy() to create independent copy'''

sparse_orig = csr_array([[1, 0], [0, 2]])
sparse_copy = sparse_orig.copy()

print("Original:\n", sparse_orig.toarray())
# Original:
#  [[1 0]
#  [0 2]]

print("Copy:\n", sparse_copy.toarray())
# Copy:
#  [[1 0]
#  [0 2]]

# Modify copy
sparse_copy[0, 0] = 99

print("Original:\n", sparse_orig.toarray())  # Unchanged
# Original:
#  [[1 0]
#  [0 2]]

print("Copy:\n", sparse_copy.toarray())
# Copy:
#  [[99  0]
#  [ 0  2]]


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 5. Specialized Building Functions ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

###################################
## block_diag() - Block diagonal ##
###################################
'''
Create block diagonal matrix from list of matrices
block_diag(mats, format=None, dtype=None)
'''

mat1 = csr_array([[1, 2], [3, 4]])
mat2 = csr_array([[5, 6, 7]])
mat3 = csr_array([[8]])

block_diag_mat = sparse.block_diag([mat1, mat2, mat3], format='csr')

print(block_diag_mat.toarray())
# [[1 2 0 0 0 0]
#  [3 4 0 0 0 0]
#  [0 0 5 6 7 0]
#  [0 0 0 0 0 8]]
'''mat1 occupies top-left 2x2 block, mat2 the next 1x3 block, and mat3 the bottom-right 1x1'''

##############################################################
## hstack() and vstack() - Horizontal and Vertical stacking ##
##############################################################
'''Combine sparse arrays horizontally or vertically'''

A = csr_array([[1, 2], [3, 4]])
B = csr_array([[5, 6], [7, 8]])

# Horizontal stack
h_stacked = sparse.hstack([A, B])
print(h_stacked.toarray())
# [[1 2 5 6]
#  [3 4 7 8]]

# Vertical stack
v_stacked = sparse.vstack([A, B])
print(v_stacked.toarray())
# [[1 2]
#  [3 4]
#  [5 6]
#  [7 8]]

################################
## kron() - Kronecker product ##
################################
'''Kronecker product of two sparse arrays'''

A_small = csr_array([[1, 2], [3, 4]])
B_small = csr_array([[0, 5], [6, 0]])

kron_prod = sparse.kron(A_small, B_small, format='csr')
print("Kronecker product A ⊗ B:")
print(kron_prod.toarray())
# [[ 0  5  0 10]
#  [ 6  0 12  0]
#  [ 0 15  0 20]
#  [18  0 24  0]]
'''
Each element a_ij of A is multiplied by the entire matrix B to form blocks in the resulting matrix.

For example, the element at (0,0) in A is 1, so the top-left block in the result is 1*B.
=> [[0, 5],
    [6, 0]]

The element at (0,1) in A is 2, so the top-right block in the result is 2*B.
=> [[0, 10],
    [12, 0]]

And so on
'''
