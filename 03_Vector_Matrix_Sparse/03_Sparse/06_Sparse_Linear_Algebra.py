'''
scipy.sparse - Sparse Linear Algebra

1. Solving Linear Systems:
   + spsolve(): Direct solver for Ax = b
   + factorized(): LU factorization for multiple solves
   + splu() and spilu(): LU decompositions

2. Iterative Solvers:
   + cg(): Conjugate gradient (symmetric positive definite)
   + gmres(): Generalized minimal residual
   + bicgstab(): Biconjugate gradient stabilized
   + minres(): Minimum residual
   + lgmres(), gcrotmk(): Advanced iterative methods

3. Eigenvalue Problems:
   + eigs(): General eigenvalues (ARPACK)
   + eigsh(): Symmetric/Hermitian eigenvalues
   + svds(): Singular value decomposition

4. Matrix Norms and Properties:
   + norm(): Various matrix norms
   + Matrix properties: condition number, rank

5. Matrix Decompositions:
   + LU decomposition
   + Incomplete LU (ILU) for preconditioning
   + QR decomposition (limited support)

6. Preconditioners:
   + LinearOperator: Custom preconditioners
   + spilu(): Incomplete LU preconditioner
   + Using preconditioners with iterative solvers
'''

import numpy as np
from scipy import sparse
from scipy.sparse import csr_array, diags_array
from scipy.sparse.linalg import (
    spsolve, factorized, splu, spilu,
    cg, gmres, bicgstab,
    eigs, eigsh, svds,
    norm, LinearOperator
)


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 1. Solving Linear Systems --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

###############################
## spsolve() - Direct solver ##
###############################
'''
Solve Ax = b directly using sparse LU factorization
Best for: Small to medium systems, single solve
'''

# Create a simple system: Ax = b
A = csr_array([[4, 1, 0],
               [1, 4, 1],
               [0, 1, 4]], dtype=float)

b = np.array([1, 2, 3], dtype=float)

# Solve using spsolve
x = spsolve(A, b)
print(f"\nSolution x: {x}")
# Solution x: [0.17857143 0.28571429 0.67857143]

# Verify solution
residual = np.linalg.norm(A @ x - b)
print(f"Residual ||Ax - b||: {residual:.2e}") # 4.44e-16

###########################################
## factorized() - Reusable factorization ##
###########################################
'''
Factorize once using LU, solve multiple times
Best for: Multiple solves with same A, different b
'''

# Factorize A once
solve = factorized(A.tocsc()) # This function requires CSC format

# Solve for multiple right-hand sides
b1 = np.array([1, 0, 0], dtype=float)
b2 = np.array([0, 1, 0], dtype=float)
b3 = np.array([0, 0, 1], dtype=float)

x1 = solve(b1)
x2 = solve(b2)
x3 = solve(b3)

print("Solution for b = [1, 0, 0]:", x1) # [ 0.26785714 -0.07142857  0.01785714]
print("Solution for b = [0, 1, 0]:", x2) # [-0.07142857  0.28571429 -0.07142857]
print("Solution for b = [0, 0, 1]:", x3) # [ 0.01785714 -0.07142857  0.26785714]

# These solutions are actually columns of A^(-1)
A_inv_approx = np.column_stack([x1, x2, x3])
print(A_inv_approx.round(4))
# [[ 0.2679 -0.0714  0.0179]
#  [-0.0714  0.2857 -0.0714]
#  [ 0.0179 -0.0714  0.2679]]

print((A_inv_approx @ A).round(2))
# [[1. 0. 0.]
#  [0. 1. 0.]
#  [0. 0. 1.]]

########################################
## splu() - Explicit LU decomposition ##
########################################
'''
Get explicit LU factors
Provides more control over the factorization
'''

lu = splu(A.tocsc()) # LU requires CSC format

print(f"LU object: {lu}") # <SuperLU object at 0x767000dfbb40>
print(f"Shape: {lu.shape}") # (3, 3)

