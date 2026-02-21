'''
1. Matrix and vector products
   + np.dot()                  : dot product of two arrays (matrix multiply for 2D; inner product for 1D).
   + np.inner()                : inner product of two arrays.
   + np.outer()                : outer product of two 1D vectors.
   + np.matmul() / @ operator  : matrix product of two arrays (preferred for 2D).
   + np.kron()                 : Kronecker product of two arrays.
   + np.einsum()               : evaluates the Einstein summation convention on operands.
   + np.linalg.matrix_power()  : raise a square matrix to an integer power.
   + np.tensordot()            : tensor dot product along specified axes.

2. Decompositions
   + np.linalg.cholesky()      : Cholesky decomposition (A = L @ L.T for SPD matrices).
   [scipy.linalg] cho_factor / cho_solve: factorize once, solve many RHS efficiently.
   + np.linalg.qr()            : QR factorization (A = Q @ R).
   + np.linalg.svd()           : Singular Value Decomposition (A = U @ diag(s) @ Vt).
   [scipy.linalg] lu()     : LU decomposition with partial pivoting (A = P @ L @ U).
   [scipy.linalg] schur()  : Schur decomposition (A = Z @ T @ Z.H).

3. Matrix eigenvalues
   + np.linalg.eig()           : eigenvalues and right eigenvectors of a general square matrix.
   + np.linalg.eigh()          : eigenvalues and eigenvectors of a real symmetric / complex Hermitian matrix.
   + np.linalg.eigvals()       : eigenvalues only (no eigenvectors) for a general matrix.
   + np.linalg.eigvalsh()      : eigenvalues only for a symmetric / Hermitian matrix.
   [scipy.linalg] eig(A, B): generalized eigenvalue problem A v = lambda B v.

4. Norms and other numbers
   + np.linalg.norm()          : matrix or vector norm.
   + np.linalg.cond()          : condition number of a matrix.
   + np.linalg.det()           : determinant of a square matrix.
   + np.linalg.matrix_rank()   : matrix rank via SVD.
   + np.linalg.slogdet()       : sign and log of the determinant (numerically stable).
   + np.trace()                : sum of diagonal elements.

5. Solving equations and inverting matrices
   + np.linalg.solve()         : solve Ax = b for a square, non-singular A.
   + np.linalg.lstsq()         : least-squares solution to Ax = b for overdetermined systems.
   + np.linalg.inv()           : compute the inverse of a matrix.
   + np.linalg.pinv()          : Moore-Penrose pseudoinverse (works for rectangular / singular matrices).
   [scipy.linalg] solve_triangular(): solve Lx = b exploiting triangular structure.
   [scipy.linalg] pinvh()           : pseudoinverse optimized for symmetric / Hermitian matrices.

6. Matrix functions  (scipy.linalg — not in numpy.linalg)
   + spla.expm()   : matrix exponential  e^A.
   + spla.logm()   : matrix logarithm    log(A).
   + spla.sqrtm()  : matrix square root  A^(1/2).
   + spla.funm()   : apply an arbitrary scalar function to a matrix.

7. Matrix equation solvers  (scipy.linalg — not in numpy.linalg)
   + spla.solve_sylvester()              : solve AX + XB = Q.
   + spla.solve_continuous_lyapunov()    : solve AX + XA^H = Q.

8. Special matrices  (scipy.linalg — not in numpy.linalg)
   + spla.block_diag()  : construct a block-diagonal matrix from sub-matrices.
   + spla.toeplitz()    : construct a Toeplitz matrix.
   + spla.circulant()   : construct a circulant matrix.
   + spla.hilbert()     : construct the Hilbert matrix (classic ill-conditioned matrix).
'''

import numpy as np
import scipy.linalg as spla

# 3x3 Symmetric Positive Definite (SPD) matrix — works for Cholesky, eigh, solve
A = np.array([[2., 1., 1.],
              [1., 3., 2.],
              [1., 2., 4.]])
# array([[2., 1., 1.],
#        [1., 3., 2.],
#        [1., 2., 4.]])

# 3x3 general (non-symmetric) matrix — used for eig, LU, Schur
G = np.array([[1., 2., 3.],
              [0., 4., 5.],
              [1., 0., 2.]])
# array([[1., 2., 3.],
#        [0., 4., 5.],
#        [1., 0., 2.]])

# 4x2 rectangular matrix — used for SVD and lstsq
M = np.array([[1., 2.],
              [3., 4.],
              [5., 6.],
              [7., 8.]])
# array([[1., 2.],
#        [3., 4.],
#        [5., 6.],
#        [7., 8.]])

v1 = np.array([1., 2., 3.])   # 1D vector
v2 = np.array([4., 5., 6.])   # 1D vector
b  = np.array([1., 2., 3.])   # RHS vector for Ax = b


#-------------------------------------------------------------------------------------------------#
#------------------------------ 1. Matrix and vector products ------------------------------------#
#-------------------------------------------------------------------------------------------------#

##############
## np.dot() ##
##############
'''
np.dot() computes the dot product of two arrays.

- 1D arrays  : inner product (scalar).
- 2D arrays  : matrix multiplication (same as A @ B).
- Higher dim : sum product over the last axis of the first and second-to-last of the second.
'''

print(np.dot(v1, v2))
# 32.0  (1*4 + 2*5 + 3*6 = 32)

print(np.dot(A, b))
# [ 7. 13. 17.]  (matrix-vector product; same as A @ b)

print(np.dot(A, G))
# [[ 3.  8. 13.]
#  [ 3. 14. 22.]
#  [ 5. 10. 21.]]
# matrix-matrix product (same as A @ G)

################
## np.inner() ##
################
'''
np.inner() computes the inner product of two arrays.

For 1D arrays, identical to np.dot().
For higher dimensions, it sums over the last axes of both inputs.
'''

print(np.inner(v1, v2))
# 32.0  (same as np.dot for 1D)

