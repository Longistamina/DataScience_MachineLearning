# Reference link: https://www.w3schools.com/python/python_regex.asp

# A RegEx, or Regular Expression, is a sequence of characters that forms a search pattern.
# RegEx can be used to check if a string contains the specified search pattern.

# Python has a built-in package called re, which can be used to work with Regular Expressions.

'''
1. Example
2. "[]" = A set of characters
3. "\" = Signals a special sequence, or escapes special character
4. "." = Any character (except newline character)
5. "^" = Starts with
6. "$" = Ends with
7. "*" = Zero or more occurrences
8. "+" = One or more occurrences
9. "?" = Zero or one occurrences
10. "{}" = Exactly the specified number of occurrences
11. "|" = Either or
12. () group capturing
13. (?:) non-group capturing
14. re.match(): Determines if the RE matches at the beginning of the string
15. re.findall(): Returns a list containing all matches
16. re.search(): Returns a Match object if there is a match anywhere in the string
17. re.split(): Returns a list where the string has been split at each match
18. re.sub(): Replaces one or many matches with a string
19. Match Object
'''


#-------------------------------------------------------------------------#
#------------------------------- 1. Example ------------------------------#
#-------------------------------------------------------------------------#

import re

txt = "The rain in Spain"
x = re.match("^The.*Spain$", txt)

if x:
  print("YES! We have a match!")
else:
  print("No match")


#---------------------------------------------------------------------------------------------#
#-------------------------- 2. "[]" = A set of characters ------------------------------------#
#---------------------------------------------------------------------------------------------#

import re

txt = "The rain in Spain"

x = re.findall("[a-m]", txt) # Find all lower case characters alphabetically between "a" and "m":
print(x) # ['h', 'e', 'a', 'i', 'i', 'a', 'i']


'''
# [arn]	Returns a match where one of the specified characters (a, r, or n) is present	
# [a-n]	Returns a match for any lower case character, alphabetically between a and n	
# [^arn]	Returns a match for any character EXCEPT a, r, and n	
# [0123]	Returns a match where any of the specified digits (0, 1, 2, or 3) are present	
# [0-9]	Returns a match for any digit between 0 and 9	
# [0-5][0-9]	Returns a match for any two-digit numbers from 00 and 59	
# [a-zA-Z]	Returns a match for any character alphabetically between a and z, lower case OR upper case	
# [+]	In sets, +, *, ., |, (), $,{} has no special meaning, so [+] means: return a match for any + character in the string
'''


#-------------------------------------------------------------------------------------------------------------------------------#
#-------------------------- 3. "\" = Signals a special sequence, or escapes special character ----------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------#

import re

txt = "That will be 59 dollars"

x = re.findall("\d", txt) # Find all digit characters:
print(x) # ['5', '9']

'''
                                       SPECIAL CHARACTERS with \

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
'''



#--------------------------------------------------------------------------------------------------------------#
#-------------------------- 4. "." = Any character (except newline character) ---------------------------------#
#--------------------------------------------------------------------------------------------------------------#

import re

txt = "hello planet"

x = re.findall("he..o", txt) # Search for a sequence that starts with "he", followed by two (any) characters, and an "o":
print(x) # ['hello']


#---------------------------------------------------------------------------------#
#-------------------------- 5. "^" = Starts with ---------------------------------#
#---------------------------------------------------------------------------------#

import re

txt = "hello planet"

x = re.findall("^hello", txt) # Check if the string starts with 'hello':
if x:
  print("Yes, the string starts with 'hello'")
else:
  print("No match")

# Output: Yes, the string starts with 'hello'


#------------------------------------------------------------------------------------------------#
#---------------------------------- 6. "$" = Ends with ------------------------------------------#
#------------------------------------------------------------------------------------------------#

import re

txt = "hello planet"

x = re.findall("planet$", txt) #Check if the string ends with 'planet':
if x:
  print("Yes, the string ends with 'planet'")
else:
  print("No match")

#Output: Yes, the string ends with 'planet'


#----------------------------------------------------------------------------------------------#
#-------------------------- 7. "*" = Zero or more occurrences ---------------------------------#
#----------------------------------------------------------------------------------------------#

import re

text = "a aa aaa aaaa b bb bbb"

# 1. Using * (zero or more)
# Matches 'a' followed by zero or more 'a' characters

pattern1 = r"a*"
matches1 = re.findall(pattern1, text)
print("With * (zero or more):", matches1)  # Output: ['a', 'aa', 'aaa', 'aaaa', '', 'b', 'bb', 'bbb', '']
                                           # Output has two '' characters (meaning match "no a")
                                           # One '' is for the space character ' ' (has no "a")
                                           # Other '' is for the empty character '' (also has no "a")