# Solve using LU factors
x_lu = lu.solve(b)
print(f"\nSolution using LU: {x_lu}")
# [0.17857143 0.28571429 0.67857143]

# Access L and U factors
L = lu.L
U = lu.U

print(L.toarray())
# [[1.         0.         0.        ]
#  [0.25       1.         0.        ]
#  [0.         0.26666667 1.        ]]

print(U.toarray())
# [[4.         1.         0.        ]
#  [0.         3.75       1.        ]
#  [0.         0.         3.73333333]]

###########################
## Larger system example ##
###########################
'''
Solve a larger tridiagonal system
Common in discretized differential equations
'''

n = 100
# Tridiagonal matrix: -1, 2, -1
main_diag = np.ones(n) * 2
off_diag = np.ones(n-1) * -1
A_large = diags_array([off_diag, main_diag, off_diag],
                       offsets=[-1, 0, 1],
                       format='csc')
'''
A_large looks like:
array([[ 2., -1.,  0., ...,  0.,  0.,  0.],
       [-1.,  2., -1., ...,  0.,  0.,  0.],
       [ 0., -1.,  2., ...,  0.,  0.,  0.],
       ...,
       [ 0.,  0.,  0., ...,  2., -1.,  0.],
       [ 0.,  0.,  0., ..., -1.,  2., -1.],
       [ 0.,  0.,  0., ...,  0., -1.,  2.]], shape=(100, 100))
'''

b_large = np.ones(n)
b_large[0] = 0
b_large[-1] = 0
'''
b_large looks like:
array([0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
       1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0.])
'''

x_large = spsolve(A_large, b_large)

print(f"System size: {n}x{n}") # 100x100
print(f"Solution (first 5): {x_large[:5]}") # [ 49.  98. 146. 193. 239.]
print(f"Solution (last 5): {x_large[-5:]}") # [239. 193. 146.  98.  49.]

print(f"Residual: {np.linalg.norm(A_large @ x_large - b_large):.2e}") # Residual: 1.24e-12


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 2. Iterative Solvers -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

###############################
## cg() - Conjugate Gradient ##
###############################
'''
cg(): Conjugate Gradient Method

For symmetric positive definite matrices
Fast convergence for well-conditioned systems
Returns (solution, info) where info=0 means success
'''

# Create symmetric positive definite (SPD) matrix
n = 50
A_spd = diags_array([np.ones(n-1), np.ones(n)*3, np.ones(n-1)],
                    offsets=[-1, 0, 1], format='csr')

b_spd = np.random.rand(n)

# Solve with CG
x_cg, info = cg(A_spd, b_spd, rtol=1e-6)

print(f"System size: {n}x{n}") # 50x50
print(f"Convergence info: {info} (0 = success)") # 0
print(f"Solution norm: {np.linalg.norm(x_cg):.4f}") # 1.1108
print(f"Residual: {np.linalg.norm(A_spd @ x_cg - b_spd):.2e}") # 3.44e-06

# With iteration callback
iterations = []
def callback(xk):
    iterations.append(np.linalg.norm(A_spd @ xk - b_spd))

x_cg2, info2 = cg(A_spd, b_spd, rtol=1e-6, callback=callback)
print(f"Number of iterations: {len(iterations)}")
print(f"Residual history (first 5): {[f'{r:.2e}' for r in iterations[:5]]}")
# Residual history (first 5): ['9.42e-01', '3.67e-01', '1.48e-01', '5.85e-02', '2.20e-02']

#####################
## gmres() - GMRES ##
#####################
'''
gmres(): Generalized Minimal Residual

Generalized Minimal Residual method
Works for general non-symmetric systems
More memory intensive than CG
'''

# Non-symmetric system
A_nonsym = csr_array([[5, 2, 0, 0],
                      [1, 4, 1, 0],
                      [0, 2, 5, 1],
                      [0, 0, 1, 3]], dtype=float)

b_nonsym = np.array([1, 2, 3, 4], dtype=float)

x_gmres, info = gmres(A_nonsym, b_nonsym, rtol=1e-6)

