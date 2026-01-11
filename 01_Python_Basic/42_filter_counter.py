'''
1. filter() function
   + Basic use with normal function
   + Basic use with lambda function
   + Using filter() with None
   + Other examples
   
2. collections.Counter (from collections import Counter)
   + Basic use with lists/strings
   + most_common() method
   + Counter arithmetic operations
   + elements() method: create an iterator with repeated elements
   + update() and subtract() methods
   + Other examples
'''

#--------------------------------------------------------------------------------------------------#
#--------------------------------------- 1. filter() function -------------------------------------#
#--------------------------------------------------------------------------------------------------#
'''
The filter() function is one of Python's most powerful built-in functions for data filtering and manipulation.

The filter() function creates an iterator from elements of an iterable for which a function returns True.

Syntax: filter(function, iterable)

Like map(), filter() returns an iterator, 
so you need to convert it to a list or another iterable type to see the materialized results.
'''

####################################
## Basic use with normal function ##
####################################

numbers = [1, 5.2, 3, 7.9, 2.8, 10, 15.6]

def is_integer(num):
    return isinstance(num, int) # Check if num is an integer

filter_object = filter(is_integer, numbers)
print(filter_object) # <filter object at 0x7f7014402bc0>

int_numbers = list(filter_object) # Convert filter object to list
print(int_numbers) # [1, 3, 10]

####################################
## Basic use with lambda function ##
####################################

angels = ["Lilith", "ADAM", "Sachiel", "SHAMSHEL", "Ramiel", "GAGHIEL", "Israfel", "SANDALPHON"]

# Filter out the angles that are in uppercase
angels_upper = list(filter(lambda angel: angel.isupper(), angels))
print(angels_upper) # ['ADAM', 'SHAMSHEL', 'GAGHIEL', 'SANDALPHON']

# Filter out the angles whose name is less than or equal 6 characters
angels_short = list(filter(lambda angel: len(angel) <= 6, angels))
print(angels_short) # ['Lilith', 'ADAM', 'Ramiel']

####################################
##    Using filter() with None    ##
####################################
'''
When you pass None as the function argument, 
filter() removes all "falsy" values (0, empty strings, empty iterables, False, None, etc.)
'''

mixed_data = [0, 1, '', 'data', None, False, True, [], [1, 2]]
clean_data = list(filter(None, mixed_data))

print(clean_data) # [1, 'data', True, [1, 2]]

####################
## Other examples ##
####################

# Filter sales data above threshold
sales_data = [150, 250, 300, 125, 450, 200, 380]
high_sales = list(filter(lambda x: x >= 300, sales_data))
print(high_sales)  # Output: [300, 450, 380]

# Filter employees within working age range
employee_ages = [22, 35, 28, 41, 33, 29, 38, 45, 26, 52]
working_age = list(filter(lambda age: 25 <= age <= 45, employee_ages))
print(working_age)  # Output: [35, 28, 41, 33, 29, 38, 45, 26]

# Filter specific email domains
emails = ['john@company.com', 'alice@gmail.com', 'bob@company.com']
company_emails = list(filter(lambda email: '@company.com' in email, emails))
print(company_emails)  # Output: ['john@company.com', 'bob@company.com']


#--------------------------------------------------------------------------------------------------#
#-------------------- 2. collections.Counter (from collections import Counter) --------------------#
#--------------------------------------------------------------------------------------------------#
'''
The Counter class from the collections module is a specialized dictionary subclass designed for 
counting hashable objects. It's incredibly useful for frequency analysis and tallying operations.

Counter is a dict subclass where elements are stored as dictionary keys and their counts as values.
Counts can be zero or negative, making it flexible for various counting scenarios.

Syntax: Counter(iterable or mapping or keyword args)

Counter provides several powerful methods beyond standard dict operations, 
making it the go-to tool for counting operations in Python.
'''

from collections import Counter

##################################
## Basic use with lists/strings ##
##################################

# Count characters in a string
text = "mississippi"
char_count = Counter(text)
print(char_count)  # Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})

# Count elements in a list
fruits = ["apple", "banana", "apple", "orange", "banana", "apple"]
fruit_count = Counter(fruits)
print(fruit_count)  # Counter({'apple': 3, 'banana': 2, 'orange': 1})

