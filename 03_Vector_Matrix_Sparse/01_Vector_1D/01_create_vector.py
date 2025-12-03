'''
1. Create a 1D vector using np.array():
   + from list
   + from tuple

2. Create a 1D vector using other numpy functions:
   + np.arange()
   + np.linspace()
   + np.zeros()
   + np.ones()
   + np.full()
   + np.random.rand()
   + np.random.randn()
   + np.random.uniform()
   + np.random.randint()
   + np.random.seed(): for reproducibility
   + np.choose()

3. Create a 1D array with dtype specified (int, float, complex, bool, etc.)
'''

import numpy as np


#-----------------------------------------------------------------------------------------------------------------#
#----------------------------------- 1. Create 1D vector using np.array() ----------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#

#################
## From a list ##
#################

vector_list = np.array([10, 20, 30, 40, 50])

print(vector_list)
# [10 20 30 40 50]

##################
## From a tuple ##
##################

vector_tuple = np.array((5.6, 15.7, 25.92, 35, 45))

print(vector_tuple)
# [ 5.6  15.7  25.92 35.   45.  ]


#-----------------------------------------------------------------------------------------------------------------#
#------------------------------ 2. Create 1D vector using other numpy functions ----------------------------------#
#-----------------------------------------------------------------------------------------------------------------#

#######################
## Using np.arange() ##
#######################
'''np.arange(start, stop, step)'''

vector_arange = np.arange(0, 20, 2)

print(vector_arange)
# [ 0  2  4  6  8 10 12 14 16 18]

#########################
## Using np.linspace() ##
#########################
'''np.linspace(start, stop, num)'''

vector_linspace = np.linspace(0, 1, 5)

print(vector_linspace)
# [0.   0.25 0.5  0.75 1.  ]

######################
## Using np.zeros() ##
######################
'''np.zeros(shape)'''

vector_zeros = np.zeros(6)

print(vector_zeros)
# [0. 0. 0. 0. 0. 0.]

#####################
## Using np.ones() ##
#####################
'''np.ones(shape)'''

vector_ones = np.ones(4)

print(vector_ones)
# [1. 1. 1. 1.]

#####################
## Using np.full() ##
#####################
'''np.full(shape, fill_value)'''

vector_full = np.full(5, 7)

print(vector_full)
# [7 7 7 7 7]

############################
## Using np.random.rand() ##
############################
'''
np.random.rand(shape)
Creates an array of the given shape and populates it with random samples from a uniform distribution over [0, 1).
'''

vector_rand = np.random.rand(8)

print(vector_rand)
# [0.6467176  0.0945626  0.9247842  0.63424422 0.68531672 0.95500185
#  0.22267681 0.92068831]

#############################
## Using np.random.randn() ##
#############################
'''
np.random.randn(shape)
Creates an array of the given shape and populates it with random samples from the standard normal distribution.
                                                                                  (mean = 0, standard deviation = 1)
'''

vector_randn = np.random.randn(7)

print(vector_randn)
# [ 1.31882829 -0.01315057  0.08711981  0.28162462  0.24418609  1.39280667
#   0.7394099 ]

###############################
## Using np.random.uniform() ##
###############################
'''
np.random.uniform(low, high, size)
Creates an array of the given size and populates it with random samples from a uniform distribution over [low, high).
'''

vector_uniform = np.random.uniform(5.0, 15.0, 5)

print(vector_uniform)
# [ 6.46700683 12.07411923  5.75504924 14.80880126 10.86106915]

###############################
## Using np.random.randint() ##
###############################
'''
np.random.randint(low, high, size)
Creates an array of the given size and populates it with random integers from low (inclusive) to high (exclusive).
'''

vector_randint = np.random.randint(10, 50, 6)

print(vector_randint)
# [46 40 46 21 36 40]

############################
## Using np.random.seed() ##
############################
'''
np.random.seed(seed)
Sets the seed for NumPy's random number generator to ensure reproducibility.
'''

np.random.seed(42)
vector_seeded = np.random.rand(5)

print(vector_seeded)
# [0.37454012 0.95071431 0.73199394 0.59865848 0.15601864]

'''
Always produces the same output when the seed is set.
If the seed is changed, then different random numbers will be generated.
'''

#######################
## Using np.choose() ##
#######################
'''
np.choose(a, choices)
Constructs an array by picking elements from a list of choices based on the indices provided in array 'a'.
'''

choices = [np.array([10, 20, 30, 40, 50]), np.array([60, 70, 80, 90, 100])]
idx = np.array([0, 1, 0, 0, 1])

vector_choose = np.choose(idx, choices)
print(vector_choose)
# [ 10  70  30  40 100]
'''
10: the 1st element from choices[0]
70: the 2nd element from choices[1]
30: the 3rd element from choices[0]
40: the 4th element from choices[0]
100: the 5th element from choices[1]
'''


#-----------------------------------------------------------------------------------------------------------------#
#----------------------------------- 3. Create a 1D array with dtype specified -----------------------------------#
#-----------------------------------------------------------------------------------------------------------------#

vector_float32 = np.array([1, 2, 3, 4, 5], dtype=np.float32)
print(vector_float32) # [1. 2. 3. 4. 5.]
print(vector_float32.dtype) # float32

vector_int64 = np.array([1.5, 2.7, 3.9, 4.1, 5.6], dtype=np.int64)
print(vector_int64) # [1 2 3 4 5] (values are truncated to integers)
print(vector_int64.dtype) # int64
