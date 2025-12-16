'''
0. Create a 1D string vector:
   + np.array(list_of_strings)
   + np.array(list_of_strings, dtype='U')
   + np.array(list_of_strings, dtype='Un'): fixed-length Unicode strings of length n
   + np.array(list_of_strings, dtype=np.dtypes.StringDType()): unlimited-length strings

1. Slicing: np.strings.slice(start, stop, step)
   
2. Case conversions:
   + np.strings.capitalize()
   + np.strings.upper()
   + np.strings.lower()
   + np.strings.title()
   + np.strings.swapcase()

3. Stripping:
   + np.strings.strip()
   + np.strings.lstrip()
   + np.strings.rstrip()

4. Length and Count:
   + np.strings.str_len()
   + np.strings.count()

5. Find and Search:
   + np.strings.find()
   + np.strings.rfind()
   + np.strings.index()
   + np.strings.rindex()

6. Replacement: np.strings.replace()

7. Alignment:
    + np.strings.center()
    + np.strings.ljust()
    + np.strings.rjust()
    + np.strings.zfill()

8. Expand Tabs: np.strings.expandtabs()

9. Partitioning:
    + np.strings.partition()
    + np.strings.rpartition()
    
10. Combination:
    + np.strings.add()
    + np.strings.multiply()

11. Formatting: np.strings.mod()

12. Translation: np.strings.translate()

13. Encoding and Decoding:
    + np.strings.encode()
    + np.strings.decode()

14. Boolean checks:
   + np.strings.isalpha()
   + np.strings.isdecimal()
   + np.strings.isdigit()
   + np.strings.isnumeric()
   + np.strings.isalnum()
   + np.strings.isspace()
   + np.strings.islower()
   + np.strings.isupper()
   + np.strings.istitle()

15. Prefix and Suffix checks:
   + np.strings.startswith()
   + np.strings.endswith()

16. Comparison:
    + np.strings.equal()
    + np.strings.not_equal()
    + np.strings.less()
    + np.strings.less_equal()
    + np.strings.greater()
    + np.strings.greater_equal()

17. Boolean Indexing: vector[np.strings.function(vector, args)]
'''

import numpy as np
import pytz

np.random.seed(33)
vector_tz = np.random.choice(pytz.all_timezones, size=15, replace=False) # Randomly select 15 timezones

print(vector_tz)
# ['Asia/Kuala_Lumpur' 'Asia/Sakhalin' 'Antarctica/Vostok' 'Europe/Istanbul'
#  'Europe/Madrid' 'Asia/Kuching' 'Africa/Kampala' 'Africa/El_Aaiun'
#  'Europe/Samara' 'Europe/Copenhagen' 'Europe/Zaporozhye'
#  'America/Eirunepe' 'Africa/Ndjamena' 'America/Havana' 'Brazil/DeNoronha']


#-------------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 0. Create a 1D string vector -------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#

###############################
## np.array(list_of_strings) ##
###############################

list_of_strings = ['apple', 'banana', 'cherry', 'date']

vector_strings = np.array(list_of_strings)
print(vector_strings)
# ['apple' 'banana' 'cherry' 'date']

vector_strings = np.array(['Hans Solo', 'Luke Skywalker', 'Leia Organa']) # Shorthand
print(vector_strings)
# ['Hans Solo' 'Luke Skywalker' 'Leia Organa']

##########################################
## np.array(list_of_strings, dtype='U') ##
##########################################
'''
dtype='U' creates an array of Unicode strings, with no fixed length.

Numpy will automatically determine the maximum length needed to store the strings.
'''

vector_unicode = np.array(["cat", "dog", "birds", "blounder fish"], dtype='U')
print(vector_unicode)
# ['cat' 'dog' 'birds' 'blounder fish']

repr(vector_unicode)
# "array(['cat', 'dog', 'birds', 'blounder fish'], dtype='<U13')"

###########################################
## np.array(list_of_strings, dtype='Un') ##
###########################################
'''dtype='Un' creates an array of fixed-length Unicode strings of length n.'''

vector_fixed_unicode = np.array(["cat", "dog", "birds", "blounder fish"], dtype='U5')
repr(vector_fixed_unicode)
# "array(['cat', 'dog', 'birds', 'bloun'], dtype='<U5')"
'''The last string is truncated to "bloun" to fit the fixed length of 5 characters.'''

