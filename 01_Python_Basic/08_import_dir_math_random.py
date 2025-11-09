#------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- math Library ---------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------#

import math
a = math.sqrt(16) # 4
b = math.pow(2,3) # 2**3 = 8
math.pi # pi number

print(dir(math)) # list out all the functions, methods and attributes of an object

# math.floor(x) => Return the smallest and nearest integer number of x
math.floor(5.25) # returns 5

# math.modf(x) => Separate and returns the decimal and the quotient of a float number
decimal, quotient = math.modf(3.5)
print(decimal) # 0.5
print(quotient) # 3.0

'''
The math.modf() does not always return the expected exact decimal and quotient.

Take math.modf(2.5) as example:
# Most of the time, it returns (0.5, 2.0)
# But sometimes, it returns (0.49999999999999994, 2.0)
# Or (0.5000000000000001, 2.0)

This is due to the way floating-point numbers are represented in binary, which can lead to small rounding errors.
'''


#---------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------ random Library -----------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------#

import random

n1 = random.random() # Generate a random float number in range of [0,1)
print(n1)

n2 = random.uniform(10,20) # Generate a random float number x where 10 =< x < 20
print(n2)

n3 = random.randrange(10,20,1) # Returns a randomly selected element from the specified range (start = 10, stop = 20, step = 1).
print(n3)

n4 = random.randint(10,20) # Generate a random integer number in range of [10,20]
print(n4)

################

random.seed(42) # Set the seed for random number generator for reproducibility
print(random.random()) # This will always print the same number when the seed is set to