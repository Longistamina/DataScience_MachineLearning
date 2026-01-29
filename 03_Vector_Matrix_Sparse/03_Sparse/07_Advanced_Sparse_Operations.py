'''
scipy.sparse - Advanced Sparse Operations

1. Canonical Formats and Duplicates:
   + has_canonical_format: Check if in canonical form
   + sum_duplicates(): Sum duplicate entries
   + Sorted indices and efficiency

2. Zero Management:
   + eliminate_zeros(): Remove explicit zeros
   + prune(): Remove small entries
   + nnz vs count_nonzero()

3. Reshape and Transpose:
   + reshape(): Change dimensions
   + transpose() and .T: Matrix transpose
   + Efficiency considerations

4. Graph Algorithms:
   + connected_components(): Find connected components
   + shortest_path(): Compute shortest paths
   + minimum_spanning_tree(): Find MST
   + Graph traversals

5. Saving and Loading:
   + save_npz() and load_npz(): NumPy compressed format
   + mmwrite() and mmread(): Matrix Market format
   + pickle: General Python serialization

6. Advanced Construction:
   + bmat(): Block matrix construction
   + kronecker products: kron()
   + Tensor products

7. Performance Optimization:
   + Format conversion strategy
   + Memory management
   + Parallel operations
   + Best practices for large-scale problems

'''

import numpy as np
from scipy import sparse
from scipy.sparse import (csr_array, csc_array, coo_array, lil_array,
                          diags_array, eye_array, random_array)
from scipy.sparse.csgraph import (connected_components, shortest_path,
                                  minimum_spanning_tree, depth_first_order,
                                  breadth_first_order)
import os
import pickle

#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 1. Canonical Formats and Duplicates ----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

##########################
## Canonical format
##########################

'''
Canonical format requirements:
- No duplicate entries
- Sorted indices
- No explicit zeros

Formats with canonical form: COO, CSR, CSC, BSR
'''

print("--- Canonical Formats ---")

# Create COO with duplicates
row = np.array([0, 0, 1, 1, 0])  # Note: (0,0) appears twice
col = np.array([0, 0, 1, 2, 0])
data = np.array([1, 2, 3, 4, 5])

coo_dup = coo_array((data, (row, col)), shape=(3, 3))

print("COO array with duplicates:")
print(f"Stored elements: {coo_dup.nnz}")
print(f"Has canonical format: {coo_dup.has_canonical_format}")
print("Dense representation (duplicates summed):")
print(coo_dup.toarray())
# [[8 0 0]    <- 1+2+5=8 at position (0,0)
#  [0 3 4]
#  [0 0 0]]

##########################
## sum_duplicates()
##########################

'''
Sum duplicate entries in-place
Changes array to canonical format
'''

print("\n--- sum_duplicates() ---")

coo_dup.sum_duplicates()
print(f"After sum_duplicates():")
print(f"Stored elements: {coo_dup.nnz}")
print(f"Has canonical format: {coo_dup.has_canonical_format}")

# Access internal arrays
print(f"\nInternal structure:")
print(f"Row indices: {coo_dup.row}")
print(f"Col indices: {coo_dup.col}")
print(f"Data values: {coo_dup.data}")

##########################
## Sorted indices
##########################

'''
Canonical format has sorted indices
Important for efficient operations
'''

print("\n--- Sorted Indices ---")

# Unsorted COO
row_unsorted = [2, 0, 1, 0]
col_unsorted = [1, 2, 0, 0]
data_unsorted = [1, 2, 3, 4]

coo_unsorted = coo_array((data_unsorted, (row_unsorted, col_unsorted)), 
                         shape=(3, 3))

print(f"Unsorted COO canonical format: {coo_unsorted.has_canonical_format}")

# Convert to CSR (automatically sorts)
csr_sorted = coo_unsorted.tocsr()
print(f"\nCSR (auto-sorted) canonical format: {csr_sorted.has_canonical_format}")

# Check CSR structure
print(f"CSR indices: {csr_sorted.indices}")
print(f"CSR indptr: {csr_sorted.indptr}")

#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 2. Zero Management ---------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

##########################
## eliminate_zeros()
##########################

'''
Remove explicit zeros from sparse array
Reduces memory and improves performance
Operates in-place
'''

print("\n--- eliminate_zeros() ---")

# Create array with explicit zeros
row_zero = [0, 0, 1, 1, 2]
col_zero = [0, 1, 1, 2, 2]
data_zero = [1, 0, 2, 0, 3]  # Two explicit zeros

