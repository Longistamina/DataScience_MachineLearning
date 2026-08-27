'''
1. Automatic Parallelization with ``@jit(parallel=True)`` decorator.
    + The Goal: It tells Numba to scan your function and automatically identify parts of the code
                that can be run simultaneously on multiple CPU cores.

    + Loop Fusion: If your code performs several small array operations one after another
                    (e.g., A = B + C, then D = A * 2),
                    parallelizing them individually is often slow
                    because the computer has to write data to memory
                    and read it back repeatedly (poor cache behavior).
                    => Instead, Numba fuses these adjacent operations into a single, larger "kernel"
                    and runs that in parallel. This is much faster.

    + Zero Effort: Unlike other Numba tools like ``@vectorize`` where you have to rewrite code to define kernels explicitly,
                   ``parallel=True`` attempts to do this automatically on your existing standard Python/NumPy code.

2. Supported operators: https://numba.readthedocs.io/en/stable/user/parallel.html#supported-operations

3. Explicit Parallel Loops (``prange``):
    + Sometimes Numba cannot figure out if a standard for loop is safe to parallelize.
      You can force it by replacing Python's range with Numba's prange (parallel range).

    + You must ensure there are no cross-iteration dependencies.
      This means iteration ``i`` cannot depend on the result of iteration ``i-1``

    + The floor division ``//=`` is not supported,
      because the order of operations changes the mathematical result
'''

import numba as nb
import numpy as np

##-------------------##
## Example: 1D array ##
##-------------------##

@nb.njit(parallel=True) # ``@njit`` is ``@jit(nopython=True)``
def sum_vector(A):
    total = 0
    for i in nb.prange(len(A)): # Numba splits this loop across CPU cores safely
        total += A[i]
    return total

vector = np.ones(12)
print(vector)
print(sum_vector(vector))
# 12.0

##-------------------##
## Example: 2D array ##
##-------------------##

@nb.njit(parallel=True)
def prod_matrix(M, axis=None):
    rows, cols = M.shape

    if axis == 0:
        result = np.ones(cols, dtype=M.dtype)
        for j in nb.prange(cols):
            for i in range(rows):
                result[j] *= M[i, j]

    elif axis == 1:
        result = np.ones(rows, dtype=M.dtype)
        for i in nb.prange(rows):
            for j in range(cols):
                result[i] *= M[i, j]

    else:
        result = np.ones(1, dtype=M.dtype)
        total = 1.0
        for i in range(rows):
            for j in range(cols):
                total *= M[i, j]
        result[0] = total

    return result

matrix = np.linspace(1, 10, 12).reshape(3, 4)
print(matrix)
# [[ 1.          1.81818182  2.63636364  3.45454545]
#  [ 4.27272727  5.09090909  5.90909091  6.72727273]
#  [ 7.54545455  8.36363636  9.18181818 10.        ]]

print(prod_matrix(matrix, 0))
# [ 32.23966942  77.41547708 143.03906837 232.39669421]

print(prod_matrix(matrix, 1))
# [  16.55897821  864.68957038 5794.41021788]

print(prod_matrix(matrix))
# [82966542.7842008]

'''
NOTE:

Only prange loops with a single entry block and single exit block can be converted such that they will be run in parallel.

Exceptional control flow, such as an assertion, in the loop can generate multiple exit blocks
and cause the loop not to be run in parallel.
If this is the case, Numba will issue a warning indicating which loop could not be parallelized.

for example:
```
for i in nb.prange(something):
    if condition1:
        result = ....
    else:
        condtion = ...
```
'''

##----------------------##
## Caution on data race ##
##----------------------##
'''
If the elements specified by the slice or index are written to simultaneously by multiple parallel threads,
the compiler may not detect such cases and then a race condition would occur.
'''

@nb.njit(parallel=True)
def prange_wrong_result1(x):
    n = x.shape[0]
    y = np.zeros(4)
    for i in nb.prange(n):
        # accumulating into the same element of `y` from different
        # parallel iterations of the loop results in a race condition
        y[:] += x[i]
    return y

@nb.njit(parallel=True)
def prange_wrong_result2(x):
    n = x.shape[0]
    y = np.zeros(4)
    for i in nb.prange(n):
        # accumulating into the same element of `y` from different
        # parallel iterations of the loop results in a race condition
        y[i % 4] += x[i]
    return y

##-----------------------##
## Unsuppoted Operations ##
##-----------------------##
'''
1. Mutating a list is not safe:
    @njit(parallel=True)
    def invalid():
        z = []
        for i in prange(10000):
            z.append(i)
        return z

2. Induction variables are not associated with thread ID
    @njit(parallel=True)
    def invalid():
        n = get_num_threads()
        z = [0 for _ in range(n)]
        for i in prange(100):
            z[i % n] += i
        return z
'''
