'''
0. Create a 1D string vector:
   + np.array(list_of_strings)
   + np.array(list_of_strings, dtype='U')
   + np.array(list_of_strings, dtype='Un'): fixed-length Unicode strings of length n

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

11. Formating: np.strings.mod()

12. Translation: np.strings.translate()

13. Encoding and Decoding:
    + np.strings.encode()
    + np.strings.decode()

14. Boolean checks:
   + np.strings.isalpha()
   + np.strings.isdigit()
   + np.strings.isnumeric()
   + np.strings.isdecimal()
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