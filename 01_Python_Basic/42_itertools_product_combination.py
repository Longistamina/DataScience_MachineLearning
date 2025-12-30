'''
itertools is a Python module that provides functions that create iterators for memory efficient looping.

Flow of contents:
1. count(): Creates an iterator that generates consecutive integers starting from a specified number.
2. cycle(): Creates an iterator that cycles through an iterable indefinitely.
3. repeat(): Creates an iterator that repeats an object a specified number of times or indefinitely.
4. accumulate(): Creates an iterator that returns accumulated sums or results of a binary function applied to the elements of an iterable.
5. chain(): Combines multiple iterables into a single iterable.
6. compress(): Filters elements from an iterable based on a selector iterable.
7. dropwhile(): Drops elements from an iterable as long as a predicate is true, then returns the rest.
8. filterfalse(): Filters elements from an iterable where a predicate is false.
9. groupby(): Groups elements from an iterable based on a key function.
10. islice(): Returns selected elements from an iterable based on specified start, stop, and step parameters.
11. pairwise(): Returns consecutive pairs of elements from an iterable.
12. starmap(): Applies a function to elements from multiple iterables, returning results as tuples.
13. takewhile(): Takes elements from an iterable as long as a predicate is true, then stops.
14. tee(): Creates multiple independent iterators from a single iterable.
15. zip_longest(): Combines multiple iterables into tuples, filling missing values with a specified fill value.
16. product(): Computes the Cartesian product of input iterables.
17. permutations(): Generates all possible orderings of elements in an iterable.
18. combinations(): Generates all possible combinations of a specified length from an iterable.
19. combinations_with_replacement(): Generates combinations of a specified length from an iterable, allowing repeated elements.
'''

#--------------------------------------------------------------------------------------------#
#-------------------------------------- 1. count() ------------------------------------------#
#--------------------------------------------------------------------------------------------#

# count() creates an iterator that generates consecutive integers starting from a specified number.
# It can be used to create an infinite sequence of numbers, which can be useful in various
'''
NOTE: it will not stop until you stop it manually (using a stop condition or KeyboardInterrupt Ctrl+C).
'''

from itertools import count

counter = count(start=10, step=2)  # Start from 5, increment by 2

for num in counter:
    print(num)
    if num == 30:  # Stop condition to prevent infinite loop
        break

# 10
# 12
# 14
# 16
# 18
# 20
# 22
# 24
# 26
# 28
# 30


#--------------------------------------------------------------------------------------------#
#-------------------------------------- 2. cycle() ------------------------------------------#
#--------------------------------------------------------------------------------------------#

# cycle() creates an iterator that cycles through an iterable indefinitely.
'''
NOTE: it will not stop until you stop it manually (using a stop condition or KeyboardInterrupt Ctrl+C).
'''

from itertools import cycle

colors = ['red', 'green', 'blue']

cyler = cycle(colors)

for i, color in enumerate(cyler):
    print(f"{i} - {color}")
    if i == 8:  # Stop after 9 iterations to prevent infinite loop
        break

# 0 - red
# 1 - green
# 2 - blue
# 3 - red
# 4 - green
# 5 - blue
# 6 - red
# 7 - green
# 8 - blue


#--------------------------------------------------------------------------------------------#
#-------------------------------------- 3. repeat() -----------------------------------------#
#--------------------------------------------------------------------------------------------#

# repeat() creates an iterator that repeats an object a specified number of times or indefinitely.

from itertools import repeat

repeater = repeat(object='Hello', times=3)  # Repeat 'Hello' 3 times

print(repeater) # repeat('Hello', 3)
                # Not an iterator, but a repeat object

print(list(repeater))  # Convert to list to see the repeated values
# ['Hello', 'Hello', 'Hello']


print(
    list(
        repeat(
            object = ["A", True, 3.14],
            times = 4
        )
    )
)
# [['A', True, 3.14], ['A', True, 3.14], ['A', True, 3.14], ['A', True, 3.14]]


###########################
## Loop through repeater ##
###########################

repeater = repeat(object='Hello', times=3)

for i, value in enumerate(repeater):
    print(f"{i} - {value}")
# 0 - Hello
# 1 - Hello
# 2 - Hello


