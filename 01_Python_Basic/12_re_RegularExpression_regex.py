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
7. "*" = Zero or More occurrences (greedy)
8. "+" = One or More occurrences (greedy)
9. "?" = Zero or One occurrences
10. "*?" = Zero or More occurences, but as few as possible (non-greedy)
11. "+?" = One or More occurences, but as few as possible (non-greedy)
12. "{}" = Exactly the specified number of occurrences
13. "|" = Either or
14. () = group capturing
15. (?:) = non-group capturing
16. (?<=Y)X and (?<!Y)X = Positive lookbehind and Negative lookbehind
17. X(?=Y) and X(?!Y) = Positive lookahead and Negative lookahead
18. regex module: Combine non-greedy, lookbehind and lookahead
19. re.match(): Determines if the RE matches at the beginning of the string
20. re.findall(): Returns a list containing all matches
21. re.search(): Returns a Match object if there is a match anywhere in the string
22. re.split(): Returns a list where the string has been split at each match
23. re.sub(): Replaces one or many matches with a string
24. Match Object
'''


#-------------------------------------------------------------------------#
#------------------------------- 1. Example ------------------------------#
#-------------------------------------------------------------------------#

import re

txt = "The rain in Spain"
x = re.match(r"^The.*Spain$", txt)

if x:
  print("YES! We have a match!")
else:
  print("No match")


#---------------------------------------------------------------------------------------------#
#-------------------------- 2. "[]" = A set of characters ------------------------------------#
#---------------------------------------------------------------------------------------------#

import re

txt = "The rain in Spain"

x = re.findall(r"[a-m]", txt) # Find all lower case characters alphabetically between "a" and "m":
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

x = re.findall(r"\d", txt) # Find all digit characters:
print(x) # ['5', '9']

"""
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

## \., \*, \+, \$, \(, \), \[, \], \{, \}, \|, \\	Use to search for special characters
"""


#--------------------------------------------------------------------------------------------------------------#
#-------------------------- 4. "." = Any character (except newline character) ---------------------------------#
#--------------------------------------------------------------------------------------------------------------#

import re

txt = "hello planet"

x = re.findall(r"he..o", txt) # Search for a sequence that starts with "he", followed by two (any) characters, and an "o":
print(x) # ['hello']


#---------------------------------------------------------------------------------#
#-------------------------- 5. "^" = Starts with ---------------------------------#
#---------------------------------------------------------------------------------#

import re

txt = "hello planet"

x = re.findall(r"^hello", txt) # Check if the string starts with 'hello':
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

# Output: Yes, the string ends with 'planet'


#-------------------------------------------------------------------------------------------------------#
#-------------------------- 7. "*" = Zero or More occurrences (greedy) ---------------------------------#
#-------------------------------------------------------------------------------------------------------#

import re

text = "a aa aaa aaaa b bb bbb"

# 1. Using * (zero or more)
# Matches zero or more occurrences of 'a' characters

pattern = r"a*"
print(re.findall(pattern, text))

# Output: ['a', '', 'aa', '', 'aaa', '', 'aaaa', '', '', '', '', '', '', '', '', '', '']
# The r"*a*" pattern matches 'a' characters of varying lengths, including zero occurrences (represented by empty strings).
# So "" means zero occurrence of 'a'
# For example, the "b" or "bb" have no 'a' characters, so it matches zero occurrences, resulting in an empty string in the output list.


#------------------------------------------------------------------------------------------------------#
#-------------------------- 8. "+" = One or More occurrences (greedy) ---------------------------------#
#------------------------------------------------------------------------------------------------------#

import re

text = "a aa aaa aaaa b bb bbb"

# 2. Using + (one or more)
# Matches one or more occurrences of 'a' characters

pattern = r"a+"
print(re.findall(pattern, text))

# Output: ['a', 'aa', 'aaa', 'aaaa']
# The r"+a+" pattern matches 'a' characters of varying lengths, but only those with at least one occurrence.
# So it does not match the "b" or "bb" since they have no 'a' characters.


#--------------------------------------------------------------------------------------------#
#-------------------------- 9. "?" = Zero or One occurrence ---------------------------------#
#--------------------------------------------------------------------------------------------#

import re

text = "a aa aaa aaaa b bb bbb"

# 3. Using ? (zero or one)
# Matches zero or one occurrence of 'a' characters

pattern = r"a?"
print(re.findall(pattern, text))

# Output: ['a', '', 'a', 'a', '', 'a', 'a', 'a', '', 'a', 'a', 'a', 'a', '', '', '', '', '', '', '', '', '', '']
# The r"?a?" pattern matches one-length 'a' characters, including zero occurrences (represented by empty strings).
# So "" means zero occurrence of 'a' (like in "b" or "bb")


#-----------------------------------------------------------------------------------------------------------------#
#-------------------- 10. "*?" = Zero or More occurences, but as few as possible (non-greedy) --------------------#
#-----------------------------------------------------------------------------------------------------------------#

import re

text = '<a>first</a><b>second</b>'

print(re.search(r'<b.*>', text).group())   # Output: <b>second</b>
print(re.search(r'<b.+?>', text).group())  # Output: <b>second</b>

print(re.search(r'<b.*?>', text).group())  # Output: <b>

'''
Explanation:
1. In the first example, the pattern <b.*> uses the greedy quantifier *, 
   which matches as many characters as possible.
   Therefore, it captures everything from the first <b> to the last >, resulting in <b>second</b>.

