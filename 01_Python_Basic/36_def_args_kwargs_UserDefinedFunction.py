'''
Python functions are reusable blocks of code that perform specific tasks.
They help organize your code, make it more modular, and enable code reusability.
Functions are defined using the def keyword and can accept inputs (parameters) and return outputs.

Parameters: these are the variables defined in a function's signature that accept input values.
Arguments: these are the actual values passed to a function's parameters when it is called
'''

##########################################

'''
def function_name(parameters):
    """Optional docstring"""
    # Function body
    return value  # Optional

+ def keyword: Starts the function definition
+ Function name: Should follow Python naming conventions (snake_case)
+ Parameters: Input values in parentheses (optional)
+ Colon (:): Marks the start of the function body
+ Indented code block: The function's implementation
+ return statement: Returns a value to the caller (optional)
'''

##########################################

'''
Flow of contents:
1. Define a function using def: without parameters, with parameters, with default parameters.
2. Return a value using "return" statement.
3. Constraint the data type of parameters using type hints.
4. Positional arguments: passing arguments in the order of parameters.
5. Keyword arguments: passing arguments by explicitly specifying the parameter names.
6. Default arguments: parameters with default values that can be omitted when calling the function.
7. *args (Variable Positional Arguments): allows passing a variable number of positional arguments to a function.
8. **kwargs (Variable Keyword Arguments): allows passing a variable number of keyword arguments to a function.
'''


#------------------------------------------------------------------------------------------------------------#
#----------------------------------- 1. Define a function using def -----------------------------------------#
#------------------------------------------------------------------------------------------------------------#

#######################################
## Basic function without parameters ##
#######################################

def greet():
    """Simple greeting function."""
    print("Hello, World! This is a basic function without parameters.")


# Call the function
greet()
# Hello, World! This is a basic function without parameters.


##############################
## Function with parameters ##
##############################

def add_numbers(x, y):
    """Add two numbers."""
    print(f"{x} + {y} = {x + y}")


# Call the function with arguments
add_numbers(
    x = 5, # x and y are parameters
    y = 10 # 5 and 10 are arguments passed to the function's parameters
)
# 5 + 10 = 15


# Call the function with positional arguments
add_numbers(3, 7)
# 3 + 7 = 10


######################################
## Function with default parameters ##
######################################

def customer_info(name, age=30, job="Unknown"):
    """Display customer information with a default age and job"""
    print(f"Customer Name: {name}, Age: {age}", f"Job: {job}")

# Call the function with default parameters
customer_info("Alice")
# Customer Name: Alice, Age: 30 Job: Unknown


# Call the function with custom parameters (repalacing default values)
customer_info("Bob", 25, "Engineer")
# Customer Name: Bob, Age: 25 Job: Engineer


#------------------------------------------------------------------------------------------------------------#
#------------------------------- 2. Return a value using "return" statement ---------------------------------#
#------------------------------------------------------------------------------------------------------------#

# "return" statement is used to exit a function and return a value to the caller.

###############
## Example 1 ##
###############
def square(number):
    """Return the square of a number."""
    return number * number

# Call the function and store the returned value
result = square(4)
print(f"The square of 4 is: {result}")


###############
## Example 2 ##
###############

def input_customer_info():
    """Input customer information and return it as a dictionary."""
    name = input("Enter customer name: ")
    age = int(input("Enter customer age: "))
    job = input("Enter customer job: ")
    
    return {"name": name, "age": age, "job": job}

# Call the function and store the returned dictionary
customer_data = input_customer_info()

print(f"Customer Data: {customer_data}")
#Customer Data: {'name': 'Zetharax', 'age': 150000, 'job': 'Creator of the world'}


#------------------------------------------------------------------------------------------------------------#
#--------------------------- 3. Constraint the data type of parameters using type hints ---------------------#
#------------------------------------------------------------------------------------------------------------#

###############
## Example 1 ##
###############

def multiply(a: int, b: int) -> int:
    """Multiply two integers and return the result (also integer)."""
    return a * b

result_1 = multiply(3, 5) # a and b must be integers
print(result_1) # 15