##############################################################
## np.array(list_of_strings, dtype=np.dtypes.StringDType()) ##
##############################################################
'''dtype=np.dtypes.StringDType() creates an array of unlimited-length strings.'''

vector_unlimited = np.array(["cat", "dog", "birds", "blounder fish"], dtype=np.dtypes.StringDType())
repr(vector_unlimited)
# "array(['cat', 'dog', 'birds', 'blounder fish'], dtype=StringDType())"


#-------------------------------------------------------------------------------------------------------------------#
#-------------------------------- 1. Slicing: np.strings.slice(start, stop, step) ----------------------------------#
#-------------------------------------------------------------------------------------------------------------------#

print(np.strings.slice(vector_tz, 5, 10))
# ['Kuala' 'Sakha' 'ctica' 'e/Ist' 'e/Mad' 'Kuchi' 'a/Kam' 'a/El_' 'e/Sam'
#  'e/Cop' 'e/Zap' 'ca/Ei' 'a/Ndj' 'ca/Ha' 'l/DeN']

print(np.strings.slice(vector_tz, None, None, 3))
# ['Aauauu' 'Aaaan' 'Aataoo' 'Eo/tb' 'Eo/dd' 'Aaui' 'Ai/ml' 'Ai/_i' 'Eo/ma'
#  'Eo/phe' 'Eo/poy' 'Araine' 'Ai/je' 'Araan' 'Bz/Noa']

print(np.strings.slice(vector_tz, None, None, -1)) # Reverse each string
# ['rupmuL_alauK/aisA' 'nilahkaS/aisA' 'kotsoV/acitcratnA' 'lubnatsI/eporuE'
#  'dirdaM/eporuE' 'gnihcuK/aisA' 'alapmaK/acirfA' 'nuiaA_lE/acirfA'
#  'aramaS/eporuE' 'negahnepoC/eporuE' 'eyhzoropaZ/eporuE'
#  'epenuriE/aciremA' 'anemajdN/acirfA' 'anavaH/aciremA' 'ahnoroNeD/lizarB']


#-------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 2. Case conversions --------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#

print(vector_tz)
# ['Asia/Kuala_Lumpur' 'Asia/Sakhalin' 'Antarctica/Vostok' 'Europe/Istanbul'
#  'Europe/Madrid' 'Asia/Kuching' 'Africa/Kampala' 'Africa/El_Aaiun'
#  'Europe/Samara' 'Europe/Copenhagen' 'Europe/Zaporozhye'
#  'America/Eirunepe' 'Africa/Ndjamena' 'America/Havana' 'Brazil/DeNoronha']

#############################
## np.strings.capitalize() ##
#############################

print(np.strings.capitalize(vector_tz))
# ['Asia/kuala_lumpur' 'Asia/sakhalin' 'Antarctica/vostok' 'Europe/istanbul'
#  'Europe/madrid' 'Asia/kuching' 'Africa/kampala' 'Africa/el_aaiun'
#  'Europe/samara' 'Europe/copenhagen' 'Europe/zaporozhye'
#  'America/eirunepe' 'Africa/ndjamena' 'America/havana' 'Brazil/denoronha']

########################
## np.strings.upper() ##
########################

print(np.strings.upper(vector_tz))
# ['ASIA/KUALA_LUMPUR' 'ASIA/SAKHALIN' 'ANTARCTICA/VOSTOK' 'EUROPE/ISTANBUL'
#  'EUROPE/MADRID' 'ASIA/KUCHING' 'AFRICA/KAMPALA' 'AFRICA/EL_AAIUN'
#  'EUROPE/SAMARA' 'EUROPE/COPENHAGEN' 'EUROPE/ZAPOROZHYE'
#  'AMERICA/EIRUNEPE' 'AFRICA/NDJAMENA' 'AMERICA/HAVANA' 'BRAZIL/DENORONHA']

########################
## np.strings.lower() ##
########################

