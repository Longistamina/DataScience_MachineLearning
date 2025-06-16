'''
Dictionary:
    ## A dictionary is a collection of key-value pairs.
    ## Each key is unique and maps to a specific value.
    ## Dictionaries are mutable, meaning you can change their content.
# => use dictionary when you need to store data in key-value pairs for fast lookups
# => or when you need to associate values with unique keys.

Table of contents:
#### Create dictionary: {}, dict()
#### Access values by key: dict[key]
#### Check if key exists
#### Add and Remove key-value pairs: .update(), .pop(), .popitem(), .clear()
#### Dictionary Methods: .keys(), .values(), .items(), .get(), .setdefault(), .copy()
#### Loop through keys, values, and items
#### Dictionary Comprehension
'''

#----------------------------------------------------#
#----------------- Create dictionary ----------------#
#----------------------------------------------------#

# Create an empty dictionary
empty_dict_1 = {}      # {}
empty_dict_2 = dict()  # {}

print(type(empty_dict_1))  # <class 'dict'>
print(type(empty_dict_2))  # <class 'dict'>


# Create a dictionary with key-value pairs
dict_1 = {
    'name': 'Alice',
    'age': 30,
    'city': 'New York'
}
print(dict_1)  # {'name': 'Alice', 'age': 30, 'city': 'New York'}


# Create a dictionary using the dict() constructor
dict_2 = dict(name='Bob', age=25, city='Los Angeles')
print(dict_2)  # {'name': 'Bob', 'age': 25, 'city': 'Los Angeles'}


# Create a dictionary from a list of tuples
dict_3 = dict([('name', 'Charlie'), ('age', 35), ('city', 'Chicago')])
print(dict_3)  # {'name': 'Charlie', 'age': 35, 'city': 'Chicago'}


# Create a dictionanry with iterable values
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


# Create a dictionary with mixed data types
dict_6 = {
    'name': 'David',
    'age': 40,
    'is_student': False,
    'grades': [90, 85, 88],
    'address': {'city': 'Miami', 'state': 'FL'}
}
print(dict_5)  
# {'name': 'David', 'age': 40, 'is_student': False, 'grades': [90, 85, 88], 'address': {'city': 'Miami', 'state': 'FL'}}


#----------------------------------------------------#
#----------------- Access values by key -------------#
#----------------------------------------------------#

# Access values by key
dict_acces = {
    'name': 'Eve',
    'age': 28,
    'city': 'San Francisco'
}
print(dict_acces['name'])  # Eve
print(dict_acces['age'])   # 28
print(dict_acces['city'])  # San Francisco


# Accessing a key that does not exist raises a KeyError
# print(dict_acces['country'])  # KeyError: 'country'


# Use the get() method to avoid KeyError
# Accessing a key that does not exist using get() method
print(dict_acces.get('country'))  # None
print(dict_acces.get('name'))     # Eve


# Access values within a list from a dictionary
dict_list_access = {
    'ID': [1, 2, 3],
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [30, 25, 35]
}
print(dict_list_access['Name'][0])  # Alice
print(dict_list_access['Age'][2])   # 35


# Access values within a nested dictionary
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


#----------------------------------------------------#
#----------------- Check if key exists --------------#
#----------------------------------------------------#
# Check if a key exists in the dictionary
dict_check = {
    'name': 'Grace',
    'age': 22,
    'city': 'Boston'
}

# Using 'in' operator
print('name' in dict_check)  # True
print('country' in dict_check)  # False

# Using the get() method
print(dict_check.get('age') is not None)  # True
print(dict_check.get('country') is not None)  # False

# Using the keys() method
print('city' in dict_check.keys())  # True
print('country' in dict_check.keys())  # False


