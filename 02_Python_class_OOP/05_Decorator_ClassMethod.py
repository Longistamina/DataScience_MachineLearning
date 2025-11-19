# Class methods are the methods that are bound to the class, not the instance of the class.
# Class methods always require "cls" as the first argument, which refers to the class itself
# Class methods also need a return value, otherwise it will return None by default

# @classmethod is a decorator that indicates the below method is a class method

# When to use: we should use class methods to do something that is related to the class
#              but does not need to be unique per instance
#              and IS involved in creating new instances of the class (like construct_from_csv() below)

import csv

class Employee:
    @classmethod # indicates the below method is a class method, not an instance method
    def demo_class_method(cls): # class method requires "cls" as the first argument, like "self" for instance method
        print("This is a demo class method of the class Item")

    @classmethod
    def construct_from_csv(cls, file_path: str): #A function to construct an instance of the class from a .csv file
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f) # Read .csv file as a dictionary
            employees = list(reader)

        return employees

print(Employee.demo_class_method()) # Execute a class method
                                    # This is a demo class method of the class Item
                                    # None (this is because we did not define the return value for the demo method)

csv_path = "/home/longdpt/Documents/Academic/DataScience_MachineLearning_Python_SQL/01_Python_Basic/class_OOP/class_method_employees.csv"

lst_employees = Employee.construct_from_csv(file_path=csv_path)
print(lst_employees)
# {'Name': 'Alice', 'Age': '30', 'City': 'New York'}
# {'Name': 'Bob', 'Age': '25', 'City': 'Los Angeles'}
# {'Name': 'Charlie', 'Age': '35', 'City': 'Chicago'}

### NOT RECOMMEND: class methods can be called from an instance, but should not do so
