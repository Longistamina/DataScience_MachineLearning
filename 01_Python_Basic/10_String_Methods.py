"""
Flow of contents:

1. Basic Transformations:
   - Case transformations: .capitalize(), .upper(), .lower(), .title(), .swapcase(), .casefold()
   - Stripping methods: .strip(), .lstrip(), .rstrip()

2. Count and Search:
   - Counting occurrences: .count()
   - Finding positions: .find(), .rfind(), .index(), .rindex()

3. Boolean Checks:
   - Character type checks: .isalpha(), .isdecimal(), .isdigit(), .isnumeric(), .isalnum(), .isspace()
   - Case checks: .isupper(), .islower(), .istitle()
   - ASCII and printable checks: .isascii(), .isprintable(), .isidentifier()

4. Prefix/Suffix Checks:
   - Pattern checks: .startswith(), .endswith()

5. Splitting and Joining:
   - Splitting methods: .split(), .rsplit(), .partition(), .rpartition(), .splitlines()
   - Joining method: .join()

6. Replacement and Removal:
   - Replacement: .replace()
   - Prefix/suffix removal: .removeprefix(), .removesuffix()

7. Formatting and Alignment:
   - Formatting: .format(), .format_map()
   - Alignment: .center(), .ljust(), .rjust(), .zfill()

8. Tab Expansion:
   - Tab handling: .expandtabs()

9. Translation:
   - Character translation: .maketrans(), .translate()

10. Encoding/Decoding:
    - Text encoding: .encode()
"""

#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 1. Basic Transformations -------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

##########################
## Case transformations ##
##########################

s1 = 'Hello World python'

k1 = s1.capitalize()    # 'Hello world python' - capitalize first character only
k2 = s1.upper()         # 'HELLO WORLD PYTHON' - all uppercase
k3 = s1.lower()         # 'hello world python' - all lowercase
k4 = s1.title()         # 'Hello World Python' - capitalize first letter of each word
k5 = s1.swapcase()      # 'hELLO wORLD pYTHON' - swap case of all characters
k6 = s1.casefold()      # 'hello world python' - aggressive lowercase for caseless matching

print(f"capitalize(): '{k1}'") # 'Hello world python'
print(f"upper(): '{k2}'")      # 'HELLO WORLD PYTHON'
print(f"lower(): '{k3}'")      # 'hello world python'
print(f"title(): '{k4}'")      # 'Hello World Python'
print(f"swapcase(): '{k5}'")   # 'hELLO wORLD pYTHON'
print(f"casefold(): '{k6}'")   # 'hello world python'

#######################
## Stripping methods ##
#######################

s2 = ' Hello World Python '

k7 = s2.strip()         # 'Hello World Python' - remove whitespace from both ends
k8 = s2.lstrip()        # 'Hello World Python ' - remove whitespace from left
k9 = s2.rstrip()        # ' Hello World Python' - remove whitespace from right

print(f"strip(): '{k7}'")   # 'Hello World Python'
print(f"lstrip(): '{k8}'")  # 'Hello World Python '
print(f"rstrip(): '{k9}'")  # ' Hello World Python'

################################
## Custom character stripping ##
################################

s3 = '---Hello World---'

k10 = s3.strip('-')     # 'Hello World' - remove '-' from both ends
k11 = s3.lstrip('-')    # 'Hello World---' - remove '-' from left only
k12 = s3.rstrip('-')    # '---Hello World' - remove '-' from right only

print(f"Custom strip example: '{s3}' -> '{k10}'")
# '---Hello World---' -> 'Hello World'


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 2. Count and Search ------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

poem = '''
Shall I compare thee to a summer's day?
Thou art more lovely and more temperate:
Rough winds do shake the darling buds of May,
And summer's lease hath all too short a date;
'''

#######################
## Count occurrences ##
#######################

print(poem.count('s')) # 9
print(poem.lower().count('s')) # 10

title = 'PYTHON PROGRAMMING'
print(f"Count 'P' from index 2 to 10: {title.count('P', 2, 10)}") # 1 (excludes first 'P')

