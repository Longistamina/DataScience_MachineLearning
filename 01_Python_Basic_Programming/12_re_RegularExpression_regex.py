# Reference link: https://www.w3schools.com/python/python_regex.asp

# A RegEx, or Regular Expression, is a sequence of characters that forms a search pattern.
# RegEx can be used to check if a string contains the specified search pattern.

# Python has a built-in package called re, which can be used to work with Regular Expressions.

import re

re.findall()  #Returns a list containing all matches
re.search()   #Returns a Match object if there is a match anywhere in the string
re.split()    #Returns a list where the string has been split at each match
re.sub()      #Replaces one or many matches with a string

#----------------------------------------------------------------------#
#------------------------------- Example ------------------------------#
#----------------------------------------------------------------------#
import re

txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)

if x:
  print("YES! We have a match!")
else:
  print("No match")

#------------------------------------------------------------------------------------------#
#-------------------------- "[]" ~ A set of characters ------------------------------------#
#------------------------------------------------------------------------------------------#
import re

txt = "The rain in Spain"

x = re.findall("[a-m]", txt) #Find all lower case characters alphabetically between "a" and "m":
print(x) #['h', 'e', 'a', 'i', 'i', 'a', 'i']

# [arn]	Returns a match where one of the specified characters (a, r, or n) is present	
# [a-n]	Returns a match for any lower case character, alphabetically between a and n	
# [^arn]	Returns a match for any character EXCEPT a, r, and n	
# [0123]	Returns a match where any of the specified digits (0, 1, 2, or 3) are present	
# [0-9]	Returns a match for any digit between 0 and 9	
# [0-5][0-9]	Returns a match for any two-digit numbers from 00 and 59	
# [a-zA-Z]	Returns a match for any character alphabetically between a and z, lower case OR upper case	
# [+]	In sets, +, *, ., |, (), $,{} has no special meaning, so [+] means: return a match for any + character in the string


#------------------------------------------------------------------------------------------------------------------------------#
#-------------------------- "\" ~ Signals a special sequence, or escapes special character ------------------------------------#
#------------------------------------------------------------------------------------------------------------------------------#
import re

txt = "That will be 59 dollars"

x = re.findall("\d", txt) #Find all digit characters:
print(x) #['5', '9']


# Special characters:
## \A	Returns a match if the specified characters are at the beginning of the string =>	"\AThe"	

## \b	Returns a match where the specified characters are at the beginning or at the end of a word => r"\bain"; r"ain\b"
## (the "r" in the beginning is making sure that the string is being treated as a "raw string")	

## \B	Returns a match where the specified characters are present, but NOT at the beginning (or at the end) of a word => r"ain\B"; r"\Bain"
## (the "r" in the beginning is making sure that the string is being treated as a "raw string")	


## \d	Returns a match where the string contains digits (numbers from 0-9)	"\d"	
## \D	Returns a match where the string DOES NOT contain digits	"\D"	

## \s	Returns a match where the string contains a white space character	"\s"	
## \S	Returns a match where the string DOES NOT contain a white space character	"\S"	

## \w	Returns a match where the string contains any word characters (characters from a to Z, digits from 0-9, and the underscore _ character)	"\w"	
## \W	Returns a match where the string DOES NOT contain any word characters	"\W"	

## \Z	Returns a match if the specified characters are at the end of the string	"Spain\Z"


#--------------------------------------------------------------------------------------------------------------#
#-------------------------- "." ~ Any character (except newline character) ------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
import re
txt = "hello planet"

x = re.findall("he..o", txt) #Search for a sequence that starts with "he", followed by two (any) characters, and an "o":
print(x) #['hello']

#---------------------------------------------------------------------------------#
#-------------------------- "^" ~ Starts with ------------------------------------#
#---------------------------------------------------------------------------------#
import re
txt = "hello planet"

x = re.findall("^hello", txt) #Check if the string starts with 'hello':
if x:
  print("Yes, the string starts with 'hello'")
else:
  print("No match")

#Output: Yes, the string starts with 'hello'

#-------------------------------------------------------------------------------#
#-------------------------- "$" ~ Ends with ------------------------------------#
#-------------------------------------------------------------------------------#
import re
txt = "hello planet"

x = re.findall("planet$", txt) #Check if the string ends with 'planet':
if x:
  print("Yes, the string ends with 'planet'")
else:
  print("No match")

#Output: Yes, the string ends with 'planet'

