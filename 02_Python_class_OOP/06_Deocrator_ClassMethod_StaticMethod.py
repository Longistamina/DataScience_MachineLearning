import csv
from pathlib import Path

#--------------------------------------------------------------------------------------#
#----------------------------- Decorator: @classmethod --------------------------------#
#--------------------------------------------------------------------------------------#
'''
# Class methods are the methods that are bound to the class, not the instance of the class.
# Class methods always require "cls" as the first argument, which refers to the class itself
# Class methods also need a return value, otherwise it will return None by default

# @classmethod is a decorator that indicates the below method is a class method

# When to use: we should use class methods to do something that is related to the class
#              but does not need to be unique per instance
#              and want to have access to class attributes or other class methods
'''

class Employee:

    class_atribute = "This is a class attribute of Employee class"

    @classmethod # indicates the below method is a class method, not an instance method
    def demo_class_method(cls, attr=False): # class method requires "cls" as the first argument, like "self" for instance method
        if attr:
            print(cls.class_atribute)
        else:
            print("This demo class method has been executed successfully!")

    @classmethod
    def construct_from_csv(cls, file_path: str|Path): #A function to construct an instance of the class from a .csv file
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f) # Read .csv file as a dictionary
            employees = list(reader)

        cls.demo_class_method(attr=False) # Call another class method from this class method
        return employees

########################################################

Employee.demo_class_method(attr=False)
# This is a demo class method of the class Item

Employee.demo_class_method(attr=True)
# This is a class attribute of Employee class

########################################################

csv_path = next(Path("/home/").glob("**/Documents/**/class_method_employees.csv"))
print(csv_path)
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/02_Python_class_OOP/class_method_employees.csv

lst_employees = Employee.construct_from_csv(file_path=csv_path)
print(lst_employees)
# {'Name': 'Alice', 'Age': '30', 'City': 'New York'}
# {'Name': 'Bob', 'Age': '25', 'City': 'Los Angeles'}
# {'Name': 'Charlie', 'Age': '35', 'City': 'Chicago'}

'''NOT RECOMMEND: class methods can be called from an instance, but should not do so'''


#--------------------------------------------------------------------------------------#
#------------------------------ Decorator: @staticmethod ------------------------------#
#--------------------------------------------------------------------------------------#
'''
# Static methods are like class method, but they are not bound to the class
# Static methods DO NOT require "cls" as the first argument, i.e not bound or refer to the class
# => hence they cannot access class attributes or other class methods directly

# @staticmethod is a decorator that indicates the below method is a static method

# When to use: we should use static methods to do something that is related to the class
#              but does not need to be unique per instance
#              and does not require accessing other class atributes and class methods
'''

class DemoStatic:

    class_attribute = "I am a class attribute"

    @staticmethod
    def demo_static_method(attr=False): #No need any compulsory arguments like "cls" or "self"
        if attr:
            print(DemoStatic.class_attribute)
            '''print(cls.class_attribute) # This will raise an error'''
        else:
            print("This demo static method has been executed successfully!")

    @staticmethod
    def add_numbers(addend_1: float, addend_2: float): # No need any compulsory arguments like "cls" or "self"

        DemoStatic.demo_static_method(attr=False) # Call another static method from this static method
        '''cls.demo_static_method(attr=False) # This will raise an error'''
        return addend_1 + addend_2

########################################################################

DemoStatic.demo_static_method() # Execute a static method without "cls" or "self" arguments
# This demo static method has been executed successfully!

DemoStatic.demo_static_method(attr=True) # Execute a static method with "cls" or "self" arguments
# I am a class attribute

########################################################################

# Execute a static method with return value without "cls" or "self" arguments
add_result = DemoStatic.add_numbers(10, 35.5)
print(add_result) # Output: 45.5

'''NOT RECOMMEND: static methods can be called from an instance, but should not do so'''