csr_zeros = csr_array((data_zero, (row_zero, col_zero)), shape=(3, 3))

print("Before eliminate_zeros():")
print(f"Stored elements: {csr_zeros.nnz}")
print(f"Non-zero elements: {csr_zeros.count_nonzero()}")
print("Matrix:")
print(csr_zeros.toarray())

csr_zeros.eliminate_zeros()

print("\nAfter eliminate_zeros():")
print(f"Stored elements: {csr_zeros.nnz}")
print("Matrix (unchanged):")
print(csr_zeros.toarray())

##########################
## prune()
##########################

'''
Remove entries smaller than threshold
Useful for removing numerical noise
'''

print("\n--- prune(): Remove Small Entries ---")

# Array with small values
A_small = csr_array([[1.0, 1e-10, 2.0],
                     [1e-9, 3.0, 1e-8],
                     [4.0, 1e-7, 5.0]])

print("Original matrix:")
print(A_small.toarray())
print(f"Stored elements: {A_small.nnz}")

# Prune values below 1e-6
A_pruned = A_small.copy()
A_pruned.data[np.abs(A_pruned.data) < 1e-6] = 0
A_pruned.eliminate_zeros()

print("\nAfter pruning (threshold=1e-6):")
print(A_pruned.toarray())
print(f"Stored elements: {A_pruned.nnz}")

##########################
## nnz vs count_nonzero()
##########################

'''
nnz: number of stored elements (including explicit zeros)
count_nonzero(): actual non-zero elements
'''

print("\n--- nnz vs count_nonzero() ---")

A_compare = csr_array([[1, 0, 2],
                       [0, 0, 0],
                       [3, 0, 4]])

print("Matrix:")
print(A_compare.toarray())
print(f"nnz (stored): {A_compare.nnz}")
print(f"count_nonzero(): {A_compare.count_nonzero()}")

# Add explicit zero
A_explicit = A_compare.copy()
A_explicit[0, 1] = 1
A_explicit[0, 1] = 0  # Now (0,1) might be explicit zero

print(f"\nAfter setting A[0,1]=1 then A[0,1]=0:")
print(f"nnz (stored): {A_explicit.nnz}")
print(f"count_nonzero(): {A_explicit.count_nonzero()}")

#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 3. Reshape and Transpose ---------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

##########################
## Reshape
##########################

'''
Reshape sparse arrays
Must preserve total number of elements
May change sparsity pattern
'''

print("\n--- reshape(): Reshape Sparse Arrays ---")

A_reshape = csr_array([[1, 0, 2, 0],
                       [0, 3, 0, 4],
                       [5, 0, 6, 0]])

print("Original (3x4):")
print(A_reshape.toarray())
print(f"Shape: {A_reshape.shape}")

# Reshape to 2x6
A_reshaped = A_reshape.reshape((2, 6))
print("\nReshaped to (2x6):")
print(A_reshaped.toarray())
print(f"Shape: {A_reshaped.shape}")

# Reshape to 6x2
A_reshaped2 = A_reshape.reshape((6, 2))
print("\nReshaped to (6x2):")
print(A_reshaped2.toarray())

# Can also reshape to 1D (not common)
A_flat = A_reshape.reshape((-1,))
print(f"\nFlattened shape: {A_flat.shape}")

##########################
## Transpose
##########################

'''
Transpose: swap rows and columns
Very efficient in sparse formats
CSR.T -> CSC (just view, no copy)
'''

print("\n--- transpose() and .T ---")

A_trans = csr_array([[1, 0, 2],
                     [0, 3, 0],
                     [4, 0, 5]])

print("Original CSR:")
print(A_trans.toarray())
print(f"Type: {type(A_trans)}")

# Transpose
A_T = A_trans.T
print("\nTranspose (.T):")
print(A_T.toarray())
print(f"Type: {type(A_T)}")  # CSR -> CSC

# Transpose back
A_TT = A_T.T
print("\nDouble transpose (.T.T):")
print(A_TT.toarray())
print(f"Type: {type(A_TT)}")  # CSC -> CSR

# Using transpose() method
A_transpose = A_trans.transpose()
print(f"\nUsing .transpose() method: {type(A_transpose)}")

##########################
## Conjugate transpose
##########################

'''
For complex matrices
.H or .conj().T
'''

print("\n--- Conjugate Transpose ---")

A_complex = csr_array([[1+2j, 0],
                       [3-1j, 4+0j]])

