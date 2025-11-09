#---------------------------------------------------------------------------------------#
#---------------------------------------- input() --------------------------------------#
#---------------------------------------------------------------------------------------#

# When use input to define a variable, the returned datatype will always be "str"

x = int(input("Input variable x: "))
y = int(input("Input variable y: "))

print("Sum x + y =", x+y)
print("Subtract x - y =", x-y)
print("Multiplication x*y = ", x*y)
print("Division x/y =", x/y)


#--------------------------------------------------------------------------------------#
#---------------------------------------- eval() --------------------------------------#
#--------------------------------------------------------------------------------------#

k1 = eval('2+3+5') # eval considers this as a mathematic expression, hence returns 10 as the result of 2+3+5
print(f'''
k1 = {k1}
type_k1 = {type(k1)}
\n''')

k2 = eval('25') # eval considers this as an integer, hence returns 25 as integer
print(f'''
k2 = {k2}
type_k2 = {type(k2)}
\n''')

k3 = eval('1.75') # eval considers this as a real number, hence returns 1.75 as float
print(f'''
k3 = {k3}
type_k3 = {type(k3)}
\n''')

k4 = eval('20,23,45') # eval considers this as a tuple, hence returns (20, 23, 45) as a tuple
print(f'''
k4 = {k4}
type_k4 = {type(k4)}
\n''')

k5 = eval('[12,13,14,15]') # eval considers this as a list, hence returns [12, 13, 14, 15] as list
print(f'''
k5 = {k5}
type_k5 = {type(k5)}
\n''')

abc = 9.5
k = eval('abc') # In this case, eval() will use pre-defined variable abc to evaluate variable k
print(f'''
k = abc = {k}
type_k = type_abc = {type(k)}
\n''')

k = eval('xyz') # Raise error because eval considers this abc as an undefined variable 


#----------------------------------------------------------------------------------------------------------#
#---------------------------------------- combine input() and eval() --------------------------------------#
#----------------------------------------------------------------------------------------------------------#

radius = eval(input("Input radius of a circle: "))

print(f"Area of the circle = {3.14 * (radius**2)}")
