# List is a type of iteration in Python
# List allows storing duplicate HETEROGENEOUS datat (different datatypes)
# (however, should store homogeneous data to facilitate processing steps)
# First element has index = 0
# Last element has index = len(list) - 1 (or -1)

# Table content:
## Create a list
## Index/Access list's elements
## Update list's elements
## List methods: count, index, insert, append, extend, remove, pop, clear, copy, sort, reverse
## List concat and multiply
## map() to apply custom function to List
## List and Loops
## List comprehension


#------------------------------------------------------#
#----------------- Create a list ----------------------#
#------------------------------------------------------#

empty_list_1 = []      # => []
empty_list_2 = list()  # => []

list_num = [1, 2, 3, 4, 4] # Allow duplicate values
print(list_num)

tuple_str = ("A", "b", "C", "d", "A")
list_str = list(tuple_str)
print(list_str)

from datetime import date
list_mix = ["Lentani", 35.5, 20, date(1885, 12, 21), False]
print(list_mix)

text_str = "What,can,I,do,for,you,?"
list_split = text_str.split(",")
print(list_split)


#-----------------------------------------------------------------------#
#----------------- Index / Access list's elements ----------------------#
#-----------------------------------------------------------------------#

fruits = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]

print(fruits[0]) # apple
print(fruits[1]) # banana

print(fruits[-1]) # mango
print(fruits[-2]) # melon

print(fruits[:4]) # or fruits[0:4]
                  # ['apple', 'banana', 'cherry', 'orange']

print(fruits[2:]) # or fruits(2:-1)
                  # ['cherry', 'orange', 'kiwi', 'melon', 'mango']

print(fruits[-1:-4]) # []
                     # empty list because it index from the last element [-1] to the right
                     # but nothing is at the right at [-1], so return empty list

print(fruits[-1:-5:-1]) # ['mango', 'melon', 'kiwi', "orange"]
                        # negative sign "-" means reverse indexing (from left to right)
                        # with step = 1
                        # the -5 "cherry" are excluded

print(fruits[-1:-5:-2]) # ['mango', 'kiwi']
                        # reverse indexing with steps = -2, so "melon" and "orange" are bypassed
                        # the -5 "cherry" are excluded

print(fruits[-4:-1]) # ['orange', 'kiwi', 'melon']
                     # index from right to left as default
                     # start with -4 "orange"
                     # stop at -1 "mango" but excluded
                     #===> ['orange', 'kiwi', 'melon']


#---------------------------------------------------------#
#----------------- Update list item ----------------------#
#---------------------------------------------------------#

predators = ["tiger", "lion", "leopard"]
print(predators)

predators[2] = "wolf"
print(predators) # ['strawberry', 'guava', 'pear']

predators[0:2] = ["bear", "godzilla"]
print(predators) # ['bear', 'godzilla', 'wolf']

predators[1:] = ["eagle"]
print(predators) # ['bear', 'eagle']

# predators[1:] = "eagle"
# print(predators) # return ['bear', 'e', 'a', 'g', 'l', 'e']


#-----------------------------------------------------#
#----------------- List methods ----------------------#
#-----------------------------------------------------#

programmer_life = ["waking", "eating", "debugging", "crying", "hoping", "committing", "sweating", "crying"]

# .count() returns the number of a specified element within a list
print(programmer_life.count("crying")) # 2

# .index() returns the index of the first element with the specified value
print(programmer_life.index("crying")) # 3 (index of the first "crying")
print(programmer_life.index("committing"))

# .insert() to insert new element at a specified index
programmer_life.insert(0, "dreaming")
print(programmer_life)

## Notice: print(programmer_life.insert(0, "dreaming")) will return None
## => because it modifies the original list directly (in-place) and doesn’t create or return a new list.

# 
# append, extend, remove, pop, clear, copy, sort, reverse