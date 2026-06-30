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

5. Advanced Construction:
   + bmat(): Block matrix construction
   + kronecker products: kron()
   + Tensor products

6. Performance Optimization:
   + Format conversion strategy
   + Memory management
   + Parallel operations
   + Best practices for large-scale problems
'''

import numpy as np
from scipy import sparse
from scipy.sparse import (csr_array, coo_array, lil_array,
                          diags_array, eye_array, random_array)
from scipy.sparse.csgraph import (connected_components, shortest_path,
                                  minimum_spanning_tree, depth_first_order,
                                  breadth_first_order)



#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 1. Canonical Formats and Duplicates ----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

######################
## Canonical format ##
######################
'''
Canonical format requirements:
- No duplicate entries
- Sorted indices
- No explicit zeros

Formats with canonical form: COO, CSR, CSC, BSR
'''

# Create COO with duplicates
row = np.array([0, 0, 1, 1, 0])  # Note: (0,0) appears twice
col = np.array([0, 0, 1, 2, 0])
data = np.array([1, 2, 3, 4, 5])

coo_dup = coo_array((data, (row, col)), shape=(3, 3))

print("COO array with duplicates:")
print(f"Stored elements: {coo_dup.nnz}") # 5
print(f"Has canonical format: {coo_dup.has_canonical_format}") # False
print("Dense representation (duplicates summed):")
print(coo_dup.toarray())
# [[8 0 0]    <- 1+2+5=8 at position (0,0)
#  [0 3 4]
#  [0 0 0]]

######################
## sum_duplicates() ##
######################
'''
Sum duplicate entries in-place
Changes array to canonical format
'''

coo_dup.sum_duplicates()
print(f"After sum_duplicates():")
print(f"Stored elements: {coo_dup.nnz}") # 3
print(f"Has canonical format: {coo_dup.has_canonical_format}") # True

# Access internal arrays
print(f"\nInternal structure:")
print(f"Row indices: {coo_dup.row}") # [0 1 1]
print(f"Col indices: {coo_dup.col}") # [0 1 2]
print(f"Data values: {coo_dup.data}") # [8 3 4]

####################
## Sorted indices ##
####################
'''
Canonical format has sorted indices
Important for efficient operations
'''

# Unsorted COO
row_unsorted = [2, 0, 1, 0]
col_unsorted = [1, 2, 0, 0]
data_unsorted = [1, 2, 3, 4]

coo_unsorted = coo_array((data_unsorted, (row_unsorted, col_unsorted)),
                         shape=(3, 3))

print(f"Unsorted COO canonical format: {coo_unsorted.has_canonical_format}") # False

# Convert to CSR (automatically sorts)
csr_sorted = coo_unsorted.tocsr()
print(f"\nCSR (auto-sorted) canonical format: {csr_sorted.has_canonical_format}") # True

# Check CSR structure
print(f"CSR indices: {csr_sorted.indices}") # [0 2 0 1]
print(f"CSR indptr: {csr_sorted.indptr}")   # [0 2 3 4]


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 2. Zero Management -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

#######################
## eliminate_zeros() ##
#######################
'''
Remove explicit zeros from sparse array
Reduces memory and improves performance
Operates in-place
'''

# Create array with explicit zeros
row_zero = [0, 0, 1, 1, 2]
col_zero = [0, 1, 1, 2, 2]
data_zero = [1, 0, 2, 0, 3]  # Two explicit zeros

csr_zeros = csr_array((data_zero, (row_zero, col_zero)), shape=(3, 3))

print("Before eliminate_zeros():")
print(f"Stored elements: {csr_zeros.nnz}") # 5
print(f"Non-zero elements: {csr_zeros.count_nonzero()}") # 3
print("Matrix:")
print(csr_zeros.toarray())
# [[1 0 0]
#  [0 2 0]
#  [0 0 3]]

csr_zeros.eliminate_zeros()

print("\nAfter eliminate_zeros():")
print(f"Stored elements: {csr_zeros.nnz}") # 3
print("Matrix (unchanged):")
print(csr_zeros.toarray())
# [[1 0 0]
#  [0 2 0]
#  [0 0 3]]

#############
## prune() ##
#############
'''
Remove entries smaller than threshold
Useful for removing numerical noise
'''

# Array with small values
A_small = csr_array([[1.0, 1e-10, 2.0],
                     [1e-9, 3.0, 1e-8],
                     [4.0, 1e-7, 5.0]])

print("Original matrix:")
print(A_small.toarray())
# [[1.e+00 1.e-10 2.e+00]
#  [1.e-09 3.e+00 1.e-08]
#  [4.e+00 1.e-07 5.e+00]]

print(f"Stored elements: {A_small.nnz}") # 9

# Prune values below 1e-6
A_pruned = A_small.copy()
A_pruned.data[np.abs(A_pruned.data) < 1e-6] = 0
A_pruned.eliminate_zeros()

print("\nAfter pruning (threshold=1e-6):")
print(A_pruned.toarray())
# [[1. 0. 2.]
#  [0. 3. 0.]
#  [4. 0. 5.]]

print(f"Stored elements: {A_pruned.nnz}") # 5

############################
## nnz vs count_nonzero() ##
############################
'''
nnz: number of stored elements (including explicit zeros)
count_nonzero(): actual non-zero elements
'''

A_compare = csr_array([[1, 0, 2],
                       [0, 0, 0],
                       [3, 0, 4]])

print(f"nnz (stored): {A_compare.nnz}") # 4
print(f"count_nonzero(): {A_compare.count_nonzero()}") # 4

# Add explicit zero
A_explicit = A_compare.copy()
A_explicit[0, 1] = 1
A_explicit[0, 1] = 0  # Now (0,1) might be explicit zero

print(f"\nAfter setting A[0,1]=1 then A[0,1]=0:")
print(f"nnz (stored): {A_explicit.nnz}") # 5
print(f"count_nonzero(): {A_explicit.count_nonzero()}") # 4


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 3. Reshape and Transpose -------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

#############
## Reshape ##
#############
'''
Reshape sparse arrays
Must preserve total number of elements
May change sparsity pattern
'''

A_reshape = csr_array([[1, 0, 2, 0],
                       [0, 3, 0, 4],
                       [5, 0, 6, 0]])

print("Original (3x4):")
print(A_reshape.toarray())
print(f"Shape: {A_reshape.shape}") # (3, 4)

# Reshape to 2x6
A_reshaped = A_reshape.reshape((2, 6))
print(A_reshaped.toarray())
# [[1 0 2 0 0 3]
#  [0 4 5 0 6 0]]

# Reshape to 6x2
A_reshaped2 = A_reshape.reshape((6, 2))
print(A_reshaped2.toarray())
# [[1 0]
#  [2 0]
#  [0 3]
#  [0 4]
#  [5 0]
#  [6 0]]

# Can also reshape to 1D (not common)
A_flat = A_reshape.reshape((-1,))
print(A_flat.toarray())
# [1 0 2 0 0 3 0 4 5 0 6 0]

###############
## Transpose ##
###############
'''
Transpose: swap rows and columns
Very efficient in sparse formats
CSR.T -> CSC (just view, no copy)
'''

A_trans = csr_array([[1, 0, 2],
                     [0, 3, 0],
                     [4, 0, 5]])

print(f"Type: {type(A_trans)}")
# Type: <class 'scipy.sparse._csr.csr_array'>

# Transpose
A_T = A_trans.T
print(A_T.toarray())
# [[1 0 4]
#  [0 3 0]
#  [2 0 5]]
print(f"Type: {type(A_T)}")  # Type: <class 'scipy.sparse._csc.csc_array'> (CSR -> CSC)

# Transpose back
A_TT = A_T.T
print(A_TT.toarray())
# [[1 0 2]
#  [0 3 0]
#  [4 0 5]]
print(f"Type: {type(A_TT)}")  # Type: <class 'scipy.sparse._csr.csr_array'> (CSC -> CSR)

# Using transpose() method
A_transpose = A_trans.transpose()
print(f"\nUsing .transpose() method: {type(A_transpose)}") # <class 'scipy.sparse._csc.csc_array'>

#########################
## Conjugate transpose ##
#########################
'''
For complex matrices
.H or .conj().T
'''

A_complex = csr_array([[1+2j, 0],
                       [3-1j, 4+0j]])

print("Complex matrix:")
print(A_complex.toarray())
# [[1.+2.j 0.+0.j]
#  [3.-1.j 4.+0.j]]

A_H = A_complex.conj().T
print("\nConjugate transpose:")
print(A_H.toarray())
# [[1.-2.j 3.+1.j]
#  [0.+0.j 4.+0.j]]


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 4. Graph Algorithms ---------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

############################
## connected_components() ##
############################
'''
Find connected components in a graph
Graph represented as sparse adjacency matrix

