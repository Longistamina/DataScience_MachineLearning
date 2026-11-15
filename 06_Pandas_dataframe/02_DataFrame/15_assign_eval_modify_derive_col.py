'''
1. Using df["col_name"] = ...
   + Modify existing columns: df["existing_col"] = ...
   + Add new columns: df["new_col"] = ...

2. Using df.assign()
   + Modify existing columns: df = df.assign(existing_col=lambda df: ...)
   + Add new columns: df = df.assign(new_col=...)
                      OR df.assign(new_col=c("existing_col")...)
                      OR df.assign(new_col=lambda df: ...)
   + Using df.assign(**kwargs) to avoid overlap with python keywords

3. Using df.eval()
   + Modify existing columns
   + Add new columns
'''

from pathlib import Path

import numpy as np
import pandas as pd
from pandas import col as c

data_dir = Path.home().rglob("*/DataScience_MachineLearning/data")
data_dir = next(data_dir)

df_baseball = (
    pd.read_csv(
        filepath_or_buffer=data_dir/"baseball.csv",
        usecols=["Name", "Team", "Height", "Weight"],
        dtype={"Team": "category"}
    )
    .rename(columns=lambda col: col.lower())
)

print(df_baseball.head(3))
#               name team  height  weight
# 0    Adam_Donachie  BAL      74     180
# 1        Paul_Bako  BAL      74     215
# 2  Ramon_Hernandez  BAL      72     210

print(df_baseball.dtypes)
# name           str
# team      category
# height       int64
# weight       int64
# dtype: object

# =========================================================================================
# 1. Using df["col_name"] = ...
# =========================================================================================

##---------------------------------##
##     Modify existing columns     ##
##---------------------------------##
'''df["existing_col"] = ...'''

df_demo = df_baseball.copy()

# Convert Height from inches to cm
df_demo["height"] = df_demo["height"] * 0.0254
print(df_demo.head(3))
#               name team  height  weight  Raise
# 0    Adam_Donachie  BAL  1.8796     180  False
# 1        Paul_Bako  BAL  1.8796     215  False
# 2  Ramon_Hernandez  BAL  1.8288     210  False

# Convert Team to lowercase (then back to category)
df_demo["team"] = df_demo["team"].str.lower().astype("category")
print(df_demo.head(3))
#               name team  height  weight
# 0    Adam_Donachie  bal  1.8796     180
# 1        Paul_Bako  bal  1.8796     215
# 2  Ramon_Hernandez  bal  1.8288     210

##----------------------------##
##     Derive new columns     ##
##----------------------------##
'''df["new_col"] = ...'''

df_demo = df_baseball.copy()

# Add new columns for Height in m and Weight in kg, and BMI
df_demo["height_m"] = df_demo["height"] * 0.0254
df_demo["weight_kg"] = df_demo["weight"] * 0.453592
df_demo["bmi"] = df_demo["weight_kg"] / (df_demo["height_m"] ** 2)

print(df_demo.head(3))
#               name team  height  weight  height_m  weight_kg        bmi
# 0    Adam_Donachie  BAL      74     180    1.8796   81.64656  23.110376
# 1        Paul_Bako  BAL      74     215    1.8796   97.52228  27.604061
# 2  Ramon_Hernandez  BAL      72     210    1.8288   95.25432  28.480805

# =========================================================================================
# 2. Using df.assign()
# =========================================================================================

##---------------------------------##
##     Modify existing columns     ##
##---------------------------------##
'''df = df.assign(existing_col = lambda df: ...)'''

# Modify a single column: Weight from lbs to kg #
print(
    df_baseball
    .assign(weight = c('weight') * 0.453592)
    .head(3)
)
#               name team  height    weight
# 0    Adam_Donachie  BAL      74  81.64656
# 1        Paul_Bako  BAL      74  97.52228
# 2  Ramon_Hernandez  BAL      72  95.25432

# Modify multiple columns: Height from inches to cm, Weight from lbs to kg, Team to lowercase
print(
   df_baseball
  .assign(
      height = c('height') * 0.0254, # or use lambda df: df["height"] * 0.0254
      weight = c("weight") * 0.453592, # or use lambda df: df["weight"] * 0.453592
      team = c("team").str.lower().astype("category") # or use lambda df: df["team"].str.lower().astype("category")
  )
  .head(3)
)
#               name team  height    weight
# 0    Adam_Donachie  bal  1.8796  81.64656
# 1        Paul_Bako  bal  1.8796  97.52228
# 2  Ramon_Hernandez  bal  1.8288  95.25432

##----------------------------##
##     Derive new columns     ##
##----------------------------##
'''df = df.assign(new_col = ...) OR df.assign(new_col = lambda df: ...)'''

# Derive single column
np.random.seed(0)
print(
    df_baseball
    .assign(Raise = np.random.choice([True, False], size=len(df_baseball)))
    .head(3)
)
#               name team  height  weight  Raise
# 0    Adam_Donachie  BAL      74     180   True
# 1        Paul_Bako  BAL      74     215  False
# 2  Ramon_Hernandez  BAL      72     210  False

