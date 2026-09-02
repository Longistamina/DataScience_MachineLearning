'''
Numba is a compiler for Python array and numerical functions that gives you the power to speed up your applications
with high performance functions written directly in Python.

Numba generates optimized machine code from pure Python code using the LLVM compiler infrastructure.

Numba’s main features are:
+ on-the-fly code generation (at import time or runtime, at the user’s preference)
+ native code generation for the CPU (default) and GPU hardware
+ integration with the Python scientific software stack (thanks to Numpy)
'''

import numba as nb
import numpy as np


##-## Example ##-##
@nb.jit # just-in-time compilation
def sum2d(arr):
    M, N = arr.shape
    result = 0.0
    for i in range(M):
        for j in range(N):
            result += arr[i,j]
    return result

##---------------##

np.random.seed(42)
tensor = np.random.randn(int(1e4), int(1e3))

sum_tensor = sum2d(tensor)
print(sum_tensor)
# -639.5751574852098