print(f"Convergence info: {info}") # 0 (success)
print(f"Solution: {x_gmres}") # [0.01801802 0.45495495 0.16216216 1.27927928]
print(f"Residual: {np.linalg.norm(A_nonsym @ x_gmres - b_nonsym):.2e}") # 2.00e-15

###########################
## bicgstab() - BiCGSTAB ##
###########################
'''
bicgstab(): BiCGSTAB Method

Biconjugate Gradient Stabilized
Often faster than GMRES for non-symmetric systems
Less memory intensive
'''

x_bicg, info = bicgstab(A_nonsym, b_nonsym, rtol=1e-6)

print(f"Convergence info: {info}") # 0 (success)
print(f"Solution: {x_bicg}") # [0.01801802 0.45495495 0.16216216 1.27927928]
print(f"Residual: {np.linalg.norm(A_nonsym @ x_bicg - b_nonsym):.2e}") # 9.22e-16

#####################################
## Comparison: Direct vs Iterative ##
#####################################

import time

n = 500
A_compare = diags_array([np.ones(n-1), np.ones(n)*4, np.ones(n-1)],
                        offsets=[-1, 0, 1], format='csr')
b_compare = np.ones(n)

# Direct solver
start = time.time()
x_direct = spsolve(A_compare, b_compare)
time_direct = time.time() - start

# Iterative solver (CG)
start = time.time()
x_iter, info = cg(A_compare, b_compare, rtol=1e-6)
time_iter = time.time() - start

print(f"\nDirect solver time: {time_direct*1000:.2f} ms") # 0.58 ms
print(f"Iterative solver time: {time_iter*1000:.2f} ms") # 0.53 ms

print(f"Direct residual: {np.linalg.norm(A_compare @ x_direct - b_compare):.2e}") # 2.38e-15
print(f"Iterative residual: {np.linalg.norm(A_compare @ x_iter - b_compare):.2e}") # 2.17e-05


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 3. Eigenvalue Problems -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

#####################################
## eigsh() - Symmetric eigenvalues ##
#####################################
'''
eigsh(): Symmetric Eigenvalue Problems

Compute a few eigenvalues/eigenvectors of symmetric matrix
Uses ARPACK (implicitly restarted Arnoldi method)
Much faster than dense methods for large sparse matrices
'''

# Create symmetric matrix
n = 100
A_sym = diags_array([np.ones(n-1)*-1, np.ones(n)*2, np.ones(n-1)*-1],
                    offsets=[-1, 0, 1], format='csr')

# Compute smallest 5 eigenvalues
k = 5
eigenvalues, eigenvectors = eigsh(A_sym, k=k, which='SM')

print(f"Matrix size: {n}x{n}") # 100x100
print(f"Eigenvalues: {eigenvalues}") # [0.00096744 0.00386881 0.0087013  0.01546026 0.02413912]
print(f"Eigenvectors shape: {eigenvectors.shape}") # (100, 5)
# print(f"Eigenvectors:\n{eigenvectors}")

# Verify first eigenpair
lam0, v0 = eigenvalues[0], eigenvectors[:, 0]
residual = np.linalg.norm(A_sym @ v0 - lam0 * v0)
print(f"\nFirst eigenpair residual: {residual:.2e}") # 1.90e-15

# Compute largest eigenvalues
eigenvalues_large, _ = eigsh(A_sym, k=k, which='LM') # LM means Largest Magnitude
print(f"\nLargest {k} eigenvalues: {eigenvalues_large}")
# [3.97586088 3.98453974 3.9912987  3.99613119 3.99903256]

##################################
## eigs() - General eigenvalues ##
##################################
'''
eigs(): General Eigenvalue Problems

For non-symmetric matrices
Can compute complex eigenvalues
'''

# Non-symmetric matrix
A_gen = csr_array([[4, 1, 0, 0, 0],
                   [1, 4, 1, 0, 0],
                   [0, 2, 4, 1, 0],
                   [0, 0, 1, 4, 1],
                   [0, 0, 0, 2, 4]], dtype=float)

