'''
1. arr.copy(): Creates a copy of the array.

2. arr.view(): Creates a view of the array (shallow copy).

3. arr.astype(new_dtype): Converts the array to a different data type.
'''

import numpy as np


#-----------------------------------------------------------------------------------------------------------------#
#--------------------------------- 1. array.copy(): Creates a copy of the array. ---------------------------------#
#-----------------------------------------------------------------------------------------------------------------#

original_vector = np.array([1, 2, 3, 4, 5])
print(original_vector)
# [1 2 3 4 5]

copied_vector = original_vector.copy()
print(copied_vector)
# [1 2 3 4 5]

print(id(original_vector)) # 139748935997008
print(id(copied_vector))   # 139748935996432

'''
By using array.copy(), we create a new array that is a copy of the original array.

So when the original array is modified, the copied array remains unchanged, as they occupy different memory locations.
'''

