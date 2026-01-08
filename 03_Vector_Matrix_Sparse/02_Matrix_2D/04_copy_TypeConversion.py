'''
1. arr.copy(): Creates a copy of the array.

2. arr.astype(new_dtype): Converts the array to a different data type.
'''

import numpy as np

np.random.seed(42)
matrix = np.random.uniform(1, 11, size=(3, 5))

print(matrix)
# [49. 49. 49. 49. 49. 50. 50. 50. 51. 56.]


#-----------------------------------------------------------------------------------------------------------------#
#--------------------------------- 1. array.copy(): Creates a copy of the array. ---------------------------------#
#-----------------------------------------------------------------------------------------------------------------#

copied_matrix = matrix.copy()
print(copied_matrix[:10])
# [49. 49. 49. 49. 49. 50. 50. 50. 51. 56.]

print(id(matrix))          # 140028990011504
print(id(copied_matrix))   # 140030373244112

'''
By using array.copy(), we create a new array that is a copy of the original array.
So when the original array is modified, the copied array remains unchanged, as they occupy different memory locations.
'''


#-----------------------------------------------------------------------------------------------------------------#
#-------------------- 2. array.astype(new_dtype): Converts the array to a different data type. -------------------#
#-----------------------------------------------------------------------------------------------------------------#

int_matrix = matrix.copy().astype(np.int32)
print(int_matrix[:10])
# [49 49 49 49 49 50 50 50 51 56]

complex_matrix = matrix.copy().astype(np.complex64)
print(complex_matrix[:10])
# [49.+0.j 49.+0.j 49.+0.j 49.+0.j 49.+0.j 50.+0.j 50.+0.j 50.+0.j 51.+0.j 56.+0.j]

'''
All numpy data types are here: https://numpy.org/doc/stable/user/basics.types.html
'''