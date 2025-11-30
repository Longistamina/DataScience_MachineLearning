''' Tuple ()

Tuple stores many elements, each has its own value and index

Tuple allows HETEROGENEOUS datatype

Tuple is like List, but with ONE key difference:
    => UNABLE to change or modify

Tuple still allows duplicate values (because it has index to distinguish)

Should use Tuple when you don't want others modify your data


Table of contents:
## Create a tuple
## Index/Access tuple's elements
## Update tuple's elements
## Tuple methods: .count() and .index()
## Tuple concat and multiply
## Tuple and Loops and 2D tuple
## Tuple comprehension
## Numeric Tuple calculating with Aggregate Functions
## map() and tuple comprehension for tuple element-wise calculation
## Example: calculating Lunar Year based on Solar Year
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

tup2 = (1, 2, 3, 4, 5)
tup3 = 6, 7, 8, 9, 10
tup4 = 8,              # If have only one element, must end with "," to make Python understand this as Tuple
tup5 = ('abc',)
tup6 = ('cdf', True, 1.2, 3, ["Name", False])


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

print(fruits[2:5]) # from fruits[2] to fruits[5] but excluded fruits[5]
                   # ('cherry', 'orange', 'kiwi')

print(fruits[1:6:2]) # from fruits[1] to fruits[6] but excluded fruits[6]  
                     # ('banana', 'orange', 'melon')

print(fruits[-1:-4]) # ()
                     # empty tuple because it index from the last element [-1] to the right
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

# Check if item exist in Tuple
if "apple" in fruits:
    print("Yes, 'apple' is in the fruits Tuple")


#--------------------------------------------------------------#
#----------------- Modify tuple via list ----------------------#
#--------------------------------------------------------------#

'''
Again, Tuple DOES NOT allow modifying its elements
So, if we still need to make modifications => convert to list first using list(tuple_name)

After that, we can apply list modifying methods: 
      insert, append, extend, remove, pop, clear, copy, sort, reverse
'''

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


#------------------------------------------------------#
#----------------- Tuple methods ----------------------#
#------------------------------------------------------#

# Tuple has only 2 methods: .count() and .index() (they work like the ones of list)

float_tup = (3.72, 8.15, 0.49, 6.03, 1.27, 0.49, 0.48, 0.49)

###############
### .count() ##
###############
'''.count() returns the number of a specified element within a tuple'''

print(float_tup.count(0.49)) # 3 (value 0.49 shows up 3 times)

##############
## .index() ##
##############
'''.index() returns the index of the first element with the specified value'''
 
print(float_tup.index(0.49)) # 2 (index of the first 0.49 is 2)


#-------------------------------------------------------------------#
#---------------- Tuple concat and duplicate -----------------------#
#-------------------------------------------------------------------#

tuple1 = ("a", "b" , "c")
tuple2 = (1, 2, 3)

# concat tuple using "+"
tuple_add = tuple1 + tuple2
print(tuple_add) # ('a', 'b', 'c', 1, 2, 3)


# duplicate tuple using "*"
tuple_dup = tuple1*2 + tuple2*3
print(tuple_dup) 
# ('a', 'b', 'c', 'a', 'b', 'c', 1, 2, 3, 1, 2, 3, 1, 2, 3)


#---------------------------------------------------------------------#
#---------------- Tuple and Loops and 2D Tuple -----------------------#
#---------------------------------------------------------------------#

philosophes = "Voltaire", "Rousseau", "Montesquieu", "Diderot"

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

tup_customers = (
    ['Lucy','Rashford',2000],
    ('Marcus','Aurelius',300000),
    ('Hamazuki','Sento',500000000)
)

# Method 1:
for item in tup_customers:
    first_name = item[0]
    last_name = item[1]
    purchase = item[2]
    print(f'{first_name} {last_name}: {purchase} USD')

# Method 2:
for first_name, last_name, purchase in tup_customers:
    print(f'{first_name} {last_name}: {purchase} USD')

'''
for first_name, purchase in tup_customers:
    print(f'{first_name}: {purchase} USD')
===> ValueError: too many values to unpack (expected 2)

