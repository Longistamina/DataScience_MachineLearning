# Move to the directory containing the rectangle_module.py
import os
os.chdir("/home/longdpt/Documents/Academic/DataScience_MachineLearning/02_Python_class_OOP/rectangle_project")

# Import the RectangleCalculator class from the rectangle_module.py
from rectangle_module import RectangleCalculator


#-----------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------- [RECOMMENDED] Canon way to use an imported class ----------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------#

# Initialize an object belonging to the RectangleCalculator module with given attributes (length and width)
rectangle = RectangleCalculator(length=355, width=263)

# Display information
print(rectangle.length) # 355
print(rectangle.width) # 263
print(rectangle.perimeter) # 1236.0
print(rectangle.area) # 93365.0

print(rectangle.summary())
# Result of the nameless rectangle:
# ++ Length = 355
# ++ Width = 263
# ++ Perimeter = 2 * (355 + 263) = 1236.0
# ++ Area = 355 * 263 = 93365.0


######################################################################
## Change the attributes (length and width) of the rectangle object ##
## which will automatically update the perimeter and area as well   ##
######################################################################

rectangle.length = 55
rectangle.width = 23

print(rectangle.perimeter) # 156.0
print(rectangle.area) # 1265.0

print(rectangle.summary())
# Result of the nameless rectangle:
# ++ Length = 55
# ++ Width = 23
# ++ Perimeter = 2 * (55 + 23) = 156.0
# ++ Area = 55 * 23 = 1265.0


###################################################################
## Try to change rectangle.perimeter and rectangle.area directly ##
###################################################################

from loguru import logger

try:
    rectangle.perimeter = 33
except Exception as e:
    logger.error(e) 
    # | ERROR    | __main__:<module>:5 - property 'perimeter' of 'RectangleCalculator' object has no setter

try:
    rectangle.area = 260
except Exception as e:
    logger.error(e) 
    # | ERROR    | __main__:<module>:4 - property 'area' of 'RectangleCalculator' object has no setter

'''
Here, the codes return errors because the perimeter and area are properties of the RectangleCalculator class,
(a method that is defined with the @property decorator, works like an attribute but is actually a method).

The true corresponding attributes are self.__perimeter and self.__area, which are private attributes of the class.
So, they cannot be accessed directly from outside the class.

This will prevent users from changing the perimeter and area directly, keep the integrity of the class, 
and ensure that the perimeter and area are always calculated based on the length and width.
'''


###############################################################################################
## (NOT RECOMMENDED) Access the private attributes self.__perimeter and self.__area directly ##
###############################################################################################

rectangle = RectangleCalculator(length=355, width=263)

old_perimeter = rectangle.perimeter
old_area = rectangle.area

rectangle._RectangleCalculator__perimeter = 289
rectangle._RectangleCalculator__area = 600

print(f"Length: {rectangle.length}") # 355
print(f"Width: {rectangle.width}") # 263

print(f"Old perimeter: {old_perimeter}") # 1236.0
print(f"New perimeter: {rectangle._RectangleCalculator__perimeter}") # 289.0

print(f"Old area: {old_area}") # 93365.0
print(f"New area: {rectangle._RectangleCalculator__area}") # 600.0

'''
This is NOT recommended because it breaks the encapsulation principle of OOP.

The new perimeter and area values are not calculated based on the length and width anymore.
Instead, they are set directly, which can lead to inconsistencies and non-integrity.
'''


#-------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------- non-canon way to use an imported class ----------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------#

############################################################################
## Initialize an empty object belonging to the RectangleCalculator module ##
############################################################################

rectangle = RectangleCalculator() # No attributes are defined

print(rectangle.length) # None
print(rectangle.width) # None

print(rectangle.perimeter) # None
print(rectangle.area) # None

print(rectangle.summary())
# | CRITICAL | rectangle_module:summary:234 - NO valid inputs were given! They are expected to be POSITIVE NUMBERS (greater than zero)


####################################################
## Update attributes (self.length and self.width) ##
####################################################

rectangle.length = 33
rectangle.width = 25.5

print(rectangle.length) # 33
print(rectangle.width) # 25.5

print(rectangle.perimeter) # None
print(rectangle.area) # None

print(rectangle.summary())
# Result of the nameless rectangle:
# ++ Length = 33
# ++ Width = 25.5
# ++ Perimeter = 2 * (33 + 25.5) = 117.0
# ++ Area = 33 * 25.5 = 841.5

#---------------------------------------------------------------------------------------------------------------------------#
#--------------------------- Display everything of the RectangleCalculator (attributes and methods) ------------------------#
#---------------------------------------------------------------------------------------------------------------------------#

for info in dir(RectangleCalculator):
    print(info)

# _RectangleCalculator__load_rectangle_inputs
# _RectangleCalculator__save_output_file
# _RectangleCalculator__valiate_input_number
# _RectangleCalculator__validate_output_directory
# _RectangleCalculator__validate_output_file
# __class__
# __delattr__
# __dict__
# __dir__
# __doc__
# __eq__
# __format__
# __ge__
# __getattribute__
# __getstate__
# __gt__
# __hash__
# __init__
# __init_subclass__
# __le__
# __lt__
# __module__
# __ne__
# __new__
# __reduce__
# __reduce_ex__
# __repr__
# __setattr__
# __sizeof__
# __str__
# __subclasshook__
# __weakref__
# _display_saving_single_output_message
# _single_workflow
# area
# perimeter
# summary


#---------------------------------------------------------------------------------------------------------------------------#
#-------------- Display everything of the rectangle object from RectangleCalculator (attributes and methods) ---------------#
#---------------------------------------------------------------------------------------------------------------------------#

rectangle = RectangleCalculator()

for info in dir(rectangle):
    print(info)
# _RectangleCalculator__length
# _RectangleCalculator__load_rectangle_inputs
# _RectangleCalculator__save_output_file
# _RectangleCalculator__valiate_input_number
# _RectangleCalculator__validate_output_directory
# _RectangleCalculator__validate_output_file
# _RectangleCalculator__width
# __class__
# __delattr__
# __dict__
# __dir__
# __doc__
# __eq__
# __format__
# __ge__
# __getattribute__
# __getstate__
# __gt__
# __hash__
# __init__
# __init_subclass__
# __le__
# __lt__
# __module__
# __ne__
# __new__
# __reduce__
# __reduce_ex__
# __repr__
# __setattr__
# __sizeof__
# __str__
# __subclasshook__
# __weakref__
# _cores
# _display_saving_single_output_message
# _input
# _json_count
# _output
# _single_output_path
# _single_workflow
# area
# length
# perimeter
# summary
# width