# chr() return the character corresponding to a given index in ASCII
# ord() return the index corresponding to a given character in ASCII
# ASCII code tabel: https://www.ascii-code.com/

chr(97) # 'a'
chr(65) # 'A'

ord('A') # 65
ord('a') # 97

chr(178) # square sign: ²

print('X'+chr(178)) # X²
print(f'X{chr(178)}') # X²

quadratic_equation = f"aX{chr(178)} + bX + c = 0" # quadratic equation = phương trình bậc 2
print(quadratic_equation) # aX² + bX + c = 0


################################################################
## Create a quadratic equation string using input() and chr() ##
################################################################

a = eval(input('Input coefficient  A: '))
b = eval(input('Input coefficient  B: '))
c = eval(input('Input coefficient  C: '))

quadratic_equation = f'{a}X{chr(178)} + {b}X +{c} = 0'
print(quadratic_equation)