#--------------------------------------------------------------------------------------------#
#-------------------------------------- 4. accumulate() -------------------------------------#
#--------------------------------------------------------------------------------------------#

# accumulate() creates an iterator that returns accumulated sums or results of a binary function applied to the elements of an iterable.

from itertools import accumulate

numbers = [1, 2, 3, 4, 5]

accumulated = accumulate(numbers) # Default applied function is sum, but you can specify a different function
                                  # operator.add can be used to specify addition explicitly

print(list(accumulated))
# [1, 3, 6, 10, 15]
# 1 = 1
# 3 = 1 + 2
# 6 = 1 + 2 + 3
# 10 = 1 + 2 + 3 + 4
# 15 = 1 + 2 + 3 + 4 + 5


#############################################
## Using a custom function with accumulate ##
#############################################

from itertools import accumulate
from operator import mul  # Importing multiplication operator

numbers = [1, 2, 3, 4, 5]
accumulated_product = accumulate(numbers, func=mul)  # Using multiplication as the binary function

print(list(accumulated_product))
# [1, 2, 6, 24, 120]
# 1 = 1
# 2 = 1 * 2
# 6 = 1 * 2 * 3
# 24 = 1 * 2 * 3 * 4
# 120 = 1 * 2 * 3 * 4 * 5


#--------------------------------------------------------------------------------------------#
#-------------------------------------- 5. chain() ------------------------------------------#
#--------------------------------------------------------------------------------------------#

# chain() combines multiple iterables into a single iterable.

from itertools import chain

iterable1 = [1, 2, 3]
iterable2 = ['a', 'b', 'c']

chained_iterable = chain(iterable1, iterable2)
print(list(chained_iterable))
# [1, 2, 3, 'a', 'b', 'c']

chained_iterable = chain(iterable1, iterable2, iterable1, iterable2) # Chaining multiple iterables
print(list(chained_iterable))
# [1, 2, 3, 'a', 'b', 'c', 1, 2, 3, 'a', 'b', 'c']


#--------------------------------------------------------------------------------------------#
#-------------------------------------- 6. compress() ---------------------------------------#
#--------------------------------------------------------------------------------------------#

# compress() filters elements from an iterable based on a selector iterable.
# the selector iterable determines which elements to include in the output.

from itertools import compress

data = ['A', 'B', 'C', 'D', 'E']
selectors = [1, 0, 1, 0, 1]  # Selector iterable (1=include, 0=exclude)

compressed_data = compress(data, selectors)
print(list(compressed_data))
# ['A', 'C', 'E']


###########################
## More advanced example ##
###########################

numbers = [1, 2, 3, 4, 5]

even = [(num % 2 == 0) for num in numbers]  # Selector for even numbers
print(even)  # [False, True, False, True, False]

compressed_even_numbers = compress(numbers, even)
print(list(compressed_even_numbers))
# [2, 4]


#--------------------------------------------------------------------------------------------#
#-------------------------------------- 7. dropwhile() --------------------------------------#
#--------------------------------------------------------------------------------------------#

# dropwhile() drops elements from an iterable as long as a predicate is true, then returns the rest.

from itertools import dropwhile

data = [1, 2, 3, 4, 5, 6, 1, 1, 2, 4]

remaining = dropwhile(lambda x: x < 4, data)  # Drops elements while they are less than 4
print(list(remaining))
# [4, 5, 6, 1, 1, 2, 4]
# It stops dropping elements when it encounters the first element that is not less than 4
# (which is 4 in this case) and returns the rest of the iterable.


#--------------------------------------------------------------------------------------------#
#-------------------------------------- 8. filterfalse() ------------------------------------#
#--------------------------------------------------------------------------------------------#

# filterfalse() filters elements from an iterable where a predicate is false.

from itertools import filterfalse

nums = range(100)

filtered = filterfalse(lambda x: x % 10, nums)  # Filters out numbers that are multiples of 10
print(list(filtered))
# [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]

list(filter(None, nums))  # This will return all elements in nums since None is not a predicate


#--------------------------------------------------------------------------------------------#
#-------------------------------------- 9. groupby() ----------------------------------------#
#--------------------------------------------------------------------------------------------#

# groupby() groups elements from an iterable based on a key function.
'''
NOTE: groupby() only groups consecutive elements that have the same key.
'''