print(np.inner(A, G))
# [[ 7.  9.  4.] (7 = A[0,:] @ G[0,:] = 2*1 + 1*0 + 1*1 = 3 + 0 + 4 = 7)
#  [13. 22.  5.]
#  [17. 28.  9.]]
# 3x3 matrix: element [i,j] = dot(A[i,:], G[j,:])  (sum over columns)

################
## np.outer() ##
################
'''
np.outer() computes the outer product of two 1D vectors.

Result[i, j] = v1[i] * v2[j]. Produces an (m, n) matrix from vectors of length m and n.
'''

print(np.outer(v1, v2))
# [[ 4.  5.  6.]
#  [ 8. 10. 12.]
#  [12. 15. 18.]]

##################
## np.matmul()  ##
## (@ operator) ##
##################
'''
np.matmul() performs matrix multiplication of two arrays.

For 2D arrays, equivalent to np.dot(). The @ operator is the preferred shorthand.
Does NOT support scalar multiplication (use * for that).
'''

print(np.matmul(A, b))
# [ 7. 13. 17.]

print(A @ b)
# [ 7. 13. 17.]  (preferred syntax using @ operator)

print(A @ G)
# [[ 3.  8. 13.]
#  [ 3. 14. 22.]
#  [ 5. 10. 21.]]
# matrix-matrix product (A.shape=(3,3), G.shape=(3,3) → result.shape=(3,3))

###############
## np.kron() ##
###############
'''
np.kron() computes the Kronecker product of two arrays.

kron(A, B) replaces each element A[i,j] of A with the block A[i,j] * B.
Common use: constructing block-structured matrices and quantum operations.
'''

I2 = np.eye(2)
# array([[1., 0.],
#        [0., 1.]])

K  = np.array([[1., 2.], [3., 4.]])
# array([[1., 2.],
#        [3., 4.]])

print(np.kron(I2, K))
# [[1. 2. 0. 0.]
#  [3. 4. 0. 0.]
#  [0. 0. 1. 2.]
#  [0. 0. 3. 4.]]
# I2 ⊗ K places a copy of K at each non-zero position of I2 → block-diagonal
'''
First block: I2[0,0]*K = 1*K = K
Second block: I2[0,1]*K = 0*K = 0 * 2x2 zero block
Third block: I2[1,0]*K = 0*K = 0 * 2x2 zero block
Fourth block: I2[1,1]*K = 1*K = K
'''

print(np.kron(K, I2))
# [[1. 0. 2. 0.]
#  [0. 1. 0. 2.]
#  [3. 0. 4. 0.]
#  [0. 3. 0. 4.]]  (different ordering)

#################
## np.einsum() ##
#################
'''
np.einsum() evaluates Einstein summation using a subscript string.

Subscript notation specifies which axes to sum over and the output shape.
Very flexible: can express dot products, outer products, transposes, traces, etc.
'''

print(np.einsum('ij,j->i', A, b))
# [ 7. 13. 17.]  (matrix-vector product: sum over j → equivalent to A @ b)

print(np.einsum('ij,ji->', A, G))
# 38.0: trace of A @ G.T  (sum over all i,j of A[i,j]*G[j,i])

print(np.einsum('ij->ji', A))
# 3x3: transpose of A

print(np.einsum('ii', A))
# 9.0: trace of A  (sum diagonal elements)

print(np.einsum('i,j->ij', v1, v2))
# outer product:
# [[ 4.  5.  6.]
#  [ 8. 10. 12.]
#  [12. 15. 18.]]

# ─── Ellipsis notation: '...' stands for any number of batch dimensions ───────────────────────

batch_M = np.stack([A, G])     # shape (2, 3, 3) — a batch of 2 matrices
batch_b = np.stack([b, b])     # shape (2, 3)    — a batch of 2 vectors
batch_v = np.stack([v1, v2])   # shape (2, 3)    — a batch of 2 vectors

# Batch matrix-vector product: apply A@b and G@b in one call
print(np.einsum('...ij,...j->...i', batch_M, batch_b))
# [[ 7. 13. 17.]   ← A @ b
#  [14. 23.  7.]]  ← G @ b
# '...' absorbs the batch dimension; 'ij,j->i' is the per-matrix logic

# Batch trace: extract the trace of each matrix in the stack
print(np.einsum('...ii->...', batch_M))
# [9. 7.]  (trace(A)=9, trace(G)=7)

# Batch dot product: compute v·v for each vector in the batch
print(np.einsum('...i,...i->...', batch_v, batch_v))
# [14. 77.]  (v1·v1 = 1+4+9 = 14,  v2·v2 = 16+25+36 = 77)

# Batch matrix-matrix product: compute M^2 for each matrix in the stack
print(np.einsum('...ij,...jk->...ik', batch_M, batch_M))
# [[ 6.  7.  8.]      ← A @ A
#  [ 7. 14. 15.]
#  [ 8. 15. 21.]]
# [[ 4. 10. 19.]      ← G @ G
#  [ 5. 16. 30.]
#  [ 3.  2.  7.]]

# Batch outer product: compute v ⊗ v (rank-1 matrix) for each vector
print(np.einsum('...i,...j->...ij', batch_v, batch_v))
# shape (2, 3, 3)
# batch_v[0] ⊗ batch_v[0]:                   batch_v[1] ⊗ batch_v[1]:
# [[1.  2.  3.]                               [[16. 20. 24.]
#  [2.  4.  6.]                                [20. 25. 30.]
#  [3.  6.  9.]]                               [24. 30. 36.]]


##############################
## np.linalg.matrix_power() ##
##############################
'''
np.linalg.matrix_power() raises a square matrix to an integer power n.

n > 0: repeated matrix multiplication  (G^n = G @ G @ ... n times)
n = 0: identity matrix
n < 0: power of the inverse            (G^-1 @ G^-1 @ ... |n| times)
'''