#----------------------------------------------------------------------------------------------#
#-------------------------- "*" ~ Zero or more occurrences ------------------------------------#
#----------------------------------------------------------------------------------------------#
import re
txt = "hello planet"

x = re.findall("he.*o", txt) #Search for a sequence that starts with "he", followed by 0 or more  (any) characters, and an "o":
print(x) #['hello']

#---------------------------------------------------------------------------------------------#
#-------------------------- "*" ~ One or more occurrences ------------------------------------#
#---------------------------------------------------------------------------------------------#
import re
txt = "hello planet"

x = re.findall("he.+o", txt) #Search for a sequence that starts with "he", followed by 1 or more  (any) characters, and an "o":
print(x)#['hello']

#---------------------------------------------------------------------------------------------#
#-------------------------- "?" ~ Zero or one occurrences ------------------------------------#
#---------------------------------------------------------------------------------------------#
import re
txt = "hello planet"

x = re.findall("he.?o", txt) #Search for a sequence that starts with "he", followed by 0 or 1  (any) character, and an "o":
print(x) #[]
         #This time we got no match, because there were not zero, not one, but two characters between "he" and the "o"

#------------------------------------------------------------------------------------------------------------------#
#-------------------------- "{}" ~ Exactly the specified number of occurrences ------------------------------------#
#------------------------------------------------------------------------------------------------------------------#
import re
txt = "hello helllo planet"

x = re.findall("he.{2}o", txt) #Search for a sequence that starts with "he", followed excactly 2 (any) characters, and an "o":
print(x) #['hello']
         #Not return 'helllo' cause 'helllo' has 3 characters between "he" and "o"

#-------------------------------------------------------------------------------#
#-------------------------- "|" ~ Either or ------------------------------------#
#-------------------------------------------------------------------------------#
import re
txt = "The rain in Spain falls mainly in the plain!"

x = re.findall("falls|stays", txt) #Check if the string contains either "falls" or "stays":
print(x) #['falls']

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#Output: Yes, there is at least one match!


#----------------------------------------------------------------------------#
#-------------------------- re.findall() ------------------------------------#
#----------------------------------------------------------------------------#
# The findall() function returns a list containing all matches.

import re
txt = "The rain in Spain"

x = re.findall("ai", txt) #Return a list containing every occurrence of "ai":
print(x) #['ai', 'ai']

x = re.findall("Portugal", txt)
print(x) #[]

#---------------------------------------------------------------------------#
#-------------------------- re.search() ------------------------------------#
#---------------------------------------------------------------------------#
# The search() function searches the string for a match, and returns a Match object if there is a match.

import re
txt = "The rain in Spain"

x = re.search("\s", txt)
print("The first white-space character is located in position:", x.start()) #Return 3

x = re.search("Portugal", txt)
print(x) #Return None

#--------------------------------------------------------------------------#
#-------------------------- re.split() ------------------------------------#
#--------------------------------------------------------------------------#
# The split() function returns a list where the string has been split at each match:

import re
txt = "The rain in Spain"

x = re.split("\s", txt)
print(x) #['The', 'rain', 'in', 'Spain']

x = re.split("\s", txt, 1) #Split the string only at the first occurrence
print(x) #['The', 'rain in Spain']

#------------------------------------------------------------------------#
#-------------------------- re.sub() ------------------------------------#
#------------------------------------------------------------------------#
# The sub() function replaces the matches with the text of your choice:

import re
txt = "The rain in Spain"

x = re.sub("\s", "_", txt) #Replace all white-space characters with the "_" character:
print(x) #The_rain_in_Spain

x = re.sub("\s", "_", txt, 2) #Replace only the first 2 occurrences:
print(x) #The_rain_in Spain

#------------------------------------------------------------------------#
#-------------------------- Match Object---------------------------------#
#------------------------------------------------------------------------#
# A Match Object is an object containing information about the search and the result.
# Note: If there is no match, the value None will be returned, instead of the Match Object.

import re
txt = "The rain in Spain"

x = re.search("ai", txt)
print(x) #this will print an object
         # <_sre.SRE_Match object; span=(5, 7), match='ai'>

x = re.search(r"\bS\w+", txt) #Search for an upper case "S" character in the beginning of a word, and print the word:

print(x.span()) #Return a tuple containing the start, and end positions of the match
                #Here return (12,17) means the match starts at 12, ends at 17

print(x.string) #Returns the string passed into the function
                #Here return "The rain in Spain"

print(x.group()) #Returns the part of the string where there was a match
                 #Here return "Spain"