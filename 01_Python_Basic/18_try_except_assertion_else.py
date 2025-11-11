#-----------------------------------------------#
#----------------- try except ------------------#
#-----------------------------------------------#

try:
    int_number = int(input("Input an integer number: "))
except ValueError:
    print(">>> Error: Your input is not numeric!!!!")
else:
    print("Your input is an integer")


#----------------------------------------------#
#---------- try except Exception --------------#
#----------------------------------------------#

number = 3

try:
    number / 0
except ValueError:
    print(">>> Something wrong!!!")
else:
    print("Your code has no error")
# Output: raised ZeroZeroDivisionError

## Python has many types of error: ArithmeticError, BaseException, EnvironmentError, ...
## can use "except Exception" to capture all errors that being raised

number = 0

try:
    number / 0
except Exception:
    print(">>> Something wrong!!!")
else:
    print("Your code has no error")
# Output: ">>> Something wrong!!!"


#####################################
## Exception as .... Error as .... ##
#####################################

try:
    9 / 0
except Exception as e:
    print(f">>> Error: {e}")
else:
    print("Your code has no error")

# Output: ">>> Error: division by zero"


#------------------------------------------------------#
#---------- assert except AssertionError --------------#
#------------------------------------------------------#

try:
    float_positive = float(input("Input a positive float number: "))

    assert float_positive > 0

except ValueError:
    print(">>> Error: your input is not numeric!")
except AssertionError:
    print(">>> Error: your float is not positive!")
else:
    print("Your input is right!")


#########################    
## multiple Assertions ##
#########################

try:
    number = float(input("Input a positive float number: "))

    assert number > 0, f"Your input {number} is not > 0"
    assert number > 5, f"Your input {number} is not > 5"
    assert number > 10, f"Your input {number} is not > 10"
    assert number > 15, f"Your input {number} is not > 15"

except ValueError:
    print(">>> Error: your input is not numeric!")
except AssertionError as e:
    print(">>> Error: one assertion is not satisfied!")
    print(f">>> {e}")
else:
    print(f"Your input {number} passes all Assertions")

    