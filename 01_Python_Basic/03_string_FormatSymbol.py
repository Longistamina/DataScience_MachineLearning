salary = 5000 # integer (số nguyên)
salary_coefficient = 1.475 # float (số thực)
full_name = "Tran Ngoc Dung" # character / string

print("-" * 50)

# ==============================================================================================
# 1. Format Symbol 1 (C-style)
# ==============================================================================================

strTT1 = "Full name: " + full_name + "\nSalary: " + str(salary)
print(strTT1)
# Full name: Tran Ngoc Dung
# Salary: 5000

strTT2 = "Full name: %s \nSalary: %i \nSalary coefficient: %f"%(full_name, salary, salary_coefficient)
print(strTT2)
# Full name: Tran Ngoc Dung
# Salary: 5000
# Salary coefficient: 1.475000

strTT3 = "Full name: %s \nSalary: %i \nSalary coefficient: %.2f"%(full_name, salary, salary_coefficient)
print(strTT3)
# Full name: Tran Ngoc Dung
# Salary: 5000
# Salary coefficient: 1.48


# ==============================================================================================
# 2. Format Symbol 2 (new style)
# ==============================================================================================

str1 = f'Full name: {full_name}\n Salary: {salary}\n Salary coefficient: {salary_coefficient}'
print(str1)
# Full name: Tran Ngoc Dung
#  Salary: 5000
#  Salary coefficient: 1.475

# Add comma "," as a thousand separator for salary, and round the salary_coefficient up to 2 decimal numbers
str2 = f'Full name: {full_name}\n Salary: {salary:,} VND\n Salary coefficient: {salary_coefficient:.2f}'
print(str2)
# Full name: Tran Ngoc Dung
#  Salary: 5,000 VND
#  Salary coefficient: 1.48

# Add comma "," as a thousand separator for salary, and round the salary up to 2 decimal numbers
str3 = f'Full name: {full_name}\n Salary: {salary:,.2f} VND\n Salary coefficient: {salary_coefficient}'
print(str3)
# Full name: Tran Ngoc Dung
#  Salary: 5,000.00 VND
#  Salary coefficient: 1.475

# Use ``.ne`` for scientific notation
str4 = f'Full name: {full_name}\n Salary: {salary:.2e} VND\n Salary coefficient: {salary_coefficient:.2e}'
print(str4)
# Full name: Tran Ngoc Dung
#  Salary: 5.00e+03 VND
#  Salary coefficient: 1.48e+00