print("Complex matrix:")
print(A_complex.toarray())

A_H = A_complex.conj().T
print("\nConjugate transpose:")
print(A_H.toarray())

#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 4. Graph Algorithms --------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

##########################
## connected_components()
##########################

'''
Find connected components in a graph
Graph represented as sparse adjacency matrix
'''

print("\n--- connected_components(): Graph Components ---")

# Create graph with 2 components
adjacency = csr_array([[0, 1, 1, 0, 0, 0],
                       [1, 0, 1, 0, 0, 0],
                       [1, 1, 0, 0, 0, 0],
                       [0, 0, 0, 0, 1, 1],
                       [0, 0, 0, 1, 0, 1],
                       [0, 0, 0, 1, 1, 0]])

print("Adjacency matrix:")
print(adjacency.toarray())

n_components, labels = connected_components(adjacency, directed=False)

print(f"\nNumber of components: {n_components}")
print(f"Component labels: {labels}")
print("Component 0: nodes", np.where(labels == 0)[0])
print("Component 1: nodes", np.where(labels == 1)[0])

##########################
## shortest_path()
##########################

'''
Compute shortest paths between all pairs of nodes
Various algorithms: Dijkstra, Bellman-Ford, Floyd-Warshall
'''

print("\n--- shortest_path(): Shortest Paths ---")

# Weighted graph
weights = csr_array([[0, 4, 0, 0, 0, 0, 0, 8, 0],
                     [4, 0, 8, 0, 0, 0, 0, 11, 0],
                     [0, 8, 0, 7, 0, 4, 0, 0, 2],
                     [0, 0, 7, 0, 9, 14, 0, 0, 0],
                     [0, 0, 0, 9, 0, 10, 0, 0, 0],
                     [0, 0, 4, 14, 10, 0, 2, 0, 0],
                     [0, 0, 0, 0, 0, 2, 0, 1, 6],
                     [8, 11, 0, 0, 0, 0, 1, 0, 7],
                     [0, 0, 2, 0, 0, 0, 6, 7, 0]], dtype=float)

# Replace 0 with inf (except diagonal)
weights_inf = weights.toarray().astype(float)
weights_inf[weights_inf == 0] = np.inf
np.fill_diagonal(weights_inf, 0)
weights_graph = csr_array(weights_inf)

# Compute shortest paths from node 0
dist_matrix, predecessors = shortest_path(weights_graph, 
                                          method='auto',
                                          directed=False,
                                          return_predecessors=True,
                                          indices=0)

print("Shortest distances from node 0:")
print(dist_matrix.round(1))

# Get path from 0 to 4
def get_path(predecessors, start, end):
    path = [end]
    while path[-1] != start:
        path.append(predecessors[path[-1]])
    return path[::-1]

path_0_to_4 = get_path(predecessors, 0, 4)
print(f"\nPath from 0 to 4: {path_0_to_4}")
print(f"Distance: {dist_matrix[4]:.1f}")

##########################
## minimum_spanning_tree()
##########################

'''
Find minimum spanning tree
Connects all nodes with minimum total edge weight
'''

print("\n--- minimum_spanning_tree(): MST ---")

# Use same weighted graph
mst = minimum_spanning_tree(weights)

