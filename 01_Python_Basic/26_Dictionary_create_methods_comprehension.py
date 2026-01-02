'''
Dictionary:
    ## A dictionary is a collection of key-value pairs.
    ## Each key is unique and maps to a specific value.
    ## Dictionaries are mutable, meaning you can change their content.
# => use dictionary when you need to store data in key-value pairs for fast lookups
# => or when you need to associate values with unique keys.

Table of contents:
#### Create dictionary: {}, dict()
#### Nested dictionaries
#### Access values by key: dict[key]
#### Check if key exists
#### Add, Update and Remove key-value pairs: .update(), .pop(), .popitem(), .clear()
#### Dictionary Methods: .keys(), .values(), .items(), .get(), .setdefault(), .copy()
#### Sort a dictionary
#### Loop through keys, values, and items
#### Dictionary Comprehension
'''

#----------------------------------------------------#
#----------------- Create dictionary ----------------#
#----------------------------------------------------#

################################
## Create an empty dictionary ##
################################

empty_dict_1 = {}      # {}
empty_dict_2 = dict()  # {}

print(type(empty_dict_1))  # <class 'dict'>
print(type(empty_dict_2))  # <class 'dict'>


##############################################
## Create a dictionary with key-value pairs ##
##############################################

dict_1 = {
    'name': 'Alice',
    'age': 30,
    'city': 'New York'
}
print(dict_1)  # {'name': 'Alice', 'age': 30, 'city': 'New York'}

######################################################
## Create a dictionary using the dict() constructor ##
######################################################

dict_2 = dict(name='Bob', age=25, city='Los Angeles')
print(dict_2)  # {'name': 'Bob', 'age': 25, 'city': 'Los Angeles'}

###############################################
## Create a dictionary from a list of tuples ##
###############################################

dict_3 = dict([('name', 'Charlie'), ('age', 35), ('city', 'Chicago')])
print(dict_3)  # {'name': 'Charlie', 'age': 35, 'city': 'Chicago'}

###############################################
## Create a dictionanry with iterable values ##
###############################################

dict_4 = {
    "ID": [1, 2, 3],
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [30, 25, 35]
}
print(dict_4)  # {'ID': [1, 2, 3], 'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [30, 25, 35]}

dict_5 = dict(
    ID = (4, 5, 6), 
    Name =('Alien', 'Anna', 'Chalker-chalk'), 
    Age = (32, 52, 55)
)
print(dict_5) # {'ID': (4, 5, 6), 'Name': ('Alien', 'Anna', 'Chalker-chalk'), 'Age': (32, 52, 55)}


###############################################
## Create a dictionary with mixed data types ##
###############################################

dict_6 = {
    'name': 'David',
    'age': 40,
    'is_student': False,
    'grades': [90, 85, 88],
    'address': {'city': 'Miami', 'state': 'FL'}
}
print(dict_6)  
# {'name': 'David', 'age': 40, 'is_student': False, 'grades': [90, 85, 88], 'address': {'city': 'Miami', 'state': 'FL'}}


#----------------------------------------------------#
#----------------- Nested dictionaries --------------#
#----------------------------------------------------#

# Create a nested dictionary (look like a JSON object)
nested_dict = {
    'person': {
        'name': 'Eve',
        'age': 28,
        'address': {
            'city': 'San Francisco',
            'state': 'CA',
            'zip': '94105'
        }
    },
    'company': {
        'name': 'TechCorp',
        'location': 'Silicon Valley',
        'employees': 500
    }
}

print(nested_dict)
# {'person': {'name': 'Eve', 'age': 28, 'address': {'city': 'San Francisco', 'state': 'CA', 'zip': '94105'}},
#  'company': {'name': 'TechCorp', 'location': 'Silicon Valley', 'employees': 500}}


#----------------------------------------------------#
#----------------- Access values by key -------------#
#----------------------------------------------------#

##########################
## Access values by key ##
##########################

dict_acces = {
    'name': 'Eve',
    'age': 28,
    'city': 'San Francisco'
}

print(dict_acces['name'])  # Eve
print(dict_acces['age'])   # 28
print(dict_acces['city'])  # San Francisco


'''
Accessing a key that does not exist raises a KeyError
print(dict_acces['country'])  # KeyError: 'country'
'''

#############################################
## Use the .get() method to avoid KeyError ##
#############################################

print(dict_acces.get('country'))  # None
print(dict_acces.get('name'))     # Eve

###################################################
## Access values within a list from a dictionary ##
###################################################

dict_list_access = {
    'ID': [0, 2, 3],
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [30, 25, 35]
}

print(dict_list_access['Name'][0])  # Alice
print(dict_list_access['Age'][2])   # 35

print(dict_list_access.get('ID')[1:])  # [2, 3]

##############################################
## Access values within a nested dictionary ##
##############################################

dict_nested_access = {
    'person': {
        'name': 'Frank',
        'age': 45,
        'address': {
            'city': 'Seattle',
            'state': 'WA'
        }
    }
}

print(dict_nested_access['person']['name'])  # Frank
print(dict_nested_access['person']['address']['city'])  # Seattle