result_2 = multiply(2.5, 4.0) # This will not raise an error, but it's not recommended
print(result_2) # 10.0 (not an integer, but Python does not enforce type hints at runtime)

'''
After setting datatype hint, if you then turn on the parameter-hint (shift + tab),
it will show you the expected data types for the parameters and return value.
This is useful for documentation and code readability, but it does not enforce type checking at runtime.
'''


###############
## Example 2 ##
###############

def concatenate_strings(str1: str, str2: str) -> str:
    """Concatenate two strings and return the result."""
    return str1 + str2

result_3 = concatenate_strings("Hello, ", "World!")
print(result_3)  # Hello, World!


#------------------------------------------------------------------------------------------------------------#
#--------------------- 4. Positional arguments: passing arguments in the order of parameters ----------------#
#------------------------------------------------------------------------------------------------------------#

# Positional arguments are passed to a function in the order of the parameters defined in the function signature.
# If the function has parameters `a`, `b`, and `c`, you can call it like this: `function_name(1, 2, 3)`.
# If the order is violated, it can lead to unexpected results, or even errors.

def info_display(first_name, last_name, DoB):
    """Display the full name."""
    print(f"{first_name} {last_name} - {DoB}")


# Call the function with positional arguments in the correct order
info_display("Abraham", "Lincoln", "12 February 1809")
# Abraham Lincoln - 12 February 1809


# Call the function with positional arguments in the wrong order
info_display("Lincoln", "12 February 1809", "Abraham")
# Lincoln 12 February 1809 - Abraham

'''
If the order of arguments is not respected, the output will be different from what you expect.
This is because positional arguments are matched to parameters based on their position.
'''


#------------------------------------------------------------------------------------------------------------#
#------------- 5. Keyword arguments: passing arguments by explicitly specifying the parameter names ---------#
#------------------------------------------------------------------------------------------------------------#

# Keyword arguments allow you to pass arguments to a function by explicitly specifying the parameter names.
# This makes the code more readable and allows you to pass arguments in any order.

def person_info(name, age, city):
    """Display person's information."""
    print(f"Name: {name}, Age: {age}, City: {city}")


# Call the function with keyword arguments with the same order as parameters
person_info(name = "John", age = 30, city = "New York")
# Name: John, Age: 30, City: New York


# Call the function with keyword arguments in a different order
person_info(
    city = "Los Angeles", 
    age = 25, 
    name = "Alice"
)
# Name: Alice, Age: 25, City: Los Angeles

'''
The result has the same output format (order) even though the arguments were passed in a different order.
This is because keyword arguments explicitly specify which parameter each argument corresponds to.
'''


#------------------------------------------------------------------------------------------------------------#
#------------------- 6. Default arguments: parameters with default values that can be omitted ---------------#
#------------------------------------------------------------------------------------------------------------#

# Default arguments allow you to define parameters with default values.
# If the caller does not provide a value for that parameter, the default value is used.

def greet_user(name, greeting="Hello"):
    """Greet the user with a default greeting."""
    print(f"{greeting}, {name}!")


# Call the function with a default argument
greet_user("Alice")
# Hello, Alice!


# Call the function with a custom greeting
greet_user("Bob", "Bonjour")
# Bonjour, Bob!


#-------------------------------------------------------------------------------------------------------------#
#---------------------- 7. *args (Variable Positional Arguments) ---------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

# *args allows you to pass a variable number of positional arguments to a function.
# It collects all the extra positional arguments into a TUPLE.
# This is useful when you don't know in advance how many arguments will be passed.


#####################################
## Example 1: print out all inputs ##
#####################################

def print_all(*args):
    """Print all positional arguments."""
    for arg in args:
        print(arg)

# Call the function with multiple arguments
print_all("Hello", "World", 42, True)
# Hello
# World
# 42
# True


#########################################
## Example 2: change the name of *args ##
#########################################

def sum_numbers(*nums): # Now *nums will work as *args to collect all positional arguments
    """Calculate the sum of all numbers passed as arguments."""
    if not nums:
        return "No numbers provided." # It will return this and exit the function immediately
    else:
        total = 0

    for num in nums:
        total += num
    return total


print(sum_numbers()) # No numbers provided.
print(sum_numbers(1, 2, 3, 4, 5)) # 15
print(sum_numbers(30)) # 30


