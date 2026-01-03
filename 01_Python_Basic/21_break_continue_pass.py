import time

#----------------------------#
#--------- break ------------#
#----------------------------#

for i in range(10):
    print('------------')
    if i == 5:
        print("Let's break!\n")
        break  # Exit the loop when i equals 5
    print(str(i).center(12))
    time.sleep(0.5)


# Output: 0 1 2 3 4

###########################
## break in nested loops ##
###########################

for i in range(10):
    print('================')
    print("i:", i)
    for j in range(5):
        if j == 3:
            break
        print("j", j)
# Only breaks the inner loop, does not affect the outer loop


#-------------------------------#
#--------- continue ------------#
#-------------------------------#

for i in range(10):
    print('---------------')
    if i % 2 == 0:
        print("Let's continue!")
        time.sleep(0.5)
        continue  # Skip even numbers
        print(str(i).center(15)) # This line will not be executed
        
    print(str(i).center(15))
    time.sleep(0.5)

# Output: 1 3 5 7 9


#---------------------------#
#--------- pass ------------#
#---------------------------#

for i in range(5):
    print('-----------')
    if i == 3:
        print("Let's pass!")
        time.sleep(0.5)
        pass  # Do nothing when i is 3
        print("Let's pass!") # Still executes this line
    
    print(str(i).center(12))
    time.sleep(0.5)

# Output: 0 1 2 Let's pass! 3 Let's pass! 4

'''
"pass" can work as a placeholder for future code.
'''

if 2 > 1:
    pass  # Placeholder for future code

