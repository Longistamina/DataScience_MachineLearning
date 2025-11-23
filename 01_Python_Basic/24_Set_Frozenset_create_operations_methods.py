'''
Set:
    ## Stores UNIQUE data (no duplicates allowed)
    ## Allows HETEROGENEOUS datatype
    ## It's updatable, i.e. allows modifying via .add(), .remove() and .clear()
    ## Have NO INDEX, there for no order and no duplicates allowed
=> use set when you need a mutable collection of unique items

Frozenset:
    ## Like set but not allowing modifying or changing (meaning no .add() or no .remove() ...)
    ## In other words, fronzeset is immutable
=> use frozenset when you need an immutable set that can be used as a dictionary key 
=> or when you want to ensure the set remains constant throughout your program

Set and Fronzeset do not support indexing, slicing, or other sequence-like behavior.
(because they are unordered collections, and have no index)

# Table of contents:
#### Create set and frozenset: {}, set(), frozenset()
#### Check if element exists 
#### Add and Remove elements for SET: .add(), .update(), .remove(), .discard(), .pop(), .clear()
#### Loop through elements
#### Set Operations: .union(), .intersection(), .difference(), .symmetric_difference(), .issubset(), .issuperset(), .isdisjoint()
#### .copy() method and sorted() set
'''

#------------------------------------------------------------------#
#-------------------- Create set and frozenset --------------------#
#------------------------------------------------------------------#

##################################
## create set using {} or set() ##
##################################

empty_set = set() # set()
                  # this set() function also helps convert other iterables into set containing unique values

'''
empty_set = {}         # {}
print(type(empty_set)) # 'dict' not 'set'
                         In this case, python interpretes {} as an empty dictionary, not set
'''

set_5_elements = {"Metal", "Wood", "Earth", "Water", "Fire", "Metal"}
print(set_5_elements) # {'Fire', 'Metal', 'Wood', 'Earth', 'Water'} lose one "Metal"


set_float = set([1.5, 3.7, 2.0, 4.9, 2.0]) # convert list to set
print(set_float) # {1.5, 2.0, 3.7, 4.9} lose one 2.0
                 # reorder in anscending direction

set_mix = set(("cd", "pwd", (3 + 5.5j), 2, 5.7, False, ("text", True), "cd")) # convert tuple to set
print(set_mix) # {False, 2, 5.7, ('text', True), (3+5.5j), 'pwd', 'cd'}

'''
set(1.2, 3.4, "Text") will raise error because set expected at most 1 argument (1 input)
===> must put it in a list or tupe first: set([1.2, 3.4, "Text"]) or set((1.2, 3.4, "Text"))

set([2, [3, "4"]]) will raise error because list is mutable, so they cannot be elements of a set.
===> Instead, try put them in a tuple like this: set(2, (3, "4"))
'''


########################################
## create frozenset using frozenset() ##
########################################

empty_fset = frozenset()
print(empty_fset)  # frozenset()

list_data = [1, 2, 3, 2, 1, ("True", False)]
list_fset = frozenset(list_data)
print(list_fset)  # frozenset({1, 2, 3, ('True', False)})

tuple_data = (2.5, ("True", False, (4.5 + 3j)), 6, (2.5 + 4j), 2.5)
tuple_fset = frozenset(tuple_data)
print(tuple_fset) # frozenset({2.5, ('True', False, (4.5+3j)), 6, (2.5+4j)})


#----------------------------------------------------------------------------------------------------#
#----------------------------------- Check if element exists ----------------------------------------#
#----------------------------------------------------------------------------------------------------#

# Use 'in' operator to check if an element exists in a set or frozenset

set_2 = {1, 2, 3, 4, 5}
print(3 in set_2)  # True
print(6 in set_2)  # False

fset_2 = frozenset([1, 2, 3, 4, 5])
print(3 in fset_2)  # True
print(6 in fset_2)  # False


#--------------------------------------------------------------------------------------------------------#
#---------------------------------- Add and Remove elements for SET -------------------------------------#
#--------------------------------------------------------------------------------------------------------#

###############
## set.add() ##
###############

# set.add() adds an element to the set (like list.append()) 

set_1 = {1, 2, 3}
set_1.add(4)  # add element 4 to set_1
print(set_1)  # {1, 2, 3, 4}


##################
## set.update() ##
##################

# .update(): adds elements from another set or iterable to the current set (like list.extend())

set_1.update({25, 49})  # adds "Air" and "Space" to set_demo
print(set_1)  # {1, 2, 3, 4, 49, 25}


#################
## set.remove) ##
#################

# set.remove() will raise KeyError if element not found

set_1.remove(2)  # remove element 2 from set_1
print(set_1)  # {1, 3, 4, 49, 25}


