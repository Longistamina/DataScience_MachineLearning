'''
Universal Functions (ufunc) are functions that operate on ndarrays in an element-by-element fashion,
supporting array broadcasting, type casting, and several other standard features.
-> a ufunc is a “vectorized” wrapper for a function that takes a fixed number of specific inputs
   and produces a fixed number of specific outputs.

There are two type of ufunc:
    + universal functions (ufunc): operate on scalars like 1D vectors (@numba.vectorize)
    + generalized universal functions (gufunc): operate on higher dimensional arrays and scalars (@numba.guvectorize)

If we don't pass any signatures -> dynamic ufunc, dynamic gufunc

Advantage of @vectorize and @guvectorize over @jit:
->  ufuncs automatically get other features such as reduction, accumulation or broadcasting
'''

import numba as nb
import numpy as np

np.random.seed(42)
vector_1 = np.random.randn(10).round(3)
print(vector_1)
# [ 0.497 -0.138  0.648  1.523 -0.234 -0.234  1.579  0.767 -0.469  0.543]

np.random.seed(24)
vector_2 = np.random.rand(10).round(3)
print(vector_2)
# [0.96  0.7   1.    0.22  0.361 0.74  0.996 0.316 0.137 0.384]

matrix_1 = np.arange(12).reshape(3, 4)
print(matrix_1)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

np.random.seed(24)
matrix_2 = np.random.randn(3, 4).round(3)
print(matrix_2)
# [[ 1.329 -0.77  -0.316 -0.991]
#  [-1.071 -1.439  0.564  0.296]
#  [-1.626  0.22   0.679  1.889]]


# =========================================================================================
# 1. ufunc - @numba.vectorzie
# =========================================================================================
'''
``@numba.vectorize`` allows Python functions that take scalar inputs behave as a vectorized function.
(Like numpy functions)

To create vectorized functions like what Numpy does, it requires C codes.
But here, just need to use decorator ``@numba.vectorize``

-> The vectorized function will operate over input scalars, rather than arrays.
Numba will generate the surrounding loop (or kernel) allowing efficient iteration over the actual inputs.

``@numba.vectorize`` also has 2 modes: eager and lazy
'''

##------------------##
## Single signature ##
##------------------##

@nb.vectorize([nb.float32(nb.float32, nb.float32)]) # Use ``[signature(signatures)]`` to make it iterable
def add(x, y):
    return x + y
# This Python function takes 2 scalar inputs x and y, then also returns a scalar x+y
# But by using ``@nb.vectorize``, we make it become a vectorized function, can take 2 arrays as inputs, add element-wise
'''NOTE: this only accepts float32 inputs'''

result = add(vector_1.astype(np.float32), vector_2.astype(np.float32))
print(result.round(3))
# [ 1.457  0.562  1.648  1.743  0.127  0.506  2.575  1.083 -0.332  0.927]

##---------------------##
## Multiple signatures ##
##---------------------##
'''
If you pass several signatures, beware that you have to pass most specific signatures before least specific ones
(e.g., single-precision float32 before double-precision float64),
otherwise type-based dispatching will not work as expected
'''

@nb.vectorize([
    nb.int32(nb.int32, nb.int32),       # int32 first
    nb.int64(nb.int64, nb.int64),       # int64 later
    nb.float32(nb.float32, nb.float32), # float32 first
    nb.float64(nb.float64, nb.float64)  # float64 later
])                                      # int before float
def sum(x, y):
    return x + y

# =========================================

result = sum(
    (vector_1*10).astype(np.int32),
    (vector_2*5).astype(np.int32)
)
print(result)
# [ 8  2 11 16 -1  1 19  8 -4  6]

# ========================================

result = sum(
    (vector_1*3).astype(np.float64),
    (vector_2*4).astype(np.float64)
)
print(result)
# [ 5.331  2.386  5.944  5.449  0.742  2.258  8.721  3.565 -0.859  3.165]

##----------------------------------------##
## Other features of @vectorize functions ##
##----------------------------------------##

m1_reduced = sum.reduce(matrix_1, axis=0)
print(m1_reduced)
# [12 15 18 21]

m2_reduced= sum.reduce(matrix_2, axis=1)
print(m2_reduced)
# [-0.748 -1.65   1.162]

v1_accumulated = sum.accumulate(vector_1)
print(v1_accumulated)
# [0.497 0.359 1.007 2.53  2.296 2.062 3.641 4.408 3.939 4.482]
# Original: [ 0.497 -0.138  0.648  1.523 -0.234 -0.234  1.579  0.767 -0.469  0.543]

m1_accumulated = sum.reduce(matrix_1, axis=1)
print(m1_accumulated)
# [ 6 22 38]


# =========================================================================================
# 2. gufunc - @numba.guvectorzie
# =========================================================================================
'''
The ``@numba.guvectorize()`` decorator takes the concept one step further,
allows you to write ufuncs that will work on an arbitrary number of elements of input arrays,
and take and return arrays of differing dimensions.

The typical example is a running median or a convolution filter.

``@numba.guvectorize()`` also has two modes of operation: eager and lazy
'''

