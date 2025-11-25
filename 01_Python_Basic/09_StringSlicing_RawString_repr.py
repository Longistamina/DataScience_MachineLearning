#-----------------------------------------------------------------------------------------------------#
#------------------------------------------ String slicing -------------------------------------------#
#-----------------------------------------------------------------------------------------------------#

name = "Le Anh Thu"
l = len(name)

first_element = name[0] # L
fourth_element = name[3] # A

last_element = name[-1] # u
name[l-1] # u
name[-2] # h
name[-3] # T

'''
Explanation of negative indexing (reverse indexing):

name[-3] = "T"
name[7] = "T"

=> So actually, name[-3] = name[10-3] = name[7] (10 is the length of the string "Le Anh Thu")
'''

##########################

''' Python considers 0 as the index of the first element of an iterator '''

family_name = name[0:2] # stop at element of index 2, but not include it 
family_name = name[:2]

middle_name = name[3:6]

given_name = name[7:]

given_name = name[-3:] # from the third last element to the end

name[-1:-4:-1] # "uhT" (exclude the -4)
               # The last -1 after the second ":" means slicing in reverse steps from right to left (with step = 1)
               # negative sign "-" means reverse indexing
               # -1 is "u"
               # -2 is "h"
               # -3 is "T"
               # -4 is " " but excluded
               #==> name[-1:-4:-1] returns "uhT"

name[-1:-4:-2] # uT
               # The reverse steps are -2, so "h" is now bypassed

name[-1:-4] # '' or ""
            # It returns empty string because by defaut, the step = 1 (read from left to right)
            # The -1 is already the last character, and there is nothing on its left => ''

print(name[-4:-1]) # " Th"
            # Index from right to left
            # -4 is " "
            # -3 is "T"
            # -2 is "h"
            # -1 is "u" but excluded
            #==> name[-4:-1] is " Th"

strNumbers = "123456789"
strOdd = strNumbers[0::2] # slice from start to end, but with index step = 2, return "13579"
strEven = strNumbers[1::2]  # slice from the second element to end, but with index step = 2, return "2468"

print("-" * 50) # print character '-' 50 times


#---------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- repr() function -----------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------#

###################
## Normal string ##
###################

normal_string = "Hello\nWorld"  # Normal string with escape sequences

print(normal_string)  
# Output: Hello
#         World

################
## Raw string ##
################

# raw strings are prefixed wi Python considers 0 as the index of the first element of an iterator

raw_string = r"Hello\nWorld"  # Raw string, no escape sequences

print(raw_string)  
# Output: Hello\nWorld

#####################
## repr() function ##
#####################

# repr() returns a string representation of an object that can be used to recreate the object.
# (e.g a raw string)
# It is often used for debugging purposes, as it provides a more detailed and unambiguous representation of the object.

normal_string = "This is\n the end\n"
print(normal_string)
# Output: This is
#         the end

print(repr(normal_string))
# Output: 'This is\n the end\n'