print(dict_nested_access.get('person').get('age'))  # 45
print(dict_nested_access.get('person').get('address').get('state'))  # WA


#----------------------------------------------------#
#----------------- Check if key exists --------------#
#----------------------------------------------------#

dict_check = {
    'name': 'Grace',
    'age': 22,
    'city': 'Boston'
}

#########################
## Using 'in' operator ##
#########################

print('name' in dict_check)  # True
print('country' in dict_check)  # False

############################
## Using the get() method ##
############################

print(dict_check.get('age') is not None)  # True
print(dict_check.get('country') is not None)  # False

#############################
## Using the keys() method ##
#############################

print('city' in dict_check.keys())  # True
print('country' in dict_check.keys())  # False


#-----------------------------------------------------------------------------------------------------------#
#--------------------------------- Add, Update and Remove key-value pairs ----------------------------------#
#-----------------------------------------------------------------------------------------------------------#

##############################
## Add a new key-value pair ##
##############################

dict_add = {
    'name': 'Hannah',
    'age': 26
}

dict_add['city'] = 'Austin'

print(dict_add)  # {'name': 'Hannah', 'age': 26, 'city': 'Austin'}

#############################################
## .update(): Add multiple key-value pairs ##
#############################################

dict_add.update({'country': 'USA', 'is_student': True})
print(dict_add)  # {'name': 'Hannah', 'age': 26, 'city': 'Austin', 'country': 'USA', 'is_student': True}

'''
NOTE .update(): if you have a list of dictionary like below, must use for loop to update one by one
'''
dict_gotham_villain = dict()

list_of_dicts = [
    {"Harley": {"Gender": "F", "Age": 23}},
    {"Joker": {"Gender": "M", "Age": 535}},
    {"Scarface": {"Gender": "Unknown", "Age": "Unknown"}}
]

dict_gotham_villain.update(list_of_dicts)
'''ValueError: dictionary update sequence element #0 has length 1; 2 is required'''

for small_dict in list_of_dicts:
    dict_gotham_villain.update(small_dict)
# THIS IS THE CORRECT WAY TO UPDATE

for villain, info in dict_gotham_villain.items():
    print(f"{villain}: {info}")
# Harley: {'Gender': 'F', 'Age': 23}
# Joker: {'Gender': 'M', 'Age': 535}
# Scarface: {'Gender': 'Unknown', 'Age': 'Unknown'}
'''
END NOTE
'''

#######################################
## Update an existing key-value pair ##
#######################################

dict_add['age'] = 27
print(dict_add)  # {'name': 'Hannah', 'age': 27, 'city': 'Austin', 'country': 'USA', 'is_student': True}

####################################
## .pop() Remove a key-value pair ##
####################################

removed_value = dict_add.pop('city')
print(removed_value)  # Austin
print(dict_add)  # {'name': 'Hannah', 'age': 27, 'country': 'USA', 'is_student': True}

##################################################################
## .popitem(): Remove a key-value pair (the last inserted item) ##
##################################################################

removed_item = dict_add.popitem()
print(removed_item)  # ('is_student', True)
print(dict_add)  # {'name': 'Hannah', 'age': 27, 'country': 'USA'}

#########################################
## .clear(): Clear all key-value pairs ##
#########################################

dict_add.clear()
print(dict_add)  # {}
                 # The dictionary is now empty, but still exists and has id(dict_add) = .....


#--------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------- Dictionary Methods --------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------#

# Create a sample dictionary for demonstration
sample_dict = {
    'name': 'Ivy',
    'age': 29,
    'city': 'Denver',
    'country': 'USA'
}

###########################
## .keys(): Get all keys ##
###########################

keys = sample_dict.keys()
print(keys)  # dict_keys(['name', 'age', 'city', 'country'])

###############################
## .values(): Get all values ##
###############################

values = sample_dict.values()
print(values)  # dict_values(['Ivy', 29, 'Denver', 'USA'])

#################################################
## .items(): Get all key-value pairs as tuples ##
#################################################

items = sample_dict.items()
print(items)  # dict_items([('name', 'Ivy'), ('age', 29), ('city', 'Denver'), ('country', 'USA')])

################################
## .get(): Get a value by key ##
################################

# Basic ussage
value_name = sample_dict.get('name')
print(value_name)  # Ivy

'''
if using: dictionary[key], it will raise KeyError if the key does not exist
'''

# Get a value by key that does not exist using .get() without default value
value_country = sample_dict.get('state')
print(value_country)  # None

# Get a value by key that does not exist using .get() with default value
value_state = sample_dict.get('state', 'Not Found')
print(value_state)  # Not Found

###########################################################################################################################
## .setdefault() returns the value of the specified key , or inserts the key with a specified value if it does not exist ##
###########################################################################################################################

# If the key does not exist: insert the key, with the specified value
value = sample_dict.setdefault('state', 'Colorado')
print(value)  # Colorado
print(sample_dict)  # {'name': 'Ivy', 'age': 29, 'city': 'Denver', 'country': 'USA', 'state': 'Colorado'}
                    # The dichtionary now has a new key 'state' with value 'Colorado'


