'''
scipy.sparse - Introduction to Sparse Arrays

1. What are Sparse Arrays?
   + Arrays where most elements are zero (or empty)
   + Only store non-zero elements explicitly
   + Implicit zeros are not stored, saving memory
   + Useful for large arrays with few non-zero values

2. Basic Sparse Array Creation:
   + Creating from dense arrays
   + Basic properties: shape, dtype, nnz (number of non-zero elements)
   + Converting back to dense arrays: .toarray() or .todense()

3. Understanding Stored vs Implicit Elements:
   + Stored elements: explicitly recorded values (including explicit zeros)
   + Implicit zeros: zeros not stored in memory
   + Methods: .nnz, .count_nonzero()

4. Simple Operations:
   + Basic reductions: .max(), .min(), .sum(), .mean()
   + These work similarly to dense arrays
'''

import numpy as np
from scipy.sparse import csr_array, coo_array


# =========================================================================================
# 1. What are Sparse Arrays?
# =========================================================================================
'''
Sparse arrays are special arrays where most locations contain zeros.
Instead of storing all values (including zeros), sparse arrays only store non-zero values
along with their positions, resulting in significant memory savings.

Example: A 1000x1000 array with only 50 non-zero values
- Dense storage: 1,000,000 elements
- Sparse storage: ~50 elements + position information
'''

# Create a dense array with mostly zeros
dense = np.array([[1, 0, 0, 2],
                  [0, 4, 1, 0],
                  [0, 0, 5, 0]])

print(dense)
# [[1 0 0 2]
#  [0 4 1 0]
#  [0 0 5 0]]

print("\nNumber of total elements:", dense.size)  # 12
print("Number of non-zero elements:", np.count_nonzero(dense))  # 5
print("Percentage of non-zeros: {:.1f}%".format(100 * np.count_nonzero(dense) / dense.size))  # 41.7%


# =========================================================================================
# 2. Basic Sparse Array Creation from Dense Arrays
# =========================================================================================

##-------------------------------##
## Create COO (Coordinate) array ##
##-------------------------------##
'''
COO (Coordinate) format is one of the simplest sparse formats.
It stores row indices, column indices, and data values separately.
'''

sparse_coo = coo_array(dense)
print("\nSparse COO array:")
print(sparse_coo)
# <COOrdinate sparse array of dtype 'int64'
#  with 5 stored elements and shape (3, 4)>
#   Coords        Values
#   (0, 0)        1
#   (0, 3)        2
#   (1, 1)        4
#   (1, 2)        1
#   (2, 2)        5

##------------------------------------##
## Create CSR (Compressed Sparse Row) ##
##------------------------------------##
'''
CSR format is optimized for row-based operations and arithmetic.
It's the most commonly used format for numerical computations.
'''

sparse_csr = csr_array(dense)
print("\nSparse CSR array:")
print(sparse_csr)
# <Compressed Sparse Row sparse array of dtype 'int64'
#  with 5 stored elements and shape (3, 4)>
#   Coords        Values
#   (0, 0)        1
#   (0, 3)        2
#   (1, 1)        4
#   (1, 2)        1
#   (2, 2)        5

##-------------------------##
## Basic sparse properties ##
##-------------------------##

print("\n--- Sparse Array Properties ---")
print("Shape:", sparse_csr.shape)  # (3, 4)
print("Data type:", sparse_csr.dtype)  # int64
print("Number of stored elements (.nnz):", sparse_csr.nnz)  # 5
print("Number of dimensions:", sparse_csr.ndim)  # 2


# =========================================================================================
# 3. Converting Back to Dense Arrays
# =========================================================================================

##------------------##
## Using .toarray() ##
##------------------##
'''
.toarray() returns a NumPy ndarray
This is the preferred method for getting a dense array
'''

dense_from_sparse = sparse_csr.toarray()
print("\nConverted back to dense (using .toarray()):")
print(dense_from_sparse)
# [[1 0 0 2]
#  [0 4 1 0]
#  [0 0 5 0]]

print("Type:", type(dense_from_sparse))  # <class 'numpy.ndarray'>


# =========================================================================================
# 4. Understanding Stored vs Implicit Elements
# =========================================================================================
'''
Sparse arrays distinguish between:
- Implicit zeros: zeros not stored in memory (most zeros)
- Explicit zeros: zeros that are actually stored
- Non-zero values: all other values
'''

# Create array with an explicit zero
row = [0, 0, 1, 1, 2, 2]
col = [0, 3, 1, 2, 2, 3]
data = [1, 2, 4, 1, 5, 0]  # Note: last element is 0

