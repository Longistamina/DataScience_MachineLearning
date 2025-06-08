''' Tuple ()

Tuple stores many elements, each has its own value and index

Tuple is like List, but with some key differences:
    +HOMOGENEOUS datatype only
    +UNABLE to change or modify

Tuple still allows duplicate values (because it has index to distinguish)

Should use Tuple when you don't want others modify your data
'''

#--------------------------------------------------------#
#-------------------- Create a tuple --------------------#
#--------------------------------------------------------#

empty_tup_1 = ()         # ()
empty_tup_2 = tuple()    # ()
                         # this tuple() function also helps convert other iterables into tuple

tup1 = ('one','two','three','four')
print(tup1)
print(type(tup1))

tup2 = (1,2,3,4,5)
tup3 = 6,7,8,9,10
tup4 = 8,         #If have only one element, must end with "," to make Python understand this as Tuple
tup5 = ('abc',)


#-------------------------------------------------------------------------#
#----------------- Index / Access tuple'-s elements ----------------------#
#-------------------------------------------------------------------------#

# Indexing Tuple just like indexing List
fruits = "apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"

print(fruits[0]) # apple
print(fruits[1]) # banana

print(fruits[-1]) # mango
print(fruits[-2]) # melon

print(fruits[:4]) # or fruits[0:4]
                  # ('apple', 'banana', 'cherry', 'orange')

print(fruits[2:]) # from fruits[2] to the last element fruits[-1] (and also included)
                  # ('cherry', 'orange', 'kiwi', 'melon', 'mango')

print(fruits[-1:-4]) # ()
                     # empty list because it index from the last element [-1] to the right
                     # but nothing is at the right at [-1], so return empty list

print(fruits[-1:-5:-1]) # ('mango', 'melon', 'kiwi', 'orange')
                        # negative sign "-" means reverse indexing (from left to right)
                        # with step = 1
                        # the -5 "cherry" are excluded

print(fruits[-1:-5:-2]) # ('mango', 'kiwi')
                        # reverse indexing with steps = -2, so "melon" and "orange" are bypassed
                        # the -5 "cherry" are excluded

print(fruits[-4:-1]) # ('orange', 'kiwi', 'melon')
                     # index from right to left as default
                     # start with -4 "orange"
                     # stop at -1 "mango" but excluded
                     #===> ('orange', 'kiwi', 'melon')


#--------------------------------------------------------------#
#----------------- Modify tuple via list ----------------------#
#--------------------------------------------------------------#

# Again, Tuple DOES NOT allow modifying its elements
# So, if we still need to make modifications => convert to list first using list(tuple_name)

# After that, we can apply list modifying methods: 
#       insert, append, extend, remove, pop, clear, copy, sort, reverse

predators_tup = ("tiger", "lion", "leopard")
print(predators_tup)

predators_list = list(predators_tup)
print(predators_list) # ['tiger', 'lion', 'leopard']

predators_list[2] = "wolf"
print(predators_list) # ['tiger', 'lion', 'wolf']

predators_list.extend(["eagle", "cheetah", "batman"])
print(predators_list) # ['tiger', 'lion', 'wolf', 'eagle', 'cheetah', 'batman']


# convert back to tuple using tuple() after all modifications
predators_tup = tuple(predators_list)
print(predators_tup) # ('tiger', 'lion', 'wolf', 'eagle', 'cheetah', 'batman')

# Check if item exist in Tuple
if "apple" in fruits:
    print("Yes, 'apple' is in the fruits Tuple")

#chuyển list thành tuple
lst_thu = ['Thứ 2','Thứ 3','Thứ 4','Thứ 5','Thứ 6','Thứ 7','Chủ nhật']
tup_thu = tuple(lst_thu)