print(np.linalg.matrix_power(G, 2))
# [[ 4. 10. 19.]
#  [ 5. 16. 30.]
#  [ 3.  2.  7.]]  (G @ G)

print(np.linalg.matrix_power(G, 0))
# [[1. 0. 0.]
#  [0. 1. 0.]
#  [0. 0. 1.]]  (identity)

print(np.linalg.matrix_power(G, -1))
# [[ 1.33333333 -0.66666667 -0.33333333]
#  [ 0.83333333 -0.16666667 -0.83333333]
#  [-0.66666667  0.33333333  0.66666667]]
# inverse of G  (same as np.linalg.inv(G))

####################
## np.tensordot() ##
####################
'''
np.tensordot() computes the tensor dot product by summing over specified axes.

axes=1  : equivalent to matrix multiplication or np.dot() for vectors.
axes=0  : outer product (no summation).
axes=[[ax_a], [ax_b]]: custom contraction axes.
'''

print(np.tensordot(v1, v2, axes=1))
# 32.0  (sum over the single shared axis: same as np.dot for 1D)

print(np.tensordot(v1, v2, axes=0))
# [[ 4.  5.  6.]
#  [ 8. 10. 12.]
#  [12. 15. 18.]]
# outer product (3x3 matrix)
''' [N, 1] @ [1, M] → [N, M]  (no summation) '''

print(np.tensordot(A, G, axes=[[1],[0]]))
# [[ 3.  8. 13.]
#  [ 3. 14. 22.]
#  [ 5. 10. 21.]]
# standard matrix multiplication A @ G  (contract last axis of A with first axis of G)


#-------------------------------------------------------------------------------------------------#
#--------------------------------------- 2. Decompositions ---------------------------------------#
#-------------------------------------------------------------------------------------------------#

##########################
## np.linalg.cholesky() ##
##########################
'''
np.linalg.cholesky() performs Cholesky decomposition on a Symmetric Positive Definite (SPD) matrix.

Returns L (lower triangular) such that A = L @ L.T
Requirements: A must be symmetric and positive definite.
Use case: solving SPD systems efficiently (faster than LU), sampling multivariate normals.
'''

L = np.linalg.cholesky(A)

print(L)
# [[1.4142 0.     0.    ]
#  [0.7071 1.5811 0.    ]
#  [0.7071 0.9487 1.6125]]

print(L @ L.T)
# [[2. 1. 1.]
#  [1. 3. 2.]
#  [1. 2. 4.]]  (reconstructs A exactly)

# upper=True returns U such that A = U.T @ U
U = np.linalg.cholesky(A, upper=True)
print(U.T @ U)
# [[2. 1. 1.]  ...  (same result)

##########################################
## spla.cho_factor() + spla.cho_solve() ##
##########################################
'''
spla.cho_factor() + spla.cho_solve(): factorize once, solve multiple RHS efficiently.

spla.cho_factor(A)             → (c, low): packed Cholesky factor (reusable object)
spla.cho_solve((c, low), b)    → x: solution to Ax = b using the pre-computed factor

Advantage over np.linalg.solve(): factorization cost O(n^3) is paid once;
each subsequent solve is only O(n^2). Ideal when solving Ax = b1, b2, ... b_k repeatedly.
'''

c, low = spla.cho_factor(A)

x = spla.cho_solve((c, low), b)

print(x)
# [0.0769 0.2308 0.6154]

print(A @ x)
# [1. 2. 3.]  (verifies A @ x = b)

# Solve a second RHS without re-factorizing
b2 = np.array([2., 4., 6.])
x2 = spla.cho_solve((c, low), b2)
print(x2)
# [0.1538 0.4615 1.2308]  (2 * x, as expected since b2 = 2 * b)

####################
## np.linalg.qr() ##
####################
'''
np.linalg.qr() performs QR factorization of a matrix.

Returns Q (orthogonal/unitary) and R (upper triangular) such that A = Q @ R.

mode options:
  'reduced' (default): Q shape (m, k), R shape (k, n)  where k = min(m, n)
  'complete'         : Q shape (m, m), R shape (m, n)
  'r'                : returns only R
'''

Q, R = np.linalg.qr(M)

print(Q.shape, R.shape)
# (4, 2) (2, 2)  (reduced mode: M is 4x2, so k=2)

print(Q)
# [[-0.1091 -0.8295]
#  [-0.3273 -0.4392]
#  [-0.5455 -0.0488]
#  [-0.7638  0.3416]]

print(R)
# [[ -9.1652 -10.9109]
#  [  0.      -0.9759]]

print(np.allclose(M, Q @ R))
# True  (M = Q @ R)

print(np.allclose(Q.T @ Q, np.eye(2)))
# True  (columns of Q are orthonormal)

# Complete mode: Q is a full orthogonal matrix
Q_full, R_full = np.linalg.qr(M, mode='complete')

print(Q_full.shape, R_full.shape)
# (4, 4) (4, 2)

#####################
## np.linalg.svd() ##
#####################
'''
np.linalg.svd() performs Singular Value Decomposition: A = U @ diag(s) @ Vt

Returns:
  U   : left singular vectors  (m x m for full, m x k for reduced)
  s   : singular values        (k,)  in descending order
  Vt  : right singular vectors transposed  (k x n for reduced)

Singular values measure how much each direction is "stretched" by A.
'''

U, s, Vt = np.linalg.svd(M)

print(U.shape, s.shape, Vt.shape)
# (4, 4) (2,) (2, 2)  (full SVD; U is 4x4, Vt is 2x2)

print(s)
# [14.2691  0.6268]  (two singular values; M has rank 2)

# Reconstruct M from U, s, Vt
Sigma = np.zeros_like(M)
Sigma[:s.shape[0], :s.shape[0]] = np.diag(s)

print(np.allclose(M, U @ Sigma @ Vt))
# True

