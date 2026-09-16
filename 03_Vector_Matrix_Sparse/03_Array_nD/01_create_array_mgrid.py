'''
Creating ndarray is similar like creating a vector (1D) or a matrix (2D).

1. Create a ndarray using np.array():
   + from nested list
   + from tuple of tuples

2. Create a ndarray using other NumPy functions:
   + np.arange() + reshape()
   + np.reshape()
   + np.zeros()
   + np.ones()
   + np.full()
   + np.eye()
   + np.identity()
   + np.diag()
   + np.tril(), np.triu()
   + np.fromfunction()
   + np.meshgrid() (build coordinate grids)
   + np.mgrid[::j, ::j, ::j] (like `np.meshgrid`)

3. Create ndarray using _like() functions
   + np.zeros_like(a)
   + np.ones_like(a)
   + np.full_like(a, fill_value)
   + np.empty_like(a)

4. Create random ndarray:
   + np.random.rand()
   + np.random.randn()
   + np.random.uniform()
   + np.random.randint()
   + np.random.seed(): for reproducibility
   + np.random.choice() + reshape()

5. Create a ndarray with dtype specified (int, float, complex, bool, etc.)
'''

import numpy as np

# =========================================================================================
# 1. Create a ndarray using np.array():
# =========================================================================================
'''
Beside `np.array()`, you can also use `np.asaray()`.

`np.array()` makes a copy of the object by default `(copy=True)`.

`np.asarray()` avoids copying and creates a view `(copy=False)`
if the input is already a compatible NumPy array.
This saves memory and processing time.
'''

##----------------------------##
## 3D nested list -> 3D array ##
##----------------------------##

list_3d = [
    [[1, 1, 1],
    [1, 1, 1]],

    [[2, 2, 2],
    [2, 2, 2]],

    [[3, 3, 3],
    [3, 3, 3]],
]

arr_3d = np.asarray(list_3d)
print(arr_3d)
print(arr_3d.shape)
'''
[[[1 1 1]
  [1 1 1]]

 [[2 2 2]
  [2 2 2]]

 [[3 3 3]
  [3 3 3]]]

(3, 2, 3)
'''

##-----------------------##
## 4D tuples -> 4D array ##
##-----------------------##

tuple_4d = (
    (
        ((1, 1, 1),
        (1, 1, 1)),

        ((1, 1, 1),
        (1, 1, 1)),

        ((1, 1, 1),
        (1, 1, 1)),
    ),

    (
        ((2, 2, 2),
        (2, 2, 2)),

        ((2, 2, 2),
        (2, 2, 2)),

        ((2, 2, 2),
        (2, 2, 2)),
    ),
)

arr_4d = np.asarray(tuple_4d)
print(arr_4d)
print(arr_4d.shape)
'''
[[[[1 1 1]
   [1 1 1]]
  [[1 1 1]
   [1 1 1]]
  [[1 1 1]
   [1 1 1]]]

 [[[2 2 2]
   [2 2 2]]
  [[2 2 2]
   [2 2 2]]
  [[2 2 2]
   [2 2 2]]]]

(2, 3, 2, 3)
'''

# =========================================================================================
# 2. Create a ndarray using other NumPy functions:
# =========================================================================================

##-----------------------------------##
## Example 3D arrays with `np.mgrid` ##
##-----------------------------------##
'''
When you write `np.mgrid[-1:2:5j]`
-> -1 is lower bound
-> 2 is upper bound
-> 5j is the length
-> so the outcome is like `np.linspace(-1, 1, 5)`
-> 2 will be inclusive

When you write `np.mgrid[-1:2]`
-> the outcome is like `np.arange(-1, 2)`
-> 2 will be exclusive
'''

X, Y, Z = np.mgrid[-1:1:5j, 2:5, 8:10:3j]

print(X.shape)
# (5, 3, 3)

print(Y.shape)
# (5, 3, 3)

print(Z.shape)
# (5, 3, 3)

##---------------------------------##
## Example 4D array with `np.ones` ##
##---------------------------------##

ones_4d = np.ones(shape=(2, 2, 4, 3))

print(ones_4d)
'''
[[[[1. 1. 1.]
   [1. 1. 1.]
   [1. 1. 1.]
   [1. 1. 1.]]
  [[1. 1. 1.]
   [1. 1. 1.]
   [1. 1. 1.]
   [1. 1. 1.]]]

 [[[1. 1. 1.]
   [1. 1. 1.]
   [1. 1. 1.]
   [1. 1. 1.]]
  [[1. 1. 1.]
   [1. 1. 1.]
   [1. 1. 1.]
   [1. 1. 1.]]]]
'''

# =========================================================================================
# 3. Create ndarray using _like() functions
# =========================================================================================

init_3d = np.ones((2, 3, 4))
init_4d = np.zeros((4, 3, 4, 2))

##---------------------------##
## 3D from `np.zeros_like()` ##
##---------------------------##

zeros_3d = np.zeros_like(init_3d)

print(zeros_3d.shape)
# (2, 3, 4)

##--------------------------##
## 4D from `np.full_like()` ##
##--------------------------##

eights_4d = np.full_like(init_4d, fill_value=8.0)

print(eights_4d.shape)
# (4, 3, 4, 2)

# =========================================================================================
# 4. Create random ndarrays
# =========================================================================================

##----------------------------##
## 3D from `np.random.rand()` ##
##----------------------------##

rand_3d = np.random.rand(2, 3, 4)

print(rand_3d.shape)
# (2, 3, 4)

##-----------------------------##
## 4D from `np.random.randn()` ##
##-----------------------------##

randn_4d = np.random.randn(3, 2, 4, 5)

print(randn_4d.shape)
# (3, 2, 4, 5)

# =========================================================================================
# 5. Create ndarrays with dtype specified (int, float, complex, bool, etc.)
# =========================================================================================

##--------------##
## 3D int array ##
##--------------##

int_3d = np.asarray(np.random.uniform(1, 11, (2, 3, 4)), dtype=np.int32)

print(int_3d.dtype)
# int32

##------------------##
## 4D complex array ##
##------------------##

complex_4d = np.asarray(np.random.normal(5, 2, (4, 2, 3, 2)), dtype=np.complex64)

print(complex_4d.dtype)
# complex64
