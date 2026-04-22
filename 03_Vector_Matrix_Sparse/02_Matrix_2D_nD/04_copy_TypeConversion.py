'''
1. arr.copy(): Creates a copy of the array.

2. arr.astype(new_dtype): Converts the array to a different data type.
'''

import numpy as np

np.random.seed(42)
matrix = np.random.uniform(1, 11, size=(3, 5)).round(3)

print(matrix)
# [[ 4.745 10.507  8.32   6.987  2.56 ]
#  [ 2.56   1.581  9.662  7.011  8.081]
#  [ 1.206 10.699  9.324  3.123  2.818]]


#-----------------------------------------------------------------------------------------------------------------#
#--------------------------------- 1. array.copy(): Creates a copy of the array. ---------------------------------#
#-----------------------------------------------------------------------------------------------------------------#

copied_matrix = matrix.copy()
print(copied_matrix)
# [[ 4.745 10.507  8.32   6.987  2.56 ]
#  [ 2.56   1.581  9.662  7.011  8.081]
#  [ 1.206 10.699  9.324  3.123  2.818]]

print(id(matrix))          # 129000837850640
print(id(copied_matrix))   # 129000837850352

'''
By using array.copy(), we create a new array that is a copy of the original array.
So when the original array is modified, the copied array remains unchanged, as they occupy different memory locations.
'''


#-----------------------------------------------------------------------------------------------------------------#
#-------------------- 2. array.astype(new_dtype): Converts the array to a different data type. -------------------#
#-----------------------------------------------------------------------------------------------------------------#

int_matrix = matrix.copy().astype(np.int32)
print(int_matrix)
# [[ 4 10  8  6  2]
#  [ 2  1  9  7  8]
#  [ 1 10  9  3  2]]

complex_matrix = matrix.copy().astype(np.complex64)
print(complex_matrix)
# [[ 4.745+0.j 10.507+0.j  8.32 +0.j  6.987+0.j  2.56 +0.j]
#  [ 2.56 +0.j  1.581+0.j  9.662+0.j  7.011+0.j  8.081+0.j]
#  [ 1.206+0.j 10.699+0.j  9.324+0.j  3.123+0.j  2.818+0.j]]

'''
All numpy data types are here: https://numpy.org/doc/stable/user/basics.types.html
'''