# full_matrices=False: economy/thin SVD (k = min(m,n) columns in U)
U_t, s_t, Vt_t = np.linalg.svd(M, full_matrices=False)

print(U_t.shape, s_t.shape, Vt_t.shape)
# (4, 2) (2,) (2, 2)  (thin SVD; U_t has only 2 columns)

print(np.allclose(M, U_t @ np.diag(s_t) @ Vt_t))
# True

# compute_uv=False: return only singular values (faster if U and Vt not needed)
s_only = np.linalg.svd(M, compute_uv=False)

print(s_only)
# [14.2691  0.6268]

###############
## spla.lu() ##
###############
'''
spla.lu() performs LU decomposition with partial pivoting: A = P @ L @ U

Returns:
  P : permutation matrix  (row swaps for numerical stability)
  L : unit lower triangular matrix  (diagonal = 1)
  U : upper triangular matrix

Available in scipy.linalg but NOT in numpy.linalg.
For repeated solves, prefer spla.lu_factor() + spla.lu_solve().
'''

P_lu, L_lu, U_lu = spla.lu(G)

print(P_lu)
# [[1. 0. 0.]
#  [0. 1. 0.]
#  [0. 0. 1.]]  (no row swaps needed for G)

print(L_lu)
# [[ 1.   0.   0. ]
#  [ 0.   1.   0. ]
#  [ 1.  -0.5  1. ]]

print(U_lu)
# [[1.  2.  3. ]
#  [0.  4.  5. ]
#  [0.  0.  1.5]]

print(np.allclose(G, P_lu @ L_lu @ U_lu))
# True  (G = P @ L @ U)

# Efficient repeated solving using lu_factor + lu_solve
lu_piv = spla.lu_factor(G)
x_lu   = spla.lu_solve(lu_piv, b)

print(x_lu)
# solution to Gx = b using pre-computed LU factorization

##################
## spla.schur() ##
##################
'''
spla.schur() computes the Schur decomposition: A = Z @ T @ Z.H

Returns:
  T : quasi-upper triangular (Schur form) — upper triangular for complex output
  Z : unitary (orthogonal for real) matrix of Schur vectors

For real matrices, T is block-upper-triangular with 1x1 and 2x2 blocks.
2x2 blocks correspond to conjugate complex eigenvalue pairs.
output='complex' forces a fully upper triangular T.

Available in scipy.linalg but NOT in numpy.linalg.
'''

T_s, Z_s = spla.schur(G)

print(T_s.round(4))
# [[ 0.9697  1.9097 -5.3708]
#  [-0.1285  0.9697  0.0006]
#  [ 0.      0.      5.0606]]
# 2x2 top-left block encodes the conjugate eigenvalue pair ≈ 0.9697 ± 0.4953j

print(Z_s.round(4))
# [[ 0.4826 -0.8483 -0.218 ]
#  [ 0.7429  0.5283 -0.411 ]
#  [-0.4638 -0.0364 -0.8852]]

print(np.allclose(G, Z_s @ T_s @ Z_s.T))
# True  (reconstructs G)

# Force complex upper triangular Schur form
T_c, Z_c = spla.schur(G, output='complex')
print(np.diag(T_c).round(4))
# eigenvalues on diagonal: [0.9697+0.4953j, 0.9697-0.4953j, 5.0606+0.j]


#-------------------------------------------------------------------------------------------------#
#------------------------------------- 3. Matrix eigenvalues -------------------------------------#
#-------------------------------------------------------------------------------------------------#

#####################
## np.linalg.eig() ##
#####################

'''
np.linalg.eig() computes the eigenvalues and right eigenvectors of a general square matrix.

Returns:
  w : eigenvalues (may be complex even for real input)
  v : eigenvectors as columns of v  (v[:, i] corresponds to w[i])

For symmetric/Hermitian matrices, prefer np.linalg.eigh() (real eigenvalues, faster).
'''

w, v = np.linalg.eig(G)

print(w)

# [0.9697+0.4953j  0.9697-0.4953j  5.0606+0.j]
# complex eigenvalues appear in conjugate pairs for real matrices

print(v[:, 2].real)

# real eigenvector for eigenvalue 5.0606

# Verification: A @ v[:,i] = w[i] * v[:,i]
print(np.allclose(G @ v, v * w))

# True

######################
## np.linalg.eigh() ##
######################

'''
np.linalg.eigh() computes the eigenvalues and eigenvectors of a real symmetric or
complex Hermitian matrix.

Returns:
  w : eigenvalues (always real), sorted in ascending order.
  v : orthonormal eigenvectors as columns.

Faster and always returns real eigenvalues — use this instead of eig() for SPD / symmetric matrices.
'''

w_h, v_h = np.linalg.eigh(A)

print(w_h)

# [1.308  1.6431 6.0489]  (real, sorted ascending)

print(v_h)

# [[ 0.591 -0.737 -0.328]
#  [-0.737 -0.328 -0.591]
#  [ 0.328  0.591 -0.737]]
# Columns are orthonormal eigenvectors

print(np.allclose(A, v_h @ np.diag(w_h) @ v_h.T))

# True  (eigendecomposition: A = V @ diag(w) @ V.T)

print(np.allclose(v_h.T @ v_h, np.eye(3)))

# True  (V is orthogonal: V.T @ V = I)

# UPLO='U': use upper triangle of A for computation (default 'L' = lower)
w_upper, _ = np.linalg.eigh(A, UPLO='U')
print(np.allclose(w_h, w_upper))

# True

#########################
## np.linalg.eigvals() ##
#########################

'''
np.linalg.eigvals() computes eigenvalues only (no eigenvectors) for a general matrix.

Faster than eig() when eigenvectors are not needed.
'''

print(np.linalg.eigvals(G))

# [0.9697+0.4953j  0.9697-0.4953j  5.0606+0.j]

print(np.linalg.eigvals(A))

