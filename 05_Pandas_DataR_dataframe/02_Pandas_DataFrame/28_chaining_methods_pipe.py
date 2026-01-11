'''
Chaining Methods is a technique in Pandas that allows you to apply multiple methods to a DataFrame or Series in a single line of code. This approach can make your code more concise and readable 
by reducing the need for intermediate variables.

(
    df
    .method1()
    .method2()
    .method3()
)

##################################

1. General Chaining Methods

2. Apply with .pipe() for custom functions

3. Apply with .groupby()

4. Apply with .plot() / .plot.method()

5. All-in-one workflow example
'''

import pandas as pd
import matplotlib.pyplot as plt

#-------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 1. General Chaining Methods -----------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

# Time series DataFrame
df_aq = (
    pd.read_csv("05_Pandas_DataR_dataframe/data/air_quality_no2_long.csv")
    .rename(columns={"date.utc": "date"})
    .assign(date = lambda df: pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S%z"))
)

# Time series as Series
s_aq = (
    df_aq.copy()
    .query("(country == 'FR') & (city == 'Paris')")
    .set_index("date")
    .reindex(columns=["value"])
    .squeeze() # Convert Single-Column DataFrame to Series
)


#-------------------------------------------------------------------------------------------------------------#
#--------------------------------- 2. Apply with .pipe() for custom functions --------------------------------#
#-------------------------------------------------------------------------------------------------------------#

# Example with Pokemon dataset
df_pokemon = (
    pd.read_csv(
        filepath_or_buffer="05_Pandas_DataR_dataframe/data/pokemon.csv",
        dtype={
            "Type 1": "category",
            "Type 2": "category",
            "Generation": "category",
            "Legendary": "bool"
        }
    )
    .drop(columns=["#"])
    .pipe(lambda df: df.set_axis(df.columns.str.strip().str.replace(r"\s+", "_", regex=True).str.replace(".", ""), axis=1))
    .assign(Generation = lambda df: df['Generation'].cat.as_ordered())
)

from scipy import stats

# Example with Boston Housing dataset and reframing technique
df_boston_stats = (
    pd.read_csv("05_Pandas_DataR_dataframe/data/BostonHousing.csv")
    .pipe(lambda df: df.set_axis(df.columns.str.lower(), axis=1))
    .reindex(columns=["rm", "lstat", "medv"]) # select specific columns
    .pipe(
        lambda df: pd.DataFrame(
            {
                "rm_norm": stats.norm.ppf(q=[0.25, 0.5, 0.75, 1], loc=df["rm"].mean(), scale=df["rm"].std()),
                "lstat_expon": stats.expon.ppf(q=[0.25, 0.5, 0.75, 1], scale=df["lstat"].mean()),
                "medv_gamma": stats.gamma.ppf(q=[0.25, 0.5, 0.75, 1], a=2, scale=df["medv"].mean() / 2),
            },
            index=["ppf_25th", "ppf_50th", "ppf_75th", "ppf_100th"],
        )
    )
)

print(df_boston_stats)
#             rm_norm  lstat_expon  medv_gamma
# ppf_25th   5.810726     3.640059   10.830154
# ppf_50th   6.284634     8.770435   18.908934
# ppf_75th   6.758542    17.540870   30.336306
# ppf_100th       inf          inf         inf


#-------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 3. Apply with .groupby() -------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

print(
    df_pokemon
    .groupby(by=['Type_1', 'Type_2'], dropna=True, observed=False)
    .agg(
        min_HP = ('HP', 'min'),
        max_HP = ('HP', 'max'),
        mean_HP = ('HP', 'mean')
    )
    .reset_index() # Reset index to turn the group keys into a column
)


#-------------------------------------------------------------------------------------------------------------#
#--------------------------------- 4. Apply with .plot() / .plot.method() ------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

# Using .plot()
df_pokemon.plot(
    kind="box",
    column="Attack",            # Dependent variable
    by="Generation",            # Group by "Generation" column
    notch=True,
    color="purple",             # Color of the box
    title="Box Plot of Pokemon Attack by Generation",  # Title of the plot
    ylabel="Attack",             # Label for the y-axis
    xlabel="Generation",         # Label for the x-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot

# Using .plot.method()
df_pokemon.plot.box(
    column="Attack",            # Dependent variable
    by="Generation",            # Group by "Generation" column
    notch=True,
    color="green",             # Color of the box
    title="Box Plot of Pokemon Attack by Generation",  # Title of the plot
    ylabel="Attack",             # Label for the y-axis
    xlabel="Generation",         # Label for the x-axis
    figsize=(10, 6)              # Size of the figure
)
plt.show() # Display the plot


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 5. All-in-one workflow ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

dict_subjects = {
    'Toán':'Math',
    'Ngữ văn':'Literature',
    'Địa lí':'Geography',
    'Lịch sử':'History',
    'Tiếng Anh':'English',
    'Sinh học':'Biology',
    'Vật lí':'Physics',
    'Hóa học':'Chemistry',
}

dict_translate = {
    'Nam': 'Male',
    'Nữ': 'Female',
    'Sở GDĐT Bắc Giang': 'Bac Giang DET', # DET: Dept of Education and Training
    'Sở GDĐT Hoà Bình': 'Hoa Binh DET',
    'Sở GDĐT Thừa Thiên -Huế': 'Thua Thien - Hue DET',
    'Trường Đại học Công nghiệp Tp. HCM': 'IUH' # IUH: Industrial University of Ho Chi Minh City
}

def rename_subjects(subjects_str):
    for viet, eng in dict_subjects.items():
        subjects_str = subjects_str.replace(viet, eng)
    return subjects_str

#######################

df_bac = (
    pd.read_excel("05_Pandas_DataR_dataframe/data/Baccalaureate_2016.xlsx")
    .rename(columns={ # Change column names to English
        "SOBAODANH": "ID",
        "HO_TEN": "FULL_NAME",
        "NGAY_SINH": "BIRTHDAY",
        "TEN_CUMTHI": "EXAM_LOCATION",
        "GIOI_TINH": "GENDER",
        "DIEM_THI": "SCORE",
    })
    .assign(SCORE = lambda df: df['SCORE'].apply(rename_subjects)) # Change subject names into English
    .replace(to_replace=dict_translate) # Translate other values into English
    .assign(
        BIRTHDAY = lambda df: pd.to_datetime(df['BIRTHDAY'], format='%d/%m/%Y', errors='coerce'), # Convert BIRTHDAY to datetime
        EXAM_LOCATION = lambda df: df['EXAM_LOCATION'].astype('category'), # Convert EXAM_LOCATION to category
        GENDER = lambda df: df['GENDER'].astype('category'), # Convert GENDER to category
    )
    .pipe(lambda df: # Split SCORE column into multiple subject columns
          df.assign(**{subj: df['SCORE'].str.extract(fr'{subj}:\s*(\d+\.\d+)', expand=False).astype(float) for subj in dict_subjects.values()})
    ) 
    .drop(columns=['SCORE', 'BIRTHDAY', 'EXAM_LOCATION'])
    .set_index('ID') 
)

print(df_bac.head())
#                FULL_NAME  GENDER  Math  Literature  Geography  History  English  Biology  Physics  Chemistry
# ID                                                                                                          
# 018000001  DƯƠNG VIỆT AN    Male  2.00        5.50       5.00      3.0      NaN      NaN      NaN        NaN
# 018000002      ĐỖ VĂN AN    Male  5.50        5.25       5.50      NaN     3.68      NaN      NaN        NaN
# 018000003     ĐỖ XUÂN AN    Male  4.50        5.50       3.75      NaN     2.25      NaN      NaN        NaN
# 018000004   ĐẶNG PHÚC AN  Female  3.00        6.00       5.50      NaN     1.50      NaN      NaN        NaN
# 018000005    ĐẶNG VĂN AN    Male  2.25        4.75       5.25      NaN     2.00      NaN      NaN        NaN