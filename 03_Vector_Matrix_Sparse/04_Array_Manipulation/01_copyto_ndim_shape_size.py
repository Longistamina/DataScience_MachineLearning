"""
1. np.copyto()
2. np.ndim()
3. np.shape()
4. np.size()
"""

import numpy as np


#
# --------------------------------- 1. np.copyto()
#
"""Copies values from one array to another, broadcasting as necessary."""

##------------##
## 1D example ##
##------------##

A = np.array([4, 5, 6])
B = [1, 2, 3]  # don't have to be np array

np.copyto(dst=A, src=B)

print(A)
# [1 2 3]

##------------##
## 2D example ##
##------------##

A = np.array([[1, 2, 3], [4, 5, 6]])
# [[1 2 3]
#  [4 5 6]]

B = [[4, 5, 6], [7, 8, 9]]  # don't have to be np array

np.copyto(A, B)
print(A)
# [[4 5 6]
#  [7 8 9]]


#
# --------------------------------- 2. np.ndim()
#
"""Return the number of dimensions of an array."""

vector = np.random.rand(5)
# [0.57126444 0.99962062 0.10598955 0.28800684 0.83042583]

print(np.ndim(vector))
# 1

##--------------------------##

matrix = np.random.rand(3, 4)
# [[0.86096136 0.86408397 0.06997919 0.96436848]
#  [0.05944486 0.7429009  0.59422426 0.59298668]
#  [0.19976705 0.66314253 0.05139525 0.20021914]]

print(np.ndim(matrix))
# 2

##-------------------------##

tensor = np.random.rand(2, 3, 4)
# [[[0.93713903 0.5337622  0.95489977 0.27149309]
#   [0.42269534 0.45266346 0.48035163 0.10172879]
#   [0.51773972 0.26164127 0.88253768 0.76249665]]

#  [[0.82503201 0.76863845 0.92848401 0.87800894]
#   [0.60846993 0.63991757 0.71493461 0.88612886]
#   [0.27305849 0.97869929 0.62615073 0.89921019]]]

print(np.ndim(tensor))
# 3


#
# --------------------------------- 3. np.shape()
#
"""Return the shape of an array."""

vector = np.random.rand(5)
print(np.shape(vector))
# (5,)

matrix = np.random.rand(3, 4)
print(np.shape(matrix))
# (3, 4)

tensor = np.random.rand(2, 3, 4)
print(np.shape(tensor))
# (2, 3, 4)

##--------------------------------##

print(np.shape(tensor)[0])
# 2

print(np.shape(tensor)[1])
# 3

print(np.shape(tensor)[2])
# 4


#
# --------------------------------- 4. np.size()
#
"""Return the number of elements along a given axis."""

vector = np.random.rand(5)
print(np.size(vector))
# 5

matrix = np.random.rand(3, 4)
print(np.size(matrix))  # 12
print(np.size(matrix, axis=0))  # 3
print(np.size(matrix, axis=1))  # 4

tensor = np.random.rand(2, 3, 4)
print(np.size(tensor))  # 24
print(np.size(tensor, axis=0))  # 2
print(np.size(tensor, axis=1))  # 3
print(np.size(tensor, axis=2))  # 4