# [2. 3. 4.]  ... actually computed values will be approx [1.308 1.643 6.049]
# NOTE: eigenvalues may be in any order for general matrices

print(np.linalg.eigvals(np.eye(3)))

# [1. 1. 1.]  (identity matrix has all eigenvalues = 1)

##########################
## np.linalg.eigvalsh() ##
##########################

'''
np.linalg.eigvalsh() computes eigenvalues only for a symmetric / Hermitian matrix.

Returns real eigenvalues in ascending order. Faster than eigvalsh() when eigenvectors
are not needed.
'''

print(np.linalg.eigvalsh(A))

# [1.308  1.6431 6.0489]  (real, sorted ascending)

# Product of eigenvalues = determinant
print(np.prod(np.linalg.eigvalsh(A)).round(4))

# 13.0  (== np.linalg.det(A))

# Sum of eigenvalues = trace
print(np.sum(np.linalg.eigvalsh(A)).round(4))

# 9.0   (== np.trace(A))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~ [scipy.linalg] Generalized Eigenvalue Problem ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

##################
## spla.eig()   ##
## (generalized) #
##################

'''
spla.eig(A, B) solves the GENERALIZED eigenvalue problem: A v = lambda * B v

Without B (or B=None), reduces to the standard problem (same as np.linalg.eig).
With B provided, useful in structural mechanics, quantum chemistry, and dimensionality reduction
(e.g., LDA, CCA).

scipy.linalg.eig() offers this; numpy.linalg.eig() does NOT support a second matrix argument.
'''

B_gen = np.array([[2., 0., 0.],
                  [0., 3., 0.],
                  [0., 0., 1.]])

w_gen, v_gen = spla.eig(G, B_gen)

print(w_gen)

# [3.    +0.j      0.4167+0.3997j  0.4167-0.3997j]
# eigenvalues satisfy G @ v = lambda * B_gen @ v

# Verification: G @ v[:,i] ≈ w_gen[i] * (B_gen @ v[:,i])
i = 0
print(np.allclose(G @ v_gen[:, i], w_gen[i] * (B_gen @ v_gen[:, i])))

# True

#-------------------------------------------------------------------------------------------------#
#----------------------------------- 4. Norms and other numbers ----------------------------------#
#-------------------------------------------------------------------------------------------------#

######################
## np.linalg.norm() ##
######################

'''
np.linalg.norm() computes the norm of a matrix or vector.

For vectors (ord):
  None (default) : Euclidean (L2) norm  sqrt(sum(|x|^2))
  1              : L1 norm              sum(|x|)
  -1             : min(|x|)
  np.inf         : max(|x|)

For matrices (ord):
  'fro' (default): Frobenius norm  sqrt(sum(|A|^2))
  2              : largest singular value
  -2             : smallest singular value
  1              : max column sum
  np.inf         : max row sum
'''

print(np.linalg.norm(v1))

# 3.7417  (Euclidean: sqrt(1^2 + 2^2 + 3^2) = sqrt(14))

print(np.linalg.norm(v1, ord=1))

# 6.0  (L1: 1 + 2 + 3)

print(np.linalg.norm(v1, ord=np.inf))

# 3.0  (Linf: max element)

print(np.linalg.norm(A, 'fro'))

# 6.4031  (Frobenius: sqrt(4+1+1+1+9+4+1+4+16))

print(np.linalg.norm(A, 2))

# 6.0489  (spectral norm = largest singular value)

# Along a specific axis (norm of each row)
print(np.linalg.norm(A, axis=1).round(4))

# [2.4495 3.7417 4.5826]

######################
## np.linalg.cond() ##
######################

'''
np.linalg.cond() computes the condition number of a matrix.

cond(A) = norm(A) * norm(A^-1) = sigma_max / sigma_min

Interpretation:
  cond ≈ 1     : well-conditioned (solution is stable)
  cond >> 1    : ill-conditioned (small perturbations in b can cause large errors in x)
  cond = inf   : singular matrix (no unique solution)
'''

print(np.linalg.cond(A))

# 4.6246  (well-conditioned SPD matrix)

print(np.linalg.cond(G))

# condition number of G

# Hilbert matrix: famously ill-conditioned
H5 = spla.hilbert(5)

print(np.linalg.cond(H5).round(0))

# ~476607  (extremely ill-conditioned — small errors in b → huge errors in x)

#####################
## np.linalg.det() ##
#####################

'''
np.linalg.det() computes the determinant of a square matrix.

det(A) = 0 : matrix is singular (not invertible).
det(A) ≠ 0 : matrix is invertible.
det(A @ B) = det(A) * det(B)
For large matrices, use np.linalg.slogdet() to avoid overflow/underflow.
'''

print(np.linalg.det(G))

# 6.0  (non-zero → G is invertible)

print(np.linalg.det(A))

# 13.0  (product of eigenvalues: 1.308 * 1.6431 * 6.0489 ≈ 13.0)

print(np.linalg.det(np.eye(3)))

# 1.0  (identity has det = 1)

print(np.linalg.det(2 * np.eye(3)))

# 8.0  (det(c*I_n) = c^n)

############################
## np.linalg.matrix_rank() ##
############################

'''
np.linalg.matrix_rank() estimates the matrix rank using SVD.

Rank = number of singular values above a numerical tolerance threshold.
For an m×n matrix, rank <= min(m, n).
'''

print(np.linalg.matrix_rank(M))

# 2  (M is 4×2 with full column rank)

print(np.linalg.matrix_rank(A))

# 3  (full rank 3×3 matrix)

# Rank-deficient example
M_rank1 = np.outer(v1, v2)  # rank-1 matrix: every row is a multiple of v2

print(np.linalg.matrix_rank(M_rank1))

# 1

#########################
## np.linalg.slogdet() ##
#########################

