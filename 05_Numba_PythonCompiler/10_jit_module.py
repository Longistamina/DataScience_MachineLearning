'''
Automatic module jitting with ``jit_module``

When you have a large Python module (.py file) with many functions that all
need to be compiled with Numba, manually adding the ``@jit`` or ``@njit``
decorator to every single function can be tedious.

Numba provides ``jit_module()`` to automatically replace functions declared
in the current module with their JIT-compiled equivalents.

IMPORTANT RULES (When jit_module WILL NOT affect a function):
1. Functions already wrapped with a Numba decorator (e.g., @jit, @vectorize).
2. Functions imported from OTHER modules (e.g., numpy, math).
3. Functions defined logically AFTER the ``jit_module()`` call.
'''

from numba import jit_module, jit
import numpy as np


#----------------------------------------------------------------------------------------#
#------------------------ 1. Functions defined BEFORE jit_module ------------------------#
#----------------------------------------------------------------------------------------#
# These standard Python functions will be automatically JIT-compiled.

def add(x, y):
    return x + y

def complex_math(x, y):
    return (x**2 + y**2) ** 0.5

#----------------------------------------------------------------------------------------#
#------------------------ 2. Imported & Manually Decorated Functions --------------------#
#----------------------------------------------------------------------------------------#
# These will NOT be touched or overwritten by jit_module.

# Imported from another module
np_mean = np.mean

# Already manually decorated with specific settings
@jit(nopython=True, nogil=True)
def manual_sub(x, y):
    return x - y

#----------------------------------------------------------------------------------------#
#------------------------ 3. The Magic Call: jit_module() -------------------------------#
#----------------------------------------------------------------------------------------#
'''
We call jit_module() and pass standard @jit keyword arguments.
These arguments (like nopython, error_model, fastmath) will be applied
to all eligible functions defined above this line.
'''

jit_module(nopython=True, error_model="numpy", fastmath=True)

#----------------------------------------------------------------------------------------#
#------------------------ 4. Functions defined AFTER jit_module -------------------------#
#----------------------------------------------------------------------------------------#
# This function is defined AFTER the jit_module() call, so it remains pure Python.

def late_div(x, y):
    return x / y

#----------------------------------------------------------------------------------------#
#------------------------ 5. Inspecting the Results -------------------------------------#
#----------------------------------------------------------------------------------------#
print("--- Inspecting Function Types ---")
print("If a function is JIT-compiled, it will show as a 'CPUDispatcher'.")
print("If it remains pure Python, it will show as a standard 'function'.\n")

print(f"1. add (defined before)         : {add}")
print(f"2. complex_math (defined before): {complex_math}")
print(f"3. np_mean (imported)           : {np_mean}")
print(f"4. manual_sub (already jitted)  : {manual_sub}")
print(f"5. late_div (defined after)     : {late_div}")
# 1. add (defined before)         : CPUDispatcher(<function add at 0x7f2b5c793ba0>)
# 2. complex_math (defined before): CPUDispatcher(<function complex_math at 0x7f2b5c7a0900>)
# 3. np_mean (imported)           : <function mean at 0x7f2b5998a840>
# 4. manual_sub (already jitted)  : CPUDispatcher(<function manual_sub at 0x7f2afff9cb80>)
# 5. late_div (defined after)     : <function late_div at 0x7f2afff9e5c0>

print("\n--- Execution Test ---")
# The jitted functions work exactly like normal functions but run at C-speed
print(f"add(10, 20) = {add(10, 20)}")
print(f"complex_math(3, 4) = {complex_math(3, 4)}")
# add(10, 20) = 30
# complex_math(3, 4) = 5.0
