#%%
s1 = '  it CenteR one   '
k1 = s1.capitalize() #=> '  It CenteR one   '    capitalize the first character of the string
k2 = s1.upper()      #=> '  IT CENTER ONE   '    capitalize all characters
k3 = s1.lower()      #=> '  it center one   '    decapitalize all characters
k4 = s1.title()      #=> '  It CenteR One   '    capitalize the first character of each word
k6 = s1.strip()      #=> 'it CenteR One'         remove the space character ' ' from both ends
print()

s2 = ',20 30,'
k7 = s2.strip(',') #=> '20 30' remove ',' character from both ends

#---------------------------------- Count --------------------------------------------------------------#
#%%
poem = '''
Shall I compare thee to a summer’s day?
Thou art more lovely and more temperate:
Rough winds do shake the darling buds of May,
And summer’s lease hath all too short a date;
Sometime too hot the eye of heaven shines,
And often is his gold complexion dimm'd;
And every fair from fair sometime declines,
By chance or nature’s changing course untrimm'd;
But thy eternal summer shall not fade,
Nor lose possession of that fair thou ow’st;
Nor shall death brag thou wander’st in his shade,
When in eternal lines to time thou grow’st:
So long as men can breathe or eyes can see,
So long lives this, and this gives life to thee.
'''
print(poem)
print(poem.count('n'))
print(poem.lower().count('n'))
#method count() distinguished uppercase from lowercase, therefor poem.count('n') and poem.lower().count('n') give different results

title = 'SHAKESPEAR SONNET 18'
print(title.count('S',2,10)) #Count the number of character 'S' from index 2 to index 10-1 (or index 9) of the string

#---------------FIND AND REPLACE--------------#
#%%
str = 'Hoa Chanh nở giữa vườn Chanh'
strFind = 'Chanh'
strReplace = 'Cam'
strNew = str.replace(strFind, strReplace)
strNew2 = str.replace(strFind, strReplace, 1) #Replace only one time at the first matched result
print(strNew)

#------------------------------------------------#
#%%
full_name = 'Tran Thi Anh Thu'
i = full_name.find(' ') #Find the first ' ' character from left to right, and return its index
j = full_name.find(' ', i+1) #Find ' ' character from index i to end
k = full_name.rfind(' ') #Find the first ' ' character from RIGHT to left, and return its index
print()

# %%
phone = '0903123456'
k1 = phone.isdigit() #=> True if all characters are DIGITS. Else if there is at least one alphabetic character, return False
k2 = phone.isnumeric() #=> True if all characters are NUMERIC. Else if there is at least one alphabetic character, return False

money = '1500VND'
id = 'ASDK'
k3 = money.isalpha() #=> True if all characters are ALPHABETIC. Else if there is at least one numeric or digit character, return False
k4 = id.isalpha() #=> T
k5 = money.isalnum() #=> True if all the characters are alphanumeric (like "Company123", "4student5")
k6 = id.isupper() #=> T
k7 = id.islower()#=> F

#%%
#------------- .format()---------------#
price = 1200000000.453
str_price1 = '{:,} VND'.format(price) # '1,200,000,000.453 VND'
str_price2 = '{:,.2f} VND'.format(price) # '1,200,000,000.45 VND'
# .format() method formats the specified value(s) and insert them inside the string's placeholder {}.
print()

#%%
#---------------- Marginalize (canle) --------------------#
strD = 'Abc'
str1 = strD.center(20)     #'        Abc         '
str2 = strD.center(20,'*') #'********Abc*********'
str3 = strD.rjust(20) #Marginalize towards the RIGHT with the width of 20 characters
str4 = strD.ljust(20) #Marginalize towards the LEFT with the width of 20 characters

#-------------- SPLIT ------------------#
#%%
full_name = 'Arthur Conan Doyle'
str1 = full_name.split() # => ['Arthur', 'Conan', 'Doyle']

numbers = '12,13,14,15,16'
str2 = numbers.split(',') # => ['12', '13', '14', '15', '16']
str3 = numbers.split(',', maxsplit=2) # => ['12', '13', '14,15,16']
print()