'''
np.linalg.slogdet() returns the sign and natural log of the absolute determinant.

Returns: (sign, logabsdet)
  det(A) = sign * exp(logabsdet)

Use instead of det() when the determinant might overflow or underflow (very large/small matrices).
Numerically stable for high-dimensional covariance matrices (e.g., log-likelihood in ML).
'''

sign, logabsdet = np.linalg.slogdet(G)

print(sign, logabsdet)

# 1.0  1.7918  (det = 1.0 * exp(1.7918) ≈ 6.0)

print(sign * np.exp(logabsdet))

# 6.0  (recovers the determinant)

# Useful for log-likelihoods: log|Σ| = slogdet(Σ)[1]
Sigma_cov = A  # treat A as a covariance matrix
log_det_sigma = np.linalg.slogdet(Sigma_cov)[1]

print(log_det_sigma.round(4))

# 2.5649  (log(det(A)) = log(13) ≈ 2.5649)

#################
## np.trace()  ##
#################

'''
np.trace() returns the sum of the diagonal elements of a matrix (the trace).

trace(A) = sum of eigenvalues = sum(w)
For square matrices: trace(A @ B) = trace(B @ A)  (cyclic property)
offset parameter: allows summing off-diagonal elements.
'''

print(np.trace(A))

# 9.0  (2 + 3 + 4; sum of diagonal elements)

print(np.sum(np.linalg.eigvalsh(A)).round(4))

# 9.0  (trace = sum of eigenvalues)

print(np.trace(A, offset=1))

# 3.0  (sum of the first super-diagonal: A[0,1] + A[1,2] = 1 + 2 = 3)

print(np.trace(G @ A))

# trace(G @ A) = trace(A @ G)  (cyclic invariance)

#-------------------------------------------------------------------------------------------------#
#----------------------- 5. Solving equations and inverting matrices -----------------------------#
#-------------------------------------------------------------------------------------------------#

#######################
## np.linalg.solve() ##
#######################

'''
np.linalg.solve() solves the linear system Ax = b for a square, non-singular matrix A.

More numerically stable and faster than computing np.linalg.inv(A) @ b.
For SPD systems, scipy's Cholesky solver is even faster.
'''

x = np.linalg.solve(A, b)

print(x)

# [0.0769 0.2308 0.6154]

print(A @ x)

# [1. 2. 3.]  (verifies the solution)

# Solve multiple RHS at once: b is a matrix, each column is a separate RHS
B_rhs = np.column_stack([b, 2*b, b + 1])

X_multi = np.linalg.solve(A, B_rhs)

print(X_multi.shape)

# (3, 3)  (each column of X_multi is the solution for the corresponding column of B_rhs)

#######################
## np.linalg.lstsq() ##
#######################

'''
np.linalg.lstsq() finds the least-squares solution to Ax = b for overdetermined systems.

Minimizes ||Ax - b||_2. Returns the solution even when no exact solution exists.

Returns: (x, residuals, rank, singular_values)
rcond: cutoff for treating singular values as zero (-1 or None = machine precision)
'''

b_od = np.array([1., 2., 3., 4.])  # 4-element b for 4×2 matrix M

x_ls, res, rank, sv = np.linalg.lstsq(M, b_od, rcond=None)

print(x_ls)

# [0.   0.5]  (best-fit solution; M has shape 4×2)

print(res)

# residuals (empty if rank < n or m <= n)

print(rank)

# 2  (full column rank)

print(sv.round(4))

# [14.2691  0.6268]  (singular values of M)

# Verify: M @ x_ls is the projection of b_od onto the column space of M
print((M @ x_ls).round(4))

# [ 1.  2.  3.  4.]  (fits well in this case)

#####################
## np.linalg.inv() ##
#####################

'''
np.linalg.inv() computes the (full) inverse of a square matrix.

A @ inv(A) = inv(A) @ A = I

IMPORTANT: avoid using inv(A) @ b to solve linear systems.
  Use np.linalg.solve(A, b) instead — it is faster and more numerically stable.
  inv() is useful when you need the inverse matrix itself (e.g., covariance matrices in ML).
'''

A_inv = np.linalg.inv(A)

print(A_inv)

# [[ 0.6154 -0.1538 -0.0769]
#  [-0.1538  0.5385 -0.2308]
#  [-0.0769 -0.2308  0.3846]]

print(np.allclose(A @ A_inv, np.eye(3)))

# True

# Avoid this pattern (slower and less stable):
x_via_inv = A_inv @ b

# Prefer this instead:
x_via_solve = np.linalg.solve(A, b)

print(np.allclose(x_via_inv, x_via_solve))

# True  (same result, but solve is preferred)

######################
## np.linalg.pinv() ##
######################

'''
np.linalg.pinv() computes the Moore-Penrose pseudoinverse of a matrix.

Works for any shape (m×n), including rectangular and singular matrices.
For full-rank square matrices, pinv(A) = inv(A).
For overdetermined systems (m > n): pinv(M) @ b gives the least-squares solution.
'''

M_pinv = np.linalg.pinv(M)

print(M_pinv)

# [[-1.   -0.5   0.    0.5 ]
#  [ 0.85  0.45  0.05 -0.35]]

print(M_pinv.shape)

# (2, 4)  (pseudoinverse of a 4×2 matrix is 2×4)

print(np.allclose(M_pinv @ M, np.eye(2)))

# True  (M_pinv @ M = I for full column-rank M)

# Least-squares solution via pinv (equivalent to lstsq for consistent systems)
x_pinv = M_pinv @ b_od

print(x_pinv)

# [0.  0.5]  (same result as lstsq)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~ [scipy.linalg] Triangular Solver & Hermitian Pseudoinverse ~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

############################
## spla.solve_triangular() ##
############################

'''
spla.solve_triangular() solves Lx = b where L is a lower (or upper) triangular matrix.

Much faster than np.linalg.solve() for triangular systems — exploits the structure
via forward/backward substitution (O(n^2) vs O(n^3) for general LU solve).

Use case: back-substitution after Cholesky or QR decomposition.
'''