# Derive multiple columns
print(
    df_baseball
    .assign(
        height_m = c("height") * 0.0254,
        weight_kg = c("weight") * 0.453592,
        bmi = c("weight_kg") / (c("height_m") ** 2)
    )
    .head(3)
)
#               name team  height  weight   height_m  weight_kg       bmi
# 0    Adam_Donachie  BAL      74     180     1.8796   81.64656  0.002311
# 1        Paul_Bako  BAL      74     215     1.8796   97.52228  0.002760
# 2  Ramon_Hernandez  BAL      72     210     1.8288   95.25432  0.002848

##-----------------------------------------------------------------##
## Using df.assign(**kwargs) to avoid overlap with python keywords ##
##-----------------------------------------------------------------##
'''df = df.assign(**{keyword_col = ...}) OR df.assign(**{keyword_col = lambda df: ...})'''

# Add "raise" column (keyword conflict with Python)
np.random.seed(0)
print(
    df_baseball
    .assign(**{'raise': np.random.choice([True, False], size=len(df_baseball))})
    .head(3)
)
#               name team  height  weight  raise
# 0    Adam_Donachie  BAL      74     180   True
# 1        Paul_Bako  BAL      74     215  False
# 2  Ramon_Hernandez  BAL      72     210  False

# Multiple columns (NOT RECOMMENDED)
print(
    df_baseball
    .assign(**{
        "height_m": c("height") * 0.0254,
        "weight_kg": c("weight") * 0.453592,
        "bmi": c("weight_kg") / (c("height_m") ** 2),
        "team": c("team").str.lower().astype("category")
    })
    .head(3)
)
#               name team  height  weight  height_m  weight_kg        bmi
# 0    Adam_Donachie  bal      74     180    1.8796   81.64656  23.110376
# 1        Paul_Bako  bal      74     215    1.8796   97.52228  27.604061
# 2  Ramon_Hernandez  bal      72     210    1.8288   95.25432  28.480805

# Apply for loops **{col: pd.col(col)... for col in cols}
print(
    df_baseball
    .assign(**{col: c(col).astype(float) for col in ["height", "weight"]})
    .head(5)
)
#               name       team    height    weight
#           <object> <category> <float64> <float64>
# 0    Adam_Donachie        BAL     180.0     180.0
# 1        Paul_Bako        BAL     215.0     215.0
# 2  Ramon_Hernandez        BAL     210.0     210.0
# 3     Kevin_Millar        BAL     210.0     210.0
# 4      Chris_Gomez        BAL     188.0     188.0

# =========================================================================================
# 3. Using df.eval()
# =========================================================================================
'''
Support operators: +, -, *, /, //, %, ** and parentheses () for grouping.

If the column name has special characters => put in backticks ``: `variable name` (like SQL style)

Can use @ to reference variables outside the DataFrame like: @variable_name.
'''

inch_to_m = 0.0254
lbs_to_kg = 0.453592

##---------------------------------##
##     Modify existing columns     ##
##---------------------------------##
'''df.eval("existing_col = ...", inplace=True/False)'''

# Modify a single column: Weight from lbs to kg
print(
    df_baseball
    .eval('weight = weight * @lbs_to_kg')
    .head(3)
)
#               name team  height    weight
# 0    Adam_Donachie  BAL      74  81.64656
# 1        Paul_Bako  BAL      74  97.52228
# 2  Ramon_Hernandez  BAL      72  95.25432

# Modify multiple columns
print(
    df_baseball
    .eval(
        """
        height = height * @inch_to_m
        weight = weight * @lbs_to_kg
        team = team.str.lower().astype('category')
        """
    )
    .head(3)
)
#               name team  height    weight
# 0    Adam_Donachie  bal  1.8796  81.64656
# 1        Paul_Bako  bal  1.8796  97.52228
# 2  Ramon_Hernandez  bal  1.8288  95.25432

##----------------------------##
##     Derive new columns     ##
##----------------------------##
'''df.eval("new_col = ...", inplace = True/False)'''

# Derive single column (apply ``)
print(
    df_baseball
    .eval('bmi = `weight` / (`height` ** 2)')
    .head(3)
)
#               name team  height  weight       bmi
# 0    Adam_Donachie  BAL      74     180  0.032871
# 1        Paul_Bako  BAL      74     215  0.039262
# 2  Ramon_Hernandez  BAL      72     210  0.040509

# Derive multiple columns
print(
   df_baseball
   .eval(
       '''
       height_m = height * @inch_to_m
       weight_kg = weight * @lbs_to_kg
       bmi = weight_kg / (height_m ** 2)
       '''
   )
   .head(3)
)
#               name team  height  weight  height_m  weight_kg        bmi
# 0    Adam_Donachie  BAL      74     180    1.8796   81.64656  23.110376
# 1        Paul_Bako  BAL      74     215    1.8796   97.52228  27.604061
# 2  Ramon_Hernandez  BAL      72     210    1.8288   95.25432  28.480805
