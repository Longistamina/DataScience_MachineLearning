'''
scipy.sparse - Sparse Array Formats

1. COO (Coordinate) Format - coo_array():
   + Simplest format: stores row, column, and data arrays
   + Fast construction and conversion to other formats
   + Does not support arithmetic operations directly
   + Allows duplicates

2. CSR (Compressed Sparse Row) - csr_array():
   + Most commonly used format
   + Efficient row slicing and matrix-vector products
   + Fast arithmetic operations
   + Efficient for row-based operations

3. CSC (Compressed Sparse Column) - csc_array():
   + Similar to CSR but column-oriented
   + Efficient column slicing
   + Fast arithmetic operations
   + Efficient for column-based operations

4. BSR (Block Sparse Row) - bsr_array():
   + For arrays with dense sub-blocks
   + Efficient for block-structured matrices
   + Common in finite element methods

5. DIA (Diagonal) - dia_array():
   + For arrays with values along diagonals
   + Very memory efficient for diagonal matrices
   + Limited functionality (no slicing/indexing)

6. DOK (Dictionary of Keys) - dok_array():
   + Dictionary-based storage
   + Efficient for incremental construction
   + Supports single-element access and modification

7. LIL (List of Lists) - lil_array():
   + Row-based list of lists
   + Efficient for constructing sparse arrays incrementally
   + Good for row slicing and modification
'''

import numpy as np
from scipy.sparse import (coo_array, csr_array, csc_array,
                          bsr_array, dia_array, dok_array, lil_array)

# Create a sample dense array for demonstrations
dense = np.array([[1, 0, 0, 2],
                  [0, 4, 1, 0],
                  [0, 0, 5, 0]])

print("Original dense array:")
print(dense)
# [[1 0 0 2]
#  [0 4 1 0]
#  [0 0 5 0]]


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 1. COO (Coordinate) Format -------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
COO format stores three arrays:
- row: row indices of non-zero elements
- col: column indices of non-zero elements
- data: values of non-zero elements

Best for:
- Initial construction
- Converting to other formats
- Modifying sparse structure

Not good for:
- Arithmetic operations (need to convert to CSR/CSC)
- Slicing or indexing
'''

##########################
## Method 1: From dense ##
##########################

coo = coo_array(dense)
print("\n--- COO Format ---")
print(coo)
# <COOrdinate sparse array of dtype 'int64'
#  with 5 stored elements and shape (3, 4)>
#   Coords        Values
#   (0, 0)        1
#   (0, 3)        2
#   (1, 1)        4
#   (1, 2)        1
#   (2, 2)        5

#######################################
## Method 2: From (data, (row, col)) ##
#######################################
'''The most flexible way to construct COO arrays'''

row = np.array([0, 0, 1, 1, 2])
col = np.array([0, 3, 1, 2, 2])
data = np.array([1, 2, 4, 1, 5])

coo_from_coords = coo_array((data, (row, col)), shape=(3, 4))
print("\nCOO from coordinates:")
print(coo_from_coords.toarray())
# [[1 0 0 2]
#  [0 4 1 0]
#  [0 0 5 0]]

##############################
## Accessing COO attributes ##
##############################

print("Row indices:", coo.row) # [0 0 1 1 2]
print("Column indices:", coo.col) # [0 3 1 2 2]
print("Data values:", coo.data) # [1 2 4 1 5]

#########################
## Handling duplicates ##
#########################
'''
COO format allows duplicate entries at the same location
Duplicates are summed when converted to other formats
'''

row_dup = np.array([0, 0, 0])  # Three entries at (0,0)
col_dup = np.array([0, 0, 0])
data_dup = np.array([1, 2, 3])

coo_dup = coo_array((data_dup, (row_dup, col_dup)), shape=(2, 2))
print(coo_dup)
# <COOrdinate sparse array of dtype 'int64'
#         with 3 stored elements and shape (2, 2)>
#   Coords        Values
#   (0, 0)        1
#   (0, 0)        2
#   (0, 0)        3

print("Stored elements:", coo_dup.nnz)  # 3

print(coo_dup.toarray())  # [[6 0], [0 0]] (1+2+3=6)
# [[6 0]
#  [0 0]]
# (1+2+3=6)
# Dense representation (duplicates summed)

# Remove duplicates
coo_dup.sum_duplicates()
print("Stored elements:", coo_dup.nnz)  # 1 (after summing duplicates)
print(coo_dup)
# <COOrdinate sparse array of dtype 'int64'
#         with 1 stored elements and shape (2, 2)>
#   Coords        Values
#   (0, 0)        6


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 2. CSR (Compressed Sparse Row) Format --------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
CSR format stores:
- data: array of non-zero values (in row-major order)
- indices: array of column indices
- indptr: array of row pointer (where each row starts)

Best for:
- Arithmetic operations
- Matrix-vector multiplication
- Row slicing
- Most numerical computations

Default format for many scipy.sparse functions
'''

