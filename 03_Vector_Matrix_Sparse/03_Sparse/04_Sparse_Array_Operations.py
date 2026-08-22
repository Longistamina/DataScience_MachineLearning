'''
scipy.sparse - Sparse Array Operations

1. Arithmetic Operations:
   + Addition and subtraction: A + B, A - B
   + Scalar multiplication: scalar * A
   + Element-wise multiplication: A.multiply(B)
   + Matrix multiplication: A @ B or A.dot(B)
   + Division: A / scalar
   + Power: A.power(n)

2. Matrix Products:
   + Matrix-vector product: A @ v
   + Matrix-matrix product: A @ B
   + Transpose products: A.T @ B

3. Reductions and Aggregations:
   + Sum, mean, max, min over axes
   + Matrix norms
   + Counting non-zeros

4. Element-wise Operations:
   + Absolute value: abs(A)
   + Sign, ceil, floor, round
   + Mathematical functions (with limitations)

5. Comparison Operations:
   + Element-wise comparisons
   + Maximum and minimum

6. Special Operations:
   + Conjugate and transpose
   + Diagonal extraction
   + Trace
'''

import numpy as np
from scipy.sparse import csr_array
from scipy.sparse.linalg import norm


# =========================================================================================
# 1. Arithmetic Operations
# =========================================================================================

##---------------------##
## Setup test matrices ##
##---------------------##

A = csr_array([[1, 0, 2],
               [0, 3, 0],
               [4, 0, 5]])

B = csr_array([[2, 0, 1],
               [0, 1, 0],
               [1, 0, 2]])

print(A.toarray())
# [[1 0 2]
#  [0 3 0]
#  [4 0 5]]

print(B.toarray())
# [[2 0 1]
#  [0 1 0]
#  [1 0 2]]

##--------------------------##
## Addition and Subtraction ##
##--------------------------##
'''
Addition and subtraction work element-wise
Result is typically in CSR format
Both matrices must have the same shape
'''

print("\n--- Addition and Subtraction ---")

C_add = A + B
print(C_add.toarray())
# [[3 0 3]
#  [0 4 0]
#  [5 0 7]]

C_sub = A - B
print(C_sub.toarray())
# [[-1  0  1]
#  [ 0  2  0]
#  [ 3  0  3]]

##-----------------------##
## Scalar Multiplication ##
##-----------------------##
'''
Multiply sparse matrix by a scalar
Very efficient - only multiplies stored elements
'''

C_scaled = 3 * A
print(C_scaled.toarray())
# [[ 3  0  6]
#  [ 0  9  0]
#  [12  0 15]]

C_scaled2 = A * 0.5
print(C_scaled2.toarray())
# [[0.5 0.  1. ]
#  [0.  1.5 0. ]
#  [2.  0.  2.5]]

##-----------------------------##
## Element-wise Multiplication ##
##-----------------------------##
'''
Element-wise (Hadamard) product using .multiply()
Regular * operator also works for sparse arrays
'''

C_elemwise = A.multiply(B)
print(C_elemwise.toarray())
# [[2 0 2]
#  [0 3 0]
#  [4 0 10]]

# Alternative: using * operator
C_elemwise2 = A * B
print(C_elemwise2.toarray())
# [[ 2  0  2]
#  [ 0  3  0]
#  [ 4  0 10]]

##----------##
## Division ##
##----------##
'''
Division by scalar
Note: Division by sparse array not directly supported
'''

C_div = A / 2
print(C_div.toarray())
# [[0.5 0.  1. ]
#  [0.  1.5 0. ]
#  [2.  0.  2.5]]

##-------##
## Power ##
##-------##
'''
Raise each element to a power
Use .power(n) method
'''

C_power = A.power(2)
print(C_power.toarray())
# [[ 1  0  4]
#  [ 0  9  0]
#  [16  0 25]]

C_power3 = A.power(3)
print(C_power3.toarray())
# [[  1   0   8]
#  [  0  27   0]
#  [ 64   0 125]]

# Square root
C_sqrt = A.power(0.5)
print(C_sqrt.toarray().round(3))
# [[1.    0.    1.414]
#  [0.    1.732 0.   ]
#  [2.    0.    2.236]]


# =========================================================================================
# 2. Matrix Products
# =========================================================================================

C = csr_array([[3, 0],
               [0, 0],
               [1, 4]])

