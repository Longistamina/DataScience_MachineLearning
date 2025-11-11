#-----------------------------#
#----------- if --------------#
#-----------------------------#

score = float(input("Input a score: "))

if score >= 5.0:
    print("Pass")

if score >= 5.0: print("Pass")

if (score >= 5.0) and (score >= 8.0):
    print("Good")

if not (score >= 5.0):
    print("Fail")

#----------------------------------#
#----------- if else --------------#
#----------------------------------#

score = float(input("Input a score: "))

if score >= 5.0:
    print("Pass")
else:
    print("Fail")


#---------------------------------------#
#----------- if elif else --------------#
#---------------------------------------#

score = float(input("Input a score: "))

if score >= 9.0:
    print("Excellent")
elif score >= 8.0:
    print("Very good")
elif score >= 6.5:
    print("Good")
elif score >= 5.0:
    print("Average")
else:
    print("Fail")


############## WRONG LOGIC CASE ################

score = float(input("Input a score: "))

if score >= 5.0:
    print("Average")
elif score >= 6.5:
    print("Good")
elif score >= 8.0:
    print("Very good")
elif score >= 9.0:
    print("Execellent")
else:
    print("Fail")

# Input 9.5 => Output "Average", not "Execellent"

############## WRONG LOGIC CASE ################


#-----------------------------#
#---------- if nest ----------#
#-----------------------------#

number = int(input("Input an integer number: "))

if number > 0:
    print("The number is positive.")
    
    if number % 2 == 0:
        print("It is even.")
    else:
        print("It is odd.")
        
else:
    print("The number is not positive.")
