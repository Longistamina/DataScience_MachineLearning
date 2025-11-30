'''
List is a type of iteration in Python

List allows storing duplicate HETEROGENEOUS data (different datatypes)
(however, should store homogeneous data to facilitate processing steps)

First element has index = 0
Last element has index = len(list) - 1 (or -1)

# Table of contents:
## Create a list
## Index/Access list's elements
## Update list's elements
## List methods: count, index, insert, append, extend, remove, pop, clear, copy, sort, reverse
## List concat and multiply
## List and Loops and 2D list
## List comprehension
## Numeric List calculating with Aggregate Functions
## map() and list comprehension for list element-wise calculation
'''


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
# ['What', 'can', 'I', 'do', 'for', 'you', '?']


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

print(fruits[2:]) # from fruits[2] to the last element fruits[-1] (and also included)
                  # ['cherry', 'orange', 'kiwi', 'melon', 'mango']

print(fruits[2:5]) # from fruits[2] to fruits[5] but excluded fruits[5]
                   # ['cherry', 'orange', 'kiwi']

print(fruits[1:6:2]) # from fruits[1] to fruits[6] but excluded fruits[6]
                     # ['banana', 'orange', 'melon']

print(fruits[-1:-4]) # []
                     # empty list because it index from the last element [-1] to the right
                     # but nothing is at the right at [-1], so return empty list

print(fruits[-1:-5:-1]) # ['mango', 'melon', 'kiwi', 'orange']
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

# Check if item exist in List
if "apple" in fruits:
    print("Yes, 'apple' is in the fruits list")


#---------------------------------------------------------#
#----------------- Update list item ----------------------#
#---------------------------------------------------------#

predators = ["tiger", "lion", "leopard"]
print(predators)

predators[2] = "wolf"
print(predators) # ['tiger', 'lion', 'wolf']

predators[0:2] = ["bear", "godzilla"]
print(predators) # ['bear', 'godzilla', 'wolf']

predators[1:] = ["eagle"]
print(predators) # ['bear', 'eagle']

'''
predators[1:] = "eagle"
print(predators) # return ['bear', 'e', 'a', 'g', 'l', 'e']
'''

#-----------------------------------------------------#
#----------------- List methods ----------------------#
#-----------------------------------------------------#

# .count()
# .index()
# .insert()
# .append()
# .extend()
# .remove()
# .pop()
# .clear()
# .copy()
# .sort()
# .reverse()

programmer_life = ["waking", "eating", "debugging", "crying", "hoping", "crying"]

###############
### .count() ##
###############
'''.count() returns the number of a specified element within a list'''

print(programmer_life.count("crying")) # 2

##############
## .index() ##
##############
'''.index() returns the index of the first element with the specified value'''

print(programmer_life.index("crying")) # 3 (index of the first "crying")
print(programmer_life.index("eating")) # 1

###############
## .insert() ##
############### 
'''.insert() to insert new element at a specified index'''

programmer_life.insert(0, "dreaming")
print(programmer_life) 
# ['dreaming', 'waking', 'eating', 'debugging', 'crying', 'hoping', 'crying']

'''
NOTE: print(programmer_life.insert(0, "dreaming")) will return None
      => because it modifies the original list directly (in-place) and doesn't create or return a new list.
'''

###############
## .append() ##
###############
'''.append() adds ONLY ONE element per run at the end of the list'''

programmer_life.append(4)
print(programmer_life)
# ['dreaming', 'waking', 'eating', 'debugging', 'crying', 'hoping', 'crying', 4]

animals = ["dog", "cat", "bird"]
animals.append([4, 3])
print(animals) # ["dog", "cat", "bird", [4, 3]]

###############
## .extend() ##
###############
'''.extend() acts like .append() but can add any iterable object with separate elements'''

moods = ["happy", "sad", "anxious"]
thistuple = ("Yay!!!!", True, 142.2) # or can be a list or set
moods.extend(thistuple)
print(moods) # ['happy', 'sad', 'anxious', 'Yay!!!!', True, 142.2]

animals = ["dog", "cat", "bird"]
animals.extend([4, 3])
print(animals) #["dog", "cat", "bird", 4, 3]