##-----------------------##
## Matrix-Matrix Product ##
##-----------------------##
'''
Standard matrix multiplication using @ or .dot()
Result is usually CSR format
'''

# Using @ operator (Python 3.5+)
C_matmul = A @ C
print(C_matmul.toarray())
# [[ 5  8]
#  [ 0  0]
#  [17 20]]

# Using .dot() method
C_dot = A.dot(C)
print(C_dot.toarray())
# [[ 5  8]
#  [ 0  0]
#  [17 20]]

##-----------------------##
## Matrix-Vector Product ##
##-----------------------##
'''
Multiply matrix by vector
Very efficient for CSR format
Result is a dense numpy array
'''

v = np.array([1, 2, 3])
result = A @ v
print(result)
# [ 7  6 19]

# Also works with column vectors
v_col = np.array([[1], [2], [3]])
result_col = A @ v_col
print(result_col)
# [[ 7]
#  [ 6]
#  [19]]

##--------------------##
## Transpose Products ##
##--------------------##
'''
Transpose using .T property
Transpose is efficient - just changes format (CSR <-> CSC)
'''

print(A.T.toarray())
# [[1 0 4]
#  [0 3 0]
#  [2 0 5]]

AT_C = A.T @ C
print(AT_C.toarray())
# [[ 7 16]
#  [ 0  0]
#  [11 20]]

A_AT = A @ A.T
print(A_AT.toarray())
# [[ 5  0  14]
#  [ 0  9   0]
#  [14  0  41]]


# =========================================================================================
# 3. Reductions and Aggregations
# =========================================================================================

##---------------------##
## Sum, Mean, Max, Min ##
##---------------------##
'''
Reduction operations over entire array or specific axis
Result is dense array when reducing over an axis
'''

print("Sum of all elements:", A.sum())  # 15
print("Mean of all elements:", A.mean())  # 1.6667
print("Max element:", A.max())  # 5
print("Min element:", A.min())  # 0

# Sum over axes
print(A.sum(axis=0))  # [5 3 7] (vertical)
print(A.sum(axis=1))  # [3 3 9] (horizontal)

# Mean over axes
print(A.mean(axis=0)) # [1.66666667 1.         2.33333333] (vertical)
print(A.mean(axis=1)) # [1.         1.         3.        ] (horizontal)

# Max over axes
print(A.max(axis=0).toarray()) # [4 3 5] (vertical)
print(A.max(axis=1).toarray()) # [2 3 5] (horizontal)

##--------------------##
## Counting non-zeros ##
##--------------------##
'''Different ways to count non-zero elements'''

# Total non-zeros
print(A.nnz) # 5
print(A.count_nonzero()) # 5

# Non-zeros per column
nnz_per_col = np.diff(A.tocsc().indptr)
print(nnz_per_col)  # [2 1 2]

# Non-zeros per row
nnz_per_row = np.diff(A.tocsr().indptr)
print(nnz_per_row)  # [2 1 2]

##--------------##
## Matrix Norms ##
##--------------##
'''Compute various matrix norms using scipy.sparse.linalg.norm'''

print("Frobenius norm:", norm(A, 'fro'))
# 7.416 (sqrt(1^2+0^2+2^2+0^2+3^2+0^2+4^2+0^2+5^2) = sqrt(55))

print("Infinity norm (max row sum):", norm(A, np.inf))
# 9.0 (max row sum: row 3 -> 4+5=9)

print("1-norm (max column sum):", norm(A, 1))  # 7.0
# 7.0 (max column sum: col 3 -> 2+5=7)


# =========================================================================================
# 4. Element-wise Operations
# =========================================================================================

##----------------##
## Absolute Value ##
##----------------##
'''Take absolute value of all elements'''

A_neg = csr_array([[-1, 0, 2],
                   [0, -3, 0],
                   [4, 0, -5]])

A_abs = abs(A_neg)
print(A_abs.toarray())
# [[1 0 2]
#  [0 3 0]
#  [4 0 5]]

##-------------------##
## Sign, Ceil, Floor ##
##-------------------##
'''
Apply mathematical functions
Note: These create dense results in some cases
'''

A_float = csr_array([[-1.5, 0, 2.3],
                     [0, 3.7, 0],
                     [4.2, 0, -5.9]])

# Original
print(A_float.toarray())
# [[-1.5  0.   2.3]
#  [ 0.   3.7  0. ]
#  [ 4.2  0.  -5.9]]

