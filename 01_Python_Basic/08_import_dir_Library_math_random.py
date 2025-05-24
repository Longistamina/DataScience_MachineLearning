#--------------------------------------------------------#
#------------------- math Library -----------------------#
#--------------------------------------------------------#

import math
a = math.sqrt(16) #--> a = 4
b = math.pow(2,3) #--> b = 2**3 = 8
math.pi #---> pi number

print(dir(math)) #---> list out all the functions, methods and attributes of an object

#math.floor(x) => Return the smallest and nearest integer number of x, math.floor(5.25) returns 5

#math.modf(x) => Separate and returns the decimal and the quotient of a float number, modf(7.5) => (0.5,7.0)
decimal, quotient = math.modf(3.5)
print(decimal)
print(quotient)

#----------------------------------------------------------#
#------------------- random Library -----------------------#
#----------------------------------------------------------#
import random

n1 = random.random() #Generate a random float number in range of [0,1)
print(n1)

n2 = random.uniform(10,20) #Generate a random float number x where 10 =< x < 20
print(n2)

n3 = random.randrange(10,20,1) #Returns a randomly selected element from the specified range (start = 10, stop = 20, step = 1).
print(n3)

n4 = random.randint(10,20) #Generate a random integer number in range of [10,20]
print(n4)
