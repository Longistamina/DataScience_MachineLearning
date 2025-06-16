#--------------------------#
#------ for loop ----------#
#--------------------------#

for i in range(1, 20):
    if i%2 != 0: 
        print(i)

#### for zip

lst_name = ["Socrates", "Plato", "Aristotle"]
lst_age = [80, 57, 35]

for name, age in zip(lst_name, lst_age):
    print(f'{name}: {age} years old')


#--------------------------#
#------ for Nest ----------#
#--------------------------#

######## apply for Nest to create multiplication table #########

print('-'*116)
print('Multiplication table - Method 1'.center(116))
print('-'*116)

mult_table = ''

for n in range(1,11,1):
    for i in range (2,10,1):
        mult_table += f'{i:2} x {n:2} = {i*n:2}   ' # {i:2} means the space range of this character is 2
    mult_table +='\n'
print(mult_table)

print('-'*116)
print('Multiplication table - Method 2'.center(116))
print('-'*116)

for n in range(1,11,1):
    for i in range (2,10,1):
        print(f'{i:2} x {n:2} = {i*n:2}',end='   ') # {i:2} means the space range of this character is 2
    print()
    