# Sign
A_sign = A_float.sign()
print(A_sign.toarray())
# [[-1.  0.  1.]
#  [ 0.  1.  0.]
#  [ 1.  0. -1.]]

# Ceil
A_ceil = A_float.ceil()
print(A_ceil.toarray())
# [[-1.  0.  3.]
#  [ 0.  4.  0.]
#  [ 5.  0. -5.]]

# Floor
A_floor = A_float.floor()
print(A_floor.toarray())
# [[-2.  0.  2.]
#  [ 0.  3.  0.]
#  [ 4.  0. -6.]]

##---------------------##
## Exponential and Log ##
##---------------------##
'''
Exponential functions
NOTE: only has expm1() for sparse arrays

expm1 means exp_minus_1 = exp(x) - 1
'''

A_small = csr_array([[0, 1], [2, 0]])
print(A_small.toarray())
# [[0 1]
#  [2 0]]

# expm1() is better: exp(x) - 1, keeps zeros as zeros
A_expm1 = A_small.expm1()
print(A_expm1.toarray().round(3))
# [[0.    1.718]
#  [6.389 0.   ]]
'''
exp(0) = 1
=> expm1(0) = 1 - 1 = 0
=> preserves sparsity
'''


# =========================================================================================
# 5. Comparison Operations
# =========================================================================================

##--------------------------##
## Element-wise Comparisons ##
##--------------------------##
'''
Compare sparse matrices element-wise
Returns sparse matrix of booleans (True or False)
'''

A_comp = csr_array([[1, 0, 3],
                    [0, 2, 0],
                    [4, 0, 1]])

B_comp = csr_array([[2, 0, 3],
                    [0, 1, 0],
                    [3, 0, 2]])

# Greater than
comparison = A_comp > B_comp
print(comparison.toarray())
# [[False False False]
#  [False  True False]
#  [ True False False]]

# Equal to
comparison_eq = A_comp == 3
print(comparison_eq.toarray())
# [[False False  True]
#  [False False False]
#  [False False False]]

# Not equal
comparison_ne = A_comp != 0
print(comparison_ne.toarray())
# [[ True False  True]
#  [False  True False]
#  [ True False  True]]

##---------------------##
## Maximum and Minimum ##
##---------------------##
'''Element-wise maximum and minimum between two arrays'''

max_result = A_comp.maximum(B_comp)
print(max_result.toarray())
# [[2 0 3]
#  [0 2 0]
#  [4 0 2]]

min_result = A_comp.minimum(B_comp)
print("\nElement-wise minimum(A, B):")
print(min_result.toarray())
# [[1 0 3]
#  [0 1 0]
#  [3 0 1]]


# =========================================================================================
# 6. Special Operations
# =========================================================================================

##-----------##
## Conjugate ##
##-----------##
'''
Conjugate for complex matrices
.conj() or .conjugate()
'''

A_complex = csr_array([[1+2j, 0], [0, 3-1j]])
print(A_complex.toarray())
# [[1.+2.j 0.+0.j]
#  [0.+0.j 3.-1.j]]

A_conj = A_complex.conj()
print(A_conj.toarray())
# [[1.-2.j 0.+0.j]
#  [0.+0.j 3.+1.j]]

##---------------------##
## Diagonal Extraction ##
##---------------------##
'''
Extract diagonal elements using .diagonal()
Returns numpy array
'''

A_diag = csr_array([[1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]])

main_diag = A_diag.diagonal()
print(main_diag)
# [1 5 9]

upper_diag = A_diag.diagonal(k=1)
print(upper_diag)
# [2 6]

lower_diag = A_diag.diagonal(k=-1)
print(lower_diag)
# [4 8]

##-------##
## Trace ##
##-------##
'''Sum of diagonal elements'''

print("\nTrace (sum of diagonal):", A_diag.trace())  # 15

##--------------##
## Set Diagonal ##
##--------------##
'''
Modify diagonal values using .setdiag()
Operates in-place
'''

A_setdiag = csr_array([[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 9]])

A_setdiag.setdiag([10, 20, 30])
print(A_setdiag.toarray())
# [[10  2  3]
#  [ 4 20  6]
#  [ 7  8 30]]

# Set off-diagonal
A_setdiag.setdiag([100, 200], k=1)
print(A_setdiag.toarray())
# [[ 10 100   3]
#  [  4  20 200]
#  [  7   8  30]]