L_tri = np.tril(G)  # extract lower triangular part of G

print(L_tri)

# [[1. 0. 0.]
#  [0. 4. 0.]
#  [1. 0. 2.]]

x_tri = spla.solve_triangular(L_tri, b, lower=True)

print(x_tri)

# [1.  0.5 1. ]

print(L_tri @ x_tri)

# [1. 2. 3.]  (verifies the solution)

# upper=True: solve Ux = b for upper triangular U
U_tri = np.triu(G)

x_upper = spla.solve_triangular(U_tri, b, lower=False)

print(np.allclose(U_tri @ x_upper, b))

# True

###################
## spla.pinvh()  ##
###################

'''
spla.pinvh() computes the pseudoinverse of a symmetric / Hermitian matrix.

Uses the eigendecomposition (more efficient and numerically stable for symmetric matrices
than the SVD-based np.linalg.pinv()).

For a full-rank SPD matrix A: pinvh(A) = inv(A).
'''

A_pinvh = spla.pinvh(A)

print(A_pinvh)

# [[ 0.6154 -0.1538 -0.0769]
#  [-0.1538  0.5385 -0.2308]
#  [-0.0769 -0.2308  0.3846]]

print(np.allclose(A_pinvh, np.linalg.inv(A)))

# True  (for full-rank SPD matrices, pinvh = inv)

# Advantage for rank-deficient symmetric matrices
A_sing = np.outer(v1, v1)  # rank-1 symmetric matrix

print(np.linalg.matrix_rank(A_sing))

# 1  (rank-deficient)

print(spla.pinvh(A_sing).round(4))

# pseudoinverse of rank-deficient symmetric matrix (np.linalg.inv would fail)

#-------------------------------------------------------------------------------------------------#
#--------------------------- 6. Matrix functions  (scipy.linalg) ---------------------------------#
#-------------------------------------------------------------------------------------------------#

#################
## spla.expm() ##
#################

'''
spla.expm() computes the matrix exponential e^A.

NOT element-wise (that would be np.exp(A)).
e^A is defined via the Taylor series: I + A + A^2/2! + A^3/3! + ...

Key application: solving ODEs  dx/dt = A x  → x(t) = expm(A*t) @ x(0)
Also used in graph theory, quantum mechanics, and continuous-time Markov chains.
'''

A_skew = np.array([[0.,  1.],
                   [-1., 0.]])   # skew-symmetric generator of 2D rotation

print(spla.expm(A_skew))

# [[ 0.5403  0.8415]
#  [-0.8415  0.5403]]
# = [[cos(1)  sin(1)]
#    [-sin(1) cos(1)]]  (rotation matrix by 1 radian!)

# expm(t * A_skew) traces out a rotation by t radians
print(spla.expm(np.pi * A_skew).round(4))

# [[-1.  0.]    (rotation by π = 180°)
#  [-0. -1.]]   ≈ -I

# expm and logm are inverses
print(np.allclose(spla.expm(spla.logm(A)), A))

# True

#################
## spla.logm() ##
#################

'''
spla.logm() computes the principal matrix logarithm log(A), the inverse of expm().

Requires A to be non-singular and have no negative real eigenvalues.

Applications: interpolation between matrices (geodesics on matrix manifolds),
diffusion tensor imaging (DTI), SE(3) Lie group operations in robotics/structure prediction.
'''

print(spla.logm(np.eye(3)).round(4))

# [[0. 0. 0.]
#  [0. 0. 0.]
#  [0. 0. 0.]]  (log of identity = zero matrix)

# Log of a rotation matrix gives the rotation generator
R = spla.expm(np.pi/4 * A_skew)  # rotation by 45°
print(spla.logm(R).round(4))

# [[ 0.     0.7854]
#  [-0.7854 0.    ]]  (= pi/4 * A_skew, recovers the generator)

# expm ∘ logm = identity
print(np.allclose(spla.expm(spla.logm(A)), A))

# True

##################
## spla.sqrtm() ##
##################

'''
spla.sqrtm() computes the matrix square root S such that S @ S = A.

For diagonal matrices, sqrtm is the element-wise square root of the diagonal.
For SPD matrices, the result is also symmetric positive definite.

Application: computing geodesic means of covariance matrices, whitening transforms.
'''

A_diag = np.array([[4., 0.],
                   [0., 9.]])

print(spla.sqrtm(A_diag))

# [[2. 0.]
#  [0. 3.]]  (element-wise sqrt for diagonal matrices)

S = spla.sqrtm(A)

print(np.allclose(S @ S, A))

# True  (S @ S = A)

# Whitening: X_white = sqrtm(inv(Sigma)) @ X  so X_white has identity covariance

##################
## spla.funm()  ##
##################

'''
spla.funm(A, func) applies an arbitrary scalar function to a matrix via its Schur decomposition.

Uses the formula: funm(A) = Z @ diag(func(eigenvalues)) @ Z.H  (for diagonalizable A)
Can be used to compute any matrix function: sin, cos, etc.
'''

print(spla.funm(A_skew, np.sin).round(4))

# [[ 0.      1.1752]
#  [-1.1752 -0.    ]]  (matrix sine; sinh(1) ≈ 1.1752)

print(spla.funm(A, np.sqrt).round(4))

# matrix square root (equivalent to sqrtm for valid inputs)

print(np.allclose(spla.funm(A, np.exp), spla.expm(A)))

# True  (funm with np.exp reproduces expm)

#-------------------------------------------------------------------------------------------------#
#----------------------- 7. Matrix equation solvers  (scipy.linalg) ------------------------------#
#-------------------------------------------------------------------------------------------------#

###########################
## spla.solve_sylvester() ##
###########################