print(np.strings.lower(vector_tz))
# ['asia/kuala_lumpur' 'asia/sakhalin' 'antarctica/vostok' 'europe/istanbul'
#  'europe/madrid' 'asia/kuching' 'africa/kampala' 'africa/el_aaiun'
#  'europe/samara' 'europe/copenhagen' 'europe/zaporozhye'
#  'america/eirunepe' 'africa/ndjamena' 'america/havana' 'brazil/denoronha']

########################
## np.strings.title() ##
########################

tilte_vector = np.array(['hello world', 'numpy is great', 'string handling in python'])
print(np.strings.title(tilte_vector))
# ['Hello World' 'Numpy Is Great' 'String Handling In Python']

###########################
## np.strings.swapcase() ##
###########################

print(np.strings.swapcase(vector_tz))
# ['aSIA/kUALA_lUMPUR' 'aSIA/sAKHALIN' 'aNTARCTICA/vOSTOK' 'eUROPE/iSTANBUL'
#  'eUROPE/mADRID' 'aSIA/kUCHING' 'aFRICA/kAMPALA' 'aFRICA/eL_aAIUN'
#  'eUROPE/sAMARA' 'eUROPE/cOPENHAGEN' 'eUROPE/zAPOROZHYE'
#  'aMERICA/eIRUNEPE' 'aFRICA/nDJAMENA' 'aMERICA/hAVANA' 'bRAZIL/dEnORONHA']


#-------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------ 3. Stripping -----------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#

strip_space = np.array(['   leading space', 'trailing space   ', '   both sides   ', 'no_space'])
strip_other = np.array(['***hello***', 'hellob***', '***hello', 'no_other'])

########################
## np.strings.strip() ##
########################

print(np.strings.strip(strip_space))
# ['leading space' 'trailing space' 'both sides' 'no_space']

print(np.strings.strip(strip_other, '*'))
# ['hello' 'hellob' 'hello' 'no_other']

#########################
## np.strings.lstrip() ##
#########################

print(np.strings.lstrip(strip_space))
# ['leading space' 'trailing space   ' 'both sides   ' 'no_space']

print(np.strings.lstrip(strip_other, '*'))
# ['hello***' 'hellob***' 'hello' 'no_other']

#########################
## np.strings.rstrip() ##
#########################

print(np.strings.rstrip(strip_space))
# ['   leading space' 'trailing space' '   both sides' 'no_space']

print(np.strings.rstrip(strip_other, '*'))
# ['***hello' 'hellob' '***hello' 'no_other']


#-------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 4. Length and Count --------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#

##########################
## np.strings.str_len() ##
##########################

print(np.strings.str_len(vector_tz))
# [17 13 17 15 13 12 14 15 13 17 17 16 15 14 16]

########################
## np.strings.count() ##
########################

print(np.strings.count(vector_tz, 'a'))
# [3 3 2 1 1 1 4 2 3 1 1 1 3 4 2]

print(np.strings.count(vector_tz, 'Asia'))
# [1 1 0 0 0 1 0 0 0 0 0 0 0 0 0]


#-------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 5. Find and Search ---------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#

print(vector_tz)
# ['Asia/Kuala_Lumpur' 'Asia/Sakhalin' 'Antarctica/Vostok' 'Europe/Istanbul'
#  'Europe/Madrid' 'Asia/Kuching' 'Africa/Kampala' 'Africa/El_Aaiun'
#  'Europe/Samara' 'Europe/Copenhagen' 'Europe/Zaporozhye'
#  'America/Eirunepe' 'Africa/Ndjamena' 'America/Havana' 'Brazil/DeNoronha']

#######################
## np.strings.find() ##
#######################
'''Returns the lowest index of the substring if found (from the left), otherwise -1.'''

print(np.strings.find(vector_tz, 'a'))
# [ 3  3  3 10  8  3  5  5  8 13  8  6  5  6  2]

print(np.strings.find(vector_tz, '###'))
# [-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]

########################
## np.strings.rfind() ##
########################
'''Returns the highest index of the substring if found (from the right), otherwise -1.'''

print(np.strings.rfind(vector_tz, 'a'))
# [ 9  9  9 10  8  3 13 11 12 13  8  6 14 13 15]

print(np.strings.rfind(vector_tz, '###'))
# [-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]

########################
## np.strings.index() ##
########################
'''Like find(), but raises an error if the substring is not found.'''

