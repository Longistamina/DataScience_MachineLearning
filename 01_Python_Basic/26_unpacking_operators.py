'''
Unpack operators are used to unpack iterables into individual elements.

There are two types of unpacking operators in Python:
1. The asterisk (*) operator: Used to unpack iterables like lists or tuples.
2. The double asterisks (**) operator: Used to unpack dictionaries.
'''


#---------------------------------------------------------------#
#------------------ Unpacking with aterisk (*) -----------------#
#---------------------------------------------------------------#

################################################
## Unpacking a list into individual variables ##
################################################

numbers = [1, 2, 3, 4, 5]

a, b, c, d, e = numbers

print(a)  # Output: 1
print(b)  # Output: 2
print(c)  # Output: 3
print(d)  # Output: 4
print(e)  # Output: 5

#################################################
## Unpacking a tuple into individual variables ##
#################################################

coordinates = (10, 20, 30)

x, y, z = coordinates

print(x)  # Output: 10
print(y)  # Output: 20
print(z)  # Output: 30

###############################################################
## Unpacking with asterisk (*) to collect remaining elements ##
###############################################################

numbers = [1, 2, 3, 4, 5]

a, b, *rest = numbers

print(a)      # Output: 1
print(b)      # Output: 2
print(rest)   # Output: [3, 4, 5]

#################################
## Unpacking a nested iterable ##
#################################

nested_list = ["han", (20, 4000), "developer", "single", "NYC"]

name, (age, salary), profession, *other_info = nested_list
print(name)        # han
print(age)         # 20
print(salary)      # 4000
print(profession)  # developer
print(other_info)  # ['single', 'NYC']

#### for loop ####

employees = [
    ["han", (20, 4000), "developer", "single", "NYC"],
    ["luke", (25, 5000), "designer", "married", "LA"],
    ["leia", (22, 4500), "manager", "single", "SF"]
]

for name, (age, salary), profession, *other_info in employees:
    print(f"Name: {name}, Age: {age}, Salary: {salary}, Profession: {profession}, Other Info: {other_info}")
'''
Name: han, Age: 20, Salary: 4000, Profession: developer, Other Info: ['single', 'NYC']
Name: luke, Age: 25, Salary: 5000, Profession: designer, Other Info: ['married', 'LA']
Name: leia, Age: 22, Salary: 4500, Profession: manager, Other Info: ['single', 'SF']
'''

#####################################################
## Unpacking and combining lists with asterisk (*) ##
#####################################################

list1 = [1, 2, 3]
list2 = [4, 5, 6]

combined = [*list1, *list2]

print(combined)  # [1, 2, 3, 4, 5, 6]

###################################################
## Unpacking a string into individual characters ##
###################################################

string = "Hello"

chars = [*string]

print(chars)  # Output: ['H', 'e', 'l', 'l', 'o']


#---------------------------------------------------------#
#---------- Unpacking with double asterisks (**) ---------#
#---------------------------------------------------------#

############################################################
## Unpacking a dictionary into individual key-value pairs ##
############################################################

person = {'name': 'Alice', 'age': 30, 'city': 'New York'}

name, age, city = person.values()

print(name)  # Output: Alice
print(age)   # Output: 30
print(city)  # Output: New York

####################################################
## Unpacking a dictionary into another dictionary ##
####################################################

new_person = {'country': 'USA', **person}

print(new_person)  # Output: {'country': 'USA', 'name': 'Alice', 'age': 30, 'city': 'New York'}

############################################################
## Unpacking a dictionary with additional key-value pairs ##
############################################################

additional_info = {'hobby': 'reading', 'profession': 'engineer'}

combined_info = {**person, **additional_info}

print(combined_info)  
# Output: {'name': 'Alice', 'age': 30, 'city': 'New York', 'hobby': 'reading', 'profession': 'engineer'}

##################################################################
## Unpacking and merging dictionaries with double asterisk (**) ##
##################################################################

default_config = {
    'host': 'localhost',
    'port': 8080,
    'debug': False
}

user_config = {
    'port': 3000,
    'debug': True
}

final_config = {**default_config, **user_config} # Merging dictionaries
print(final_config)  # {'host': 'localhost', 'port': 3000, 'debug': True}
                     # The user_config overrides the default_config for 'port' and 'debug'
'''
When merging dictionaries using the ** unpacking operator, 
the right-side dictionary has higher priority and will override any duplicate keys from the left-side dictionary.
'''