# Compute 3 eigenvalues with largest magnitude
k = 3
eigenvalues_gen, eigenvectors_gen = eigs(A_gen, k=k, which='LM')

print(f"Eigenvalues: {eigenvalues_gen.real}") # [6.10100299 4.         5.25928013]
print(f"Imaginary parts: {eigenvalues_gen.imag}") # [0. 0. 0.]

###########################################
## svds() - Singular Value Decomposition ##
###########################################
'''
svds(): Sparse SVD

Compute a few singular values and vectors
Useful for dimensionality reduction, matrix approximation
'''

# Create rectangular matrix
m, n = 100, 50
np.random.seed(42)
A_rect = sparse.random(m, n, density=0.1, format='csr')

# Compute k largest singular values
k = 5
U, s, Vt = svds(A_rect, k=k, which='LM')

print(f"Matrix shape: {A_rect.shape}") # (100, 50)
print(f"Singular values: {s[::-1]}")  # [4.13844787 3.00104187 2.90801928 2.75496175 2.64393314]
                                      # svds returns in ascending order
print(f"U shape: {U.shape}") # (100, 5)
print(f"Vt shape: {Vt.shape}") # (5, 50)

# Reconstruct low-rank approximation
s_sorted = s[::-1]
U_sorted = U[:, ::-1]
Vt_sorted = Vt[::-1, :]
A_approx = U_sorted @ np.diag(s_sorted) @ Vt_sorted

reconstruction_error = np.linalg.norm(A_rect.toarray() - A_approx, 'fro')
print(f"\nReconstruction error (Frobenius): {reconstruction_error:.4f}") # 10.2996


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------- 4. Matrix Norms and Properties -------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

##################
## Matrix norms ##
##################
'''Compute various matrix norms'''

A_norm = csr_array([[1, 0, 2],
                    [0, 3, 0],
                    [4, 0, 5]])

# Different norms
frobenius = norm(A_norm, 'fro')
inf_norm = norm(A_norm, np.inf)
one_norm = norm(A_norm, 1)

print(f"\nFrobenius norm: {frobenius:.4f}") # 7.4162
print(f"Infinity norm (max row sum): {inf_norm:.4f}") # 9.0000
print(f"1-norm (max column sum): {one_norm:.4f}") # 7.0000

###############################
## Condition number estimate ##
###############################
'''
Estimate condition number
High condition number indicates ill-conditioned system

#################

Condition number κ(A) = ||A|| * ||A^(-1)||
This indicates sensitivity of solution to perturbations
'''

# Well-conditioned matrix
A_good = diags_array([1, 2, 3, 4, 5])
eigs_good = eigsh(A_good, k=2, which='BE', return_eigenvectors=False)
cond_good = max(abs(eigs_good)) / min(abs(eigs_good))

print(f"Well-conditioned matrix condition number: {cond_good:.2f}") # 5.00

# Ill-conditioned matrix (nearly singular)
A_bad = diags_array([1, 1.00001, 2, 3, 0.00001])
eigs_bad = eigsh(A_bad, k=2, which='BE', return_eigenvectors=False)
cond_bad = max(abs(eigs_bad)) / min(abs(eigs_bad))

print(f"Ill-conditioned matrix condition number: {cond_bad:.2e}") # 3.00e+05


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 5. Matrix Decompositions --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

######################
## LU Decomposition ##
######################
'''
LU factorization: A = PLU
P: permutation, L: lower triangular, U: upper triangular
'''

A_lu = csr_array([[2, 1, 1],
                  [4, 3, 3],
                  [8, 7, 9]], dtype=float)

lu_factors = splu(A_lu)

# Access factors
L = lu_factors.L
U = lu_factors.U
P = sparse.csr_array((np.ones(A_lu.shape[0]),
                      (lu_factors.perm_r, np.arange(A_lu.shape[0]))))

print(L.toarray())
# [[1.         0.         0.        ]
#  [0.25       1.         0.        ]
#  [0.5        0.66666667 1.        ]]

