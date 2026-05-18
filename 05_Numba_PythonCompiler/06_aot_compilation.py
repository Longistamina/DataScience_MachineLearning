'''
AOT = ahead-of-time compilation
-> Compilation of a function in a separate step before running the program code,
   producing an on-disk binary object which can be distributed independently.

This is the traditional kind of compilation known in languages such as C, C++ or Fortran.

############################

Benefits:
    + AOT compilation produces a compiled extension module which does not depend on Numba
      (can run on different machines without installing Numba, but need Numpy)
    + There is no compilation overhead at runtime, nor any overhead of importing Numba.

Limitations:
    + AOT compilation only allows for regular functions, not ufuncs.
    + You have to specify function signatures explicitly.
    + Each exported function can have only one signature (but you can export several different signatures under different names).
    + Exported functions do not check the types of the arguments that are passed to them; the caller is expected to provide arguments of the correct type.
    + AOT compilation produces generic code for your CPU’s architectural family (for example “x86-64”),
    while JIT compilation produces code optimized for your particular CPU model.

Types: https://numba.readthedocs.io/en/stable/reference/types.html#numba-types
'''

from numba.pycc import CC
import numpy as np
from pathlib import Path

current_dir = Path().cwd()
print(current_dir)
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/05_Numba_PythonCompiler

##################################################
## Step 1. Define ``CC`` object and module name ##
##################################################

cc = CC('aot_demo') # declare a module named ``aot_demo`` to contain the compiled functions

# cc.verbose = True
# Uncomment the this line to print out the compilation steps

############################################
## Step 2. Export functions to the module ##
############################################

@cc.export('multf', 'f8(f8, f8)') # function `multf`, with float signatures
@cc.export('multi', 'i4(i4, i4)') # function `multi` with int signatures
def mult(a, b):
    return a * b
'''
Two functions ``multf`` and ``multi`` share the same core ``mult``
'''

@cc.export('square', 'f8(f8)') # function `square` with float signatures
def square(a):
    return a ** 2

# This function is an implementation of the second-order centered difference on a 1d array
@cc.export('centdiff_1d', 'f8[:](f8[:], f8)')
def centdiff_1d(u, dx):
    D = np.empty_like(u)
    D[0] = 0
    D[-1] = 0
    for i in range(1, len(D) - 1):
        D[i] = (u[i+1] - 2 * u[i] + u[i-1]) / dx**2
    return D

#######################
## Step 3. Compiling ##
#######################

cc.compile()
# Start compiling
# -> generate an extension module named ``aot_demo*.so`` at the current working directory
#
# This ``aot_demo*.so`` has 4 functions mentioned above: ``multf``, ``multi``, ``square`` and ``centdiff_1d``

'''NOTE: only call ``cc.compile()`` only one time!!!'''

#####################################################
## Test out the compiled functions in ``aot_demo`` ##
#####################################################

if __name__ == "__main__":

    import aot_demo # import compiled ``aot_demo``

    #---- scalar outputs ----#
    print(aot_demo.multf(3.5, -2.4)) # -8.4
    print(aot_demo.multi(2, 3)) # 6
    print(aot_demo.square(-2.8)) # 7.839999999999999

    #---- array output ----#
    in_arr = np.arange(10).astype(np.float64)
    dx = np.float64(3.5)

    result = aot_demo.centdiff_1d(in_arr, dx)
    print(result)
    # [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
