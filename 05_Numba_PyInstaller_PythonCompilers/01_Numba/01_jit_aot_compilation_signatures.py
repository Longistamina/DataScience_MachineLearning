'''
Numba provides several utilities for code generation,
but its central feature is the numba.jit(), or ``@numba.jit``

JIT = Just-in-time compilation
-> Compilation of a function at execution time

Using this decorator, you can mark a function for optimization by Numba’s JIT compiler.
Various invocation modes trigger differing compilation options and behaviours.

##-----------------------------------------------------------------------------##

1. Lazy compilation
2. Eager compilation
3. Numba signatures (data types)
4. Calling and inlining other functions
'''

import numba as nb
import numpy as np
import math


# =========================================================================================
# 1. Lazy Compilation
# =========================================================================================
'''
Lazy Compilation is that we let @numba.jit decide how and when to optimize.
In this mode, the function will not be compiled until the first execution/call.

(Just-in-Time compilation, JIT compilation)

Numba will infer the argument types at call time,
and generate optimized code based on this information.

Numba can handle different types -> different outputs
'''

@nb.jit # lazy compilation, not compile here
def add(x, y):
    return x + y

result = add(2, 3) # Compilation starts here at the first execution/call
print(result)
# 5

result = add(-3, -9) # No recompilation, the types are the same as the first call, reuse old compiled machine codes.
print(result)
# -12

result = add(2j, -3.2) # Recompilation here because the types are now different
print(result)
# (-3.2+2j)


# =========================================================================================
# 2. Eager Compilation
# =========================================================================================
'''
Eager Compilation is when you specify the function's signatures (data types).
By doing so, we tell numba which signatures/types of the function in advance
-> It can compile right away at definition, before the first execution/call happens

(Ahead-of-Time compilation, AOT compilation)

For example:
+ @numba.jit(numba.float32(numba.int32, numba.int32)) -> takes two numba.int32 numbers as inputs, and returns a numba.float32
+ @numba.jit((numba.int8, numba.int8)) -> takes two numba.int8 as inputs, the output's signature will be infered

NOTE: if the input types are not the same as the given signatures, numba will force them into the signatures
'''

##--------------------------------##
## Example (output(input, input)) ##
##--------------------------------##

@nb.jit(nb.float32(nb.int64, nb.int64)) # Eager compilation right here, before the first execution
def sum_square(x, y):
    return x**2 + y**2

result = sum_square(3, 5)
print(result)
# 34.0

result = sum_square(-5.2, 1.6) # It will force -5.2 to -5, and 1.6 to 1, then execute
print(result)
# 26.0 (= 5**2 + 1**2)

##---------------------------------##
## Example ((input, input, input)) ##
##---------------------------------##

@nb.jit((nb.int32, nb.float32, nb.complex64)) # MUST always wrap all the signatures into a TUPLE
def sum(x, y, z):
    return x + y + z

result = sum(2, -3.5, 6-9j)
print(result)
# (4.5-9j)
'''Here, numba automatically infer the signature of the output as complex'''

##----------------------------------------##
## Example (output(scalar, array, array)) ##
##----------------------------------------##

@nb.jit(nb.float64[:, :](nb.float64, nb.int32[:, :], nb.float32[:, :])) # ``nb.int32[:, :]`` means a 2D array with int32 type
def simple_array_operation(scalar, arr1, arr2):
    output = scalar * arr1 + arr2 # Result in a nb.float64
    return output

'''
Here, must define the output as ``nb.float64[:, :]``, because one input (the scalar) is nb.float64,
so all the computings will result in ``nb.float64``.
(the ``output`` becomes ``nb.float64[:, :]``)

If we use ``nb.float32[:, :](nb.float64, nb.int32[:, :], nb.float32[:, :])``,
the ``nb.float32[:, :]`` inside the ``@nb.jit()`` will be mismatched with the type of the ``output``
-> error
'''

# =========================================================================================

np.random.seed(42)
arr1 = np.random.randint(30, size=(4, 3)).astype(np.int32)
print(arr1)
# [[ 6 19 28]
#  [14 10  7]
#  [28 20  6]
#  [25 18 22]]

np.random.seed(24)
arr2 = np.random.randn(4, 3).astype(np.float32)
print(arr2)
# [[ 1.3292122  -0.7700335  -0.31628036]
#  [-0.9908104  -1.0708163  -1.4387133 ]
#  [ 0.5644168   0.2957219  -1.6264043 ]
#  [ 0.2195652   0.6788048   1.8892727 ]]

result = simple_array_operation(
    scalar=math.pi,
    arr1=arr1,
    arr2=arr2
)
print(result)
# [[20.17876811 58.92022694 87.64831394]
#  [42.99148676 30.34511026 20.55243526]
#  [88.52901113 63.12757496 17.22315164]
#  [78.75938154 57.22747258 71.00431107]]


# =========================================================================================
# 3. Numba signatures
# =========================================================================================
'''
Explicit ``@jit`` signatures can use a number of types.  Here are some common ones:

* ``void`` is the return type of functions returning nothing (which actually return :const:`None` when called from Python)

* ``intp`` and ``uintp`` are pointer-sized integers (signed and unsigned, respectively)

* ``intc`` and ``uintc`` are equivalent to C ``int`` and ``unsigned int`` integer types

* ``int8``, ``uint8``, ``int16``, ``uint16``, ``int32``, ``uint32``, ``int64``, ``uint64``
    are fixed-width integers of the corresponding bit width (signed and unsigned)

* ``float32`` and ``float64`` are single- and double-precision floating-point numbers, respectively

* ``complex64`` and ``complex128`` are single- and double-precision complex numbers, respectively

* array types can be specified by indexing any numeric type, e.g. ``float32[:]`` for a one-dimensional single-precision array
                                                                or ``int8[:,:]`` for a two-dimensional array of 8-bit integers.

##--------------------------##

int64 wins int32 wints int16 ...
float64 wins float32 wins float16 ...
'''


# =========================================================================================
# 4. Calling and inlining other functions
# =========================================================================================
'''
Numba-compiled functions can call other compiled functions,
and can also be called by other compiled functions.

Numba-compiled functions can also be inlined by other native functions
(depending on optimizer heuristics.)
'''

@nb.jit
def square(x):
    return x**2

@nb.jit
def sum_sqr(nums):
    sum = 0
    for x in nums:
        sum += square(x) # call a numba-compiled function inside another compiled function
    return sum

arr_inputs = np.array([2, 3, 5, 9.2])
sum_of_square = sum_sqr(arr_inputs) # Should prioritize np.array as inputs, because numba likes this
print(sum_of_square)
# 122.63999999999999

arr_inputs = np.array([5, 3.2, 8, 7.3])
sqrt_sum_of_square = math.sqrt(sum_sqr(arr_inputs)) # inline a numba-compiled function inside a native function
print(sum_of_square)
# 12.350303639992015
