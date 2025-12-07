'''
1. Using df["col_name"] = ...
   + Modify existing columns: df["existing_col"] = ...
   + Add new columns: df["new_col"] = ...

2. Using df.assign()
   + Modify existing columns: df = df.assign(existing_col=lambda df: ...)
   + Add new columns: df = df.assign(new_col=...) OR df.assign(new_col=lambda df: ...)
   + Using df.assign(**kwargs) to avoid overlap with python keywords

3. Using df.eval()
   + Modify existing columns
   + Add new columns
'''

import pandas as pd
import numpy as np

df_baseball = pd.read_csv(
    filepath_or_buffer = "05_Pandas_DataR_dataframe/data/baseball.csv",
    usecols = ["Name", "Team", "Height", "Weight"],
    dtype = {"Team": "category"}
)

print(df_baseball.head(3))
#               Name Team  Height  Weight
# 0    Adam_Donachie  BAL      74     180
# 1        Paul_Bako  BAL      74     215
# 2  Ramon_Hernandez  BAL      72     210

print(df_baseball.dtypes)
# Name        object
# Team      category
# Height       int64
# Weight       int64
# dtype: object


#---------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 1. Using df["col_name"] = ... ---------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

#####################################
##     Modify existing columns     ##
#####################################
'''df["existing_col"] = ...'''

df_demo = df_baseball.copy()

# Convert Height from inches to cm
df_demo["Height"] = df_demo["Height"] * 2.54
print(df_demo.head(3))
#               Name Team  Height  Weight
# 0    Adam_Donachie  BAL  187.96     180
# 1        Paul_Bako  BAL  187.96     215
# 2  Ramon_Hernandez  BAL  182.88     210

# Convert Team to lowercase (then back to category)
df_demo["Team"] = df_demo["Team"].str.lower().astype("category")
print(df_demo.head(3))
#               Name Team  Height  Weight
# 0    Adam_Donachie  bal  187.96     180
# 1        Paul_Bako  bal  187.96     215
# 2  Ramon_Hernandez  bal  182.88     210

################################
##     Derive new columns     ##
################################
'''df["new_col"] = ...'''

df_demo = df_baseball.copy()

# Add new columns for Height in m and Weight in kg, and BMI
df_demo["Height_cm"] = df_demo["Height"] * 0.0254
df_demo["Weight_kg"] = df_demo["Weight"] * 0.453592
df_demo["BMI"] = df_demo["Weight_kg"] / (df_demo["Height_cm"] ** 2)

print(df_demo.head(3))
#               Name Team  Height  Weight  Height_cm  Weight_kg        BMI
# 0    Adam_Donachie  BAL      74     180     1.8796   81.64656  23.110376
# 1        Paul_Bako  BAL      74     215     1.8796   97.52228  27.604061
# 2  Ramon_Hernandez  BAL      72     210     1.8288   95.25432  28.480805


#---------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 2. Using df.assign() -----------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

#####################################
##     Modify existing columns     ##
#####################################
'''df = df.assign(existing_col = lambda df: ...)'''

#-----------------
## Modify a single column: Weight from lbs to kg
#-----------------

df_demo = df_baseball.copy().assign(Weight = lambda df: df["Weight"] * 0.453592)

print(df_demo.head(3))
#               Name Team  Height    Weight
# 0    Adam_Donachie  BAL      74  81.64656
# 1        Paul_Bako  BAL      74  97.52228
# 2  Ramon_Hernandez  BAL      72  95.25432

#-----------------
## Modify multiple columns: Height from inches to cm, Weight from lbs to kg, Team to lowercase
#-----------------

df_demo = df_baseball.copy().assign(
    Height = lambda df: df["Height"] * 2.54,
    Weight = lambda df: df["Weight"] * 0.453592,
    Team = lambda df: df["Team"].str.lower().astype("category")
)

print(df_demo.head(3))
#               Name Team  Height    Weight
# 0    Adam_Donachie  bal  187.96  81.64656
# 1        Paul_Bako  bal  187.96  97.52228
# 2  Ramon_Hernandez  bal  182.88  95.25432

################################
##     Derive new columns     ##
################################
'''df = df.assign(new_col = ...) OR df.assign(new_col = lambda df: ...)'''

#-----------------
## Derive single column
#-----------------

# Add Raise column with random True/False values
np.random.seed(0)
df_demo = df_baseball.copy().assign(Raise = np.random.choice([True, False], size=len(df_baseball)))
print(df_demo.head(3))
#               Name Team  Height  Weight  Raise
# 0    Adam_Donachie  BAL      74     180   True
# 1        Paul_Bako  BAL      74     215  False
# 2  Ramon_Hernandez  BAL      72     210  False

# Add BMI column
df_demo = df_baseball.copy().assign(BMI = lambda df: df["Weight"] / (df["Height"] ** 2))
print(df_demo.head(3))
#               Name Team  Height  Weight       BMI
# 0    Adam_Donachie  BAL      74     180  0.032871
# 1        Paul_Bako  BAL      74     215  0.039262
# 2  Ramon_Hernandez  BAL      72     210  0.040509

#-----------------
## Derive multiple columns
#-----------------

# Add Height in cm, Weight in kg, and BMI columns
df_demo = df_baseball.copy().assign(
    Height_cm = lambda df: df["Height"] * 2.54,
    Weight_kg = lambda df: df["Weight"] * 0.453592,
    BMI = lambda df: df["Weight_kg"] / (df["Height_cm"] ** 2)
)