2. In the second example, the pattern <b.+?> uses the non-greedy quantifier +?, 
   but the ".+?" still requires at least one character to be matched.
   Since there are characters between <b> and </b>, it captures the entire <b>second</b>.
  
3. In the third example, the pattern <b.*?> uses the non-greedy quantifier *?, 
   The ".*?" matches as few characters as possible, so it stops at the first > it encounters, resulting in <b>.
   (between <b amd > there is no character, so it matches zero occurrence of any character)
'''


#-----------------------------------------------------------------------------------------------------------------#
#------------------- 11. "+?" = One or More occurences, but as few as possible (non-greedy) ----------------------#
#-----------------------------------------------------------------------------------------------------------------#

import re

text = '<foo>, <>, <bar>, <baz>, <>'

print(re.findall(r'<.+>', text))    # Output: ['<foo>, <>, <bar>, <baz>, <>']
print(re.findall(r'<.*?>', text))   # Output: ['<foo>', '<>', '<bar>', '<baz>', '<>']

print(re.findall(r'<.+?>', text))   # Output: ['<foo>', '<>, <bar>', '<baz>'] ('<>, <bar>' still contains characters between < and >, so it matches)
print(re.findall(r'<\w+?>', text))  # Output: ['<foo>', '<bar>', '<baz>']

'''
Explanation:
1. In the first example, the pattern <.+> uses the greedy quantifier +, 
   which matches as many characters as possible.
   Therefore, it captures everything from the first < to the last >, 
   resulting in '<foo>, <>, <bar>, <baz>, <>' (one string as a whole).

2. In the second example, the pattern <.*?> uses the non-greedy quantifier *?, 
   which matches as few characters as possible.
   Therefore, it captures each individual tag, resulting in ['<foo>', '<>', '<bar>', '<baz>', '<>'].

3. In the third example, the pattern <.+?> uses the non-greedy quantifier +?, 
   which matches as few characters as possible but requires at least one character.
   Therefore, it captures each individual tag that contains at least one character between < and >, 
   resulting in ['<foo>', '<bar>', '<baz>'] (it excludes the empty tags <>).
