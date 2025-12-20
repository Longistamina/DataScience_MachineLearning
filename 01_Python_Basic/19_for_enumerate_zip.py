#-----------------------------------------------------------#
#------------------------ for loop -------------------------#
#-----------------------------------------------------------#

for _ in range(5):
    print("Hello, World!")

for i in range(1, 20):
    if i%2 != 0: 
        print(i)

#### for zip() ####

lst_name = ["Socrates", "Plato", "Aristotle"]
lst_age = [80, 57, 35]

for name, age in zip(lst_name, lst_age):
    print(f'{name}: {age} years old')
# Socrates: 80 years old
# Plato: 57 years old
# Aristotle: 35 years old


#-----------------------------------------------------------#
#------------------------ for Nest -------------------------#
#-----------------------------------------------------------#

## apply for Nest to create multiplication table

print('-' * 116)
print('Multiplication table - Method 1'.center(116))
print('-' * 116)

mult_table = ''

for n in range(1, 11, 1):
    for i in range (2, 10, 1):
        mult_table += f'{i:2} x {n:2} = {i * n:2}   ' # {i:2} means the space range of this character is 2
    mult_table +='\n'
print(mult_table)

print('-' * 116)
print('Multiplication table - Method 2'.center(116))
print('-' * 116)

for n in range(1, 11, 1):
    for i in range (2, 10, 1):
        print(f'{i:2} x {n:2} = {i*n:2}', end='   ') # {i:2} means the space range of this character is 2
    print()
    

#------------------------------------------------------------------#
#------------------------ for enumerate() -------------------------#
#------------------------------------------------------------------#

# enumerate() is a built-in function that adds a counter to an iterable and returns it as an enumerate object.
# It is commonly used in loops to get both the index and the value of items in a list or other iterable.

lst_fruits = ['apple', 'banana', 'cherry']

print(enumerate(lst_fruits))  # Output: <enumerate object at 0x...>

print(list(enumerate(lst_fruits)))  # Output: [(0, 'apple'), (1, 'banana'), (2, 'cherry')]


# Use enumerate in a for loop
for index, fruit in enumerate(lst_fruits):
    print(f'Index: {index}, Fruit: {fruit}')
# Output:
# Index: 0, Fruit: apple
# Index: 1, Fruit: banana
# Index: 2, Fruit: cherry


# Use enumerate with a start index
for index, fruit in enumerate(lst_fruits, start=1):
    print(f'Index: {index}, Fruit: {fruit}')
# Output:
# Index: 1, Fruit: apple
# Index: 2, Fruit: banana
# Index: 3, Fruit: cherry


# Use enumerate with _, vals to ignore the index
for _, fruit in enumerate(lst_fruits):
    print(f'Fruit: {fruit}')
# Output:
# Fruit: apple
# Fruit: banana
# Fruit: cherry

# Use enumerate with _, _ to ignore both index and value
for _, _ in enumerate(lst_fruits):
    print('This is a fruit.')
# Output:
# This is a fruit.
# This is a fruit.
# This is a fruit.