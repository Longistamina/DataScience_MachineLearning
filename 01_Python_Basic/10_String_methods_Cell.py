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
