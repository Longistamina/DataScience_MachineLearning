# Class methods are the methods that are bound to the class, not the instance of the class.
# Class methods always require "cls" as the first argument, which refers to the class itself
# Class methods also need a return value, otherwise it will return None by default

# @classmethod is a decorator that indicates the below method is a class method

# When to use: we should use class methods to do something that is related to the class
#              but does not need to be unique per instance
#              and want to have access to class attributes or other class methods

import csv

class Employee:
    
    class_atribute = "This is a class attribute of Employee class"
    
    @classmethod # indicates the below method is a class method, not an instance method
    def demo_class_method(cls, attr=False): # class method requires "cls" as the first argument, like "self" for instance method
        if attr:
            print(cls.class_atribute)
        else:
            print("This demo class method has been executed successfully!")

    @classmethod
    def construct_from_csv(cls, file_path: str): #A function to construct an instance of the class from a .csv file
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

csv_path = "/home/longdpt/Documents/Academic/DataScience_MachineLearning/02_Python_class_OOP/class_method_employees.csv"

lst_employees = Employee.construct_from_csv(file_path=csv_path)
print(lst_employees)
# {'Name': 'Alice', 'Age': '30', 'City': 'New York'}
# {'Name': 'Bob', 'Age': '25', 'City': 'Los Angeles'}
# {'Name': 'Charlie', 'Age': '35', 'City': 'Chicago'}

'''NOT RECOMMEND: class methods can be called from an instance, but should not do so'''