#---------------------------------------------------------------------------------------------#
#-------------------------- 8. "+" = One or more occurrences ---------------------------------#
#---------------------------------------------------------------------------------------------#

import re

text = "a aa aaa aaaa b bb bbb"

# 2. Using + (one or more)
# Matches 'a' followed by one or more 'a' characters

pattern2 = r"a+"
matches2 = re.findall(pattern2, text)
print("With + (one or more):", matches2)  # Output: ['a', 'aa', 'aaa', 'aaaa']

#---------------------------------------------------------------------------------------------#
#-------------------------- 9. "?" = Zero or one occurrences ---------------------------------#
#---------------------------------------------------------------------------------------------#
import re
text = "a aa aaa aaaa b bb bbb"

# 3. Using ? (zero or one)
# Matches 'a' followed by zero or one 'a' character

pattern3 = r"a?"
matches3 = re.findall(pattern3, text)
print("With + (one or more):", matches3) 
# Output: ['a', '', 'a', 'a', '', 'a', 'a', 'a', '', 'a', 'a', 'a', 'a', '', '', '', '', '', '', '', '', '', '']


#------------------------------------------------------------------------------------------------------------------#
#-------------------------- 10. "{}" = Exactly the specified number of occurrences --------------------------------#
#------------------------------------------------------------------------------------------------------------------#

import re
txt = "hello helllo planet"

x = re.findall("he.{2}o", txt) # Search for a sequence that starts with "he", followed excactly 2 (any) characters, and an "o":
print(x) # ['hello']
         # Not return 'helllo' cause 'helllo' has 3 characters between "he" and "o"

#########

text = "1234 56 7 89012"
pattern = r"\d{1,3}" # {1,3} quantifier meaning at least 1 digit and at most 3 digits
matches = re.findall(pattern, text)
print(matches) # Output: ['123', '4', '56', '7', '890', '12']


#-------------------------------------------------------------------------------#
#-------------------------- 11. "|" = Either or --------------------------------#
#-------------------------------------------------------------------------------#

import re

txt = "The rain in Spain falls mainly in the plain!"

x = re.findall("falls|stays", txt) # Check if the string contains either "falls" or "stays":
print(x) # ['falls']

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

# Output: Yes, there is at least one match!


#-----------------------------------------------------------------------------#
#------------------------- 12. () group capturing ----------------------------#
#-----------------------------------------------------------------------------#

import re

# Sample text
text = "cat123 dog456 bird789"

##################################
## 1. Regex without parentheses ##
##################################

# Matches 'cat' followed by digits
pattern1 = r"\w+\d+"
matches1 = re.findall(pattern1, text)
print("Without parentheses:", matches1)  # Output: ['cat123', 'dog456', 'bird789']

############################################
## 2. Regex with capturing parentheses () ##
############################################

# Captures the letters and digits separately
pattern2 = r"(\w+)(\d+)"
matches2 = re.findall(pattern2, text)
print("With capturing parentheses:", matches2)  # Output: [('cat', '123'), ('dog', '456'), ('bird', '789')]

####################################################
## 3. Use "()" and "| to capture different groups ##
####################################################

# Capture pattern starts with 'c' or 'd' followed by digits
pattern3 = r"(c\w+|d\w+)\d+"
print(re.findall(pattern3, text))  # Output: ['cat12', 'dog45', 'd78']


#----------------------------------------------------#
#--------- 13. (?:) non-group capturing -------------#
#----------------------------------------------------#

import re

# Sample text
text = "date: 2025-05-25 or 2025/05/25"

############################################
## 1. Regex with capturing parentheses () ##
############################################

# Captures year, month, and day separately
pattern1 = r"(\d{4})[-/](\d{2})[-/](\d{2})"
matches1 = re.findall(pattern1, text)
print("With capturing parentheses:", matches1)  # Output: [('2025', '05', '25'), ('2025', '05', '25')]

############################################
## 2. Regex with non-capturing group (?:) ##
############################################

# Groups the separator (hyphen or slash) but only captures the entire date
pattern2 = r"\d{4}(?:[-/])\d{2}(?:[-/])\d{2}"
matches2 = re.findall(pattern2, text)
print("With non-capturing group:", matches2)  # Output: ['2025-05-25', '2025/05/25']

##########################################################################
## 3. Use non-capturing group (?:) with alternation | to match patterns ##
##########################################################################