#################

A connected component is a maximal subset of nodes
where every node can reach every other node through some path.
'''

# Create graph with 2 components
adjacency = csr_array([[0, 1, 1, 0, 0, 0],
                       [1, 0, 1, 0, 0, 0],
                       [1, 1, 0, 0, 0, 0],
                       [0, 0, 0, 0, 1, 1],
                       [0, 0, 0, 1, 0, 1],
                       [0, 0, 0, 1, 1, 0]])

print("Adjacency matrix:")
print(adjacency.toarray())
# [[0 1 1 0 0 0]
#  [1 0 1 0 0 0]
#  [1 1 0 0 0 0]
#  [0 0 0 0 1 1]
#  [0 0 0 1 0 1]
#  [0 0 0 1 1 0]]

n_components, labels = connected_components(adjacency, directed=False) # undirected graph

print(f"\nNumber of components: {n_components}") # 2
print(f"Component labels: {labels}") # [0 0 0 1 1 1]
print("Component 0: nodes", np.where(labels == 0)[0]) # [0 1 2]
print("Component 1: nodes", np.where(labels == 1)[0]) # [3 4 5]

'''
Component 0: Nodes {0, 1, 2} form a triangle where all three nodes are interconnected
Component 1: Nodes {3, 4, 5} also form a triangle with mutual connections