###############
## .remove() ##
###############
'''.remove() to remove ONLY ONE element from a list per run based its VALUE'''

programmer_life.remove("debugging")
print(programmer_life) # ['dreaming', 'waking', 'eating', 'crying', 'hoping', 'crying', 4]

############
## .pop() ##
############
'''.pop() to remove ONLY ONE element from a list per run based its INDEX'''

programmer_life.pop(3)
print(programmer_life) # ['dreaming', 'waking', 'eating', 'hoping', 'crying', 4]

##############
## .clear() ##
##############
'''.clear() will remove all the elements from a list and return an empty list []'''
 
programmer_life.clear()
print(programmer_life) # []
print(id(programmer_life)) # still has the id, meaning the variable still exists

'''
del programmer_life  ## This will erases the variable entirely, no more existence, no more id
print(id(programmer_life)) ## raise NameError because the variable does not exist (has been deleted)
'''

#############
## .copy() ##
#############
'''.copy() to copy a list (resulting an object having DIFFERENT ID)'''
 
list_original = [1, "a", 2.0, "c", "b", False]
print(f"list_original   : {list_original}")
print(f"list_original id: {id(list_original)}\n")

list_copy_1 = list_original.copy()
print(f"list_copy_1   : {list_copy_1}")
print(f"list_copy_1 id: {id(list_copy_1)}\n") # DIFFERENT id from list_original

list_copy_2 = list_original
print(f"list_copy_2 id: {list_copy_2}")
print(f"list_copy_2 id: {id(list_copy_2)}\n") # SAME id as list_original
                                              # meaning that if list_original changes, this list_copy_2 will also change

print(f"list_original and list_copy_2 share the SAME id: {str(id(list_original) == id(list_copy_2)).upper()}\n")

list_original.append("Goodnight")
print(f"list_original: {list_original}") # [1, 'a', 2.0, 'c', 'b', False, 'Goodnight']
print(f"list_copy_2: {list_copy_2}")     # [1, 'a', 2.0, 'c', 'b', False, 'Goodnight']
print(f"list_copy_1: {list_copy_1}")     # [1, 'a', 2.0, 'c', 'b', False]

#############
## .sort() ##
#############
'''.sort() to sort a list in ascending or descending, A-Z or Z-A'''
 
names = ["Kitana", "Bruce", "Zealot", "Anna", "Nina"]
names.sort() # sort Ascending
print(names) # ['Anna', 'Bruce', 'Kitana', 'Nina', 'Zealot']

names = ["Kitana", "Bruce", "Zealot", "Anna", "Nina"]
names.sort(reverse=True) # sort Descending
print(names) # ['Zealot', 'Nina', 'Kitana', 'Bruce', 'Anna']

numbers = [3.72, 8.15, 0.49, 6.03, 1.27]
numbers.sort()
print(numbers) # [0.49, 1.27, 3.72, 6.03, 8.15]

numbers = [3.72, 8.15, 0.49, 6.03, 1.27]
numbers.sort(reverse=True)
print(numbers) # [8.15, 6.03, 3.72, 1.27, 0.49]

################
## .reverse() ##
################
'''.reverse() to reverse the current order of a list "180 degrees"''' 
 
from datetime import date
list_mix = ["Lentani", 35.5, 20, date(1885, 12, 21), False]

list_mix.reverse()
print(list_mix) # [False, datetime.date(1885, 12, 21), 20, 35.5, 'Lentani']


#-----------------------------------------------------------------#
#------------------- List concat and multiply --------------------#
#-----------------------------------------------------------------#

lst1 = [1, 3, 5]
lst2 = [2, 4, 6, 8]
lst3 = ['A', 'B', 'C']

lst_add = lst1 + lst2 
print(lst_add) # [1, 3, 5, 2, 4, 6, 8]

print(lst1 + lst3) # [1, 3, 5, 'A', 'B', 'C']

lst_multiply = lst1*3
print(lst_multiply) # [1, 3, 5, 1, 3, 5, 1, 3, 5]

print(lst3*4) # ['A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C']

print(lst1*2 + lst3*3) # [1, 3, 5, 1, 3, 5, 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C']

#-------------------------------------------------------------------#
#------------------ List and Loops and 2D list ---------------------#
#-------------------------------------------------------------------#