'''
spla.solve_sylvester(A, B, Q) solves the Sylvester equation: AX + XB = Q

A is (m×m), B is (n×n), Q is (m×n), X is the unknown (m×n).

Applications: control theory (Lyapunov stability), decoupling of ODEs,
pole placement in linear systems.
'''

A_s = np.array([[1., 0.],
                [0., 2.]])

B_s = np.array([[3., 0.],
                [0., 4.]])

Q_s = np.array([[1., 1.],
                [1., 1.]])

X_s = spla.solve_sylvester(A_s, B_s, Q_s)

print(X_s)

# [[0.25        0.2        ]
#  [0.2         0.16666667]]

print(A_s @ X_s + X_s @ B_s)

# [[1. 1.]
#  [1. 1.]]  (verifies AX + XB = Q)

#####################################
## spla.solve_continuous_lyapunov() ##
#####################################

'''
spla.solve_continuous_lyapunov(A, Q) solves the continuous Lyapunov equation: AX + XA^H = Q

Special case of the Sylvester equation with B = A^H.
A solution X exists and is unique if A has no eigenvalues that are negatives of each other.

Applications:
  - Stability analysis of linear dynamical systems.
  - Computing the steady-state covariance of a stochastic system dx = Ax dt + dW.
  - Gramians in model order reduction.
'''

A_l = np.array([[-1., 0.],
                [ 0., -2.]])   # stable matrix (all eigenvalues have negative real parts)

Q_l = np.array([[1., 0.],
                [0., 1.]])     # identity: input covariance (or desired Gramian)

X_l = spla.solve_continuous_lyapunov(A_l, Q_l)

print(X_l)

# [[-0.5   0.  ]
#  [ 0.   -0.25]]

print(A_l @ X_l + X_l @ A_l.T)

# [[1. 0.]
#  [0. 1.]]  (verifies AX + XA.T = Q)

# Interpretation: X_l is the steady-state covariance of dx = A_l @ x dt + dW

#-------------------------------------------------------------------------------------------------#
#--------------------------- 8. Special matrices  (scipy.linalg) ---------------------------------#
#-------------------------------------------------------------------------------------------------#

#####################
## spla.block_diag() ##
#####################

'''
spla.block_diag(*arrs) constructs a block-diagonal matrix from the input arrays.

Each input array becomes a block on the diagonal; off-diagonal blocks are zero.
Inputs can have different shapes.
'''

B1 = np.array([[1, 2], [3, 4]])
B2 = np.array([[5, 6], [7, 8]])
B3 = np.array([[9]])

BD = spla.block_diag(B1, B2, B3)

print(BD)

# [[1 2 0 0 0]
#  [3 4 0 0 0]
#  [0 0 5 6 0]
#  [0 0 7 8 0]
#  [0 0 0 0 9]]

# Common use: block-diagonal covariance matrices, independent subsystems
BD_eye = spla.block_diag(np.eye(2), np.eye(3))

print(BD_eye.shape)

# (5, 5)  (block identity)

####################
## spla.toeplitz() ##
####################

'''
spla.toeplitz(c, r) constructs a Toeplitz matrix.

A Toeplitz matrix has constant diagonals: T[i,j] = c[i-j] (or r[j-i] for upper part).
If only c is given: a symmetric Toeplitz matrix is constructed.

Applications: time-series analysis, convolution operations, signal processing.
'''

print(spla.toeplitz([1, 2, 3, 4]))

# [[1 2 3 4]
#  [2 1 2 3]
#  [3 2 1 2]
#  [4 3 2 1]]  (symmetric: diagonals are constant)

# Asymmetric: c defines the first column, r defines the first row
print(spla.toeplitz(c=[1, 2, 3], r=[1, 4, 5]))

# [[1 4 5]
#  [2 1 4]
#  [3 2 1]]

#####################
## spla.circulant() ##
#####################

'''
spla.circulant(c) constructs a circulant matrix from the first column c.

Each subsequent column is the previous column shifted down by one position (cyclically).
Circulant matrices are simultaneously diagonalizable by the DFT matrix:
  C = F^H @ diag(F @ c) @ F

Applications: cyclic convolution, periodic boundary conditions, signal filtering.
'''

print(spla.circulant([1, 2, 3]))

# [[1 3 2]
#  [2 1 3]
#  [3 2 1]]  (each row is a cyclic shift of the previous)

# Eigenvectors of any circulant matrix are the DFT basis vectors
c_vec = np.array([3., 1., 0., 1.])
C = spla.circulant(c_vec)
evals_C = np.fft.fft(c_vec)  # eigenvalues are the DFT of the first column!

print(np.allclose(np.linalg.eigvals(C), evals_C[[0, 3, 2, 1]]))  # (up to ordering)

####################
## spla.hilbert()  ##
####################

'''
spla.hilbert(n) constructs the n×n Hilbert matrix: H[i,j] = 1 / (i + j - 1)

The Hilbert matrix is symmetric positive definite, but famously ill-conditioned:
its condition number grows exponentially with n, making it a classic test case for
numerical algorithms.

scipy.linalg.invhilbert(n) provides the exact integer inverse for comparison.
'''

print(spla.hilbert(3))

# [[1.     0.5    0.3333]
#  [0.5    0.3333 0.25  ]
#  [0.3333 0.25   0.2   ]]

# Condition numbers explode with size
for n in [3, 5, 7, 10]:
    H_n = spla.hilbert(n)
    print(f"hilbert({n:2d})  cond = {np.linalg.cond(H_n):.2e}")

# hilbert( 3)  cond = 5.24e+02
# hilbert( 5)  cond = 4.77e+05
# hilbert( 7)  cond = 4.75e+08
# hilbert(10)  cond = 1.60e+13  (nearly singular at double precision)

# Exact inverse (avoids floating-point error using integer arithmetic)
print(spla.invhilbert(3))

# [[ 9. -36.  30.]
#  [-36. 192. -180.]
#  [ 30. -180. 180.]]