##################################
## Consecutive grouping example ##
##################################

from itertools import groupby

data = [('A', 1), ('A', 2), ('B', 3), ('B', 4), ('C', 5)]

grouped_data = groupby(data, key=lambda x: x[0])  # Group by the first element of each tuple

for key, group in grouped_data:
    print(key, list(group), sep = ": ")
# A: [('A', 1), ('A', 2)]
# B: [('B', 3), ('B', 4)]
# C: [('C', 5)]


######################################
## Non-consecutive grouping example ##
######################################

from itertools import groupby

data = [('A', 1), ('B', 2), ('A', 3), ('B', 4), ('C', 5)]
sorted_data = sorted(data, key=lambda x: x[0])  # Sort data to ensure grouping works correctly

grouped_data = groupby(sorted_data, key=lambda x: x[0])  # Group by the first element of each tuple

for key, group in grouped_data:
    print(key, list(group), sep = ": ")
# A: [('A', 1), ('A', 2)]
# B: [('B', 3), ('B', 4)]
# C: [('C', 5)]


###################################
## Grouping duplicates in a list ##
###################################

from itertools import groupby

data = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
sorted_data = sorted(data)  # Sort data to ensure grouping works correctly

grouped_data = [list(g) for _, g in groupby(sorted_data)]  # Group by the elements themselves

print(grouped_data)
# [['apple', 'apple', 'apple'], ['banana', 'banana'], ['orange']]


#########################################
## Grouping with a custom key function ##
#########################################

from itertools import groupby

# List of numbers
numbers = [2, 4, 6, 7, 8, 10, 11, 12, 13]

# Group by even/odd
grouped = groupby(numbers, key=lambda x: 'Even' if x % 2 == 0 else 'Odd')

for key, group in grouped:
    print(f"{key} -> {list(group)}")
# Even -> [2, 4, 6]
# Odd -> [7]
# Even -> [8, 10]
# Odd -> [11]
# Even -> [12]
# Odd -> [13]

'''
In this example, we group the numbers into 'Even' and 'Odd' categories using a custom key function.
The key function checks if each number is even or odd and groups them accordingly.

As we can see, the groupby function only groups consecutive elements with the same key.
If the input of the same group is not consecutive, it will be "scattered"
'''


#--------------------------------------------------------------------------------------------#
#-------------------------------------- 10. islice() ----------------------------------------#
#--------------------------------------------------------------------------------------------#

# islice() returns selected elements from an iterable based on specified start, stop, and step parameters.
'''islice() takes no Keyword arguments, only positional arguments'''

from itertools import islice

data = range(10)  # Create a range object from 0 to 9

sliced_data = islice(data, 2, 8, 2)  # Get elements from index 2 to 8 with a step of 2
print(list(sliced_data))
# [2, 4, 6]


##############################################
## slice with no start, no stop and no step ##
##############################################

l = ['a', 'b', 'c', 'd', 'e']

sliced_l = islice(l, 2)  # Get elements from index 0 to 2 (default step is 1)
print(list(sliced_l))
# ['a', 'b']

sliced_l = islice(l, 2, None)  # Get elements from index 2 to the end (default step is 1)
print(list(sliced_l))
# ['c', 'd', 'e']


#--------------------------------------------------------------------------------------------#
#-------------------------------------- 11. pairwise() --------------------------------------#
#--------------------------------------------------------------------------------------------#

# pairwise() returns consecutive pairs of elements from an iterable.
'''
NOTE: if the iterable is empty or has only one element, it will return an empty iterator.
'''

from itertools import pairwise

string = "abcdefg"
pairs = pairwise(string)  # Get consecutive pairs of characters
print(list(pairs))
# [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('e', 'f'), ('f', 'g')]

string = "a"
pairs = pairwise(string)
print(list(pairs))
# []

lst = [1, 2, 3, 4, 5]
pairs = pairwise(lst)  # Get consecutive pairs of numbers
print(list(pairs))
# [(1, 2), (2, 3), (3, 4), (4, 5)]


#------------------------------------------------------------------------------------------------#
#---------------------------------------- 12.starmap() ------------------------------------------#
#------------------------------------------------------------------------------------------------#

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


