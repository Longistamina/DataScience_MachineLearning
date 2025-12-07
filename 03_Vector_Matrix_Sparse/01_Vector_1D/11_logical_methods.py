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
arr.all() and np.all(): check if all elements in the array are True (or non-zero).

(True if all are True/non-zero, False otherwise)

Can use them to verify if a boolean mask (array) is entirely True, or if all numerical values in an array are non-zero.
'''

################################
##      arr.all() method      ##
################################

#-----
## arr.all(): all elements are True (or non-zero)
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
## Logical array (mask) checking
#-----

print(vector_mixed_num > -1) # [True True True True]
print((vector_mixed_num > -1).all()) # True
# Returns True since all elements are greater than -1 (all are True)

print((vector_mixed_num == 2)) # [False False  True False]
print((vector_mixed_num == 2).all()) # False
# Returns False since not all elements are equal to 2 (not all are True)

#################################
##      np.all() function      ##
#################################

#-----
## np.all(): all elements are True (or non-zero)
#-----

print(np.all(vector_True)) # True
print(np.all(vector_False)) # False
print(np.all(vector_mixed)) # False

print(np.all(vector_ones)) # True
print(np.all(vector_zeros)) # False
print(np.all(vector_mixed_num)) # False

#-----
## Logical array (mask) checking
#-----

print(np.all(vector_mixed_num > -1)) # True
print(np.all(vector_mixed_num == 2)) # False


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------ 2. arr.any() ||| np.any(arr) --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
arr.any() and np.any(): check if any element in the array is True (or non-zero).

(False if all are False/zero, True otherwise)

Can use them to verify if a boolean mask (array) has at least one True, or if any numerical value in an array is non-zero.
'''

################################
##      arr.any() method      ##
################################

#-----
## arr.any(): any element is True (or non-zero)
#-----

print(vector_True.any())
# True
# Returns True since at least one element is True

print(vector_False.any())
# False
# Returns False since no elements are True

print(vector_mixed.any())
# True
# Returns True since at least one element is True

print(vector_ones.any())
# True
# Returns True since at least one element is non-zero

print(vector_zeros.any())
# False
# Returns False since no elements are non-zero

print(vector_mixed_num.any())
# True
# Returns True since at least one element is non-zero

#-----
## Logical array (mask) checking
#-----

print(vector_mixed_num > 1) # [False False  True False]
print((vector_mixed_num > 1).any()) # True
# Returns True since at least one element is greater than 1 (at least one is True

print((vector_mixed_num < -1)) # [False False False False]
print((vector_mixed_num < -1).any()) # False
# Returns False since no elements are less than -1 (none are True)

#################################
##      np.any() function      ##
#################################

#-----
## np.any(): any element is True (or non-zero)
#-----

print(np.any(vector_True)) # True
print(np.any(vector_False)) # False
print(np.any(vector_mixed)) # True

print(np.any(vector_ones)) # True
print(np.any(vector_zeros)) # False
print(np.any(vector_mixed_num)) # True

#-----
## Logical array (mask) checking
#-----

print(np.any(vector_mixed_num > 1)) # True
print(np.any(vector_mixed_num < -1)) # False


#--------------------------------------------------------------------------------------------------------------#
#------------------------------ 3. arr.nonzero() ||| np.nonzero(arr) ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
arr.nonzero() and np.nonzero(): return the indices of the elements that are non-zero (or True).

Can be used like arr.compress() or np.compress() to filter elements based on a boolean mask.
'''

vector_mixed = np.array([True, False, True, False])
vector_mixed_num = np.array([0, 1, 2, 0])

####################################
##      arr.nonzero() method      ##
####################################

#-----
## arr.nonzero(): indices of non-zero (or True) elements
#-----

print(vector_mixed.nonzero())
# (array([0, 2]),)
# Returns indices of True elements in the boolean array

print(vector_mixed_num.nonzero())
# (array([1, 2]),)
# Returns indices of non-zero elements in the numerical array

#-----
## Logical array (mask) checking
#-----

print(vector_mixed_num % 2 == 0)
# [ True False  True  True]

print((vector_mixed_num % 2 == 0).nonzero())
# (array([0, 2, 3]),)
# Returns indices of elements that are EVEN (True in the mask)

###################################
##      np.nonzero() function    ##
###################################

#-----
## np.nonzero(): indices of non-zero (or True) elements
#-----

print(np.nonzero(vector_mixed)) # (array([0, 2]),)
print(np.nonzero(vector_mixed_num)) # (array([1, 2]),)

#-----
## Logical array (mask) checking
#-----

print(vector_mixed_num > 0)
# [False  True  True False]

print(np.nonzero(vector_mixed_num > 0)) 
# (array([1, 2]),)
# Returns indices of elements greater than 0 (True in the mask)