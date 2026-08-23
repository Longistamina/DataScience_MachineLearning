'''
``@numba.cfunc`` decorator creates a compiled function callable from foreign C code,
using the signature of your choice.
'''

import numba as nb
import numpy as np
from scipy.integrate import quad


# =========================================================================================
# 1. @cfunc and ctypes
# =========================================================================================
'''
The @cfunc decorator has a similar usage to @jit, but with an important difference:
-> passing a single signature is mandatory
-> It determines the visible signature of the C callback

##---------------##

In Python, an integer is a complex, heavy object with built-in methods and reference counting.
In C, an integer is just a raw sequence of bits in memory.
Because of this, Python cannot naturally talk to fast, low-level libraries written in C, C++, or Fortran.

``ctypes`` acts as a translator.
It allows Python code to convert Python objects into raw C data types (like c_int, c_double, or pointers)
so that Python can directly execute functions inside compiled C libraries.
'''

@nb.cfunc("float64(float64, float64)")
def add(x, y):
    return x + y

print(type(add))
# <class 'numba.core.ccallback.CFunc'>

print(add(3, 2)) # via Python wrapper
# 5

print(add(3.5, 10)) # via Python wrapper
# 13.5

print(add.ctypes(3.2, 7)) # via ctypes wrapper
# 10.2

'''
The performance difference between the two is usually negligible for direct Python calls.
.ctypes becomes important when you need to hand the function pointer to something outside Python
'''

def integrand(t): # The function that needs to calculate integral
    return np.exp(-t) / t**2

nb_integrand = nb.cfunc("float64(float64)")(integrand) # compile the ``integrand`` function into C

print(quad(integrand, 1, np.inf))
# (0.14849550677592208, 3.8736750296130505e-10)

print(quad(nb_integrand.ctypes, 1, np.inf))
# (0.14849550677592208, 3.8736750296130505e-10)

%timeit quad(integrand, 1, np.inf) # 31 μs ± 54.2 ns per loop (mean ± std. dev. of 7 runs, 100,000 loops each)
%timeit quad(nb_integrand.ctypes, 1, np.inf) # 5.56 μs ± 12.6 ns per loop (mean ± std. dev. of 7 runs, 100,000 loops each)


# =========================================================================================
# 2. Dealing with pointers and array
# =========================================================================================
'''
C does not understand Numpy arrays.

For example, when you pass a 2D NumPy array to a native C library, C doesn't see a nice grid with rows and columns.
C only sees a raw, flat line of memory (a pointer to the first element)
and relies on you to do the math to find the right elements.

So, instead of passing a high-level array object, a C function signature usually looks like this
``void(double *input, double *output, int m, int n)``

# ``double *input``: A pointer to the starting memory address of the input data
# m and n: The number of rows and columns,
#          passed as separate integers so you know how long the flat memory block actually is.

So, the 1D memory line would require manual math like ``input[i * n + j]``

##------------------------##

Numba provides the ``nb.carray()`` function to solve this beautifully.
It takes that "dumb" C pointer and slaps a pair of "NumPy glasses" onto it.

C-order (Row-major): Reads left-to-right across rows. This is what carray assumes (and what NumPy defaults to).

##------------------------##

Fortran-order (Column-major): Reads top-to-bottom down columns.

If the foreign library was written in Fortran (or Matlab), the data is laid out differently in memory
=> must use ``nb.farray()`` so Numba calculates the indices correctly.
'''

c_sig = nb.types.void(
    nb.types.CPointer(nb.types.double), # double *in
    nb.types.CPointer(nb.types.double), # double *out
    nb.types.intc, nb.types.intc # int m, int n
)
# This ``c_sig`` tells Numba exactly what low-level types to expect from the C library calling it.

@nb.cfunc(c_sig)
def my_callback(in_, out, m, n):
    in_array = nb.carray(in_, (m, n)) # takes the raw pointer (in_) and the shape ((m, n)) and returns a functional NumPy array view.
    out_array = nb.carray(out, (m, n))
    for i in range(m):
        for j in range(n):
            out_array[i, j] = 2 * in_array[i, j]

##--------## RUN IT ##----------##

import ctypes

m, n = 2, 3

# 1. Create standard NumPy arrays.
# They MUST be float64 to match the `double` in c_sig.
input_data = np.array([[1.0, 2.0, 3.0],
                       [4.0, 5.0, 6.0]], dtype=np.float64)

# Create an empty array of the same shape to hold the results
output_data = np.zeros((m, n), dtype=np.float64)

print("Before:")
print(output_data)
# [[0. 0. 0.]
#  [0. 0. 0.]]

# 2. Define what a C double pointer looks like using Python's ctypes
DoublePointer = ctypes.POINTER(ctypes.c_double)

# 3. Extract the raw memory pointers from the NumPy arrays
in_ptr = input_data.ctypes.data_as(DoublePointer)
out_ptr = output_data.ctypes.data_as(DoublePointer)

# 4. Call the function using the .ctypes wrapper!
my_callback.ctypes(in_ptr, out_ptr, m, n)

print("\nAfter running C callback:")
print(output_data)
# [[ 2.  4.  6.]
#  [ 8. 10. 12.]]
