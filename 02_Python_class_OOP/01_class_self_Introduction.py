#------------------------------------------------------------------------#
#---------------------- example without class ---------------------------#
#------------------------------------------------------------------------#

item1_name = "Phone"
item1_price = 100
item1_quantity = 5
item1_price_total = item1_price * item1_quantity
# => These are separate independent variables

print(type(item1_name)) # str
print(type(item1_price)) # int
print(type(item1_quantity)) # int
print(type(item1_price_total)) # int
# => these variables are instances belonged to a specific class or datatype like 'str' or 'int'

print(item1_name.upper()) # PHONE
# => this .upper() is called a method, i.e a function created inside a specific class
# => here .upper() is a method of string object from string class


#------------------------------------------------------------------------#
#---------------------- first example of class --------------------------#
#------------------------------------------------------------------------#

# class: is a keyword in Python enables us to create the datatype (or class) of our own
# attribute ~ variable
# method    ~ function

# Create a class name Item
class Item:
    pass

item1 = Item()       
item1.name = "Phone" # Assign the attribute .name of item1 as "Phone"
item1.price = 100    # Assign the attribute .price of item1 as 100
item1.quantity = 5   # Assign the attribute .quantity of item1 as 5
print(type(item1))   # <class '__main__.Item'>


item2 = Item()        # Create the object item1 which belongs to class Item()
item2.name = "Laptop"
item2.price = 1000
item2.quantity = 3
print(type(item2))   # <class '__main__.Item'>


# Note: the name of a class should be written uppercase the first charcter of each words:
# => class Student:
# => class MyNewClass:
# => class RemoveMissingValues:


#-----------------------------------------------------------------#
#---------------------- "self" argument --------------------------#
#-----------------------------------------------------------------#

# "self" argument in "def method_name(self,....)" helps refer to the current instance of the class itself
# It is the way an instance method accesses the attributes (variables) and other methods of the same object
# When you define a method in a class, you explicitly include "self" as the first parameter, 
# which allows you to refer to the instance calling the method.
 

# Create a class name Item
class Item_method:
    def calculate_total_price(self, price, quantity):
        return (price * quantity)
    # def calculate_total_price(price, quantity): => raise error because all methods require "self" argument
    # must have "self" argument so that the method can access other attributes like self.price or self.quantity
    #                                                                              (item3.price)  (item3.quantity)

    

item3 = Item_method()   # Create the object item1 which belongs to class Item()
item3.name = "Car"
item3.price = 50000
item3.quantity = 1

print(item3.calculate_total_price(item3.price, item3.quantity)) # 50000