#--------------------------------------------------------------------------------------------#
#-------------------------------------- 13. takewhile() -------------------------------------#
#--------------------------------------------------------------------------------------------#

# takewhile() takes elements from an iterable as long as a predicate is true, then stops.
# it is the opposite of dropwhile().

from itertools import takewhile

data = [1, 2, 3, 4, 5, 6, 1, 1, 2, 4]

taken = takewhile(lambda x: x < 4, data)  # Takes elements while they are less than 4
print(list(taken))
# [1, 2, 3]
# It stops taking elements when it encounters the first element that is not less than 4


#--------------------------------------------------------------------------------------------#
#-------------------------------------- 14. tee() -------------------------------------------#
#--------------------------------------------------------------------------------------------#

# tee() creates multiple independent iterators from a single iterable.

from itertools import tee

data = [1, 2, 3, 4, 5]

iter1, iter2 = tee(data, 2)  # Create two independent iterators from the same data

print(list(iter1))  # [1, 2, 3, 4, 5]
print(list(iter2))  # [1, 2, 3, 4, 5]


#-------------------------------------------------------------------------------------------#
#------------------------------------- 15. zip_longest() -----------------------------------#
#-------------------------------------------------------------------------------------------#

# zip_longest() combines multiple iterables into tuples, filling missing values with a specified fill value.
# Default fill value is None.

################################
## Default fill value is None ##
################################

from itertools import zip_longest

iter1 = [1, 2, 3, 4, 5]
iter2 = ['a', 'b', 'c']
iter3 = [True, False]

zipped = zip_longest(iter1, iter2, iter3)  # Combine iterables, filling missing values with None
print(list(zipped))
# [(1, 'a', True), (2, 'b', False), (3, 'c', None), (4, None, None), (5, None, None)]

for i, j, k in zipped: # or in zip_longest(iter1, iter2, iter3, fillvalue='X'):
    print(f"{i} - {j} - {k}")
# 1 - a - True
# 2 - b - False
# 3 - c - None
# 4 - None - None
# 5 - None - None

'''
Here, the first three tuples are filled with values from the respective iterables,
while the remaining tuples are filled with None for the missing values.
'''


#######################################
## Custom fill value using fillvalue ##
#######################################

from itertools import zip_longest

iter1 = [1, 2, 3, 4, 5]
iter2 = ['a', 'b', 'c']
iter3 = [True, False]

zipped = zip_longest(iter1, iter2, iter3, fillvalue="Empty")  # Combine iterables, filling missing values with None
print(list(zipped))
# [(1, 'a', True), (2, 'b', False), (3, 'c', 'Empty'), (4, 'Empty', 'Empty'), (5, 'Empty', 'Empty')]

for i, j, k in zipped:  # or in zip_longest(iter1, iter2, iter3, fillvalue='X'):
    print(f"{i} - {j} - {k}")
# 1 - a - True
# 2 - b - False
# 3 - c - Empty
# 4 - Empty - Empty
# 5 - Empty - Empty


#--------------------------------------------------------------------------------------------#
#-------------------------------------- 16. product() ---------------------------------------#
#--------------------------------------------------------------------------------------------#

# product() computes the Cartesian product of input iterables.
'''
NOTE: it returns a one-time consumed iterator. Cannot be reused.
'''

from itertools import product

iter1 = [1, 2]
iter2 = ['a', 'b', "c"]
iter3 = [True, False]

cartesian_product = product(iter1, iter2, iter3)  # Compute the Cartesian product of the input iterables
print(list(cartesian_product))
# [(1, 'a', True), (1, 'a', False), (1, 'b', True), (1, 'b', False), (1, 'c', True), (1, 'c', False), (2, 'a', True), (2, 'a', False), (2, 'b', True), (2, 'b', False), (2, 'c', True), (2, 'c', False)]

'''
After this line, the cartesian_product iterator is exhausted.
If you try to print it again, it will return an empty list.

To reproduce the cartesian product, you need to create a new iterator.
'''

# Loop through the cartesian product
cartesian_product = product(iter1, iter2, iter3)
for result in list(cartesian_product):
    print(result)
# (1, 'a', True)
# (1, 'a', False)
# (1, 'b', True)
# (1, 'b', False)
# (1, 'c', True)
# (1, 'c', False)
# (2, 'a', True)
# (2, 'a', False)
# (2, 'b', True)
# (2, 'b', False)
# (2, 'c', True)
# (2, 'c', False)