# Matches dates with either hyphen or slash as separators
pattern3 = r"\d{4}(?:-|/)\d{2}(?:-|/)\d{2}"
matches3 = re.findall(pattern3, text)
print("With non-capturing group and alternation:", matches3)  # Output: ['2025-05-25', '2025/05/25']


#----------------------------------------------------------------------------#
#--------------------------- 14. re.match() ---------------------------------#
#----------------------------------------------------------------------------#

# The match() function checks for a match only at the BEGINNING of the string.

import re

#####################
## not None result ##
#####################

txt = "The rain in Spain"

x = re.match("The", txt) # Check if the string starts with "The":
print(x) # <re.Match object; span=(0, 3), match='The'>

if x:
  print("Yes, the string starts with 'The'")
else:
  print("No match")

###################
## None result ####
###################

# This returns None because "regex" is not at the beginning
text = "We are learning regex with geeksforgeeks"
result = re.match(r"regex", text)
print(result)  # None

if result:
  print("Match found!")
else:
  print("No match found!")  # Output: No match found!


#----------------------------------------------------------------------------#
#-------------------------- 15. re.findall() --------------------------------#
#----------------------------------------------------------------------------#

# The findall() function returns a list containing all matches.

import re
txt = "The rain in Spain"

x = re.findall("ai", txt) # Return a list containing every occurrence of "ai":
print(x) #['ai', 'ai']

x = re.findall("Portugal", txt)
print(x) # []


#---------------------------------------------------------------------------#
#-------------------------- 16. re.search() --------------------------------#
#---------------------------------------------------------------------------#

# The search() function searches the string for a match, and returns a Match object if there is a match.

import re
txt = "The rain in Spain"

x = re.search("\s", txt)
print("The first white-space character is located in position:", x.start()) # Return 3

x = re.search("Portugal", txt)
print(x) # Return None


#--------------------------------------------------------------------------#
#-------------------------- 17. re.split() --------------------------------#
#--------------------------------------------------------------------------#

# The split() function returns a list where the string has been split at each match:

import re
txt = "The rain in Spain"

x = re.split("\s", txt)
print(x) # ['The', 'rain', 'in', 'Spain']

x = re.split("\s", txt, 1) #Split the string only at the first occurrence
print(x) # ['The', 'rain in Spain']


#------------------------------------------------------------------------#
#-------------------------- 18. re.sub() --------------------------------#
#------------------------------------------------------------------------#

# The sub() function replaces the matches with the text of your choice:

import re
txt = "The rain in Spain"

x = re.sub("\s", "_", txt) # Replace all white-space characters with the "_" character:
print(x) # The_rain_in_Spain

x = re.sub("\s", "_", txt, 2) #Replace only the first 2 occurrences:
print(x) # The_rain_in Spain


#------------------------------------------------------------------------#
#-------------------------- 19. Match Object-----------------------------#
#------------------------------------------------------------------------#

# A Match Object is an object containing information about the search and the result.

# match_object.span() returns a tuple containing the start- and end positions of the match.
# match_object.string returns the string passed into the function.
# match_object.group() returns the part of the string where there was a match.
# match_object.groups() returns a tuple containing all the subgroups of the match.

'''
Note: If there is no match, the value None will be returned, instead of the Match Object.
'''

import re
txt = "The rain in Spain"

x = re.search("ai", txt)
print(x) # this will print an object
         # <_sre.SRE_Match object; span=(5, 7), match='ai'>

x = re.search(r"\bS\w+", txt) # Search for an upper case "S" character in the beginning of a word, and print the word:

print(x.span()) # Return a tuple containing the start, and end positions of the match
                # Here return (12,17) means the match starts at 12, ends at 17

print(x.string) # Returns the original string passed into the function
                # Here return "The rain in Spain"

print(x.group()) # Returns the part of the string group where there was a match
                 # Here return "Spain"


# .groups() returns a tuple containing all the subgroups of the match
import re

pos_nucleotide_1 = "312.1C"
pos_nucleotide_2 = "42.6del"

pattern = r"(\d+\.?\d+)([a-zA-Z]+\b)"

x = re.search(pattern, pos_nucleotide_1)
print(x.groups())  # Output: ('312.1', 'C')
print(x.group(1))  # Output: '312.1'
print(x.group(2))  # Output: 'C'
print(x.group())   # Output: '312.1C'

x = re.search(pattern, pos_nucleotide_2)
print(x.groups())  # Output: ('42.6', 'del')
print(x.group(1))  # Output: '42.6'
print(x.group(2))  # Output: 'del'
print(x.group())   # Output: '42.6del'