# Access counts like a dictionary
print(fruit_count["apple"])  # 3
print(fruit_count["grape"])  # 0 (returns 0 for missing elements, not KeyError!)

'''char_count and fruit_count are Counter objects, which behave like dictionaries.'''

###########################
## .most_common() method ##
###########################

# Get the n most common elements
chars = [1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 5, 5]
num_counter = Counter(numbers)

# Get all elements sorted by frequency (omit argument)
all_sorted = num_counter.most_common()
print(all_sorted)  # [(3, 4), (1, 3), (2, 2), (5, 2), (4, 1)]

# Get top 3 most common
top_3 = num_counter.most_common(3)
print(top_3)  # [(3, 4), (1, 3), (2, 2)] - returns list of (element, count) tuples

########

chars = "aabbccddeeefffggghhhiii"
char_counter = Counter(chars)

print(char_counter.most_common())  
# [('e', 3), ('f', 3), ('g', 3), ('h', 3), ('i', 3), ('a', 2), ('b', 2), ('c', 2), ('d', 2)]

print(char_counter.most_common(2))
# [('e', 3), ('f', 3)]

###################################
## Counter arithmetic operations ##
###################################

# You can add, subtract, and perform set operations with Counters
counter1 = Counter(['a', 'b', 'c', 'a', 'b', 'b'])
counter2 = Counter(['a', 'b', 'd', 'd'])

# Addition: combine counts
combined = counter1 + counter2
print(combined)  # Counter({'b': 4, 'a': 3, 'd': 2, 'c': 1})

# Subtraction: subtract counts (keeps only positive counts)
difference = counter1 - counter2
print(difference)  # Counter({'b': 2, 'c': 1, 'a': 0})

# Intersection: keep minimum counts
intersection = counter1 & counter2
print(intersection)  # Counter({'a': 1, 'b': 1})

# Union: keep maximum counts
union = counter1 | counter2
print(union)  # Counter({'b': 3, 'a': 2, 'd': 2, 'c': 1})

########################
## .elements() method ##
########################

# Returns an iterator over elements, repeating each as many times as its count
c = Counter(a=3, b=2, c=1)
print(list(c.elements()))  # ['a', 'a', 'a', 'b', 'b', 'c']

# Note: elements with count <= 0 are ignored
c2 = Counter(a=2, b=0, c=-1)
print(list(c2.elements()))  # ['a', 'a']

#######################################
## .update() and .subtract() methods ##
#######################################

# update() adds counts (like += but in-place)
counter = Counter(['a', 'b', 'c'])
counter.update(['a', 'b', 'd'])
print(counter)  # Counter({'a': 2, 'b': 2, 'c': 1, 'd': 1})

# subtract() subtracts counts (can result in zero or negative)
counter.subtract(['a', 'b', 'b'])
print(counter)  # Counter({'a': 1, 'c': 1, 'd': 1, 'b': 0})

####################
## Other examples ##
####################

# Word frequency analysis
sentence = "the quick brown fox jumps over the lazy dog the fox"
word_freq = Counter(sentence.split())
print(word_freq.most_common(2))  # [('the', 3), ('fox', 2)]

# DNA sequence nucleotide counting
dna_sequence = "ATCGATCGATCGTAGCTAGCTA"
nucleotide_count = Counter(dna_sequence)
print(nucleotide_count)  # Counter({'A': 6, 'T': 6, 'C': 5, 'G': 5})

# Finding duplicates in a dataset
data = [1, 2, 3, 2, 4, 5, 3, 6, 3]
count = Counter(data)
duplicates = [num for num, freq in count.items() if freq > 1]
print(duplicates)  # [2, 3]

# Vote counting system
votes = ['Alice', 'Bob', 'Alice', 'Charlie', 'Alice', 'Bob', 'Alice']
vote_counter = Counter(votes)
winner = vote_counter.most_common(1)[0]
print(f"Winner: {winner[0]} with {winner[1]} votes")  # Winner: Alice with 4 votes

# Character frequency for password strength analysis
password = "P@ssw0rd123!"
char_types = Counter() # Initialize empty Counter
for char in password:
    if char.isalpha():
        char_types['letters'] += 1
    elif char.isdigit():
        char_types['digits'] += 1
    else:
        char_types['special'] += 1
print(char_types)  # Counter({'letters': 5, 'digits': 4, 'special': 2})
