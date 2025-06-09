#--------------------------------------------#
#-------- __init__ explanation --------------#
#--------------------------------------------#

# __init__() method is a method that forces the definition of specific attributes when created an object from a class
# Those attributes required by __init__() if somehow are not defined will result in unsucessful object creation

class Item:
    def __init__(self, name):
        self.name = name    # define a new attribute 'name' for instance 'self' as 'self.name'
                            # assign the value defined by "name" into attribute "self.name"

item1 = Item("Phone") # "Phone" is passed into as the value of attribute 'self.name'
                      # This is equivalent to "item1.name = 'Phone'" 
                      # An instance is created: Phone

print(item1.name)     # "Phone"

item2 = Item("Laptop")
print(item2.name)     # "Laptop"

# By using __init__, we can assign the values for compulsory attributed via "item = Item(value1, valu2, ...)"
# Instead of:
#             item.attribute1 = value1
#             item.attribute2 = value2


item_no_name = Item()
# => TypeError: Item.__init__() missing 1 required positional argument: 'name'
# => This case raises error because the __init__() require us to define the value for attribute 'name'
#                                                 (but we didn't)



#------------------------------------------------------#
#------------- innit extended example -----------------#
#------------------------------------------------------#

class ItemExtend:
    def __init__(self, name_input, price_input, quantity_input):
        self.name = name_input           # Attribute self.name takes the value of name_input variable
        self.price = price_input         # Attribute self.price takes the value of price_input variable
        self.quantity = quantity_input   # Attribute self.quantity takes the value of quantity_input variable

# class Item:
#     def __init__(self, name, price, quantity):
#         self.name = name
#         self.price = price


item_extend_1 = ItemExtend()