'''
"lambda" enables concise, anonymous, single-expression functions 
that shine when passed inline to higher-order utilities (map, filter, sorted, etc.)

Use "lambda" for quick, short and throwaway functions.

Otherwise, reach for "def" once the function grows or needs a name, documentation, or multiple statements
'''

###################
## Basic example ##
###################

square = lambda x: x**2 # can under stand as "square = def square(x): return x ** 2"

print(square(x=5)) # Keyword argument
# 25

print(square(10)) # Positional argument
# 100

#########################
## Multiple parameters ##
#########################

affine_combination = lambda x, y, theta: theta*x + (1-theta)*y

affine_1 = affine_combination(x=2, y=3, theta=0.5)
print(affine_1)
# 2.5

affine_2 = affine_combination(5, 25, 0.9)
print(affine_2)
# 7.0

#######################
## lambda with map() ##
#######################

nums = [1, 2, 3, 4, 5, 6]
doubles = list(map(lambda x: x*2, nums))

print(doubles)
# [2, 4, 6, 8, 10, 12]

########################
## lambda with filter ##
########################

nums = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x%2 == 0, nums))

print(evens)
# [2, 4, 6]

##########################
## lambda with sorted() ##
##########################

#----------
## Sort words by length using lambda
#----------

words = ['lambda', 'is', 'handy']

print(sorted(words, key=lambda w: len(w))) 
# ['is', 'handy', 'lambda']

#---------------
## Sort a dictionanry by keys
#---------------

demo_dict = {
    "B": 5,
    "D": 1,
    "C": 3,
    "X": 7,
    "H": 10,
    "F": 4
}

sorted_dict_key = dict(
    sorted(
        demo_dict.items(), 
        key=lambda x: x[0], # sort by keys
        reverse=False # sort ascending
    )
)

for key, value in sorted_dict_key.items():
    print(f"{key}: {value}")
# B: 5
# C: 3
# D: 1
# F: 4
# H: 10
# X: 7

#---------------
## Sort a dictionanry by values
#---------------

sorted_dict_value = dict(
    sorted(
        demo_dict.items(), 
        key=lambda x: x[1], # sort by values
        reverse=True # sort descending
    )
)

for key, value in sorted_dict_value.items():
    print(f"{key}: {value}")
# H: 10
# X: 7
# B: 5
# F: 4
# C: 3
# D: 1  

#########################################
## use lambda for currying / factories ##
#########################################

def multiplier(n):
    return lambda x: x*n # returns a customized lambda

tripler = multiplier(3)

print(tripler(10))
# 30

############################
## lambda with logic code ##
############################

sign_check = lambda x: "Positive" if x > 0 else "Zero" if x == 0 else "Negative"

print(sign_check(15.2))
# Positive

print(sign_check(0))
# Zero

print(sign_check(-15.3))
# Negative

#############################
## Nested lambda functions ##
#############################

exponential = lambda x: (lambda y: x**y)
print(exponential(2)(3))  # 2^3 = 8
print(exponential(5)(2))  # 5^2 = 25