print(np.strings.index(vector_tz, 'a'))
# [ 3  3  3 10  8  3  5  5  8 13  8  6  5  6  2]

print(np.strings.index(vector_tz, '###'))
# ValueError: substring not found

#########################
## np.strings.rindex() ##
#########################
'''Like rfind(), but raises an error if the substring is not found.'''

print(np.strings.rindex(vector_tz, 'a'))
# [ 9  9  9 10  8  3 13 11 12 13  8  6 14 13 15]

print(np.strings.rindex(vector_tz, '###'))
# ValueError: substring not found


#-------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 6. Replacement ----------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#

print(np.strings.replace(vector_tz, 'Asia', 'ASIA'))
# ['ASIA/Kuala_Lumpur' 'ASIA/Sakhalin' 'Antarctica/Vostok' 'Europe/Istanbul'
#  'Europe/Madrid' 'ASIA/Kuching' 'Africa/Kampala' 'Africa/El_Aaiun'
#  'Europe/Samara' 'Europe/Copenhagen' 'Europe/Zaporozhye'
#  'America/Eirunepe' 'Africa/Ndjamena' 'America/Havana' 'Brazil/DeNoronha']

print(np.strings.replace(vector_tz, '/', '-'))
# ['Asia-Kuala_Lumpur' 'Asia-Sakhalin' 'Antarctica-Vostok' 'Europe-Istanbul'
#  'Europe-Madrid' 'Asia-Kuching' 'Africa-Kampala' 'Africa-El_Aaiun'
#  'Europe-Samara' 'Europe-Copenhagen' 'Europe-Zaporozhye'
#  'America-Eirunepe' 'Africa-Ndjamena' 'America-Havana' 'Brazil-DeNoronha']

print(np.strings.replace(vector_tz, 'a', '@', 2)) # Replace first 2 occurrences of 'a' in each elemement
# ['Asi@/Ku@la_Lumpur' 'Asi@/S@khalin' 'Ant@rctic@/Vostok' 'Europe/Ist@nbul'
#  'Europe/M@drid' 'Asi@/Kuching' 'Afric@/K@mpala' 'Afric@/El_A@iun'
#  'Europe/S@m@ra' 'Europe/Copenh@gen' 'Europe/Z@porozhye'
#  'Americ@/Eirunepe' 'Afric@/Ndj@mena' 'Americ@/H@vana' 'Br@zil/DeNoronh@']


#-------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 7. Alignment ----------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#

vector_fruits = np.array(['apple', 'banana', 'cherry', 'date'])
print(vector_fruits)
# ['apple' 'banana' 'cherry' 'date']

#########################
## np.strings.center() ##
#########################

print(np.strings.center(vector_fruits, 10))
# ['  apple   ' '  banana  ' '  cherry  ' '   date   ']

print(np.strings.center(vector_fruits, 12, '*'))
# ['***apple****' '***banana***' '***cherry***' '****date****']

########################
## np.strings.ljust() ##
########################

print(np.strings.ljust(vector_fruits, 10))
# ['apple     ' 'banana    ' 'cherry    ' 'date      ']

print(np.strings.ljust(vector_fruits, 12, '-'))
# ['apple-------' 'banana------' 'cherry------' 'date--------']

########################
## np.strings.rjust() ##
########################

print(np.strings.rjust(vector_fruits, 10))
# ['     apple' '    banana' '    cherry' '      date']

print(np.strings.rjust(vector_fruits, 12, '+'))
# ['+++++++apple' '++++++banana' '++++++cherry' '++++++++date']

########################
## np.strings.zfill() ##
########################

print(np.strings.zfill(vector_fruits, 10))
# ['00000apple' '0000banana' '0000cherry' '000000date']


#-------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 8. Expand Tabs ----------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#

tabbed_strings = np.array(['Hello\tWorld', 'NumPy\tis\tgreat', 'String\thandling\tin\tPython'])
print(tabbed_strings)
# ['Hello\tWorld' 'NumPy\tis\tgreat' 'String\thandling\tin\tPython']

print(np.strings.expandtabs(tabbed_strings, tabsize=4))
# ['Hello   World' 'NumPy   is  great' 'String  handling    in  Python']


#-------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 9. Partitioning ----------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#