print("Original graph edges (non-zero):", weights.nnz // 2)  # Undirected
print("MST edges:", mst.nnz // 2)
print(f"MST total weight: {mst.sum() / 2:.0f}")  # Divide by 2 for undirected

print("\nMST adjacency:")
print(mst.toarray())

##########################
## depth_first_order() and breadth_first_order()
##########################

'''
Graph traversal orders
Useful for tree algorithms
'''

print("\n--- Graph Traversals ---")

# Simple tree
tree = csr_array([[0, 1, 1, 0, 0],
                  [0, 0, 0, 1, 1],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0]])

print("Tree adjacency (directed):")
print(tree.toarray())

# Depth-first order from root 0
dfs_order, dfs_predecessors = depth_first_order(tree, 0, directed=True)
print(f"\nDepth-first order: {dfs_order}")

# Breadth-first order from root 0
bfs_order, bfs_predecessors = breadth_first_order(tree, 0, directed=True)
print(f"Breadth-first order: {bfs_order}")

#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 5. Saving and Loading ------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

##########################
## save_npz() and load_npz()
##########################

'''
Save to NumPy compressed format (.npz)
Efficient, preserves format and dtype
'''

print("\n--- save_npz() and load_npz(): NumPy Format ---")

# Create sparse array to save
A_save = random_array((100, 100), density=0.1, format='csr', random_state=42)

print(f"Original matrix: {A_save.shape}, nnz={A_save.nnz}")

# Save
filename_npz = 'sparse_matrix.npz'
sparse.save_npz(filename_npz, A_save)

print(f"Saved to {filename_npz}")

# Load
A_loaded = sparse.load_npz(filename_npz)

print(f"\nLoaded matrix: {A_loaded.shape}, nnz={A_loaded.nnz}")
print(f"Format: {type(A_loaded)}")
print(f"Matrices equal: {np.allclose(A_save.toarray(), A_loaded.toarray())}")

# Cleanup
os.remove(filename_npz)
print(f"Cleaned up {filename_npz}")

##########################
## Matrix Market format
##########################

'''
Save/load in Matrix Market format (.mtx)
Portable text format
Compatible with other software (MATLAB, etc.)
'''

print("\n--- Matrix Market Format (.mtx) ---")

from scipy.io import mmwrite, mmread

A_mm = csr_array([[1, 0, 2],
                  [0, 3, 0],
                  [4, 0, 5]])

filename_mtx = 'sparse_matrix.mtx'

# Save
mmwrite(filename_mtx, A_mm)
print(f"Saved to {filename_mtx}")

# Load
A_mm_loaded = mmread(filename_mtx)

print(f"Loaded matrix: {A_mm_loaded.shape}")
print("Matrix content:")
print(A_mm_loaded.toarray())

# Cleanup
os.remove(filename_mtx)
print(f"\nCleaned up {filename_mtx}")

##########################
## Pickle (general serialization)
##########################

'''
Use pickle for general Python serialization
Can save multiple arrays in one file
'''

print("\n--- Pickle Serialization ---")

A_pickle = csr_array([[1, 2], [3, 4]])
B_pickle = csc_array([[5, 6], [7, 8]])

filename_pkl = 'sparse_matrices.pkl'

# Save multiple arrays
with open(filename_pkl, 'wb') as f:
    pickle.dump({'A': A_pickle, 'B': B_pickle}, f)

print(f"Saved to {filename_pkl}")

# Load
with open(filename_pkl, 'rb') as f:
    data = pickle.load(f)

print(f"Loaded {len(data)} matrices")
print("A:", data['A'].toarray())
print("B:", data['B'].toarray())

# Cleanup
os.remove(filename_pkl)
print(f"\nCleaned up {filename_pkl}")

#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 6. Advanced Construction ---------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

##########################
## bmat() - Block matrix
##########################

'''
Create block matrix from 2D list
More flexible than block_array
'''

print("\n--- bmat(): Block Matrix Construction ---")

A = csr_array([[1, 2], [3, 4]])
B = csr_array([[5], [6]])
C = csr_array([[7, 8]])
D = csr_array([[9]])

# Create block matrix using bmat
block = sparse.bmat([[A, B],
                     [C, D]], format='csr')

print("Block matrix:")
print(block.toarray())
# [[1 2 5]
#  [3 4 6]
#  [7 8 9]]

# With None for zero blocks
block_diag = sparse.bmat([[A, None],
                          [None, A]], format='csr')

print("\nBlock diagonal:")
print(block_diag.toarray())

##########################
## kron() - Kronecker product
##########################

'''
Kronecker (tensor) product of two sparse arrays
Useful in FEM, quantum mechanics, etc.
'''

print("\n--- kron(): Kronecker Product ---")

A_kron = csr_array([[1, 2], [3, 4]])
B_kron = csr_array([[0, 5], [6, 0]])

# A ⊗ B
kron_prod = sparse.kron(A_kron, B_kron, format='csr')

print("A:")
print(A_kron.toarray())
print("\nB:")
print(B_kron.toarray())
print("\nA ⊗ B:")
print(kron_prod.toarray())
print(f"Shape: {A_kron.shape} ⊗ {B_kron.shape} = {kron_prod.shape}")

##########################
## Practical: 2D Laplacian via Kronecker
##########################

'''
Build 2D Laplacian using Kronecker products
Common in numerical PDEs
'''

print("\n--- 2D Laplacian using Kronecker ---")

n = 5  # Small for visualization
I = eye_array(n, format='csr')
D2 = diags_array([np.ones(n-1), -2*np.ones(n), np.ones(n-1)],
                 offsets=[-1, 0, 1], format='csr')

# 2D Laplacian = I ⊗ D2 + D2 ⊗ I
Laplacian_2D = sparse.kron(I, D2) + sparse.kron(D2, I)

print(f"2D Laplacian for {n}x{n} grid")
print(f"Shape: {Laplacian_2D.shape}")
print(f"Non-zeros: {Laplacian_2D.nnz}")
print(f"Sparsity: {100 * Laplacian_2D.nnz / (n**4):.1f}%")

#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 7. Performance Optimization ------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

##########################
## Format conversion strategy
##########################

'''
Choose format based on operation
Convert strategically to minimize overhead
'''

print("\n--- Performance Optimization ---")
print("\nFormat Conversion Strategy:")
print("1. Build in COO, DOK, or LIL (flexible)")
print("2. Convert to CSR for arithmetic and row operations")
print("3. Convert to CSC for column operations")
print("4. Reuse same format for multiple operations")

##########################
## Memory management
##########################

'''
Monitor memory usage
Use appropriate dtypes
'''

print("\n--- Memory Management ---")

# Compare memory usage of different dtypes
n = 1000
density = 0.01

A_float64 = random_array((n, n), density=density, dtype=np.float64, random_state=42)
A_float32 = random_array((n, n), density=density, dtype=np.float32, random_state=42)
A_int32 = random_array((n, n), density=density, dtype=np.int32, random_state=42)

# Approximate memory
mem_64 = A_float64.data.nbytes + A_float64.indices.nbytes + A_float64.indptr.nbytes
mem_32 = A_float32.data.nbytes + A_float32.indices.nbytes + A_float32.indptr.nbytes
mem_int = A_int32.data.nbytes + A_int32.indices.nbytes + A_int32.indptr.nbytes

print(f"Float64 memory: {mem_64/1024:.1f} KB")
print(f"Float32 memory: {mem_32/1024:.1f} KB")
print(f"Int32 memory: {mem_int/1024:.1f} KB")
print(f"\nMemory savings (float32 vs float64): {100*(1-mem_32/mem_64):.0f}%")

##########################
## Best practices summary
##########################

print("\n--- Best Practices Summary ---")
print("""
1. FORMAT SELECTION:
   - COO/DOK/LIL for construction
   - CSR for row operations and arithmetic
   - CSC for column operations

2. MEMORY EFFICIENCY:
   - Use eliminate_zeros() after modifications
   - Use sum_duplicates() for canonical form
   - Choose appropriate dtype
   - Prune small values if acceptable

3. COMPUTATIONAL EFFICIENCY:
   - Convert to CSR/CSC before loops
   - Use vectorized operations
   - Reuse factorizations for multiple solves
   - Use iterative solvers for large systems

4. NUMERICAL STABILITY:
   - Use preconditioners with iterative solvers
   - Monitor condition numbers
   - Check residuals after solving

5. LARGE-SCALE PROBLEMS:
   - Use matrix-free methods (LinearOperator)
   - Consider ILU preconditioning
   - Use iterative eigensolvers (eigsh, eigs)
   - Save/load with save_npz for efficiency
""")

##########################
## Example: Optimized workflow
##########################

print("\n--- Example: Optimized Workflow ---")

# 1. Build in LIL (fast construction)
n = 100
A_workflow = lil_array((n, n), dtype=np.float32)

# Add elements
for i in range(n):
    A_workflow[i, i] = 2.0
    if i > 0:
        A_workflow[i, i-1] = -1.0
    if i < n-1:
        A_workflow[i, i+1] = -1.0

print(f"1. Built in LIL: {A_workflow.nnz} non-zeros")

# 2. Convert to CSR (for computation)
A_workflow = A_workflow.tocsr()
print(f"2. Converted to CSR")

# 3. Eliminate zeros and sum duplicates
A_workflow.eliminate_zeros()
A_workflow.sum_duplicates()
print(f"3. Cleaned: {A_workflow.nnz} non-zeros")

# 4. Perform computation
b_workflow = np.ones(n, dtype=np.float32)
from scipy.sparse.linalg import spsolve
x_workflow = spsolve(A_workflow, b_workflow)

print(f"4. Solved linear system")
print(f"5. Solution range: [{x_workflow.min():.2f}, {x_workflow.max():.2f}]")

print("\n" + "="*80)
print("Congratulations! You have completed the scipy.sparse tutorial series.")
print("You now have comprehensive knowledge of sparse arrays in SciPy.")
print("="*80)
