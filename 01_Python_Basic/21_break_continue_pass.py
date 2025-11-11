#----------------------------#
#--------- break ------------#
#----------------------------#

for i in range(10):
    print('------------')
    if i == 5:
        print("Let's break!\n")
        break  # Exit the loop when i equals 5
    print(str(i).center(12))

# Output: 0 1 2 3 4


#-------------------------------#
#--------- continue ------------#
#-------------------------------#

for i in range(10):
    print('---------------')
    if i % 2 == 0:
        print("Let's continue!")
        continue  # Skip even numbers
    print(str(i).center(15))

# Output: 1 3 5 7 9


#---------------------------#
#--------- pass ------------#
#---------------------------#

for i in range(5):
    print('-----------')
    if i == 3:
        print("Let's pass!")
        pass  # Do nothing when i is 3
        print("Let's pass!")
    print(str(i).center(12))

# Output: 0 1 2 Let's pass! 3 Let's pass! 4