partion_vector = np.array(['apple-banana-cherry', 'date-fig-grape', 'kiwi-mango-papaya'])
print(partion_vector)
# ['apple-banana-cherry' 'date-fig-grape' 'kiwi-mango-papaya']

############################
## np.strings.partition() ##
############################

print(np.strings.partition(partion_vector, '-'))
# (array(['apple', 'date', 'kiwi'], dtype='<U5'), 
#  array(['-', '-', '-'], dtype='<U1'), 
#  array(['banana-cherry', 'fig-grape', 'mango-papaya'], dtype='<U13'))

'''
The first array(['apple', 'date', 'kiwi']) contains the substrings before the first occurrence of '-'.
The second array(['-', '-', '-']) contains the separator itself.
The third array(['banana-cherry', 'fig-grape', 'mango-papaya']) contains the substrings after the first occurrence of '-'.
'''

#############################
## np.strings.rpartition() ##
#############################

print(np.strings.rpartition(partion_vector, '-'))
# (array(['apple-banana', 'date-fig', 'kiwi-mango'], dtype='<U12'), 
#  array(['-', '-', '-'], dtype='<U1'), 
#  array(['cherry', 'grape', 'papaya'], dtype='<U6'))

'''
The first array(['apple-banana', 'date-fig', 'kiwi-mango']) contains the substrings before the last occurrence of '-'.
The second array(['-', '-', '-']) contains the separator itself.
The third array(['cherry', 'grape', 'papaya']) contains the substrings after the last occurrence of '-'.
'''


#-------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 10. Combination -----------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#

vector1 = np.array(['Hello', 'NumPy', 'String'], dtype=np.dtypes.StringDType())
vector2 = np.array(['World', 'is great', 'handling in Python'], dtype=np.dtypes.StringDType())
delimiter = np.array(['_', '_', '_'], dtype=np.dtypes.StringDType())

'''NOTE: use np.dtypes.StringDType() to create string arrays to avoid truncation issues during combination'''

######################
## np.strings.add() ##
######################

print(np.strings.add(vector1, vector2))
# ['HelloWorld' 'NumPyis great' 'Stringhandling in Python']

print(np.strings.add(vector1, delimiter, vector2))
# ['Hello_' 'NumPy_' 'String_']
'''DOES NOT WORK AS EXPECTED DUE TO BROADCASTING ISSUE WITH 3 ARRAYS'''

print(np.strings.add(np.strings.add(vector1, delimiter), vector2)) # Must use nested np.strings.add()
# ['Hello_World' 'NumPy_is great' 'String_handling in Python']

###########################
## np.strings.multiply() ##
###########################

print(np.strings.multiply(vector1, 3))
# ['HelloHelloHello' 'NumPyNumPyNumPy' 'StringStringString']

multiplicands = np.array([1, 2, 3])
print(np.strings.multiply(vector1, multiplicands))
# ['Hello' 'NumPyNumPy' 'StringStringString']


#-------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 11. Formatting -----------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#

original = np.array(['%d bytes', '%d bits', '%d KB'])
values = np.array([8, 64, 1024])

formatted = np.strings.mod(original, values)
print(formatted)
# ['8 bytes' '64 bits' '1024 KB']


#-------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 12. Translation -----------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#

print(vector_tz)
# ['Asia/Kuala_Lumpur' 'Asia/Sakhalin' 'Antarctica/Vostok' 'Europe/Istanbul'
#  'Europe/Madrid' 'Asia/Kuching' 'Africa/Kampala' 'Africa/El_Aaiun'
#  'Europe/Samara' 'Europe/Copenhagen' 'Europe/Zaporozhye'
#  'America/Eirunepe' 'Africa/Ndjamena' 'America/Havana' 'Brazil/DeNoronha']

translation_table = str.maketrans({'a': '@', 'e': '3', 'i': '1', 'o': '0'})

translated_vector = np.strings.translate(vector_tz, translation_table)
# print(translated_vector)
# ['As1@/Ku@l@_Lumpur' 'As1@/S@kh@l1n' 'Ant@rct1c@/V0st0k' 'Eur0p3/Ist@nbul'
#  'Eur0p3/M@dr1d' 'As1@/Kuch1ng' 'Afr1c@/K@mp@l@' 'Afr1c@/El_A@1un'
#  'Eur0p3/S@m@r@' 'Eur0p3/C0p3nh@g3n' 'Eur0p3/Z@p0r0zhy3'
#  'Am3r1c@/E1run3p3' 'Afr1c@/Ndj@m3n@' 'Am3r1c@/H@v@n@' 'Br@z1l/D3N0r0nh@']