#####################
## Finding methods ##
#####################

full_name = 'John Michael Smith'

print(f"Original: '{full_name}'")
print(f"find(' '): {full_name.find(' ')}")           # 4 (Index of the first space from left)
print(f"rfind(' '): {full_name.rfind(' ')}")         # 12 (Index of the first space from right)

print(f"index(' '): {full_name.index(' ')}")         # 4 (Like find but raises error if not found)
print(f"rindex(' '): {full_name.rindex(' ')}")       # 12 (Like rfind but raises error if not found)


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 3. Boolean Checks --------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

test_strings = [
    'Hello', 'WORLD', 'Hello123', 
    '123', '⅕', '³', '456.78', 
    ' ', '', 'café', 
    '\t\n', 'MyVar'
]

######################
## isalpha() method ##
######################
'''Checks if all characters are alphabetic.'''

for s in test_strings:
    print(f"{repr(s)}.isalpha(): {s.isalpha()}")
# 'Hello'.isalpha(): True
# 'WORLD'.isalpha(): True
# 'Hello123'.isalpha(): False
# '123'.isalpha(): False
# '⅕'.isalpha(): False
# '³'.isalpha(): False
# '456.78'.isalpha(): False
# ' '.isalpha(): False
# ''.isalpha(): False
# 'café'.isalpha(): True
# '\t\n'.isalpha(): False
# 'MyVar'.isalpha(): True

print(list(filter(lambda s: s.isalpha(), test_strings)))
# ['Hello', 'WORLD', 'café', 'MyVar']

########################
## isdecimal() method ##
########################
'''Checks if all characters are decimal characters (0-9).'''

for s in test_strings:
    print(f"{repr(s)}.isdecimal(): {s.isdecimal()}")
# 'Hello'.isdecimal(): False
# 'WORLD'.isdecimal(): False
# 'Hello123'.isdecimal(): False
# '123'.isdecimal(): True
# '⅕'.isdecimal(): False
# '³'.isdecimal(): False
# '456.78'.isdecimal(): False
# ' '.isdecimal(): False
# ''.isdecimal(): False
# 'café'.isdecimal(): False
# '\t\n'.isdecimal(): False
# 'MyVar'.isdecimal(): False

print(list(filter(lambda s: s.isdecimal(), test_strings)))
# ['123']

######################
## isdigit() method ##
######################
'''Checks if all characters are digits (includes decimals, superscripts, subscripts).'''

for s in test_strings:
    print(f"{repr(s)}.isdigit(): {s.isdigit()}")
# 'Hello'.isdigit(): False
# 'WORLD'.isdigit(): False
# 'Hello123'.isdigit(): False
# '123'.isdigit(): True
# '⅕'.isdigit(): False
# '³'.isdigit(): True
# '456.78'.isdigit(): False
# ' '.isdigit(): False
# ''.isdigit(): False
# 'café'.isdigit(): False
# '\t\n'.isdigit(): False
# 'MyVar'.isdigit(): False

print(list(filter(lambda s: s.isdigit(), test_strings)))
# ['123', '³']

########################
## isnumeric() method ##
########################
'''Checks if all characters are numeric (includes fractions, Roman numerals).'''

for s in test_strings:
    print(f"{repr(s)}.isnumeric(): {s.isnumeric()}")
# 'Hello'.isnumeric(): False
# 'WORLD'.isnumeric(): False
# 'Hello123'.isnumeric(): False
# '123'.isnumeric(): True
# '⅕'.isnumeric(): True
# '³'.isnumeric(): True
# '456.78'.isnumeric(): False
# ' '.isnumeric(): False
# ''.isnumeric(): False
# 'café'.isnumeric(): False
# '\t\n'.isnumeric(): False
# 'MyVar'.isnumeric(): False

print(list(filter(lambda s: s.isnumeric(), test_strings)))
# ['123', '⅕', '³']

######################
## isalnum() method ##
######################
'''Checks if all characters are alphanumeric (letters and numbers).'''

for s in test_strings:
    print(f"{repr(s)}.isalnum(): {s.isalnum()}")
