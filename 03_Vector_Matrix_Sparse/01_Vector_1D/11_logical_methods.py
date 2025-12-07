'''
1. arr.all() ||| np.all(arr): Check if all elements in the array are True (non-zero).

2. arr.any() ||| np.any(arr): Check if any element in the array is True (non-zero).

3. arr.nonzero() ||| np.nonzero(arr): Return the indices of the elements that are non-zero (True).
'''

import numpy as np

vector_True = np.array([True, True, True, True])
vector_False = np.array([False, False, False, False])
vector_mixed = np.array([True, False, True, False])

vector_ones = np.ones(4) # array([1., 1., 1., 1.])
vector_zeros = np.zeros(4) # array([0., 0., 0., 0.])
vector_mixed_num = np.array([0, 1, 2, 0]) # array([0, 1, 2, 0])


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------ 1. arr.all() ||| np.all(arr) --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
arr.all(where=conditions) and np.all(arr, where=conditions)

Check if all elements in the array are True (non-zero),
or all satisfy the given conditions.
'''

################################
##      arr.all() method      ##
################################

#-----
## arr.all(): all elements are True (non-zero)
#-----

print(vector_True.all())
# True
# Returns True since all elements are True

print(vector_False.all())
# False
# Returns False since not all elements are True

print(vector_mixed.all())
# False
# Returns False since not all elements are True

print(vector_ones.all())
# True
# Returns True since all elements are non-zero

print(vector_zeros.all())
# False
# Returns False since not all elements are non-zero

print(vector_mixed_num.all())
# False
# Returns False since not all elements are non-zero

#-----
## arr.all(where=conditions): all elements satisfy conditions
#-----

print(vector_mixed_num.all(where=(vector_mixed_num > -1)))