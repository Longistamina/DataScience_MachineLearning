# Create Item class

class Item:

    all_items = []

    def __init__(self, name: str, price: float, quantity: int):
        assert isinstance(name, str), "Name must be a string"
        assert price >= 0, "Price must be greater than zero"
        assert quantity >= 0, "Quantity must be greater than or equal to zero"

        self.name = name          
        self.price = price        
        self.quantity = quantity

        Item.all_items.append(self)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.price}, {self.quantity})"
        # Use self.__class__.name__ to get the class name dynamically
      
    def calculate_total_price(self):
        return self.price * self.quantity
    

#------------------------------------------------#
#----------- why need Inheritance? --------------#
#------------------------------------------------#

# Imagine we our item list have many types of phones.
# We want to determine whether the phone is broken or not for selling.
# If we set a new attribute like self.broken_phone in side the Item class,
# it will be applied to all the items, not just phones.

# => Create a new class Phone that inherits from Item

class Phone(Item): # The "Item" inside the parentheses means that Phone is inheriting from Item
    def __init__(self, name: str, price: float, quantity: int, broken_phone: bool=False):
        super().__init__(name, price, quantity)  
        # This links to the __init__ method of Item
        # So that we don't have to set "self.attributes = arguments" again and again
        
        self.broken_phone = broken_phone  # New attribute specific to Phone class


phone1 = Phone("iPhone 14", 1200, 5, broken_phone=True)
phone2 = Phone("Samsung Galaxy S23", 1000, 3)

print(phone1)  # Output: Phone(iPhone 14, 1200, 5, Broken: True)
print(phone2)  # Output: Phone(Samsung Galaxy S23, 1000, 3, Broken: False)
               # Here, __repr__() method is inherited from Item class

print(phone1.broken_phone)  # Output: True

print(phone1.calculate_total_price())  # Output: 6000 (1200 * 5)
                                       # It inherits the method calculate_total_price() from Item

print(Phone.all_items) # Output: [Phone(iPhone 14, 1200, 5), Phone(Samsung Galaxy S23, 1000, 3)]
                       # It also inherits the all_items attribute and the __repr__() method from Item


#----------------------------------------------------------#
#----------- Inheritance from other .py file --------------#
#----------------------------------------------------------#

# We can also import the Item class from another file like item.py and inherit from it

import csv

from item import Item # Make sure file item.py is in the same directory or adjust the import path accordingly

class Fruit(Item):
    def __init__(self, name: str, price: float, quantity: int, is_organic: bool=False):
        super().__init__(name, price, quantity)
        self.is_organic = is_organic  # New attribute specific to Fruit class


fruit1 = Fruit("Apple", 2.5, 10, is_organic=True)
fruit2 = Fruit("Banana", 1.5, 20)

print(fruit1)  # Output: Fruit(Apple, 2.5, 10, Organic: True)
print(fruit2)  # Output: Fruit(Banana, 1.5, 20, Organic: False)

print(fruit1.is_organic)  # Output: True

print(fruit1.calculate_total_price())  # Output: 25.0 (2.5 * 10)

print(Fruit.all_items)  # Output: [Fruit(Apple, 2.5, 10), Fruit(Banana, 1.5, 20)]
                        # It inherits the all_items attribute and the __repr__() method from Item