'''
Numba provides several compilation options to control the behavior of the JIT compiler.
These options can be passed to @nb.jit() to enable specific features like:

- nopython (nonpython) : Force compilation to avoid Python C API
- nogil                : Release the Global Interpreter Lock
- cache                : Save compiled functions to disk
- parallel             : Automatically parallelize loops

Each option can be used individually or in combination.
'''

import numba as nb
import numpy as np
import time
from threading import Thread


#------------------------------------------------------------------------------------------------------#
#-------------------------------------- nopython (nonpython) ------------------------------------------#
#------------------------------------------------------------------------------------------------------#
'''
The `nopython` mode (also called "nonpython") is the most important performance option.
When set to True, Numba compiles the function entirely without Python C API calls.
If compilation fails, an error is raised; otherwise, the function runs at near-C speed.

If set to False (or omitted), Numba may fall back to "object mode" which is slower.
Always use nopython=True for maximum performance.
'''

@nb.jit(nopython=True)   # equivalent to @nb.jit
def dot_product(a, b):
    result = 0.0
    for ai, bi in zip(a, b):
        result += ai * bi
    return result

x = np.array([1.0, 2.0, 3.0])
y = np.array([4.0, 5.0, 6.0])
print(dot_product(x, y))  # 32.0


#-----------------------------------------------------------------------------------------------------#
#--------------------------------------------- nogil -------------------------------------------------#
#-----------------------------------------------------------------------------------------------------#
'''
The Global Interpreter Lock (GIL) prevents multiple threads from executing Python bytecode at once.
When `nogil=True`, Numba releases the GIL inside the compiled function, allowing true multithreading.

This is useful when you run a compiled function in multiple threads concurrently.
Note: I/O operations or calling Python objects inside the function will re-acquire the GIL.
'''

@nb.jit(nopython=True, nogil=True)
def long_computation(arr):
    total = 0.0
    for i in range(len(arr)):
        total += np.sin(arr[i]) ** 2
    return total

# This function can now run in parallel threads without blocking each other
def worker(arr, results, idx):
    results[idx] = long_computation(arr)

# Create two arrays and run them in parallel
arr1 = np.random.rand(10_000_000)
arr2 = np.random.rand(10_000_000)
results = [0.0, 0.0]

t1 = Thread(target=worker, args=(arr1, results, 0))
t2 = Thread(target=worker, args=(arr2, results, 1))

start = time.time()
t1.start()
t2.start()
t1.join()
t2.join()
end = time.time()
print(f"Parallel nogil execution: {end - start:.3f} sec")
# Both threads run truly concurrently because GIL is released inside long_computation


#-----------------------------------------------------------------------------------------------------#
#--------------------------------------------- cache -------------------------------------------------#
#-----------------------------------------------------------------------------------------------------#
'''
When `cache=True`, Numba saves the compiled machine code to a file on disk after the first call.
On subsequent runs, the compiled function is loaded from cache instead of being recompiled.

This greatly speeds up startup time for functions that are called repeatedly across program runs.
Cache files are stored in __pycache__ with a signature based on the function source and Numba version.
'''

@nb.jit(nopython=True, cache=True)
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

# First run: compiles and caches
# Next time you run this script: loads from cache instantly
print(fibonacci(100))   # 3736710778780434371


#------------------------------------------------------------------------------------------------------#
#-------------------------------------------- parallel ------------------------------------------------#
#------------------------------------------------------------------------------------------------------#
'''
The `parallel=True` option attempts to automatically parallelize supported operations,
such as vectorized arithmetic, reductions, and certain loops (using `nb.prange`).

It runs on multiple CPU threads using Numba's internal parallel backend.
To use it effectively, replace `range` with `nb.prange` in loops you want to parallelize.
'''

@nb.jit(nopython=True, parallel=True)
def sum_squares_parallel(arr):
    total = 0.0
    # Use ``nb.prange`` instead of range for parallel loop
    for i in nb.prange(len(arr)):
        total += arr[i] * arr[i]
    return total

# Without parallel: @nb.jit(nopython=True, parallel=False) uses a single thread
# With parallel: Numba automatically distributes iterations across CPU cores

big_arr = np.random.rand(10_000_000)

start = time.time()
result_parallel = sum_squares_parallel(big_arr)
end = time.time()
print(f"Parallel execution time: {end - start:.3f} sec")
# Faster than sequential for large arrays


#------------------------------------------------------------------------------------------------------#
#-------------------------------------- Combining options ---------------------------------------------#
#------------------------------------------------------------------------------------------------------#
'''
Options can be combined freely. For maximum performance and parallelism:
    @nb.jit(nopython=True, nogil=True, parallel=True, cache=True)
'''

@nb.jit(nopython=True, nogil=True, parallel=True, cache=True)
def compute_stuff(matrix):
    nrows, ncols = matrix.shape
    result = 0.0
    for i in nb.prange(nrows):
        row_sum = 0.0
        for j in range(ncols):
            row_sum += np.sin(matrix[i, j]) ** 2
        result += row_sum
    return result

mat = np.random.rand(2000, 2000)
print(compute_stuff(mat))   # ~ some number