#-------------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 13. Encoding and Decoding -----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#

#########################
## np.strings.encode() ##
#########################

original_vector = np.array(['Hello World', 'NumPy is great', 'String handling in Python'])
encoded_vector = np.strings.encode(original_vector, encoding='utf-8', errors='strict')

print(encoded_vector)
# [b'Hello World' b'NumPy is great' b'String handling in Python']

#########################
## np.strings.decode() ##
#########################

original_encoded_vector = np.array([b'Hello World', b'NumPy is great', b'String handling in Python'])

decoded_vector = np.strings.decode(original_encoded_vector, encoding='utf-8', errors='strict')
print(decoded_vector)
# ['Hello World' 'NumPy is great' 'String handling in Python']


#-------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 14. Boolean checks ---------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#

test_vector = np.array(
    [
      'Hello', 'WORLD', 'Hello123', 
      '123', '⅕', '³', '₂', '456.78', 
      ' ', '', 'café', 
      '\t\n', 'MyVar'
   ]
)

np.set_printoptions(linewidth=np.inf) # To display the entire array in one line

##########################
## np.strings.isalpha() ##
##########################
'''Checks if all characters in each string are alphabetic.'''

print(np.strings.isalpha(test_vector))
# [ True  True False False False False False False False False  True False  True]

print(test_vector[np.strings.isalpha(test_vector)])
# ['Hello' 'WORLD' 'café' 'MyVar']

############################
## np.strings.isdecimal() ##
############################
'''Checks if all characters in each string are decimal digits (0-9 only).'''

print(np.strings.isdecimal(test_vector))
# [False False False  True False False False False False False False False False]

print(test_vector[np.strings.isdecimal(test_vector)])
# ['123']

##########################
## np.strings.isdigit() ##
##########################
'''Checks if all characters in each string are digits (includes digits and superscripts).'''

print(np.strings.isdigit(test_vector))
# [False False False  True False  True  True False False False False False False]

print(test_vector[np.strings.isdigit(test_vector)])
# ['123' '³' '₂']

############################
## np.strings.isnumeric() ##
############################
'''Checks if all characters in each string are numeric (includes digits, fractions, superscripts).'''

print(np.strings.isnumeric(test_vector))
# [False False False  True  True  True  True False False False False False False]

print(test_vector[np.strings.isnumeric(test_vector)])
# ['123' '⅕' '³' '₂']

##########################
## np.strings.isalnum() ##
##########################
'''Checks if all characters in each string are alphanumeric.'''

print(np.strings.isalnum(test_vector))
# [ True  True  True  True  True  True  True False False False  True False  True]

print(test_vector[np.strings.isalnum(test_vector)])
# ['Hello' 'WORLD' 'Hello123' '123' '⅕' '³' '₂' 'café' 'MyVar']

##########################
## np.strings.isspace() ##
##########################
'''Checks if all characters in each string are whitespace.'''

print(np.strings.isspace(test_vector))
# [False False False False False False False False  True False False  True False]

print(test_vector[np.strings.isspace(test_vector)])
# [' ' '\t\n']

##########################
## np.strings.islower() ##
##########################
'''Checks if all characters in each string are lowercase.'''

print(np.strings.islower(test_vector))
# [False False False False False False False False False False  True False False]

print(test_vector[np.strings.islower(test_vector)])
# ['café']

##########################
## np.strings.isupper() ##
##########################
'''Checks if all characters in each string are uppercase.'''

print(np.strings.isupper(test_vector))
# [False  True False False False False False False False False False False False]

print(test_vector[np.strings.isupper(test_vector)])
# ['WORLD']

##########################
## np.strings.istitle() ##
##########################
'''Checks if each string is in title case (first letter uppercase, rest lowercase).'''

print(np.strings.istitle(test_vector))
# [ True False  True False False False False False False False False False False]

print(test_vector[np.strings.istitle(test_vector)])
# ['Hello' 'Hello123']