print(df_demo.head(3))
#               Name Team  Height  Weight  Height_cm  Weight_kg       BMI
# 0    Adam_Donachie  BAL      74     180     187.96   81.64656  0.002311
# 1        Paul_Bako  BAL      74     215     187.96   97.52228  0.002760
# 2  Ramon_Hernandez  BAL      72     210     182.88   95.25432  0.002848

#####################################################################
## Using df.assign(**kwargs) to avoid overlap with python keywords ##
#####################################################################
'''df = df.assign(**{keyword_col = ...}) OR df.assign(**{keyword_col = lambda df: ...})'''

#--------------------
## Add "raise" column (keyword conflict with Python)
#--------------------

np.random.seed(0)
df_demo = df_baseball.copy().assign(**{"raise": np.random.choice([True, False], size=len(df_baseball))})

print(df_demo.head(3))
#               Name Team  Height  Weight  raise
# 0    Adam_Donachie  BAL      74     180   True
# 1        Paul_Bako  BAL      74     215  False
# 2  Ramon_Hernandez  BAL      72     210  False

#--------------------
## Multiple columns
#--------------------

# Add Height in cm, Weight in kg, and BMI columns
# Also modify "Team" to lowercase

df_demo = df_baseball.copy().assign(**{
    "height_cm": lambda df: df["Height"] * 2.54,
    "weight_kg": lambda df: df["Weight"] * 0.453592,
    "bmi": lambda df: df["weight_kg"] / (df["height_cm"] ** 2),
    "Team": lambda df: df["Team"].str.lower().astype("category")
})

print(df_demo.head(3))
#               Name Team  Height  Weight  height_cm  weight_kg       bmi
# 0    Adam_Donachie  bal      74     180     187.96   81.64656  0.002311
# 1        Paul_Bako  bal      74     215     187.96   97.52228  0.002760
# 2  Ramon_Hernandez  bal      72     210     182.88   95.25432  0.002848

#------------------
## Apply for loops **{col: lambda df: ... for col in cols}
#------------------

print(
    df_baseball
    .copy()
    .assign(**{col: lambda df: df[col].astype(float) for col in ["Height", "Weight"]})
    .head(5)
)
#               Name       Team    Height    Weight
#           <object> <category> <float64> <float64>
# 0    Adam_Donachie        BAL     180.0     180.0
# 1        Paul_Bako        BAL     215.0     215.0
# 2  Ramon_Hernandez        BAL     210.0     210.0
# 3     Kevin_Millar        BAL     210.0     210.0
# 4      Chris_Gomez        BAL     188.0     188.0


#---------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 3. Using df.eval() ------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

'''
Support operators: +, -, *, /, //, %, ** and parentheses () for grouping.

If the column name has special characters => put in backticks ``: `variable name` (like SQL style)

Can use @ to reference variables outside the DataFrame like: @variable_name.
'''

inch_to_m = 0.0254
lbs_to_kg = 0.453592

#####################################
##     Modify existing columns     ##
#####################################
'''df.eval("existing_col = ...", inplace=True/False)'''

#-----------------
## Modify a single column: Weight from lbs to kg
#-----------------

df_demo = df_baseball.copy().eval("Weight = Weight * @lbs_to_kg", inplace=False)
print(df_demo.head(3))
#               Name Team  Height    Weight
# 0    Adam_Donachie  BAL      74  81.64656
# 1        Paul_Bako  BAL      74  97.52228
# 2  Ramon_Hernandez  BAL      72  95.25432

#-----------------
## Modify multiple columns
#-----------------

df_demo = df_baseball.copy().eval(
    """
    Height = Height * @inch_to_m
    Weight = Weight * @lbs_to_kg
    Team = Team.str.lower().astype('category')
    """
)

print(df_demo.head(3))
#               Name Team  Height    Weight
# 0    Adam_Donachie  bal  1.8796  81.64656
# 1        Paul_Bako  bal  1.8796  97.52228
# 2  Ramon_Hernandez  bal  1.8288  95.25432

################################
##     Derive new columns     ##
################################
'''df.eval("new_col = ...", inplace = True/False)'''

#-----------------
## Derive single column (apply ``)
#-----------------

df_demo = df_baseball.copy().eval("BMI = `Weight` / (`Height` ** 2)", inplace = False)
print(df_demo.head(3))
#               Name Team  Height  Weight       BMI
# 0    Adam_Donachie  BAL      74     180  0.032871
# 1        Paul_Bako  BAL      74     215  0.039262
# 2  Ramon_Hernandez  BAL      72     210  0.040509

#-----------------
## Derive multiple columns
#-----------------

df_demo = df_baseball.copy().eval(
    """
    height_m = Height * @inch_to_m
    weight_kg = Weight * @lbs_to_kg
    bmi = weight_kg / (height_m ** 2)
    """,
    inplace = False
)

print(df_demo.head(3))
#               Name Team  Height  Weight  height_m  weight_kg        bmi
# 0    Adam_Donachie  BAL      74     180    1.8796   81.64656  23.110376
# 1        Paul_Bako  BAL      74     215    1.8796   97.52228  27.604061
# 2  Ramon_Hernandez  BAL      72     210    1.8288   95.25432  28.480805