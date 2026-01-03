#-------------------------------------------------------------#
#------------------------ while loop -------------------------#
#-------------------------------------------------------------#

n = 1
while n <= 10:
    print(n, end=', ')
    n += 1
print('END')

##### while True ####

i = 1
while True:
    print(i)
    i += 1
    if i > 5:
        break


#-------------------------------------------------------------#
#------------------------ while Nest -------------------------#
#-------------------------------------------------------------#

## apply while Nest to create multiplication table

print()
print('-' * 131)
print(' ' * 50, 'Multiplication table - while loop', ' '*60)
print('-' * 131)

i = 1
mult_table = ''
while i <= 10:
    n = 1
    while n <= 9:
        mult_table += f'{n:2} x {i:2} = {n*i:2}   ' # {i:2} means the space range of this character is 2
        n += 1
    i += 1
    mult_table +='\n'
    
print(mult_table)