###############################################
## Example 3: combine *args with enumerate() ##
###############################################

def sign_check(*nums):
    """Check the sign of the numbers, return: positive, negative or zero"""
    nums = list(nums) # Convert to string to enable modification
    
    for idx, number in enumerate(nums):
        if number > 0:
            nums[idx] = "positive"
        elif number < 0:
            nums[idx] = "negative"
        else:
            nums[idx] = "zero"
    
    return nums

print(sign_check(2, 2.4, 3.5, -6, 1, -22.0, 0))
# ['positive', 'positive', 'positive', 'negative', 'positive', 'negative', 'zero']


###############################################
## Example 4: concatenate strings with *args ##
###############################################

def create_message(*strings): # now *strings will work as *args to collect all positional arguments
    """Create a message from multiple parts."""
    return " ".join(str(info) for info in strings)

print(create_message("Hello", "world", "from", "Python"))
# "Hello world from Python"


#-------------------------------------------------------------------------------------------------------------#
#---------------------------------- 8. **kwargs (Variable Keyword Arguments) ---------------------------------#
#-------------------------------------------------------------------------------------------------------------#

# **kwargs allows you to pass a variable number of keyword arguments to a function.
# It collects all the extra keyword arguments into a dictionary.


##########################
## **kwargs explanation ##
##########################

def demo_kwargs(**kwargs):
    """Display all keyword arguments."""
    print(type(kwargs))  # <class 'dict'>
    print(kwargs)  # {'key1': 'value1', 'key2': 'value2', ...}
    print(kwargs.keys())  # dict_keys(['key1', 'key2', ...])
    print(kwargs.values())  # dict_values(['value1', 'value2', ...])


# Call the function with multiple keyword arguments
demo_kwargs(key1 = "value1", key2 = "value2", key3 = 42)
# <class 'dict'>
# {'key1': 'value1', 'key2': 'value2', 'key3': 42}
# dict_keys(['key1', 'key2', 'key3'])
# dict_values(['value1', 'value2', 42])


#################################
## Change the name of **kwargs ##
#################################

def display_info(**info):  # Now **info will work as **kwargs to collect all keyword arguments
    """Display information from keyword arguments."""
    for key, value in info.items():
        print(f"{key}: {value}")
        

# Call the function with keyword arguments
display_info(name = "Alice", age = 30, city = "New York")
# name: Alice
# age: 30
# city: New York


########################################################################
## Example: calculate salary with required fields and optional fields ##
########################################################################

from loguru import logger

def calculate_salary(**info):
    """Calculate salary based on required and optional fields."""
    
    if "name" not in info: # check if 'name' is in the dictionary info
        logger.error("Name is required.") # log an error message if 'name' is not provided
        return None # return None and exit the function
    
    if 'salary_daily' not in info:
        return "Daily salary is required."
    
    if "working_days" not in info:
        return "Working days are required."
    
    # Extract information from the dictionary **info
    name = info['name']
    salary_daily = info['salary_daily']
    working_days = info['working_days']

    # Calculate base salary
    base_salary = salary_daily * working_days

    # Default bonus is 0 if not provided
    bonus = info.get('bonus', 0)
    
    total_salary = base_salary + bonus

    logger.info(f"Calculating salary for {name}:\nBase Salary = {base_salary}\nBonus = {bonus}\n==> Total Salary = {total_salary}")
    return {"Name": name, "Total Salary": total_salary}


#----------------------
## Call the function with required and optional fields
#----------------------

salary_info = calculate_salary(
    name = "Alice",
    salary_daily = 100,
    working_days = 20,
    bonus = 500
)
# | INFO     | __main__:calculate_salary:19 - Calculating salary for Alice:
# Base Salary = 2000
# Bonus = 500
# ==> Total Salary = 2500

print(salary_info)
# {'Name': 'Alice', 'Total Salary': 2500}


#-----------------------
## Call the functionn lacking required fields
#-----------------------

salary_info = calculate_salary(
    salary_daily = 100,
    working_days = 20,
    bonus = 500
)
# | ERROR    | __main__:calculate_salary:4 - Name is required.

print(salary_info)  
# None