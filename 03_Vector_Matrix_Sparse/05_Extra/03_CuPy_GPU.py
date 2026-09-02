'''
CuPy is a GPU-accelerated library for numerical computations in Python,
designed to be compatible with NumPy. It allows for efficient array
operations on NVIDIA GPUs using CUDA (have ROCm support for AMD GPUs as well).

It also provides support for sparse matrices through the `cupyx.scipy.sparse` module,
which is similar to SciPy's sparse matrix module but optimized for GPU computations.

##-------------------------------------------##

1. CuPy demo with normal arrays

2. CuPy demo with sparse matrices
'''

import cupy as cp
import numpy as np
from cupyx.scipy import sparse

cp.set_printoptions(linewidth=1000)
np.set_printoptions(linewidth=1000)


# =========================================================================================
# 1. CuPy demo with normal arrays
# =========================================================================================

##---------------##
## Create Arrays ##
##---------------##

cp.random.seed(0)
A_gpu = cp.random.rand(10000, 10000)

cp.random.seed(1)
B_gpu = cp.random.rand(10000, 10000)

print(A_gpu)
# [[0.14756221 0.32758648 0.88863337 ... 0.88140656 0.08681464 0.89672066]
#  [0.85209843 0.26967087 0.71928284 ... 0.75468756 0.0786614  0.15341472]
#  [0.1049938  0.29851131 0.80930753 ... 0.34552936 0.16501329 0.96517445]
#  ...
#  [0.03699526 0.68037352 0.42715291 ... 0.5471596  0.99946659 0.14129451]
#  [0.96705988 0.82266607 0.51053929 ... 0.7211233  0.33754479 0.63121816]
#  [0.04423195 0.12753905 0.24293089 ... 0.14995271 0.4689688  0.30793824]]

print(A_gpu.device)
# <CUDA Device 0> (stored in GPU memory)

print(A_gpu.nbytes / (1024 ** 2), "MB")
# 762.939453125 MB

##------------------##
## Array Operations ##
##------------------##

print(A_gpu.dot(B_gpu)) # or cp.matmul(A, B)
# [[2478.37666184 2470.41236716 2521.0490513  ... 2502.25405829 2490.03047083 2515.71143485]
#  [2480.32637555 2478.70355098 2486.73514427 ... 2516.86361691 2492.99540592 2522.79742063]
#  [2489.82734065 2474.28743772 2511.62868848 ... 2532.88420052 2496.29222507 2520.33419977]
#  ...
#  [2481.09588946 2487.88668375 2526.74290933 ... 2509.78810339 2493.2084694  2497.43372284]
#  [2484.24238221 2481.83557796 2526.42467699 ... 2535.62021729 2499.90602272 2524.21466758]
#  [2460.90550794 2452.02306515 2491.7197573  ... 2492.46703241 2454.33505379 2511.76930667]]

##-----------------------------------##
## Performance comparison wiht NumPy ##
##-----------------------------------##

import time

# Warm-up
C_gpu = A_gpu.dot(B_gpu)

# Measure CuPy performance
start_gpu = time.time()
C_gpu = A_gpu.dot(B_gpu)
cp.cuda.Stream.null.synchronize()  # Ensure all GPU computations are done
end_gpu = time.time()
gpu_time = end_gpu - start_gpu
print(f"CuPy GPU time: {gpu_time:.4f} seconds") # 10.9515 seconds

# Measure NumPy performance
A_cpu = cp.asnumpy(A_gpu)
B_cpu = cp.asnumpy(B_gpu)
start_cpu = time.time()
C_cpu = A_cpu.dot(B_cpu)
end_cpu = time.time()
cpu_time = end_cpu - start_cpu
print(f"NumPy CPU time: {cpu_time:.4f} seconds") # 2.2554 seconds


# =========================================================================================
# 2. CuPy demo with sparse matrices
# =========================================================================================

##----------------------##
## Create Sparse Matrix ##
##----------------------##

rows = 10000
cols = 10000
density = 0.001  # 0.1% non-zero entries

cp.random.seed(0)
A_sparse_gpu = sparse.random(rows, cols, density=density, format='csr', dtype=cp.float32)

print(A_sparse_gpu)
# Segmentation fault (core dumped)
'''This is because CuPy sparse does not support AMD GPUs hardware :((((('''