philosophes = ["Voltaire", "Rousseau", "Montesquieu", "Diderot"]

###############################
## For loop through elements ##
###############################

for homme in philosophes:
    print(homme)

##############################
## For loop through indices ##
##############################

for index, element in enumerate(philosophes):
    print(f"{index} - {element}")

################################
## While loop through indices ##
################################

i = 0
while i < len(philosophes):
    print(f"{i} - {philosophes[i]}")
    i += 1

##########################
## Loop through 2D list ##
##########################

lst_customers = [
    ['Lucy', 'Rashford', 2000],
    ['Marcus', 'Aurelius', 300000],
    ['Hamazuki', 'Sento', 500000000]
]

# Method 1:
for item in lst_customers:
    first_name = item[0]
    last_name = item[1]
    purchase = item[2]
    print(f'{first_name} {last_name}: {purchase} USD')

# Method 2:
for first_name, last_name, purchase in lst_customers:
    print(f'{first_name} {last_name}: {purchase} USD')

'''
for first_name, purchase in lst_customers:
    print(f'{first_name}: {purchase} USD')
===> ValueError: too many values to unpack (expected 2)

it raises error because the number of iterators and the number of items are not corresponding
'''


#-----------------------------------------------------------#
#------------------- List comprehension --------------------#
#-----------------------------------------------------------#

samurais = ["Miyamoto Musashi", "Oda Nobunaga", "Sanada Yukimura", "Honda Tadakatsu"]

samurais_upper = [name.upper() for name in samurais]
print(samurais_upper) # ['MIYAMOTO MUSASHI', 'ODA NOBUNAGA', 'SANADA YUKIMURA', 'HONDA TADAKATSU']

samurais_y = [name for name in samurais if (("y" in name) or ("Y" in name))]
print(samurais_y) # ['Miyamoto Musashi', 'Sanada Yukimura']

even_numbers = [number for number in range(20) if (number % 2 == 0)]
print(even_numbers) # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

even_numbers = [number if (number % 2 == 0) else "odd" for number in range(10)]
print(even_numbers) # [0, 'odd', 2, 'odd', 4, 'odd', 6, 'odd', 8, 'odd']


#------------------------------------------------------------------------------------------#
#------------------ Numeric List calculating with Aggregate Functions ---------------------#
#------------------------------------------------------------------------------------------#

# For numeric list, can use math aggregate functions

# Aggregate Functions are those which take many input numbers but return ONLY ONE output (like mean, min, max, std...)

import numpy as np

lst_floats = [213.0, 321.5, 56198.99, 65489.55, 213.68]

print(np.sum(lst_floats))
print(np.mean(lst_floats))
print(np.median(lst_floats))
print(np.min(lst_floats))
print(np.max(lst_floats))
print(np.var(lst_floats))
print(np.std(lst_floats))

'''
print(sum(["A", "b", "c"])) #=> TypeError
'''


#-------------------------------------------------------------------------------------------------------#
#------------------ map() and list comprehension for list element-wise calculation ---------------------#
#-------------------------------------------------------------------------------------------------------#

import numpy as np

# Use map() to perform list element-wise transformation
# map() returns a map object; therefore must convert back into list to get the final calculated list
# map(function, iteration) | list(map(function, iteration))

lst_floats = [213.0, 321.5, 56198.99, 65489.55, 213.68]

output_lst = map(np.sqrt, lst_floats)
print(output_lst) # <map object at 0x7fc3b19c3550>

output_lst = list(map(np.sqrt, lst_floats)) # convert map object into list before printing out
print(output_lst)
print([float(x) for x in output_lst])
# [14.594519519326424, 17.930421077041107, 237.06326159909298, 255.90926126265927, 14.617797371697284]

output_lst = list(map(lambda x: x/100, lst_floats)) # combine map() with lambda function
print(output_lst)
# [2.13, 3.215, 561.9899, 654.8955000000001, 2.1368]

#----------
## Use list comprehension to perform list element-wise transformation
#----------

lst_complexes = [(3+2j), (4+5j), (9.5 + 10j)]

output_lst = [complex**2 for complex in lst_complexes]
print(output_lst)
# [(5+12j), (-9+40j), (-9.75+190j)]