# All basic datatypes in Python: https://www.w3schools.com/python/python_datatypes.asp
# Python numbers: int, float, complex -> https://www.w3schools.com/python/python_numbers.asp

# Casting is the act of converting a variable's original datatype into another one
# Casting reference link: https://www.w3schools.com/python/python_casting.asp

## int() to convert into integer number
x = int(1)    # x will be 1
y = int(2.8)  # y will be 2
z = int("3")  # z will be 3
u = int("-4") # u will be -4

## float() to convert into float number
x = float(1)      # x will be 1.0
y = float(2.8)    # y will be 2.8
z = float("3")    # z will be 3.0
w = float("4.2")  # w will be 4.2
u = float(".2")   # u will be 0.2
v = float("-.51") # v will be -0.51

## complex() to convert into complex number
x = complex(1)        # x will be (1+0j)
y = complex("3+5j")   # y will be (3+5j)
z = complex(4 + 6.8j) # z will be (4+6.8j)

## str() to convert into string
x = str("s1") # x will be 's1'
y = str(2)    # y will be '2'
z = str(3.0)  # z will be '3.0'


#-----------------------------------------------------------------------------------------------------------------#
#------------------------------------ Exception with "infinity" and "inf" ----------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#

##########################
## float() and infinity ##
##########################

float("infinity") # inf
float("+infinity") # inf
float("-infinity") # -inf

float("inf") # inf
float("+inf") # inf
float("-inf") # -inf

float("inf") == float("+infinity") # True

############################
## complex() and infinity ##
############################

#--------
## real part
#--------

complex("infinity+2j") # (inf+2j)
complex("+infinity+2j") # (inf+2j)
complex("-infinity+2j") # (-inf+2j)

complex("inf+2j") # (inf+2j)
complex("+inf+2j") # (inf+2j)
complex("-inf+2j") # (-inf+2j)


#--------
## image part
#--------

complex("3+infinityj") # (3+infj)
complex("3-infinityj") # (3-infj)

complex("3+infj") # (3+infj)
complex("3-infj") # (3-infj)


#-----------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------- isinstance() -------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#
'''
isinstance checks whether an object is an instance of a given class (or any of several classes), 
returning True or False. 

It also considers inheritance, so subclasses count as instances of their parent classes.

isinstance(obj, classinfo).

(classinfo can be a single class/type or a tuple of classes/types.)
'''

print(isinstance(5, int)) # True

print(isinstance(5.0, float)) # True

print(isinstance(5, (int, float, complex))) # True, because 5 is an instance of int, which is in the tuple

print(isinstance("hello", str)) # True

print(isinstance(3+4j, complex)) # True

print(isinstance([1, 2, 3], list)) # True

print(isinstance("1.2", (int, float))) # False, because "1.2" is a string, not an int or float

demo_str = "Hello, World!"
print(isinstance(demo_str, str)) # True

demo_cpx = 3 + 4j
print(isinstance(demo_cpx, complex)) # True
print(isinstance(demo_cpx, (int, float))) # False, because demo_cpx is not an int or float