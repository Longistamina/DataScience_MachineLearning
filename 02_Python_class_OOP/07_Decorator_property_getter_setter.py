#----------------------------------------------------------------#
#---------------- @property Decorator: getter -------------------#
#----------------------------------------------------------------#

# Python has a decorator called @property that allows you to define a method as a property (or attribute)
# This means you can access it like an attribute, but it behaves like a method.

class Item:
    def __init__(self, name: str, price: float, quantity: int):
        assert isinstance(name, str), "Name must be a string"
        assert price >= 0, "Price must be greater than zero"
        assert quantity >= 0, "Quantity must be greater than or equal to zero"

        self.name = name          
        self.price = price        
        self.quantity = quantity

    @property # This decorator allows us to define a method as a property
    def total_price(self):
        return self.price * self.quantity

    def __repr__(self):
        return f"Item({self.name}, {self.price}, {self.quantity})"
    
item1 = Item("Laptop", 1500, 3)

print(item1)  # Output: Item(Laptop, 1500, 3)

print(item1.total_price)  # Output: 4500 (1500 * 3)
                          # Accessing total_price like an attribute, but it behaves like a method 
                          # no need for parentheses like item1.total_price() in other files

## ATTENTION: @property is read-only by default
item1.total_price = 5000  # This will raise an "AttributeError: can't set attribute"


#----------------------------------------------------------------#
#---------------- @property Decorator: setter -------------------#
#----------------------------------------------------------------#

# To make a property writable, you can define a setter method using the @property decorator
# and the @<property_name>.setter decorator.

class ItemWithSetter:
    def __init__(self, name: str, price: float, quantity: int):
        assert isinstance(name, str), "Name must be a string"
        assert price >= 0, "Price must be greater than zero"
        assert quantity >= 0, "Quantity must be greater than or equal to zero"

        self.name = name          
        self.price = price        
        self.quantity = quantity
        
        self._total_price = self.price * self.quantity
        # We set the name of the attribute as _total_price (internal use)
        # This will avoid the overlap name with total_price method below (as a property)
        # And avoid RecursionError when we call "obj.total_price"
    
    def __repr__(self):
        return f"ItemWithSetter({self.name}, {self.price}, {self.quantity})"

    @property
    def total_price(self):
        return self._total_price

    @total_price.setter # This setter allows you to modify the total price directly
    def total_price(self, value):
        print("You are trying to set the new total price")
        self._total_price = value
        # do not need to return a value from a property setter in Python 
        # because setter methods are only meant to set the value, not to return anything.
    
       

item2 = ItemWithSetter("Phone", 1000, 5)
print(item2.total_price)  # Output: 5000 (1000 * 5)

# Now we can set the total price directly
item2.total_price = 6000  # Print out "You are trying to set the new total price"
                          # This will set the total price to 6000
                          # Raise no error because we defined a setter method

print(item2.total_price)  # Output: 6000

## WARNING: though the _total_price changed, the price and quantity remain unchanged
'''
#--------------------------------------#

# Python also has many other built-in decorators like @staticmethod, @classmethod, etc.
# Explore yourself to learn more about them and enjoy Python OOP!

#--------------------------------------#
'''