it raises error because the number of iterators and the number of items are not corresponding
'''


#------------------------------------------------------------#
#---------------- Tuple comprehension -----------------------#
#------------------------------------------------------------#

samurais = "Miyamoto Musashi", "Oda Nobunaga", "Sanada Yukimura", "Honda Tadakatsu"

samurais_upper = tuple(name.upper() for name in samurais)
print(samurais_upper) # ('MIYAMOTO MUSASHI', 'ODA NOBUNAGA', 'SANADA YUKIMURA', 'HONDA TADAKATSU')

samurais_y = tuple(name for name in samurais if (("y" in name) or ("Y" in name)))
print(samurais_y) # ('Miyamoto Musashi', 'Sanada Yukimura')

even_numbers = tuple(number for number in range(20) if (number % 2 == 0))
print(even_numbers) # (0, 2, 4, 6, 8, 10, 12, 14, 16, 18)

even_numbers = tuple(number if (number % 2 == 0) else "odd" for number in range(10))
print(even_numbers) # (0, 'odd', 2, 'odd', 4, 'odd', 6, 'odd', 8, 'odd')

'''
samurais_upper = (name.upper() for name in samurais)
print(samurais_upper)
==> <generator object <genexpr> at 0x7fda43f13850>
'''


#-------------------------------------------------------------------------------------------#
#---------------- Numeric Tuple calculating with Aggregate Functions -----------------------#
#-------------------------------------------------------------------------------------------#

# For numeric tuple, can use math aggregate functions

# Aggregate Functions are those which take many input numbers but return ONLY ONE output (like mean, min, max, std...)

import numpy as np

lst_floats = (213.0, 321.5, 56198.99, 65489.55, 213.68)

print(np.sum(lst_floats))
print(np.mean(lst_floats))
print(np.median(lst_floats))
print(np.min(lst_floats))
print(np.max(lst_floats))
print(np.var(lst_floats))
print(np.std(lst_floats))

# string_tup = ("A", "b", "c")
# print(sum(string_tup)) #=> TypeError


#--------------------------------------------------------------------------------------------------------#
#---------------- map() and tuple comprehension for list element-wise calculation -----------------------#
#--------------------------------------------------------------------------------------------------------#

import numpy as np

# Use map() to perform tuple element-wise calculation
# map() returns a map object; therefore must convert back into tuple to get the final calculated tuple
# map(function, iteration) | list(map(function, iteration))

tuple_floats = (213.0, 321.5, 56198.99, 65489.55, 213.68)

output = map(np.sqrt, tuple_floats)
print(output) # <map object at 0x7fda43fbf5e0>

output_tuple = tuple(map(np.sqrt, tuple_floats)) #convert map object into tuple before printing out
print(output_tuple)

output_tuple = tuple(map(lambda x: x / 100, tuple_floats)) #combine map() with lambda function
print(output_tuple)


# Use tuple comprehension to perform list element-wise calculation
tuple_complexes = ((3 + 2j), (4 + 5j), (9.5 + 10j))

output_tuple = tuple(complex ** 2 for complex in tuple_complexes)
print(output_tuple)


#------------------------------------------------------------------------------------------------------------#
#-------------------------- Tuple application example: calculate Lunar Year ---------------------------------#
#------------------------------------------------------------------------------------------------------------#

print()
print('Calculate Lunar Year'.center(60))
print('-' * 60)

# Thien_Can        = 'Canh', 'Tân', 'Nhâm', 'Quý', 'Giáp', 'Ất', 'Bính', 'Đinh','Mậu','Kỷ'
tup_Heavenly_Stems = 'Geng', 'Xin', 'Ren',' Gui', 'Jia', 'Yi', 'Bing', 'Ding', 'Wu', 'Ji'

# Dia_Chi            = 'Thân',   'Dậu',     'Tuất', 'Hợi', 'Tý', 'Sửu', 'Dần',  'Mão',    'Thìn',   'Tỵ',    'Ngọ',   'Mùi'
tup_Earthly_Branches = 'Monkey', 'Rooster', 'Dog', 'Pig', 'Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake', 'Horse', 'Goat'

while True:
    try:
        solar_year = int(input('Please input a solar year: '))
        assert (solar_year >= 1) and (solar_year <= 9999), '>>>Error: a solar year must range from 1 to 9999, please try again!!!'
    
    except ValueError:
        print(">>Error: your input must be a number, please try again!!!")
    
    except AssertionError as e:
        print(e)
    
    else:
        stem_index   = solar_year % 10 # The remainer of solar_year%10 will be the index value of tup_Heavenly_Stems
        branch_index = solar_year % 12 # The remainer of solar_year%12 will be the index value of tup_Earthly_Branches
        
        print(f'The corresponding Lunar Year is: {tup_Heavenly_Stems[stem_index]} {tup_Earthly_Branches[branch_index]}')
    
    continue_program = input('If you want to continue press [y], otherwise press any key to exit: ')
    if continue_program == 'y':
        print() 
        continue
    else: break
print('\n--Program End--')