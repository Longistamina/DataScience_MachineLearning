# List is a type of iteration in Python
# List allows storing duplicate HETEROGENEOUS datat (different datatypes)
# (however, should store homogeneous data to facilitate processing steps)
# First element has index = 0
# Last element has index = len(list) - 1 (or -1)

# Table of contents:
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

programmer_life = ["waking", "eating", "debugging", "crying", "hoping", "crying"]


# .count() returns the number of a specified element within a list
print(programmer_life.count("crying")) # 2


# .index() returns the index of the first element with the specified value
print(programmer_life.index("crying")) # 3 (index of the first "crying")
print(programmer_life.index("eating")) # 1


# .insert() to insert new element at a specified index
programmer_life.insert(0, "dreaming")
print(programmer_life) 
#['dreaming', 'waking', 'eating', 'debugging', 'crying', 'hoping', 'crying']


## Notice: print(programmer_life.insert(0, "dreaming")) will return None
## => because it modifies the original list directly (in-place) and doesn’t create or return a new list.


# .append() adds ONLY ONE element per run at the end of the list
programmer_life.append(4)
print(programmer_life)
#['dreaming', 'waking', 'eating', 'debugging', 'crying', 'hoping', 'crying', 4]

animals = ["dog", "cat", "bird"]
animals.append([4, 3])
print(animals)
#["dog", "cat", "bird"], [4, 3]]


# .extend() acts like .append() but can add any iterable object with separate element
moods = ["happy", "sad", "anxious"]
thistuple = ("Yay!!!!", True, 142.2) # or can be a list or set
moods.extend(thistuple)
print(moods) # ['happy', 'sad', 'anxious', 'Yay!!!!', True, 142.2]


# .remove() to remove ONLY ONE element from a list per run based its VALUE
programmer_life.remove("debugging")
print(programmer_life) # ['dreaming', 'waking', 'eating', 'crying', 'hoping', 'crying', 4]


# .pop() to remove ONLY ONE element from a list per run based its INDEX
programmer_life.pop(3)
print(programmer_life) # ['dreaming', 'waking', 'eating', 'hoping', 'crying', 4]


# .clear() will remove all the elements from a list and return an empty list []
programmer_life.clear()
print(programmer_life) # []
print(id(programmer_life)) # still has the id, meaning the variable still exists

# del programmer_life  ## This will erases the variable entirely, no more existence, no more id
# print(id(programmer_life)) ## raise NameError because the variable does not exist (has been deleted)


# .copy() to copy a list (resulting an object having DIFFERENT ID)
list_original = [1, "a", 2.0, "c", "b", False]
print(f"list_original   : {list_original}")
print(f"list_original id: {id(list_original)}\n")

list_copy_1 = list_original.copy()
print(f"list_copy_1 id: {list_copy_1}")
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


# .sort() to sort a list in ascending or descending, A-Z or Z-A
names = ["Kitana", "Bruce", "Zealot", "Anna", "Nina"]
names.sort() # sort Ascending
print(names) # ['Anna', 'Bruce', 'Kitana', 'Nina', 'Zealot']

names = ["Kitana", "Bruce", "Zealot", "Anna", "Nina"]
names.sort(reverse = True) # sort Descending
print(names) # ['Zealot', 'Nina', 'Kitana', 'Bruce', 'Anna']

numbers = [3.72, 8.15, 0.49, 6.03, 1.27]
numbers.sort()
print(numbers) # [0.49, 1.27, 3.72, 6.03, 8.15]

numbers = [3.72, 8.15, 0.49, 6.03, 1.27]
numbers.sort(reverse=True)
print(numbers) # [8.15, 6.03, 3.72, 1.27, 0.49]


# .reverse() to reverse the current order of a list "180 degrees"
from datetime import date
list_mix = ["Lentani", 35.5, 20, date(1885, 12, 21), False]
list_mix.reverse()
print(list_mix) # [False, datetime.date(1885, 12, 21), 20, 35.5, 'Lentani']