##########################
## Method 1: From dense ##
##########################

csr = csr_array(dense)
print("\n--- CSR Format ---")
print(csr)
# <Compressed Sparse Row sparse array of dtype 'int64'
#         with 5 stored elements and shape (3, 4)>
#   Coords        Values
#   (0, 0)        1
#   (0, 3)        2
#   (1, 1)        4
#   (1, 2)        1
#   (2, 2)        5

########################
## Method 2: From COO ##
########################

csr_from_coo = coo.tocsr()
print("\nCSR from COO:")
print(csr_from_coo)
# <Compressed Sparse Row sparse array of dtype 'int64'
#         with 5 stored elements and shape (3, 4)>
#   Coords        Values
#   (0, 0)        1
#   (0, 3)        2
#   (1, 1)        4
#   (1, 2)        1
#   (2, 2)        5

#######################################
## Method 3: From (data, (row, col)) ##
#######################################

csr_from_coords = csr_array((data, (row, col)), shape=(3, 4))
print("\nCSR from coordinates:")
print(csr_from_coords.toarray())
# [[1 0 0 2]
#  [0 4 1 0]
#  [0 0 5 0]]
# Dense representation

############################
## CSR internal structure ##
############################

print("\nCSR internal structure:")
print("Data array:", csr.data) # [1 2 4 1 5]
print("Column indices:", csr.indices) # [0 3 1 2 2]
print("Row pointers:", csr.indptr) # [0 2 4 5]

'''
indptr[i]:indptr[i+1] gives the slice for row i
Example: Row 0 uses data[indptr[0]:indptr[1]]
'''

###########################
## CSR supports indexing ##
###########################

print("\nIndexing CSR array:")
print("Element at (1, 1):", csr[1, 1])  # 4
print("Element at (0, 2):", csr[0, 2])  # 0

##########################
## CSR supports slicing ##
##########################

print("\nRow slicing:")
print("Row 1:", csr[1, :].toarray())  # [[0 4 1 0]]
print("Column 2:", csr[:, 2].toarray())  # [[0] [1] [5]]


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 3. CSC (Compressed Sparse Column) Format -----------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
CSC format is the column-oriented version of CSR
Stores:
- data: array of non-zero values (in column-major order)
- indices: array of row indices
- indptr: array of column pointers

Best for:
- Column-based operations
- Column slicing
- Some linear algebra operations prefer CSC
'''

######################
## Create CSC array ##
######################

csc = csc_array(dense)
print("\n--- CSC Format ---")
print(csc)
# <Compressed Sparse Column sparse array of dtype 'int64'
#         with 5 stored elements and shape (3, 4)>
#   Coords        Values
#   (0, 0)        1
#   (1, 1)        4
#   (1, 2)        1
#   (2, 2)        5
#   (0, 3)        2

############################
## CSC internal structure ##
############################

print("\nCSC internal structure:")
print("Data array:", csc.data) # 1 4 1 5 2]
print("Row indices:", csc.indices) # [0 1 1 2 0]
print("Column pointers:", csc.indptr) # [0 1 2 4 5]

#####################################
## CSC efficient column operations ##
#####################################

print("\nColumn slicing (efficient in CSC):")
print("Column 1:", csc[:, 1].toarray().ravel())  # [0 4 0]
print("Column 2:", csc[:, 2].toarray().ravel())  # [0 1 5]


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 4. BSR (Block Sparse Row) Format -------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
BSR format is for sparse arrays that consist of dense sub-blocks
Useful in finite element analysis and structured problems

Stores:
- data: 3D array of dense blocks
- indices: column indices of blocks
- indptr: row pointers for blocks
- blocksize: size of each dense block
'''