###################
## set.discard() ##
###################

# set.discard() will not raise error if element not found

set_1.discard(3) # remove element 3 from set_1, no error if element not found
print(set_1)     # {1, 4, 49, 25}


###############
## set.pop() ##
###############

# set.pop() removes a random element from the set (and returns it if that element exists in the set)

'''NOTE: set.pop() will raise KeyError if the set is empty '''
set_1 = {1, 2, 3}
removed_element = set_1.pop()  # removes and returns a random element (could be 1, 2, or 3)
print(removed_element)         # prints the removed element


##################
## set.aclear() ##
##################

# set.clear() works like list.clear() to remove all elements from the set

set_1.clear()     # clear all elements in set_1
print(set_1)      # set() or {}
print(id(set_1))  # id of set_1 is still there, meaning it still exists but is now empty


'''
frozenset.add() and frozenset.remove() will raise error (same for other modifying methods)
'''
fset_1 = frozenset([1, 2, 3])
fset_1.add(4)  # AttributeError: 'frozenset' object has no attribute 'add'


#----------------------------------------------------------------------------------------------------#
#----------------------------------- Loop through elements ------------------------------------------#
#----------------------------------------------------------------------------------------------------#

# Looping through a set or frozenset is similar to looping through a list or tuple
set_5_elements = {"Metal", "Wood", "Earth", "Water", "Fire", "Metal"}
for element in set_5_elements:
    print(element)  # prints each element in set_5_elements

fset = frozenset(["cd", "pwd", (3 + 5.5j), 2, 5.7, False, ("text", True)])
for element in fset:
    print(element)  # prints each element in fset


'''
NOTE: cannot use enumerate() with set or frozenset directly because they are unordered collections
(meaning they do not have an index)
'''


#---------------------------------------------------------------------------------------------------------#
#---------------------------------------- Set Operations -------------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
 
set_a = {1, 2, 3, 4}
set_b = {3, 4, 5, 6}

################################################################
## .union(): combines elements from both sets (set_a | set_b) ##
################################################################

set_union = set_a.union(set_b)  # or set_a | set_b
print(set_union)      # {1, 2, 3, 4, 5, 6}
print(set_a | set_b)  # {1, 2, 3, 4, 5, 6}

###########################################################################
## .intersection(): returns elements common to both sets (set_a & set_b) ##
###########################################################################

set_intersection = set_a.intersection(set_b)  # or set_a & set_b
print(set_intersection)  # {3, 4}
print(set_a & set_b)     # {3, 4}

####################################################################################
## .difference(): returns elements in set_a that are not in set_b (set_a - set_b) ##
####################################################################################

set_difference = set_a.difference(set_b)  # or set_a - set_b
print(set_difference)  # {1, 2}
print(set_a - set_b)   # {1, 2}

#####################################################################################################
## .symmetric_difference(): returns elements in either set_a or set_b but not both (set_a ^ set_b) ##
#####################################################################################################

set_symmetric_difference = set_a.symmetric_difference(set_b)  # or set_a ^ set_b
print(set_symmetric_difference)  # {1, 2, 5, 6}
print(set_a ^ set_b)             # {1, 2, 5, 6}

###########################################################################################
## .issubset(): checks if set_a is a subset of set_b (set_a <= set_b) or (set_a < set_b) ##
###########################################################################################

print(set_a.issubset(set_b))  # False
print(set_a <= set_b)         # False
print(set_a < set_b)          # False

###############################################################################################
## .issuperset(): checks if set_a is a superset of set_b (set_a >= set_b) or (set_a > set_b) ##
###############################################################################################

print(set_a.issuperset(set_b))  # False
print(set_a >= set_b)           # False
print(set_a > set_b)            # False

#########################################################################
## .isdisjoint(): checks if set_a and set_b have no elements in common ##
#########################################################################

print(set_a.isdisjoint(set_b))   # False
print(set_a.isdisjoint({7, 8}))  # True, because {7, 8} has no common elements with set_a


'''Fronzeset operations are similar to set operations, but they are immutable'''


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------ .copy() method and sorted() set --------------------------------------#
#-----------------------------------------------------------------------------------------------------------#

set_demo = {"Metal", "Wood", "Earth", "Water", "Fire"}

################################################
## .copy(): creates a shallow copy of the set ##
################################################

set_copy = set_demo.copy()
print(set_copy)  # {'Fire', 'Metal', 'Wood', 'Earth', 'Water'}
print(id(set_demo) == id(set_copy)) # False, because they are different objects

################################################################
## sorted(): returns a sorted list of the elements in the set ##
################################################################

print(sorted(set_demo))  # ['Earth', 'Fire', 'Metal', 'Water', 'Wood']
                         # reuturn a sorted LIST, not a set