#--------------JOIN-----------------#
#%%
lst = ['A','B','C','D','E']
str1 = ''.join(lst)   # 'ABCDE'
str2 = ' '.join(lst)  # 'A B C D E'
str3 = ','.join(lst)  # 'A,B,C,D,E'
print()

 
'''                                ALL STRING METHODS
---------------------------------------------------------------------------------------------
capitalize()                      Return a copy with the first character uppercased and the rest lowercased. [1]
casefold()                        Return a case-folded copy for caseless matching, more aggressive than lower(). [1]
center(width, fillchar)           Return a centered string of length width, padded with fillchar (default space). [1]
count(sub, start, end)            Return number of non-overlapping occurrences of sub between start and end. [1]
encode(encoding, errors)          Return an encoded bytes version using specified encoding (default 'utf-8'). [1]
endswith(suffix, start, end)      Return True if string ends with suffix within optional bounds. [1]
expandtabs(tabsize)               Replace tabs in the string with spaces; default tab size is 8. [1]
find(sub, start, end)             Return lowest index of sub or -1 if not found within optional bounds. [1]
format(*args, **kwargs)           Perform advanced positional and keyword-based string formatting. [1]
format_map(mapping)               Like format(), but takes a single mapping object for substitutions. [1]
index(sub, start, end)            Like find(), but raises ValueError if sub is not found. [1]
isalnum()                         Return True if all characters are alphanumeric and string is non-empty. [1]
isalpha()                         Return True if all characters are alphabetic and string is non-empty. [1]
isascii()                         Return True if all characters in the string are ASCII (code point < 128). [1]
isdecimal()                       Return True if all characters are decimal characters and string is non-empty. [1]
isdigit()                         Return True if all characters are digits and string is non-empty. [1]
isidentifier()                    Return True if string is a valid Python identifier. [1]
islower()                         Return True if all cased characters are lowercase and at least one cased char exists. [1]
isnumeric()                       Return True if all characters are numeric and string is non-empty. [1]
isprintable()                     Return True if all characters are printable or the string is empty. [1]
isspace()                         Return True if all characters are whitespace and string is non-empty. [1]
istitle()                         Return True if string is titlecased (each word starts with uppercase). [1]
isupper()                         Return True if all cased characters are uppercase and at least one cased char exists. [1]
join(iterable)                    Concatenate an iterable of strings, placing this string between elements. [1]
ljust(width, fillchar)            Return a left-justified string of length width, padded with fillchar. [1]
lower()                           Return a copy with all characters converted to lowercase. [1]
lstrip(chars)                     Return a copy with leading characters removed (whitespace by default). [1]
maketrans(x, y, z)                Return a translation table usable for translate(). [1]
partition(sep)                    Split at first occurrence of sep into a 3-tuple: (head, sep, tail). [1]
removeprefix(prefix)              Return a copy with the specified prefix removed if present. [1]
removesuffix(suffix)              Return a copy with the specified suffix removed if present. [1]
replace(old, new, count)          Return a copy with all occurrences of old replaced by new (limit count). [1]
rfind(sub, start, end)            Return highest index of sub or -1 if not found within optional bounds. [1]
rindex(sub, start, end)           Like rfind(), but raises ValueError if sub is not found. [1]
rjust(width, fillchar)            Return a right-justified string of length width, padded with fillchar. [1]
rpartition(sep)                   Split at last occurrence of sep into a 3-tuple: (head, sep, tail). [1]
rsplit(sep, maxsplit)             Split from the right on sep at most maxsplit times; return list of substrings. [1]
rstrip(chars)                     Return a copy with trailing characters removed (whitespace by default). [1]
split(sep, maxsplit)              Split on sep at most maxsplit times; return a list of substrings. [1]
splitlines(keepends)              Split at line boundaries; if keepends is True, line breaks are included. [1]
startswith(prefix, start, end)    Return True if string starts with prefix within optional bounds. [1]
strip(chars)                      Return a copy with leading and trailing characters removed (whitespace by default). [1]
swapcase()                        Return a copy with uppercase characters lowercased and vice versa. [1]
title()                           Return a titlecased copy: each word starts with uppercase, others lowercase. [1]
translate(table)                  Return a copy where each character is mapped through the translation table. [1]
upper()                           Return a copy with all characters converted to uppercase. [1]
zfill(width)                      Return a numeric string left-filled with zeros to length width. [1]
'''