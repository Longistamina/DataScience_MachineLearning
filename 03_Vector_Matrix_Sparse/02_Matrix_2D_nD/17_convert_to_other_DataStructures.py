'''
1. matrix.tolist(): Converts a NumPy 2D array to a nested Python list.

2. tuple(map(tuple, matrix)): Converts a NumPy 2D array to a tuple of tuples.

3. matrix.flatten() / matrix.ravel(): Flattens a 2D array to 1D (useful for set conversion).

4. pd.DataFrame(matrix): Converts a NumPy 2D array to a Pandas DataFrame.
'''

import numpy as np
import pandas as pd

np.random.seed(0)
matrix = np.random.uniform(0, 11, (4, 3)).round(2)

print(matrix)
# [[ 6.04  7.87  6.63]
#  [ 5.99  4.66  7.1 ]
#  [ 4.81  9.81 10.6 ]
#  [ 4.22  8.71  5.82]]


# =========================================================================================
# 1. matrix.tolist()
# =========================================================================================

print(matrix.tolist())
# [[6.04, 7.87, 6.63], [5.99, 4.66, 7.1], [4.81, 9.81, 10.6], [4.22, 8.71, 5.82]]

list_matrix = matrix.tolist()
print(type(list_matrix)) # <class 'list'>
print(list_matrix) # [[6.04, 7.87, 6.63], [5.99, 4.66, 7.1], [4.81, 9.81, 10.6], [4.22, 8.71, 5.82]]


# =========================================================================================
# 2. tuple(map(tuple, matrix))
# =========================================================================================

print(tuple(map(tuple, matrix)))
# ((np.float64(6.04), np.float64(7.87), np.float64(6.63)), (np.float64(5.99), np.float64(4.66), np.float64(7.1)), (np.float64(4.81), np.float64(9.81), np.float64(10.6)), (np.float64(4.22), np.float64(8.71), np.float64(5.82)))

tuple_matrix = tuple(map(tuple, matrix))
print(type(tuple_matrix)) # <class 'tuple'>
print(tuple_matrix) # ((np.float64(6.04), np.float64(7.87), np.float64(6.63)), (np.float64(5.99), np.float64(4.66), np.float64(7.1)), (np.float64(4.81), np.float64(9.81), np.float64(10.6)), (np.float64(4.22), np.float64(8.71), np.float64(5.82)))


# =========================================================================================
# 3. matrix.flatten() / matrix.ravel()
# =========================================================================================

print(matrix.flatten())
# [ 6.04  7.87  6.63  5.99  4.66  7.1   4.81  9.81 10.6   4.22  8.71  5.82]

flattened_matrix = matrix.flatten()
print(type(flattened_matrix)) # <class 'numpy.ndarray'>
print(flattened_matrix) # [6.04 7.87 6.63 5.99 4.66 7.1  4.81 7.89 1.32 9.52 6.9  4.53]

'''NOTE: flatten() returns a copy, while ravel() returns a view when possible. Both convert 2D to 1D.'''


# =========================================================================================
# 4. pd.DataFrame(matrix)
# =========================================================================================

print(pd.DataFrame(matrix))
#       0     1      2
# 0  6.04  7.87   6.63
# 1  5.99  4.66   7.10
# 2  4.81  9.81  10.60
# 3  4.22  8.71   5.82

df_matrix = pd.DataFrame(matrix)
print(type(df_matrix)) # <class 'pandas.core.frame.DataFrame'>
print(df_matrix)
#       0     1      2
# 0  6.04  7.87   6.63
# 1  5.99  4.66   7.10
# 2  4.81  9.81  10.60
# 3  4.22  8.71   5.82
