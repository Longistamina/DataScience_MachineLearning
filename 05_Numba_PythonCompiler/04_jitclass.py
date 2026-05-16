'''
``@jitclass`` is used for compiling Python class (numba.experimental.jitclass).

All methods of a jitclass are compiled into nopython functions.

The data of a jitclass instance is allocated on the heap as a C-compatible structure
so that any compiled functions can have direct access to the underlying data, bypassing the interpreter.
'''
