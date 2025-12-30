'''
Flow of contents:
1. map()
2. itertools.starmap()
'''


'''
itertools.starmap() is similar to map(), 
but it unpacks the arguments from each tuple in the iterable(s) before applying the function.
'''

#-------------------------------------------------------------------------------------------------------#
#------------------------------------------------ map() ------------------------------------------------#
#-------------------------------------------------------------------------------------------------------#

'''
map() applies a function to every element in one or more iterables and produces a lazy, memory-efficient iterator.

map(function, iterable, *iterables) → map object creates an iterator that yields function(item1, item2, …) 
for each parallel group of items drawn from the supplied iterable(s)

map() returns a lazy map object, not a concrete collection. 
Values are computed only when the object is iterated, which keeps peak memory low for large streams.

To materialize results you must wrap with list(), tuple(), set() or loop over the iterator.
'''

################
## map object ##
################

numbers = [1, 2, 3, 4, 5]
map_object = map(lambda x: x ** 2, numbers)

# print out the map object
print(map_object)  # <map object at 0x7f8f521fffa0>

# Get the materialized results
squared = list(map_object)
print(squared)  # [1, 4, 9, 16, 25]
print(list(map(lambda x: x ** 2, numbers))) # [1, 4, 9, 16, 25]

print(list(map_object))  # [] (empty, as map object is exhausted)


########################################################
##           map(func, iterable, *iterables)          ##
########################################################

nums  = [1, 2, 3]
exps1  = [2, 3, 4]
exps2 = [5, 6, 7]

# pow(base, exp, mod) returns (base ** exp) % mod
# If the mod is not provided, it will return base ** exp (the exponentiation result only).

#-------------
## pass 2 iterables to pow() using map()
#-------------
print(list(map(pow, nums, exps1)))   # 1**2, 2**3, 3**4
                                     # [1, 8, 81]

'''
what actually happens is:
    pow(base=1, exp=2) = (1²) = 1
    pow(base=2, exp=3) = (2³) = 8
    pow(base=3, exp=4) = (3⁴) = 81
'''

#-------------
## pass 3 iterables to pow() using map()
#-------------

print(list(map(pow, nums, exps1, exps2)))
# [1, 2, 4]

'''
what actually happens is:
    pow(base=1, exp=2, mod=5) = (1²) % 5 = 1 % 5 = 1
    pow(base=2, exp=3, mod=6) = (2³) % 6 = 8 % 6 = 2
    pow(base=3, exp=4, mod=7) = (3⁴) % 7 = 81 % 7 = 4
'''


################################
## map() with lambda function ##
################################

lst_floats = [213.0, 321.5, 56198.99, 65489.55, 213.68]

output_lst = list(map(lambda x: x/100, lst_floats))

print(output_lst)
# [2.13, 3.215, 561.9899, 654.8955000000001, 2.1368]


#-------------------------------------------------------------------------------------------------------#
#---------------------------------------- itertools.starmap() ------------------------------------------#
#-------------------------------------------------------------------------------------------------------#

"""
itertools.starmap() is similar to map(), 
but it unpacks the arguments from each tuple in the iterable(s) before applying the function.
"""

from itertools import starmap


####################################
## starmap() with normal function ##
####################################

import sympy as syp

x, y, z = syp.symbols('x y z')

func_respect_order = [
    (2*x + 3*y - z, y, 1),
    (x**2 + 2*x*y + z**4, z, 3),
    (2**x + 3*z, x, 2)
]

# syp.diff(function, respect_variable, diff_time)

derrivative_result = list(starmap(syp.diff, func_respect_order))

print(derrivative_result)
# [3, 24*z, 2**x*log(2)**2]

'''
what actually happens is:
    syp.diff(2*x + 3*y - z, y, 1) => differentiating 2*x + 3*y - z with respect to y, 1 order
    syp.diff(x**2 + 2*x*y + z**4, z, 3) => differentiating x**2 + 2*x*y + z**4 with respect to z, 3 orders
    syp.diff(2**x + 3*z, x, 2 => differentiating 2**x + 3*z with respect to x, 2 orders
'''

###########################
## starmap() with lambda ##
###########################

height_width = [(1.5, 2.0), (2.0, 3.0), (3.0, 4.0)]

area = list(starmap(lambda h, w: h * w, height_width)) #NOTE: startmap() takes no keyword arguments

print(area) # 1.5*2.0, 2.0*3.0, 3.0*4.0 
            # [3.0, 6.0, 12.0]