##-----------------------------------##
## symbolic layout - return nD array ##
##-----------------------------------##

@nb.guvectorize([(nb.int32[:], nb.int32, nb.int32[:])], '(n),()->(n)')
def filter_threshold(input, threshold, result):
    for i in range(input.shape[0]):
        if input[i] < threshold:
            result[i] = threshold
        else:
            result[i] = input[i]

'''
The meaning of '(n),()->(n)'
'(n)' -> indicates that the first parameter (``input``) is the first input, a n-element 1D array
'()' -> indicates that the second parameter (``threshold``) is the second input, a scalar
`->(n)` -> indicates that the third parameter (``ressult``) is the output, a n-element 1D array

No need to use return here since the `->(n)` already told numba that the third parameter ``result`` is the output,
numba will return it automatically
'''

# =========================================================

vector_input = (vector_1*10).astype(np.int32)
print(vector_input)
# [ 4 -1  6 15 -2 -2 15  7 -4  5]

vector_filtered = filter_threshold(vector_input, 0)
print(vector_filtered)
# [ 4  0  6 15  0  0 15  7  0  5]

# ==========================================================

matrix_input = (matrix_2*10).astype(np.int32)
print(matrix_input)
# [[ 13  -7  -3  -9]
#  [-10 -14   5   2]
#  [-16   2   6  18]]

'''Here, ``@numba.guvectorize`` automatically dispatches over more complicated inputs, depending on their shapes'''

matrix_filterd = filter_threshold(matrix_input, 0)
print(matrix_filterd)
# [[13  0  0  0]
#  [ 0  0  5  2]
#  [ 0  2  6 18]]

##-----------------------------------##
## symbolic layout - return a scalar ##
##-----------------------------------##
'''
To return a scalar value only, we do this:
    + in the signatures, declare the scalar return with [:] like a 1-dimensional array (eg. int64[:]),
    + in the layout, declare it as (),
    + in the implementation, write to the first element (e.g. result[0] = acc).
'''

@nb.guvectorize([(nb.float32[:], nb.u8, nb.float32[:])], '(n),()->()', cache=False) # '->()' means return as scalar
def aggregate(input, reduction, result):
    '''
    reduction = 0 -> sum
    reduction = 1 -> mean
    reduction = 2 -> multiplication (or product)
    reduction = 3 -> min
    reduction = 4 -> max
    '''

    n = input.size

    if reduction == 0:       # sum
        acc = np.float32(0.0)
        for i in range(n):
            acc += input[i]
        result[0] = acc

    elif reduction == 1:     # mean
        acc = np.float32(0.0)
        for i in range(n):
            acc += input[i]
        result[0] = acc / n

    elif reduction == 2:     # product
        acc = np.float32(1.0)
        for i in range(n):
            acc *= input[i]
        result[0] = acc

    elif reduction == 3:     # min
        acc = input[0]
        for i in range(1, n):
            if input[i] < acc:
                acc = input[i]
        result[0] = acc

    elif reduction == 4:     # max
        acc = input[0]
        for i in range(1, n):
            if input[i] > acc:
                acc = input[i]
        result[0] = acc

    else:
        result[0] = np.nan

matrix_mean = aggregate(matrix_2.flatten().astype(np.float32), 0)
print(matrix_mean)
# -1.2359995

matrix_sum = aggregate(matrix_2.astype(np.float32), 1) # No flatten -> perform on each ``matrix_2[i, :]`` (column-wise, axis=1)
print(matrix_sum)
# [-0.187      -0.4125      0.29050002]

matrix_min = aggregate(matrix_2.flatten().astype(np.float32), 3)
print(matrix_min)
# -1.626

##--------------------------##
## Overwriting input values ##
##--------------------------##

@nb.guvectorize([(nb.float64[:], nb.float64, nb.float64[:])], '(),()->()')
def overwrite(ins, replace, outs):
    n = ins.size
    for i in range(n):
        outs[i] = replace

matrix_overwritten = overwrite(matrix_2.astype(np.float32), np.float32(35.8))
print(matrix_overwritten.round(2))
# [[35.8 35.8 35.8 35.8]
#  [35.8 35.8 35.8 35.8]
#  [35.8 35.8 35.8 35.8]]


# =========================================================================================
# 3. dufunc - dgufunc
# =========================================================================================
'''
dufunc = dynamic ufunc = @vectorize without signatures
dgufunc = dynamic gufunc = @guvectorize without signatures

For dgufunc and @guvectorize, must create a zero(s) array first (use np.zeros() or np.zeros_like()),
then pass to the function to update
'''

@nb.vectorize # dufunc
def f(x, y):
    return x - y

print(f(2, -3)) # 5

# ==================================

@nb.guvectorize('(n),()->()')
def g(x, y, out):
    acc = 0.0
    for i in range(len(x)):
        acc += x[i] * y
    out[0] = acc

out = np.zeros(1) # [0]
out = g(vector_2, 3, out)
print(out)
# [17.442]