# 'Hello'.isalnum(): True
# 'WORLD'.isalnum(): True
# 'Hello123'.isalnum(): True
# '123'.isalnum(): True
# '⅕'.isalnum(): True
# '³'.isalnum(): True
# '456.78'.isalnum(): False
# ' '.isalnum(): False
# ''.isalnum(): False
# 'café'.isalnum(): True
# '\t\n'.isalnum(): False
# 'MyVar'.isalnum(): True

print(list(filter(lambda s: s.isalnum(), test_strings)))
# ['Hello', 'WORLD', 'Hello123', '123', '⅕', '³', 'café', 'MyVar']

######################
## isspace() method ##
######################
'''Checks if all characters are whitespace.'''

for s in test_strings:
    print(f"{repr(s)}.isspace(): {s.isspace()}")
# 'Hello'.isspace(): False
# 'WORLD'.isspace(): False
# 'Hello123'.isspace(): False
# '123'.isspace(): False
# '⅕'.isspace(): False
# '³'.isspace(): False
# '456.78'.isspace(): False
# ' '.isspace(): True
# ''.isspace(): False
# 'café'.isspace(): False
# '\t\n'.isspace(): True
# 'MyVar'.isspace(): False

print(list(filter(lambda s: s.isspace(), test_strings)))
# [' ', '\t\n']

######################
## isupper() method ##
######################
'''Checks if all alphabetic characters are uppercase.'''

for s in test_strings:
    print(f"{repr(s)}.isupper(): {s.isupper()}")
# 'Hello'.isupper(): False
# 'WORLD'.isupper(): True
# 'Hello123'.isupper(): False
# '123'.isupper(): False
# '⅕'.isupper(): False
# '³'.isupper(): False
# '456.78'.isupper(): False
# ' '.isupper(): False
# ''.isupper(): False
# 'café'.isupper(): False
# '\t\n'.isupper(): False
# 'MyVar'.isupper(): False

print(list(filter(lambda s: s.isupper(), test_strings)))
# ['WORLD']

######################
## islower() method ##
######################
'''Checks if all alphabetic characters are lowercase.'''

for s in test_strings:
    print(f"{repr(s)}.islower(): {s.islower()}")
# 'Hello'.islower(): False
# 'WORLD'.islower(): False
# 'Hello123'.islower(): False
# '123'.islower(): False
# '⅕'.islower(): False
# '³'.islower(): False
# '456.78'.islower(): False
# ' '.islower(): False
# ''.islower(): False
# 'café'.islower(): True
# '\t\n'.islower(): False
# 'MyVar'.islower(): False

print(list(filter(lambda s: s.islower(), test_strings)))
# ['café']

######################
## istitle() method ##
######################
'''Checks if the string is in title case.'''

for s in test_strings:
    print(f"{repr(s)}.istitle(): {s.istitle()}")
# 'Hello'.istitle(): True
# 'WORLD'.istitle(): False
# 'Hello123'.istitle(): True
# '123'.istitle(): False
# '⅕'.istitle(): False
# '³'.istitle(): False
# '456.78'.istitle(): False
# ' '.istitle(): False
# ''.istitle(): False
# 'café'.istitle(): False
# '\t\n'.istitle(): False
# 'MyVar'.istitle(): False

print(list(filter(lambda s: s.istitle(), test_strings)))
# ['Hello', 'Hello123']

######################
## isascii() method ##
######################
'''Checks if all characters are ASCII characters.'''

for s in test_strings:
    print(f"{repr(s)}.isascii(): {s.isascii()}")
# 'Hello'.isascii(): True
# 'WORLD'.isascii(): True
# 'Hello123'.isascii(): True
# '123'.isascii(): True
# '⅕'.isascii(): False
# '³'.isascii(): False
# '456.78'.isascii(): True
# ' '.isascii(): True
# ''.isascii(): True
# 'café'.isascii(): False
# '\t\n'.isascii(): True
# 'MyVar'.isascii(): True

print(list(filter(lambda s: s.isascii(), test_strings)))
# ['Hello', 'WORLD', 'Hello123', '123', '456.78', ' ', '', '\t\n', 'MyVar']