''' 


#------------------------------------------------------------------------------------------------------------------#
#-------------------------- 12. "{}" = Exactly the specified number of occurrences --------------------------------#
#------------------------------------------------------------------------------------------------------------------#

import re

txt = "hello helllo planet"

x = re.findall(r"he.{2}o", txt) # Search for a sequence that starts with "he", followed excactly 2 (any) characters, and an "o":
print(x) # ['hello']
         # Not return 'helllo' cause 'helllo' has 3 characters between "he" and "o"

#########

text = "1234 56 7 89012"

pattern = r"\d{1,3}" # {1,3} quantifier meaning at least 1 digit and at most 3 digits

print(re.findall(pattern, text)) # Output: ['123', '4', '56', '7', '890', '12']


#-------------------------------------------------------------------------------#
#-------------------------- 13. "|" = Either or --------------------------------#
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


#----------------------------------------------------------------------------------------------------------#
#--------------------------------------- 14. () group capturing -------------------------------------------#
#----------------------------------------------------------------------------------------------------------#

import re

# Sample text
text = "cat123 dog456 bird789"

#########################################
## 1. Regex without capturing group () ##
#########################################

# Matches 'cat' followed by digits
pattern = r"[a-z]+\d+"
print(re.findall(pattern, text))  # Output: ['cat123', 'dog456', 'bird789']

######################################
## 2. Regex with capturing group () ##
######################################

# Captures the letters and digits separately
pattern = r"([a-z]+)(\d+)"
print(re.findall(pattern, text))  # Output: [('cat', '123'), ('dog', '456'), ('bird', '789')]

# Get the digits only
print(re.findall(r"([a-z]+)\d+", text)) # Output: ['cat', 'dog', 'bird']

###########################################################
## 3. Use "()" and "|" or [] to capture different groups ##
###########################################################

# Get the 'cat' and 'dog' only using []
pattern = r"([cd][a-z]+)\d+"
print(re.findall(pattern, text))  # Output: ['cat', 'dog']

# # Get the 'cat' and 'dog' only using |
pattern = r"(c[a-z]+|d[a-z]+)\d+"
print(re.findall(pattern, text))  # Output: ['cat', 'dog']

#---------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 15. (?:) non-group capturing -----------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

'''NOTE: non-capturing group (?:...) should be used with lookbehind or lookahead for better outcomes'''

import re

# Sample text
text = "+82-1012345678, asdfsdaf, +84-526913, dfdf, +82-52105948, xzdfasdrt, +87-2352345267"

###############################################
## 1. Regex without non-capturing group (?:) ##
###############################################

pattern = r"\+82-\d+"
print(re.findall(pattern, text))  # Output: ['+82-1012345678', '+82-52105948']

pattern = r"\+82-\d+|\+84-\d+|\+87-\d+"
print(re.findall(pattern, text))  # Output: ['+82-1012345678', '+84-526913', '+82-52105948', '+87-2352345267']

#-----
## Apply capturing group () to get the number part only
#-----

pattern = r"(\+82-|\+84-|\+87-)(\d+)"
print(re.findall(pattern, text))  
# Output: [('+82-', '1012345678'), ('+84-', '526913'), ('+82-', '52105948'), ('+87-', '2352345267')]
'''DOES NOT WORK AS EXPECTED'''

##########################################################################
## 3. Use non-capturing group (?:) with alternation | to match patterns ##
##########################################################################

# Matches dates with either hyphen or slash as separators
pattern = r"(?:\+82-|\+84-|\+87-)(\d+)"
print(re.findall(pattern, text))  # Output: ['1012345678', '526913', '52105948', '2352345267']


#---------------------------------------------------------------------------------------------------------------#
#---------------- 16. (?<=Y)X and (?<!Y)X = Positive lookbehind and Negative lookbehind ------------------------#
#---------------------------------------------------------------------------------------------------------------#

import re

text = "Apple &_apple_& Banana &_banana_& Cherry &_cherry_&"

#################################
## Positive lookbehind (?<=Y)X ##
#################################
'''Matches 'X' only if preceded by 'Y'.'''

pattern_pos_lookbehind = r"(?<=&_)\w+\W" # Matches worrds followed by "&_"

print(re.findall(pattern_pos_lookbehind, text))
# ['apple_&', 'banana_&', 'cherry_&']

#################################
## Negative lookbehind (?<!Y)X ##
#################################
'''Matches 'X' only if NOT preceded by 'Y'.'''

pattern_neg_lookbehind = r"(?<!&_)\b[a-zA-Z]+\b" # Matches words NOT preceded by "&_"
                                                 # \b...\b ensures whole words are matched

print(re.findall(pattern_neg_lookbehind, text))
# ['Apple', 'Banana', 'Cherry']

'''
NOTE: Lookbehind assertions are fixed-width in Python's re module.

If you need variable-width lookbehind, consider using the regex module (an alternative to re) which supports this feature.

pip3 install regex
'''

#-----------------------------------------------------------------------------------------------------------#
#-------------------- 17. X(?=Y) and X(?!Y) = Positive lookahead and Negative lookahead --------------------#
#-----------------------------------------------------------------------------------------------------------#

import re

text = "Apple &_apple_& Banana &_banana_& Cherry &_cherry_&"

###############################
## Positive lookahead X(?=Y) ##
###############################
'''Matches 'X' only if followed by 'Y'.'''

pattern_pos_lookahead = r"\W\w+(?=_&)" # Matches words followed by "_&"

print(re.findall(pattern_pos_lookahead, text))
# ['&_apple', '&_banana', '&_cherry']

###############################
## Negative lookahead X(?!Y) ##
###############################
'''Matches 'X' only if NOT followed by 'Y'.'''

pattern_neg_lookahead = r"\b[a-zA-Z]+\b(?!_&)" # Matches words NOT followed by " _&"

print(re.findall(pattern_neg_lookahead, text))
# ['Apple', 'Banana', 'Cherry']


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------ 18. regex: Combine non-greedy, lookbehind and lookahead -------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

###########################################
## Example 1: Open Reading Frames (ORFs) ##
###########################################

'''
Open Reading Frames (ORFs) are sequences in DNA that have the potential to code for proteins.
Meaning, they lie between a start codon (ATG) and a stop codon (TAA, TAG, TGA).