# Create an array with 2x2 blocks
dense_block = np.array([[1, 2, 0, 0],
                        [3, 4, 0, 0],
                        [0, 0, 5, 6],
                        [0, 0, 7, 8]])

bsr = bsr_array(dense_block, blocksize=(2, 2))

print("\n--- BSR Format ---")
print(bsr)
# <Block Sparse Row sparse array of dtype 'int64'
#         with 8 stored elements (blocksize=2x2) and shape (4, 4)>
#   Coords        Values
#   (0, 0)        1
#   (0, 1)        2
#   (1, 0)        3
#   (1, 1)        4
#   (2, 2)        5
#   (2, 3)        6
#   (3, 2)        7
#   (3, 3)        8

print("Block size:", bsr.blocksize)
# (2, 2)

print("\nDense representation:")
print(bsr.toarray())
# [[1 2 0 0]
#  [3 4 0 0]
#  [0 0 5 6]
#  [0 0 7 8]]

print("\nBSR data (blocks):")
print(bsr.data)
# [[[1 2]
#   [3 4]]

#  [[5 6]
#   [7 8]]]


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 5. DIA (Diagonal) Format ---------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
DIA format stores values along diagonals
Very efficient for diagonal or band matrices

Stores:
- data: 2D array where each row is a diagonal
- offsets: diagonal offsets from main diagonal
  - offset 0: main diagonal
  - positive offsets: above main diagonal
  - negative offsets: below main diagonal

Best for:
- Diagonal matrices
- Band matrices
- Very memory efficient

Limitations:
- Cannot be indexed or sliced
- Limited operations
'''

# Create a simple diagonal matrix
dense_diag = np.array([[1, 2, 0],
                       [0, 3, 4],
                       [0, 0, 5]])

dia = dia_array(dense_diag)

print("\n--- DIA Format ---")
print(dia)
# <DIAgonal sparse array of dtype 'int64'
#         with 5 stored elements (2 diagonals) and shape (3, 3)>
#   Coords        Values
#   (0, 0)        1
#   (1, 1)        3
#   (2, 2)        5
#   (0, 1)        2
#   (1, 2)        4

print("Diagonal data:\n", dia.data)
#  [[1 3 5]
#  [0 2 4]]

print("Diagonal offsets:", dia.offsets) # [0 1] (This means main diagonal and one above)

# Create DIA from scratch
diagonals = np.array([[1, 2, 3],     # Main diagonal
                      [4, 5, 0]])     # Upper diagonal
offsets = np.array([0, 1])

dia_custom = dia_array((diagonals, offsets), shape=(3, 3))
print("\nCustom DIA matrix:")
print(dia_custom.toarray())
# [[1 4 0]
#  [0 2 5]
#  [0 0 3]]

# Try indexing (will fail)
try:
    element = dia[0, 0]
except TypeError as e:
    print(f"\nDIA indexing error: {e}")


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 6. DOK (Dictionary of Keys) Format -----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
DOK format uses a dictionary to store non-zero elements
Keys are (row, col) tuples, values are the elements

Best for:
- Incremental construction
- Single element access
- Changing sparsity pattern

Convert to CSR/CSC for arithmetic
'''

######################
## Create DOK array ##
######################

dok = dok_array((3, 4), dtype=np.float64)
print("\n--- DOK Format ---")
print("Empty DOK array:", dok)
# Empty DOK array: <Dictionary Of Keys sparse array of dtype 'float64'
#         with 0 stored elements and shape (3, 4)>

#############################
## Add elements one by one ##
#############################

dok[0, 0] = 1
dok[0, 3] = 2
dok[1, 1] = 4
dok[1, 2] = 1
dok[2, 2] = 5

print("\nAfter adding elements:")
print(dok)
# <Dictionary Of Keys sparse array of dtype 'float64'
#         with 5 stored elements and shape (3, 4)>
#   Coords        Values
#   (0, 0)        1.0
#   (0, 3)        2.0
#   (1, 1)        4.0
#   (1, 2)        1.0
#   (2, 2)        5.0

print("\nDense representation:")
print(dok.toarray())
# [[1. 0. 0. 2.]
#  [0. 4. 1. 0.]
#  [0. 0. 5. 0.]]