##########################
## isprintable() method ##
##########################
'''Checks if all characters are printable (no control characters).'''

for s in test_strings:
    print(f"{repr(s)}.isprintable(): {s.isprintable()}")
# 'Hello'.isprintable(): True
# 'WORLD'.isprintable(): True
# 'Hello123'.isprintable(): True
# '123'.isprintable(): True
# '⅕'.isprintable(): True
# '³'.isprintable(): True
# '456.78'.isprintable(): True
# ' '.isprintable(): True
# ''.isprintable(): True
# 'café'.isprintable(): True
# '\t\n'.isprintable(): False
# 'MyVar'.isprintable(): True

print(list(filter(lambda s: s.isprintable(), test_strings)))
# ['Hello', 'WORLD', 'Hello123', '123', '⅕', '³', '456.78', ' ', '', 'café', 'MyVar']

###########################
## isidentifier() method ##
###########################
'''Checks if the string is a valid Python identifier.'''

for s in test_strings:
   print(f"{repr(s)}.isidentifier(): {s.isidentifier()}")
# 'Hello'.isidentifier(): True
# 'WORLD'.isidentifier(): True
# 'Hello123'.isidentifier(): True
# '123'.isidentifier(): False
# '⅕'.isidentifier(): False
# '³'.isidentifier(): False
# '456.78'.isidentifier(): False
# ' '.isidentifier(): False
# ''.isidentifier(): False
# 'café'.isidentifier(): True
# '\t\n'.isidentifier(): False
# 'MyVar'.isidentifier(): True

print(list(filter(lambda s: s.isidentifier(), test_strings)))
# ['Hello', 'WORLD', 'Hello123', 'café', 'MyVar']


#----------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 4. Prefix/Suffix Checks ------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

filename = 'document.pdf'
url = 'https://example.com'
greeting = 'Hello World'

##########################
## Single prefix/suffix ##
##########################

print(filename.endswith('.pdf'))  # True
print(filename.endswith('.doc'))  # False

print(url.startswith('https'))    # True
print(url.startswith('www'))      # False

########################################
## Multiple prefixes/suffixes (tuple) ##
########################################

print(filename.endswith(('.pdf', '.docx', '.txt')))  # True (only need one to match)

print(url.startswith(('http://', 'https://')))       # True (only need one to match)

print(url.startswith(('http://', 'www')))            # False (no match)

##############################
## With start/end positions ##
##############################

print(greeting.startswith('World', 6))  # True (check 'World' starting from index 6)

print(greeting.endswith('Hello', 0, 5)) # True (check 'Hello' in substring [0:5])

print(greeting.endswith('World', 0, 5)) # False (check 'World' in substring [0:5])


#----------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 5. Splitting and Joining ------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

#####################
## Basic splitting ##
#####################

full_name = 'Arthur Conan Doyle'
numbers = '12,13,14,15,16'

print(full_name.split()) # ['Arthur', 'Conan', 'Doyle']

print(numbers.split(',')) # ['12', '13', '14', '15', '16']

print(numbers.split(',', maxsplit=2)) # ['12', '13', '14,15,16']
'''maxsplit=2 means at most 2 splits, resulting in 3 parts.'''

#################
## Right split ##
#################

print(numbers.rsplit(',', maxsplit=2)) # ['12,13,14', '15', '16']

#######################
## Partition methods ##
#######################

demo_str = 'Name_Adress_Phone'

print(demo_str.partition('_')) # ('Name', '_', 'Adress_Phone')

print(demo_str.rpartition('_')) # ('Name_Adress', '_', 'Phone')

print(demo_str.partition('.')) # ('Name_Adress_Phone', '', '') # Delimiter not found

print(demo_str.rpartition('.')) # ('', '', 'Name_Adress_Phone') # Delimiter not found

################
## Splitlines ##
################

multiline = 'Line 1\nLine 2\nLine 3\nLine 4'

print(multiline.splitlines()) # ['Line 1', 'Line 2', 'Line 3', 'Line 4']

