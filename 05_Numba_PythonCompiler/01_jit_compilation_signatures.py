'''
Numba provides several utilities for code generation,
but its central feature is the numba.jit(), or ``@numba.jit``

Using this decorator, you can mark a function for optimization by Numba’s JIT compiler.
Various invocation modes trigger differing compilation options and behaviours.

##########################

1. Lazy compilation
2. Eager compilation
3. Numba signatures (data types)
4. Calling and inlining other functions
'''

import numba as nb
import math


#------------------------------------------------------------------------------------------------------#
#-------------------------------------- 1. Lazy Compilation -------------------------------------------#
#------------------------------------------------------------------------------------------------------#
'''
Lazy Compilation is that we let @numba.jit decide how and when to optimize.
In this mode, the function will not be compiled until the first execution/call.

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


#-------------------------------------------------------------------------------------------------------#
#-------------------------------------- 2. Eager Compilation -------------------------------------------#
#-------------------------------------------------------------------------------------------------------#
'''
Eager Compilation is when you specify the function's signatures (data types).
By doing so, we tell numba which signatures/types of the function in advance
-> It can compile right away at definition, before the first execution/call happens

For example:
+ @numba.jit(numba.float32(numba.int32, numba.int32)) -> takes two numba.int32 numbers as inputs, and returns a numba.float32
+ @numba.jit((numba.int8, numba.int8)) -> takes two numba.int8 as inputs, the output's signature will be infered

NOTE: if the input types are not the same as the given signatures, numba will force them into the signatures
'''

##################################
## Example output(input, input) ##
##################################

@nb.jit(nb.float32(nb.int64, nb.int64)) # Eager compilation right here, before the first execution
def sum_square(x, y):
    return x**2 + y**2

result = sum_square(3, 5)
print(result)
# 34.0

result = sum_square(-5.2, 1.6) # It will force -5.2 to -5, and 1.6 to 1, then execute
print(result)
# 26.0 (= 5**2 + 1**2)

#####################################
## Example ((input, input, input)) ##
#####################################

@nb.jit((nb.int32, nb.float32, nb.complex64)) # MUST always wrap all the signatures into a TUPLE
def sum(x, y, z):
    return x + y + z

result = sum(2, -3.5, 6 -9j)
print(result)
# (4.5-9j)
'''Here, numba automatically infer the signature of the output as complex'''


#------------------------------------------------------------------------------------------------------#
#-------------------------------------- 2. Numba signatures -------------------------------------------#
#------------------------------------------------------------------------------------------------------#
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
'''
