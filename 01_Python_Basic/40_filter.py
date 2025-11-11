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

# When you pass None as the function argument, 
# filter() removes all "falsy" values (0, empty strings, empty iterables, False, None, etc.)

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