##################################
## Product with repeat argument ##
##################################

# The repeat argument allows you to compute the Cartesian product of the same iterable multiple times.

product_with_repeat = product(iter1, iter2, repeat=2)  # Compute the Cartesian product with repeat

for result in product_with_repeat:
    print(result)
# (1, 'a', 1, 'a')
# (1, 'a', 1, 'b')
# (1, 'a', 1, 'c')
# (1, 'a', 2, 'a')
# (1, 'a', 2, 'b')
# (1, 'a', 2, 'c')
# (1, 'b', 1, 'a')
# (1, 'b', 1, 'b')
# (1, 'b', 1, 'c')
# (1, 'b', 2, 'a')
# (1, 'b', 2, 'b')
# (1, 'b', 2, 'c')
# (1, 'c', 1, 'a')
# (1, 'c', 1, 'b')
# (1, 'c', 1, 'c')
# (1, 'c', 2, 'a')
# (1, 'c', 2, 'b')
# (1, 'c', 2, 'c')
# (2, 'a', 1, 'a')
# (2, 'a', 1, 'b')
# (2, 'a', 1, 'c')
# (2, 'a', 2, 'a')
# (2, 'a', 2, 'b')
# (2, 'a', 2, 'c')
# (2, 'b', 1, 'a')
# (2, 'b', 1, 'b')
# (2, 'b', 1, 'c')
# (2, 'b', 2, 'a')
# (2, 'b', 2, 'b')
# (2, 'b', 2, 'c')
# (2, 'c', 1, 'a')
# (2, 'c', 1, 'b')
# (2, 'c', 1, 'c')
# (2, 'c', 2, 'a')
# (2, 'c', 2, 'b')
# (2, 'c', 2, 'c')


#--------------------------------------------------------------------------------------------#
#-------------------------------------- 17. permutations() ----------------------------------#
#--------------------------------------------------------------------------------------------#

# permutations() generates all possible orderings of elements in an iterable.

from itertools import permutations

letter = ['A', 'B', 'C']

permutations_result = permutations(letter)  # Generate all permutations of the letters
print(list(permutations_result))
# [('A', 'B', 'C'), ('A', 'C', 'B'), ('B', 'A', 'C'), ('B', 'C', 'A'), ('C', 'A', 'B'), ('C', 'B', 'A')]


# Loop through the permutations
permutations_result = permutations(letter)
for perm in list(permutations_result):
    print(*perm, sep=" - ")
# A - B - C
# A - C - B
# B - A - C
# B - C - A
# C - A - B
# C - B - A


##########################################
## Permutations with a specified length ##
##########################################

letter = ['A', 'B', 'C']

permutations_result = permutations(letter, r=2)  # Generate permutations of length 2
print(list(permutations_result))
# [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]


#---------------------------------------------------------------------------------------------#
#-------------------------------------- 18. combinations() -----------------------------------#
#---------------------------------------------------------------------------------------------#

# combinations() generates all possible combinations of a specified length from an iterable.
# (does not consider the order of elements)

from itertools import combinations

letters = ['A', 'B', 'C']

combination_3 = combinations(letters, r=3)  # Generate combinations of length 3
print(list(combination_3))
# [('A', 'B', 'C')]
# If the r equals the length of the iterable, it will return only one combination (the iterable itself).

combination_2 = combinations(letters, r=2)  # Generate combinations of length 2
print(list(combination_2))
# [('A', 'B'), ('A', 'C'), ('B', 'C')]


#----------------------------------------------------------------------------------------------#
#---------------------------- 19. combinations_with_replacement() -----------------------------#
#----------------------------------------------------------------------------------------------#

# combinations_with_replacement() generates combinations of a specified length from an iterable,
# allowing repeated elements.

from itertools import combinations_with_replacement

data = [0, 1, 2, 3]

result = combinations_with_replacement(data, r=2)  # Generate combinations of length 2 with replacement

for comb in list(result):
    print(comb)
# (0, 0)
# (0, 1)
# (0, 2)
# (0, 3)
# (1, 1)
# (1, 2)
# (1, 3)
# (2, 2)
# (2, 3)
# (3, 3)