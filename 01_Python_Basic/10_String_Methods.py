"""
Flow of contents:

1. Basic Transformations:
   - Case transformations: .capitalize(), .upper(), .lower(), .title(), .swapcase(), .casefold()
   - Stripping methods: .strip(), .lstrip(), .rstrip()

2. Count and Search:
   - Counting occurrences: .count()
   - Finding positions: .find(), .rfind(), .index(), .rindex()

3. Boolean Checks:
   - Character type checks: .isalpha(), .isdigit(), .isnumeric(), .isdecimal(), .isalnum(), .isspace()
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

for test_str in test_strings:
    print(f"\nTesting: '{test_str}'")

    # Define checks separately with standard comments
    checks = {
        "isalpha": test_str.isalpha,       # All alphabetic
        "isdigit": test_str.isdigit,       # All digits
        "isnumeric": test_str.isnumeric,   # All numeric (includes digits, fractions, superscripts)
        "isdecimal": test_str.isdecimal,   # All decimal digits (0-9 only)
        "isalnum": test_str.isalnum,       # All alphanumeric
        "isspace": test_str.isspace,       # All whitespace
        "isupper": test_str.isupper,       # All uppercase
        "islower": test_str.islower,       # All lowercase
        "istitle": test_str.istitle,       # Title case
        "isascii": test_str.isascii,       # All ASCII characters
        "isprintable": test_str.isprintable,  # All printable
        "isidentifier": test_str.isidentifier, # Valid Python identifier
    }

    any_true = False
    for name, func in checks.items():
        if func():
            print(f"  {name}() = True")  # comment already placed above
            any_true = True

    if not any_true:
        print("  (no properties are True)")


'''
Testing: 'Hello'
  isalpha() = True
  isalnum() = True
  istitle() = True
  isascii() = True
  isprintable() = True
  isidentifier() = True

Testing: 'WORLD'
  isalpha() = True
  isalnum() = True
  isupper() = True
  isascii() = True
  isprintable() = True
  isidentifier() = True

Testing: 'Hello123'
  isalnum() = True
  istitle() = True
  isascii() = True
  isprintable() = True
  isidentifier() = True

Testing: '123'
  isdigit() = True
  isnumeric() = True
  isdecimal() = True
  isalnum() = True
  isascii() = True
  isprintable() = True

Testing: '⅕'
  isnumeric() = True
  isalnum() = True
  isprintable() = True

Testing: '³'
  isdigit() = True
  isnumeric() = True
  isalnum() = True
  isprintable() = True

Testing: '456.78'
  isascii() = True
  isprintable() = True

Testing: ' '
  isspace() = True
  isascii() = True
  isprintable() = True

Testing: ''
  isascii() = True
  isprintable() = True

Testing: 'café'
  isalpha() = True
  isalnum() = True
  islower() = True
  isprintable() = True
  isidentifier() = True

Testing (\t\n): '
'
  isspace() = True
  isascii() = True

Testing: 'MyVar'
  isalpha() = True
  isalnum() = True
  isascii() = True
  isprintable() = True
  isidentifier() = True
'''


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

print(numbers.split(',', maxsplit = 2)) # ['12', '13', '14,15,16']
'''maxsplit=2 means at most 2 splits, resulting in 3 parts.'''

#################
## Right split ##
#################

print(numbers.rsplit(',', maxsplit = 2)) # ['12,13,14', '15', '16']

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

multiline = 'Line 1\nLine 2\rLine 3\r\nLine 4'

print(multiline.splitlines()) # ['Line 1', 'Line 2', 'Line 3', 'Line 4']

print(multiline.splitlines(keepends = True)) # ['Line 1\n', 'Line 2\r', 'Line 3\r\n', 'Line 4']

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