# .setdefault() does not change the value if the key already exists
# Instead, it returns the existing value
value = sample_dict.setdefault('city', 'New York')
print(value)  # Denver
print(sample_dict)  # {'name': 'Ivy', 'age': 29, 'city': 'Denver', 'country': 'USA', 'state': 'Colorado'}
                    # The value of the key 'city' remains unchanged

#######################################################
## .copy(): creates a shallow copy of the dictionary ##
#######################################################

dict_copy = sample_dict.copy()
print(dict_copy)  # {'name': 'Ivy', 'age': 29, 'city': 'Denver', 'country': 'USA', 'state': 'Colorado'}
                  # Modifying the copy does not affect the original dictionary


#-----------------------------------------------------------------------------------------------------------------#
#------------------------------------------- Sort a dictionary ---------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#

# Can sort a dictionary using dict(sorted(dict_name.items(), key = lambda x: x[...]), reverse = True/False)

demo_dict = {
    "B": 5,
    "D": 1,
    "C": 3,
    "X": 7,
    "H": 10,
    "F": 4
}

##########################################################
## sort a dict by its KEYS using "key = lambda x: x[0]" ##
##########################################################

sorted_dict_key = dict(
    sorted(
        demo_dict.items(), 
        key = lambda x: x[0], # sort by keys
        reverse = False # sort ascending
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

############################################################
## sort a dict by its VALUES using "key = lambda x: x[1]" ##
############################################################

sorted_dict_value = dict(
    sorted(
        demo_dict.items(), 
        key = lambda x: x[1], # sort by values
        reverse = True # sort descending
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


#----------------------------------------------------------------------#
#----------------- Loop through keys, values, and items ---------------#
#----------------------------------------------------------------------#

# Create a sample dictionary for demonstration
sample_loop_dict = {
    'name': 'Jack',
    'age': 32,
    'city': 'Seattle',
    'country': 'USA'
}

########################################
## Loop through keys using a for loop ##
########################################

for key in sample_loop_dict:
    print(f"Key: {key}")  
# Key: name 
# Key: age
# Key: city
# Key: country

#####################################
## Loop through keys using .keys() ##
#####################################

for key in sample_loop_dict.keys():
    print(f"{key}: {sample_loop_dict[key]}")
# name: Jack
# age: 32
# city: Seattle
# country: USA

#########################################
## Loop through values using .values() ##
#########################################

for value in sample_loop_dict.values():
    print(f"Value: {value}")
# Value: Jack
# Value: 32
# Value: Seattle
# Value: USA

#################################################
## Loop through key-value pairs using .items() ##
#################################################

for key, value in sample_loop_dict.items():
    print(f"{key} = {value}")
# name = Jack
# age = 32
# city = Seattle
# country = USA

####################################################
## Loop through keys and values using enumerate() ##
####################################################

for index, (key, value) in enumerate(sample_loop_dict.items()):
    print(f"Index: {index}, Key: {key}, Value: {value}")
# Index: 0, Key: name, Value: Jack
# Index: 1, Key: age, Value: 32
# Index: 2, Key: city, Value: Seattle
# Index: 3, Key: country, Value: USA


#--------------------------------------------------------------------------------------------------#
#------------------------------------- Dictionary Comprehension -----------------------------------#
#--------------------------------------------------------------------------------------------------#

# Create a dictionary using dictionary comprehension
dict_comp = {x: x**2 for x in range(5)}
print(dict_comp)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}


# Create a dictionary with conditional logic
dict_comp_cond = {x: x**2 for x in range(10) if x % 2 == 0}
print(dict_comp_cond)  # {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}


# Create a dictionary from two lists using zip()
keys = ['a', 'b', 'c']
values = [1, 2, 3]
dict_from_zip = {k: v for k, v in zip(keys, values)}
print(dict_from_zip)  # {'a': 1, 'b': 2, 'c': 3}


# Create a dictionary with mixed data types using comprehension
mixed_dict_comp = {x: (x, x**2) for x in range(5)}
print(mixed_dict_comp)  # {0: (0, 0), 1: (1, 1), 2: (2, 4), 3: (3, 9), 4: (4, 16)}


# Create a nested dictionary using comprehension
nested_dict_comp = {f'item_{x}': {'value': x, 'square': x**2} for x in range(3)}
print(nested_dict_comp)
# {'item_0': {'value': 0, 'square': 0}, 'item_1': {'value': 1, 'square': 1}, 'item_2': {'value': 2, 'square': 4}}


# Create a dictionary with keys as letters and values as their ASCII codes
dict_ascii = {chr(x): x for x in range(65, 91)}  # A-Z
print(dict_ascii)
# {'A': 65, 'B': 66, 'C': 67, 'D': 68, 'E': 69, 'F': 70, 'G': 71, 'H': 72, 'I': 73, 'J': 74,
#  'K': 75, 'L': 76, 'M': 77, 'N': 78, 'O': 79, 'P': 80, 'Q': 81, 'R': 82, 'S': 83, 'T': 84,
#  'U': 85, 'V': 86, 'W': 87, 'X': 88, 'Y': 89, 'Z': 90}