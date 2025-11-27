# Operators = toán tử

'''
a + b
a - b
a * b
a ** b -> a exponential b times (ex: 7**3 = 7*7*7 = 343)
a / b  -> conventional division
a % b  -> get the remainer (chia lay phan du)
a // b -> get the quotient (chia lay phan nguyen)
'''

#####################################################################

'''
a == b #-> equal comparision
a != b #-> inequal comparision
>      #-> greater
<      #-> less
>=     #-> equal or greater
<=     #-> equal or less
Comparsion returns  True or False
'''

#####################################################################

'''
Chain (Between) Comparisons
a < b < c
a <= b < c
a < b <= c
a <= b <= c
'''

#####################################################################

'''
a += b is equivalent to a = a + b
a *= b is equivalent to a = a * b
'''

#####################################################################

''' LOGIC
not - ~: negation
and - &: return True only when all are True
or  - |: return False only when all are False

Logic Precedence Order: not -> and -> or
(menaing NOT logic has the highest precedence, AND logic is next, OR logic has the lowest precedence)

Example:
A = True
B = False
C = True
result = A or B and C
       = A or (B and C)  # because AND has higher precedence than OR
       = A or False
       = True or False
       = True

=> That's why we should use parentheses () to explicitly specify the order of operations 
when combining multiple logical operators.

For example: (A or B) and C
'''

#####################################################################

''' IN NOT-IN
in -> return True if an element is in an interator (Example: 'k'  in 'dek')
not in -> return True if an element is not in an iterator (Example: 'k' not  in 'abc')
'''
