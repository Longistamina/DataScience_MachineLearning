'''
Set:
    ## Stores UNIQUE data (no duplicates allowed)
    ## Allows HETEROGENEOUS datatype
    ## It's updatable, i.e. allows modifying via .add(), .remove() and .clear()
    ## Have NO INDEX, there for no order and no duplicates allowed
=> use set when you need a mutable collection of unique items

Fronzeset:
    ## Like set but not allowing modifying or changing (meaning no .add() or no .remove() ...)
    ## In other words, fronzeset is immutable
=> use frozenset when you need an immutable set that can be used as a dictionary key 
=> or when you want to ensure the set remains constant throughout your program
'''

#------------------------------------------------------------------#
#-------------------- Create set and fronzeset --------------------#
#------------------------------------------------------------------#

########### create set using {} or set() ##################

empty_set = set() # {}
                    # this set() function also helps convert other iterables into set containing unique values

# empty_set = {}         # {}
# print(type(empty_set)) # 'dict' not 'set'
                         # In this case, python interpretes {} as an empty dictionary, not set

set_5_elements = {"Metal", "Wood", "Earth", "Water", "Fire", "Metal"}
print(set_5_elements) # {'Fire', 'Metal', 'Wood', 'Earth', 'Water'} lose one "Metal"
                      # reorder from A->Z

set_float = set([1.5, 3.7, 2.0, 4.9, 2.0]) # convert list to set
print(set_float) # {1.5, 2.0, 3.7, 4.9} lose one 2.0
                 # reorder in anscending direction

set_mix = set(("cd", "pwd", (3 + 5.5j), 2, 5.7, False, ("text", True)), "cd") # convert tuple to set
print(set_mix) # {False, 2, 5.7, ('text', True), (3+5.5j), 'pwd', 'cd'}

# set(1.2, 3.4, "Text") will raise error because set expected at most 1 argument (1 input)
# ===> must put it in a list or tupe first: set([1.2, 3.4, "Text"]) or set((1.2, 3.4, "Text"))

# set(2, [3, "4"]) will raise error because list is mutable, so they cannot be elements of a set.
# ===> Instead, try put them in a tuple like this: set(2, (3, "4"))


########### create fronzeset using fronzeset() ##################

empty_fset = frozenset()
print(empty_fset)  # frozenset()

list_data = [1, 2, 3, 2, 1, ("True", False)]
list_fset = frozenset(list_data)
print(list_fset)  # frozenset({1, 2, 3, ('True', False)})

tuple_data = (2.5, ("True", False, (4.5 + 3j)), 6, (2.5 + 4j), 2.5)
tuple_fset = frozenset(tuple_data)
print(tuple_fset) # frozenset({2.5, ('True', False, (4.5+3j)), 6, (2.5+4j)})