'''
The ``@stencil`` decorator is a powerful tool for operations where the new value of an array element depends on its neighbors.
This pattern is extremely common in:
    + image processing (blurring, edge detection)
    + physics simulations (heat diffusion, fluid dynamics), and finance (moving averages).
'''

import numba as nb
import numpy as np
import time

vector = np.arange(10) * 1.0
print(vector)
# [0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]

matrix = np.arange(12).reshape(3, 4) * 1.0
print(matrix)
# [[ 0.  1.  2.  3.]
#  [ 4.  5.  6.  7.]
#  [ 8.  9. 10. 11.]]


# =========================================================================================
# 1. The Core Concept: Relative Indexing
# =========================================================================================
'''
The most important feature of @stencil is relative indexing.

a[0, 0] refers to the current element being processed.
a[-1, 0] refers to the element above (or to the left in 1D).
a[1, 0] refers to the element below (or to the right in 1D).
'''

@nb.stencil
def blur_kernel(a):
    # Average the current pixel with its top, bottom, left, and right neighbors
    return 0.2 * (a[0,0] + a[-1,0] + a[1,0] + a[0,-1] + a[0,1])

# You do not need to write for loops to iterate over the rows and columns;
# Numba generates the looping code for you automatically.

print(blur_kernel(matrix))
# [[0. 0. 0. 0.]
#  [0. 5. 6. 0.]
#  [0. 0. 0. 0.]]


# =========================================================================================
# 2. @stensil(cval=...)
# =========================================================================================
'''
What happens when the stencil is centered on the very edge of the array?
For example, if you are at the top row (row 0), the stencil might ask for a[-1, 0], which is outside the array bounds.

=> Numba defines that the kernel cannot be fully applied and sets that specific output element to a constant value.

``cval`` stands for Constant Value. By default, ``@stensil(cval=0.0)``
'''

# 1. Default behavior (cval defaults to 0.0)
@nb.stencil
def sum_neighbors_default(a):
    # Sums the left neighbor, current element, and right neighbor
    return a[-1] + a[0] + a[1]

# 2. Custom cval (e.g., filling borders with 999.0)
@nb.stencil(cval=999.0)
def sum_neighbors_custom(a):
    return a[-1] + a[0] + a[1]

# Apply the stencils
out_default = sum_neighbors_default(vector)
out_custom = sum_neighbors_custom(vector)

print(f"Default cval:   {out_default}")
print(f"Custom cval:    {out_custom}")
# Default cval:   [ 0.  3.  6.  9. 12. 15. 18. 21. 24.  0.]
# Custom cval:    [999.   3.   6.   9.  12.  15.  18.  21.  24. 999.]

# =========================================================================================
# 3. @stensil(neighborhood=(..., ...))
# =========================================================================================
'''
Numba usually infers the size of the stencil by looking at the literal numbers in your indices
(e.g., seeing -1 and 1 tells it the size is 3x3).

 However, if you use a for loop inside the stencil, Numba cannot guess the bounds. You must provide them manually.
'''

# Tells Numba the kernel looks back 29 steps and forward 0 steps
@nb.stencil(neighborhood=((-29, 0),))
def moving_average(a):
    cumul = 0
    for i in range(-29, 1):
        cumul += a[i]
    return cumul / 30.0
# This calculates the 30-day moving average of a time series of data


# =========================================================================================
# 4. @stensil(neighborhood=(-29, 0))
# =========================================================================================
'''
By default, all array arguments use relative indexing.

But what if you want to pass a 1D array of weights or a lookup table?
You don't want weights[0] to mean "the weight 0 steps away from the current pixel",
you want it to mean "the first element of the weights array."
'''

@nb.stencil(standard_indexing=("weights",))
def weighted_sum(a, weights):
    # a uses relative indexing (neighbors)
    # weights uses absolute indexing (lookup table)
    return a[-1]*weights[0] + a[0]*weights[1] + a[1]*weights[2]


# =========================================================================================
# 5. @stensil(out=...)
# =========================================================================================
'''
Every generated stencil function has a hidden out parameter.
By default, calling result = my_stencil(input) allocates a new array in memory for the result.

If you are running this stencil inside a time-stepping loop (e.g., simulating heat over 1000 steps),
allocating a new array every step is slow and creates garbage collection overhead.

You can pass a pre-allocated array to reuse memory
'''

# 1. Define a simple 2D stencil kernel
# This calculates the average of the top, bottom, left, and right neighbors.
@nb.stencil
def smooth_kernel(a):
    return 0.25 * (a[-1, 0] + a[1, 0] + a[0, -1] + a[0, 1])

# Create a sample 2D grid (e.g., a temperature grid)
grid_size = (1000, 1000)
input_data = np.random.rand(*grid_size)

# By default, Numba allocates a BRAND NEW array in memory for the result.
result_default = smooth_kernel(input_data)

# Pre-allocate an output buffer ONCE.
output_buffer = np.zeros_like(input_data)
smooth_kernel(input_data, out=output_buffer) # Tell Numba to write the results directly into our pre-allocated buffer.