Since there are no edges connecting any node in {0,1,2} to any node in {3,4,5},
these form two distinct connected components.
'''

#####################
## shortest_path() ##
#####################
'''
Compute shortest paths between all pairs of nodes
Various algorithms: Dijkstra, Bellman-Ford, Floyd-Warshall
'''

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
weights_inf[weights_inf == 0] = np.inf # Replace all 0s with inf
np.fill_diagonal(weights_inf, 0) # Set diagonal back to 0
weights_graph = csr_array(weights_inf)
print(weights_graph.toarray())
# [[ 0.  4. inf inf inf inf inf  8. inf]
#  [ 4.  0.  8. inf inf inf inf 11. inf]
#  [inf  8.  0.  7. inf  4. inf inf  2.]
#  [inf inf  7.  0.  9. 14. inf inf inf]
#  [inf inf inf  9.  0. 10. inf inf inf]
#  [inf inf  4. 14. 10.  0.  2. inf inf]
#  [inf inf inf inf inf  2.  0.  1.  6.]
#  [ 8. 11. inf inf inf inf  1.  0.  7.]
#  [inf inf  2. inf inf inf  6.  7.  0.]]

# Compute shortest paths from node 0
dist_matrix, predecessors = shortest_path(weights_graph,
                                          method='auto',
                                          directed=False,
                                          return_predecessors=True,
                                          indices=0)

print("Shortest distances from node 0:")
print(dist_matrix.round(1))
# [ 0.  4. 12. 19. 21. 11.  9.  8. 14.]

# Get path from 0 to 4
def get_path(predecessors, start, end):
    path = [end]
    while path[-1] != start:
        path.append(predecessors[path[-1]])
    return path[::-1]

path_0_to_4 = get_path(predecessors, 0, 4)
print(f"\nPath from 0 to 4: {path_0_to_4}") # [np.int32(0), np.int32(7), np.int32(6), np.int32(5), 4]
print(f"Distance: {dist_matrix[4]:.1f}") # 21.0

#############################
## minimum_spanning_tree() ##
#############################
'''
Find minimum spanning tree
Connects all nodes with minimum total edge weight
'''

# Use same weighted graph
mst = minimum_spanning_tree(weights)

print("Original graph edges (non-zero):", weights.nnz // 2)  # 14 (Undirected)
print("MST edges:", mst.nnz // 2) # 4
print(f"MST total weight: {mst.sum() / 2:.0f}")  # 18 (Divide by 2 for undirected)

print("\nMST adjacency:")
print(mst.toarray())
# [[0. 4. 0. 0. 0. 0. 0. 8. 0.]
#  [0. 0. 0. 0. 0. 0. 0. 0. 0.]
#  [0. 0. 0. 7. 0. 4. 0. 0. 2.]
#  [0. 0. 0. 0. 9. 0. 0. 0. 0.]
#  [0. 0. 0. 0. 0. 0. 0. 0. 0.]
#  [0. 0. 0. 0. 0. 0. 2. 0. 0.]
#  [0. 0. 0. 0. 0. 0. 0. 1. 0.]
#  [0. 0. 0. 0. 0. 0. 0. 0. 0.]
#  [0. 0. 0. 0. 0. 0. 0. 0. 0.]]

###################################################
## depth_first_order() and breadth_first_order() ##
###################################################
'''
Graph traversal orders
Useful for tree algorithms
'''

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
print(f"\nDepth-first order: {dfs_order}") # [0 1 3 4 2]

# Breadth-first order from root 0
bfs_order, bfs_predecessors = breadth_first_order(tree, 0, directed=True)
print(f"Breadth-first order: {bfs_order}") # [0 1 2 3 4]


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 5. Advanced Construction --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

###########################
## bmat() - Block matrix ##
###########################
'''
Create block matrix from 2D list
More flexible than block_array
'''

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
# [[1 2 0 0]
#  [3 4 0 0]
#  [0 0 1 2]
#  [0 0 3 4]]

################################
## kron() - Kronecker product ##
################################
'''
Kronecker (tensor) product of two sparse arrays
Useful in FEM, quantum mechanics, etc.
'''

A_kron = csr_array([[1, 2], [3, 4]])
B_kron = csr_array([[0, 5], [6, 0]])

# A ⊗ B
kron_prod = sparse.kron(A_kron, B_kron, format='csr')

print("A:")
print(A_kron.toarray())
# [[1 2]
#  [3 4]]

print("\nB:")
print(B_kron.toarray())
# [[0 5]
#  [6 0]]

print("\nA ⊗ B:")
print(kron_prod.toarray())
# [[ 0  5  0 10]
#  [ 6  0 12  0]
#  [ 0 15  0 20]
#  [18  0 24  0]]

print(f"Shape: {A_kron.shape} ⊗ {B_kron.shape} = {kron_prod.shape}")
# Shape: (2, 2) ⊗ (2, 2) = (4, 4)

###########################################
## Practical: 2D Laplacian via Kronecker ##
###########################################
'''
Build 2D Laplacian using Kronecker products
Common in numerical PDEs
'''

n = 5  # Small for visualization
I = eye_array(n, format='csr')
D2 = diags_array([np.ones(n-1), -2*np.ones(n), np.ones(n-1)],
                 offsets=[-1, 0, 1], format='csr')

# 2D Laplacian = I ⊗ D2 + D2 ⊗ I
Laplacian_2D = sparse.kron(I, D2) + sparse.kron(D2, I)

print(f"2D Laplacian for {n}x{n} grid") # 5x5
print(f"Shape: {Laplacian_2D.shape}") # (25, 25)
print(f"Non-zeros: {Laplacian_2D.nnz}") # 325
print(f"Sparsity: {100 * Laplacian_2D.nnz / (n**4):.1f}%") # 52.0%


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 7. Performance Optimization ----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

################################
## Format conversion strategy ##
################################
'''
Choose format based on operation
Convert strategically to minimize overhead
'''

print("\nFormat Conversion Strategy:")
print("1. Build in COO, DOK, or LIL (flexible)")
print("2. Convert to CSR for arithmetic and row operations")
print("3. Convert to CSC for column operations")
print("4. Reuse same format for multiple operations")

#######################
## Memory management ##
#######################
'''
Monitor memory usage
Use appropriate dtypes
'''

# Compare memory usage of different dtypes
n = 1000
density = 0.01

A_float64 = random_array((n, n), density=density, dtype=np.float64, random_state=42)
A_float32 = random_array((n, n), density=density, dtype=np.float32, random_state=42)
A_int32 = random_array((n, n), density=density, dtype=np.int32, random_state=42)

# Approximate memory
mem_64 = A_float64.data.nbytes + A_float64.row.nbytes + A_float64.col.nbytes
mem_32 = A_float32.data.nbytes + A_float32.row.nbytes + A_float32.col.nbytes
mem_int = A_int32.data.nbytes + A_int32.row.nbytes + A_int32.col.nbytes

print(f"Float64 memory: {mem_64/1024:.1f} KB") # 156.2 KB
print(f"Float32 memory: {mem_32/1024:.1f} KB") # 117.2 KB
print(f"Int32 memory: {mem_int/1024:.1f} KB") # 117.2 KB
print(f"\nMemory savings (float32 vs float64): {100*(1-mem_32/mem_64):.0f}%") # 25%

############################
## Best practices summary ##
############################

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

#################################
## Example: Optimized workflow ##
#################################

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
# Built in LIL: 298 non-zeros

# 2. Convert to CSR (for computation)
A_workflow = A_workflow.tocsr()

# 3. Eliminate zeros and sum duplicates
A_workflow.eliminate_zeros()
A_workflow.sum_duplicates()

# 4. Perform computation
b_workflow = np.ones(n, dtype=np.float32)
from scipy.sparse.linalg import spsolve
x_workflow = spsolve(A_workflow, b_workflow)

print(f"4. Solved linear system")
print(f"5. Solution range: [{x_workflow.min():.2f}, {x_workflow.max():.2f}]")
# [50.00, 1275.00]