print(multiline.splitlines(keepends=True)) # ['Line 1\n', 'Line 2\n', 'Line 3\n', 'Line 4']

#############
## Joining ##
#############

lst = ['A', 'B', 'C', 'D', 'E']

print(''.join(lst))    # 'ABCDE'
print(' '.join(lst))   # 'A B C D E'
print(','.join(lst))   # 'A,B,C,D,E'
print(' | '.join(lst)) # 'A | B | C | D | E'

print('_'.join(['A', 'B', 'C'])) # 'A_B_C'


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 6. Replacement and Removal -----------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

text = 'Hello World Hello Universe'

#####################
## Replace methods ##
#####################

print(text.replace('Hello', 'Hi')) # 'Hi World Hi Universe'

print(text.replace('Hello', 'Hi', 1)) # 'Hi World Hello Universe' (only first occurrence)

########################################
## Remove prefix/suffix (Python 3.9+) ##
########################################

prefixed = 'prefix_dataABC'
suffixed = 'dataXYZ_suffix'

print(prefixed.removeprefix('prefix_')) # 'dataABC'
print(suffixed.removesuffix('_suffix')) # 'dataXYZ'


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 7. Formatting and Alignment ----------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

######################
## Basic formatting ##
######################

price = 1234567.89
name = "Python"
age = 25

print(f"Basic format:  {name} is {age} years old") # Python is 25 years old
print(f"Price formatting: {price:,.2f}") # 1,234,567.89

####################
## Format mapping ##
####################

data = {'name': 'Alice', 'age': 30}
template = 'Name: {name}, Age: {age}'

print(f"format_map(): '{template.format_map(data)}'") # 'Name: Alice, Age: 30'

#######################
## Alignment methods ##
#######################

word = 'Python'

print(word.center(15, '*')) # '****Python*****' (added * to both sides to center in width 15)
print(word.ljust(15, '-'))  # 'Python---------' (added - to the right to left-justify in width 15)
print(word.rjust(15, '='))  # '=========Python' (added = to the left to right-justify in width 15)
print(word.zfill(10))       # '0000Python'      (added leading zeros to make width 10)

########################
## Numbers with zfill ##
########################

number = '42'

print(number.zfill(5)) # '00042' (added leading zeros to make width 5)


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 8. Tab Expansion ---------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

tabbed_text = 'Hello\tWorld\tPython'

print(f"Original with tabs: '{tabbed_text}'")            # 'Hello      World   Python'
print(f"expandtabs(): '{tabbed_text.expandtabs()}'")     # 'Hello   World   Python' 
print(f"expandtabs(4): '{tabbed_text.expandtabs(10)}'")  # 'Hello     World     Python'


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 9. Translation -----------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

##############################
## Create translation table ##
##############################

translation_table = str.maketrans('eaiou', '12345')
#                   str.maketrans({'e':'1', 'a':'2', 'i':'3', 'o':'4', 'u':'5'})

text = 'Hello World'
translated = text.translate(translation_table)

print(f"'{text}' => '{translated}'")
# 'Hello World' => 'H2ll4 W4rld'

###############################
## Translation with deletion ##
###############################

translation_table2 = str.maketrans('aeiou', '12345', 'lw')  # Delete 'l' and 'w'

text2 = 'Hello World'
translated2 = text2.translate(translation_table2)

print(f"'{text2}' => '{translated2}'")
# 'Hello World' => 'H24 W4rd'


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 10. Encoding/Decoding ----------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

##############
## Encoding ##
##############

unicode_text = 'café naïve résumé'
print(f"Original: '{unicode_text}'") # 'café naïve résumé'

encoded_utf8 = unicode_text.encode('utf-8')
print(f"UTF-8 encoded: {encoded_utf8}") # b'caf\xc3\xa9 na\xc3\xafve r\xc3\xa9sum\xc3\xa9'

##############
## Decoding ##
##############

byte_string = b'Hello World'
print(f"Byte string: {byte_string}") # b'Hello World'

decoded = byte_string.decode('utf-8')
print(f"Decoded: '{decoded}'") # 'Hello World'