####################
## Element access ##
####################

print("\nElement access:")
print("dok[1, 1] =", dok[1, 1])  # 4.0
print("dok[0, 2] =", dok[0, 2])  # 0.0

#######################
## Dictionary access ##
#######################

print("\nAs dictionary:")
print("Keys (positions):", list(dok.keys())) # [(0, 0), (0, 3), (1, 1), (1, 2), (2, 2)]
print("Values:", list(dok.values())) # [np.float64(1.0), np.float64(2.0), np.float64(4.0), np.float64(1.0), np.float64(5.0)]


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 7. LIL (List of Lists) Format ----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
LIL format stores:
- rows: list of lists (one list per row)
- data: list of lists (data for each row)

Best for:
- Incremental construction by rows
- Changing sparse structure
- Row-based modifications

Convert to CSR for arithmetic
'''

######################
## Create LIL array ##
######################

lil = lil_array((3, 4), dtype=np.float64)
print("\n--- LIL Format ---")
print("Empty LIL array:", lil)
# Empty LIL array: <List of Lists sparse array of dtype 'float64'
#         with 0 stored elements and shape (3, 4)>

##################
## Add elements ##
##################

lil[0, 0] = 1
lil[0, 3] = 2
lil[1, 1:3] = [4, 1]  # Efficient row slicing
lil[2, 2] = 5

print("\nAfter adding elements:")
print(lil)
# <List of Lists sparse array of dtype 'float64'
#         with 5 stored elements and shape (3, 4)>
#   Coords        Values
#   (0, 0)        1.0
#   (0, 3)        2.0
#   (1, 1)        4.0
#   (1, 2)        1.0
#   (2, 2)        5.0

print("\nDense representation:")
print(lil.toarray())
# [[1. 0. 0. 2.]
#  [0. 4. 1. 0.]
#  [0. 0. 5. 0.]]

############################
## LIL internal structure ##
############################

print("\nLIL internal structure:")
print("Rows (column indices):", lil.rows) # [list([0, 3]) list([1, 2]) list([2])]
print("Data (values):", lil.data) # [list([np.float64(1.0), np.float64(2.0)]) list([4.0, 1.0]) list([np.float64(5.0)])]

##########################
## Row-based operations ##
##########################

print("\nRow slicing:")
print("Row 1:", lil[1, :].toarray()) # [0. 4. 1. 0.]


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 8. Format Comparison Summary -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

print("\n" + "="*80)
print("FORMAT COMPARISON SUMMARY")
print("="*80)

formats = {
    'COO': coo,
    'CSR': csr,
    'CSC': csc,
    'DOK': dok,
    'LIL': lil
}

for name, arr in formats.items():
    print(f"\n{name} Format:")
    print(f"  Type: {type(arr)}")
    print(f"  Stored elements: {arr.nnz}")
    print(f"  Supports indexing: {hasattr(arr, '__getitem__') and name not in ['COO']}")

# COO Format:
#   Type: <class 'scipy.sparse._coo.coo_array'>
#   Stored elements: 5
#   Supports indexing: False

# CSR Format:
#   Type: <class 'scipy.sparse._csr.csr_array'>
#   Stored elements: 5
#   Supports indexing: True

# CSC Format:
#   Type: <class 'scipy.sparse._csc.csc_array'>
#   Stored elements: 5
#   Supports indexing: True

# DOK Format:
#   Type: <class 'scipy.sparse._dok.dok_array'>
#   Stored elements: 5
#   Supports indexing: True

# LIL Format:
#   Type: <class 'scipy.sparse._lil.lil_array'>
#   Stored elements: 5
#   Supports indexing: True

print("\n" + "="*80)
print("WHEN TO USE EACH FORMAT:")
print("="*80)
print("COO: Initial construction, format conversion")
print("CSR: Arithmetic, row operations, matrix-vector products (MOST COMMON)")
print("CSC: Arithmetic, column operations")
print("BSR: Block-structured matrices")
print("DIA: Diagonal/band matrices")
print("DOK: Incremental element-by-element construction")
print("LIL: Incremental row-by-row construction")
print("="*80)

print("\nNext: Learn how to build sparse arrays in 03_Building_Sparse_Arrays.py")
