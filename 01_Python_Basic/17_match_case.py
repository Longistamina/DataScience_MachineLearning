'''
The match-case statement was introduced in Python 3.10 as a powerful alternative to lengthy if-elif-else chains, 
similar to switch-case statements in other programming languages.

This feature enables structural pattern matching and makes code more readable and maintainable


match expression:
    case pattern1:
        # code block 1
    case pattern2:
        # code block 2
    case _:
        # default case (optional)

"case _" works like "else", it catches all the remaining situations
'''

#----------------------------------------------------------#
#----------------- Example 1: input operator --------------#
#----------------------------------------------------------#

operator = input("Enter an operator: ")
x = 5
y = 10

match operator:
    case '+':
        result = x + y
    case '-':
        result = x - y
    case '*':
        result = x * y
    case '/':
        result = x / y
    case _:
        result = "Invalid operator"

print(result)


#---------------------------------------------------------#
#------------ Example 2: def and match-case --------------#
#---------------------------------------------------------#

def weekday(n):
    match n:
        case 0:
            return "Monday"
        case 1:
            return "Tuesday"
        case 2:
            return "Wednesday"
        case 3:
            return "Thursday"
        case 4:
            return "Friday"
        case 5:
            return "Saturday"
        case 6:
            return "Sunday"
        case _:
            return "Invalid day number"

print(weekday(3))  # Output: Thursday
print(weekday(6))  # Output: Sunday
print(weekday(7))  # Output: Invalid day number


#---------------------------------------------------------#
#------------ Example 3: combine values ------------------#
#---------------------------------------------------------#

def classify_grade(grade):
    match grade:
        case 10 | 9:
            return "Excellent"
        case 8 | 7:
            return "Good"
        case 6 | 5:
            return "Average"
        case 4 | 3 | 2 | 1 | 0:
            return "Poor"
        case _:
            return "Invalid grade"

print(classify_grade(10))  # Output: Excellent
print(classify_grade(7))   # Output: Good


#----------------------------------------------------------#
#------------ Example 4: match case with if ---------------#
#----------------------------------------------------------#

month = int(input("Enter month number (1-12): "))
day = int(input("Enter day number (1-31): "))

match day:
  case 1 | 2 | 3 | 4 | 5 if month == 4:
    print("A weekday in April")
  case 1 | 2 | 3 | 4 | 5 if month == 5:
    print("A weekday in May")
  case _:
    print("No match")

# Output: A weekday in May