print(U.toarray())
# [[ 8.          7.          9.        ]
#  [ 0.         -0.75       -1.25      ]
#  [ 0.          0.         -0.66666667]]

# Verify: PA = LU
PA = P @ A_lu
LU = L @ U
error = np.linalg.norm((PA - LU).toarray(), 'fro')
print(f"\nLU decomposition error ||PA - LU||: {error:.2e}") # 4.44e-16

#########################
## Incomplete LU (ILU) ##
#########################
'''
Incomplete LU (ILU)

Approximate LU factorization
Maintains sparsity pattern
Used for preconditioning iterative solvers
'''

n = 50
A_ilu = diags_array([np.ones(n-1)*-1, np.ones(n)*3, np.ones(n-1)*-1],
                    offsets=[-1, 0, 1], format='csr')

# Compute ILU
ilu = spilu(A_ilu.tocsc())

print(f"Matrix size: {n}x{n}") # 50x50
print(f"Original nnz: {A_ilu.nnz}") # 148
print(f"ILU L nnz: {ilu.L.nnz}") # 98
print(f"ILU U nnz: {ilu.U.nnz}") # 98

# np.set_printoptions(linewidth=120)
# print(ilu.L.toarray())
# print(ilu.U.toarray())


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 6. Preconditioners -------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

#################################
## Using ILU as preconditioner ##
#################################
'''
Preconditioners accelerate iterative solver convergence
ILU is a common preconditioner
'''

# Create difficult system
n = 100
A_difficult = diags_array([np.ones(n-1)*-0.5, np.ones(n)*2, np.ones(n-1)*-0.5],
                          offsets=[-1, 0, 1], format='csr')

# Add some randomness to make it harder
A_difficult = A_difficult + sparse.random(n, n, density=0.01, format='csr')
A_difficult = (A_difficult + A_difficult.T) / 2  # Make symmetric

b_difficult = np.ones(n)

# Solve without preconditioner
iterations_no_prec = []
def callback_no_prec(xk):
    iterations_no_prec.append(len(iterations_no_prec))

x_no_prec, info1 = cg(A_difficult, b_difficult, rtol=1e-6,
                      callback=callback_no_prec, maxiter=500)

# Solve with ILU preconditioner
ilu_prec = spilu(A_difficult.tocsc())

# Create LinearOperator for preconditioner
M = LinearOperator(A_difficult.shape, matvec=ilu_prec.solve)

iterations_with_prec = []
def callback_with_prec(xk):
    iterations_with_prec.append(len(iterations_with_prec))

x_with_prec, info2 = cg(A_difficult, b_difficult, M=M, rtol=1e-6,
                        callback=callback_with_prec, maxiter=500)

print(f"Without preconditioner: {len(iterations_no_prec)} iterations, info={info1}")
# Without preconditioner: 15 iterations, info=0

print(f"With ILU preconditioner: {len(iterations_with_prec)} iterations, info={info2}")
# With ILU preconditioner: 2 iterations, info=0

print(f"Speedup: {len(iterations_no_prec) / len(iterations_with_prec):.1f}x")
# Speedup: 7.5x

###########################
## Custom LinearOperator ##
###########################
'''
Create custom operators for matrix-free methods
Useful when matrix is too large to store
'''

# Define matrix-vector product without storing matrix
def matvec(v):
    """Compute Av for tridiagonal matrix"""
    n = len(v)
    result = np.zeros(n)
    result[0] = 2*v[0] - v[1]
    for i in range(1, n-1):
        result[i] = -v[i-1] + 2*v[i] - v[i+1]
    result[n-1] = -v[n-2] + 2*v[n-1]
    return result

n = 20
A_op = LinearOperator((n, n), matvec=matvec)

b_op = np.ones(n)
x_op, info = cg(A_op, b_op, rtol=1e-6)

print(f"LinearOperator size: {A_op.shape}") # (20, 20)
print(f"Solution converged: {info == 0}") # True
print(f"Solution (first 5): {x_op[:5]}") # [10. 19. 27. 34. 40.]