sparse_with_explicit_zero = csr_array((data, (row, col)))
print("\n--- Explicit vs Implicit Zeros ---")
print("Sparse array with explicit zero:")
print(sparse_with_explicit_zero)
# <Compressed Sparse Row sparse array of dtype 'int64'
#  with 6 stored elements and shape (3, 4)>
#   Coords        Values
#   (0, 0)        1
#   (0, 3)        2
#   (1, 1)        4
#   (1, 2)        1
#   (2, 2)        5
#   (2, 3)        0

print("Number of stored elements (.nnz):", sparse_with_explicit_zero.nnz)  # 6 (includes explicit zero)
print("Number of non-zero elements (.count_nonzero()):", sparse_with_explicit_zero.count_nonzero())  # 5

print("\nDense representation:")
print(sparse_with_explicit_zero.toarray())
# [[1 0 0 2]
#  [0 4 1 0]
#  [0 0 5 0]]

##--------------------------##
## Eliminate explicit zeros ##
##--------------------------##
'''
Use .eliminate_zeros() to remove explicit zeros
This method modifies the array in-place
'''

print("\nBefore eliminating zeros - stored elements:", sparse_with_explicit_zero.nnz)  # 6

sparse_with_explicit_zero.eliminate_zeros()
print("After eliminating zeros - stored elements:", sparse_with_explicit_zero.nnz)  # 5


# =========================================================================================
# 5. Simple Operations on Sparse Arrays
# =========================================================================================
'''Most reduction operations work similarly on sparse and dense arrays'''

print("\n--- Basic Operations ---")

##----------------------##
## Reduction operations ##
##----------------------##

print("Maximum value (.max()):", sparse_csr.max())  # 5
print("Minimum value (.min()):", sparse_csr.min())  # 0
print("Sum of all elements (.sum()):", sparse_csr.sum())  # 13
print("Mean of all elements (.mean()):", sparse_csr.mean())  # 1.0833...

# Compare with dense array
print("\nDense array max:", dense.max())  # 5
print("Dense array sum:", dense.sum())  # 13

##-------------------##
## Argmax and Argmin ##
##-------------------##
'''
Returns the index of max/min in the flattened array
Works the same as with dense arrays
'''

print("\nArgmax (flattened index):", sparse_csr.argmax())  # 10
print("Dense argmax:", dense.argmax())  # 10

##-----------------------##
## Axis-based operations ##
##-----------------------##
'''Reductions over an axis return dense NumPy arrays'''

print("\nMean over axis 0 (column means):")
print(sparse_csr.mean(axis=0))
# [[0.33333333 1.33333333 0.5        0.66666667]]

print("\nMean over axis 1 (row means):")
print(sparse_csr.mean(axis=1))
# [0.75 1.25 1.25]

print("\nSum over axis 0 (column sums):")
print(sparse_csr.sum(axis=0))
# [1 4 6 2]


# =========================================================================================
# 6. Memory Efficiency Demonstration
# =========================================================================================
'''Sparse arrays are most beneficial for large arrays with low density'''

# Create a large sparse array
large_size = 1000
density = 0.01  # 1% non-zero

# Generate random sparse data
np.random.seed(42)
n_nonzero = int(large_size * large_size * density)
rows = np.random.randint(0, large_size, n_nonzero)
cols = np.random.randint(0, large_size, n_nonzero)
data = np.random.randn(n_nonzero)

large_sparse = csr_array((data, (rows, cols)), shape=(large_size, large_size))

print("\n--- Memory Efficiency ---")
print(f"Array shape: {large_sparse.shape}") # (1000, 1000)
print(f"Total elements: {large_sparse.shape[0] * large_sparse.shape[1]:,}") # 1,000,000
print(f"Stored elements: {large_sparse.nnz:,}") # 10,000
print(f"Density: {100 * large_sparse.nnz / (large_sparse.shape[0] * large_sparse.shape[1]):.2f}%") # 1.00%

# Memory comparison (approximate)
dense_memory_mb = large_sparse.toarray().nbytes / (1024**2)  # 8 bytes per float64
sparse_memory_mb = (large_sparse.data.nbytes + large_sparse.indices.nbytes + large_sparse.indptr.nbytes) / (1024**2)  # data + row + col indices

print(f"\nApproximate dense memory: {dense_memory_mb:.2f} MB") # 7.63 MB
print(f"Approximate sparse memory: {sparse_memory_mb:.2f} MB") # 0.16 MB
print(f"Memory savings: {100 * (1 - sparse_memory_mb/dense_memory_mb):.2f}%") # 97.91%