We can combine non-greedy, lookbehind, and lookahead to extract sequences inside ORFs (ignore the outside parts).
'''

import regex # Must use regex module to allow variable-width lookbehind

dna_sequence = "XXXAAATGXXXCCCTCGXXXTCGTGCXXXGATTGAAGAXXXACC"

pattern_XXX_orf = r"(?<=ATG.*?)(XXX)(?=.*?(?:TAA|TAG|TGA))" # Must use (?:TAA|TAG|TGA) so that the output only contains 'XXX'

print(regex.findall(pattern_XXX_orf, dna_sequence))
# ['XXX', 'XXX', 'XXX']

#######################################################################
## Example 2: Substitute " = " -> "=" but inside parentheses () only ##
#######################################################################

import regex # Must use regex module to allow variable-width lookbehind

text = """
x = func(a = 5, b = 10)
y = another_func(c = 15, d = 20)
"""

pattern_equal_in_parentheses = r"(?<=\(.*?)\s=\s(?=.*?\))"

print(regex.sub(pattern_equal_in_parentheses, "=", text))
# x = func(a=5, b=10)
# y = another_func(c=15, d=20)


#----------------------------------------------------------------------------#
#--------------------------- 19. re.match() ---------------------------------#
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
#-------------------------- 20. re.findall() --------------------------------#
#----------------------------------------------------------------------------#

# The findall() function returns a list containing all matches.

import re

txt = "The rain in Spain"

x = re.findall(r"ai", txt) # Return a list containing every occurrence of "ai":
print(x) #['ai', 'ai']

x = re.findall("Portugal", txt)
print(x) # []


#---------------------------------------------------------------------------#
#-------------------------- 21. re.search() --------------------------------#
#---------------------------------------------------------------------------#

# The search() function searches the string for a match, and returns a Match object if there is a match.

import re

txt = "The rain in Spain"

x = re.search(r"\s", txt)
print("The first white-space character is located in position:", x.start()) # Return 3

x = re.search("Portugal", txt)
print(x) # Return None


#--------------------------------------------------------------------------#
#-------------------------- 22. re.split() --------------------------------#
#--------------------------------------------------------------------------#

# The split() function returns a list where the string has been split at each match:

import re

txt = "The rain in Spain"

x = re.split(r"\s", txt)
print(x) # ['The', 'rain', 'in', 'Spain']

x = re.split(r"\s", txt, 1) # Split atmost 1 time
print(x) # ['The', 'rain in Spain']

x = re.split(r"\s", txt, 2) # Split atmost 2 times
print(x) # ['The', 'rain', 'in Spain']


#------------------------------------------------------------------------#
#-------------------------- 23. re.sub() --------------------------------#
#------------------------------------------------------------------------#

# The sub() function replaces the matches with the text of your choice:

import re

txt = "The rain in Spain"

x = re.sub(r"\s", "_", txt) # Replace all white-space characters with the "_" character:
print(x) # The_rain_in_Spain

x = re.sub(r"\s", "_", txt, 2) # Replace only the first 2 occurrences
print(x) # The_rain_in Spain


#------------------------------------------------------------------------#
#-------------------------- 24. Match Object-----------------------------#
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
pos_nucleotide_2 = "42.6gap"
pos_nucleotide_3 = "100A"

pattern = r"(\d+\.?\d+)([a-zA-Z]+\b)"

x = re.search(pattern, pos_nucleotide_1)
print(x.groups())  # Output: ('312.1', 'C')
print(x.group(1))  # Output: '312.1'
print(x.group(2))  # Output: 'C'
print(x.group())   # Output: '312.1C'

x = re.search(pattern, pos_nucleotide_2)
print(x.groups())  # Output: ('42.6', 'gap')
print(x.group(1))  # Output: '42.6'
print(x.group(2))  # Output: 'gap'
print(x.group())   # Output: '42.6gap'

x = re.search(pattern, pos_nucleotide_3)
print(x.groups())  # Output: ('100', 'A')
print(x.group(1))  # Output: '100'
print(x.group(2))  # Output: 'A'
print(x.group())   # Output: '100A'