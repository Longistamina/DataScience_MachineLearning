from pathlib import Path

import pandas as pd
from pandas import col as c

pd.set_option("display.width", 120)

data_dir = Path.home().rglob("*/DataScience_MachineLearning/data")
data_dir = next(data_dir)

# =========================================================================================
# Step-by-step workflow
# =========================================================================================

##------------------##
### Read Excel file ##
##------------------##

df_bac = (
    pd.read_excel(data_dir/"Baccalaureate_2016.xlsx")
    .rename(columns={ # Change column names to English
        "SOBAODANH": "ID",
        "HO_TEN": "FULL_NAME",
        "NGAY_SINH": "BIRTHDAY",
        "TEN_CUMTHI": "EXAM_LOCATION",
        "GIOI_TINH": "GENDER",
        "DIEM_THI": "SCORE",
    })
)

print(df_bac.info())
# <class 'pandas.DataFrame'>
# RangeIndex: 34826 entries, 0 to 34825
# Data columns (total 6 columns):
#  #   Column         Non-Null Count  Dtype
# ---  ------         --------------  -----
#  0   ID             34826 non-null  str
#  1   FULL_NAME      34826 non-null  str
#  2   BIRTHDAY       34826 non-null  str
#  3   EXAM_LOCATION  34826 non-null  str
#  4   GENDER         34826 non-null  str
#  5   SCORE          34826 non-null  str
# dtypes: str(6)
# memory usage: 6.7 MB
# None

##----------------------------------##
## Change subject name into English ##
##----------------------------------##

dict_subjects = {
    'Toán': 'Math',
    'Ngữ văn': 'Literature',
    'Địa lí': 'Geography',
    'Lịch sử': 'History',
    'Tiếng Anh': 'English',
    'Sinh học': 'Biology',
    'Vật lí': 'Physics',
    'Hóa học': 'Chemistry',
}

# df_bac['SCORE'] = df_bac["SCORE"].replace(dict_subjects, regex=True)
df_bac = df_bac.assign(SCORE = c('SCORE').replace(dict_subjects, regex=True))

print(df_bac['SCORE'].head(3))
# 0    Math:   2.00   Literature:   5.50   History:  ...
# 1    Math:   5.50   Literature:   5.25   Geography:...
# 2    Math:   4.50   Literature:   5.50   Geography:...
# Name: SCORE, dtype: object

##----------------------------------##
## Change other values into English ##
##----------------------------------##

print(df_bac['GENDER'].unique())
# ['Nam' 'Nữ']

print(df_bac['EXAM_LOCATION'].unique())
# ['Sở GDĐT Bắc Giang' 'Sở GDĐT Hoà Bình' 'Sở GDĐT Thừa Thiên -Huế', 'Trường Đại học Công nghiệp Tp. HCM']

dict_translate = {
    'Nam': 'Male',
    'Nữ': 'Female',
    'Sở GDĐT Bắc Giang': 'Bac Giang DET', # DET: Dept of Education and Training
    'Sở GDĐT Hoà Bình': 'Hoa Binh DET',
    'Sở GDĐT Thừa Thiên -Huế': 'Thua Thien - Hue DET',
    'Trường Đại học Công nghiệp Tp. HCM': 'IUH' # IUH: Industrial University of Ho Chi Minh City
}

df_bac = (
    df_bac
    .replace(to_replace=dict_translate) # Translate values into English
    .assign(
        BIRTHDAY = lambda df: pd.to_datetime(df['BIRTHDAY'], format='%d/%m/%Y', errors='coerce'), # Convert BIRTHDAY to datetime
        EXAM_LOCATION = c('EXAM_LOCATION').astype('category'), # Convert EXAM_LOCATION to category
        GENDER = c('GENDER').astype('category'), # Convert GENDER to category
    )
)

print(df_bac.head())
# ID   FULL_NAME   BIRTHDAY  EXAM_LOCATION  GENDER                                              SCORE
# 0  ID_00001  NAME_00001 1998-01-16  Bac Giang DET    Male  Math:   2.00   Literature:   5.50   History:  ...
# 1  ID_00002  NAME_00002 1998-05-20  Bac Giang DET    Male  Math:   5.50   Literature:   5.25   Geography:...
# 2  ID_00003  NAME_00003 1998-03-02  Bac Giang DET    Male  Math:   4.50   Literature:   5.50   Geography:...
# 3  ID_00004  NAME_00004 1998-02-15  Bac Giang DET  Female  Math:   3.00   Literature:   6.00   Geography:...
# 4  ID_00005  NAME_00005 1998-06-23  Bac Giang DET    Male  Math:   2.25   Literature:   4.75   Geography:...

print(df_bac.info())
# <class 'pandas.DataFrame'>
# RangeIndex: 34826 entries, 0 to 34825
# Data columns (total 6 columns):
#  #   Column         Non-Null Count  Dtype
# ---  ------         --------------  -----
#  0   ID             34826 non-null  str
#  1   FULL_NAME      34826 non-null  str
#  2   BIRTHDAY       34806 non-null  datetime64[us]
#  3   EXAM_LOCATION  34826 non-null  category
#  4   GENDER         34826 non-null  category
#  5   SCORE          34826 non-null  str
# dtypes: category(2), datetime64[us](1), str(3)
# memory usage: 4.5 MB
# None

##-------------------------------##
## Check invalid BIRTHDAY values ##
##-------------------------------##

s_birthday = (
    pd.read_excel(data_dir/"Baccalaureate_2016.xlsx", usecols=['NGAY_SINH'])
    .rename(columns={"NGAY_SINH": "BIRTHDAY"})
    .squeeze() # Convert single-column DataFrame to Series
)
print(s_birthday)
# 0        16/01/1998
# 1        20/05/1998
# 2        02/03/1998
# 3        15/02/1998
# 4        23/06/1998
#             ...
# 34821    26/12/1998
# 34822    11/04/1998
# 34823    13/10/1998
# 34824    24/07/1998
# 34825    25/10/1998
# Name: BIRTHDAY, Length: 34826, dtype: str

s_date_check = pd.to_datetime(df_bac['BIRTHDAY'], format='%d/%m/%Y', errors='coerce')
print(s_date_check[s_date_check.isna()])
# 880     NaT
# 2262    NaT
# 2603    NaT
# 4403    NaT
# ...
# 27620   NaT
# 27818   NaT
# 29578   NaT
# 31635   NaT
# Name: BIRTHDAY, dtype: datetime64[us]

print(s_date_check[s_date_check.isna()].index)
# Index([  880,  2262,  2603,  4403,  5239,  7176,  9832, 11330, 11712, 12086, 14633, 15406, 18087, 20415, 21525, 23731,
#        27620, 27818, 29578, 31635],
#       dtype='int64')

invalid_idx = s_date_check[s_date_check.isna()].index
print(s_birthday.iloc[invalid_idx])
# 880      00/07/1996
# 2262     31/11/1997
# 2603     29/02/1998
# 4403     29/02/1998
# 5239     29/02/1985
# 7176     29/02/1998
# 9832     00/01/1998
# 11330    29/02/1998
# 11712    29/02/1997
# 12086    00/10/1997
# 14633    29/02/1998
# 15406    29/02/1997
# 18087    29/02/1998
# 20415    00/00/1982
# 21525    29/02/1998
# 23731    00/03/1997
# 27620    29/02/1997
# 27818    29/02/1998
# 29578    00/00/1998
# 31635    00/00/1998
# Name: BIRTHDAY, dtype: str

'''
##--------------------------------------------------##
## Split SCORE column into multiple subject columns ##
##--------------------------------------------------##
'''

dict_subjects_score = dict()

for subject in dict_subjects.values():
    lst_score = df_bac['SCORE'].str.extract(fr'{subject}:\s*(\d+\.\d+)', expand=False).astype(float).to_list()
    dict_subjects_score[subject] = lst_score

for subject, scores in dict_subjects_score.items():
    print(f"{subject}: {scores[:5]} ... {scores[-5:]}")
# Math: [2.0, 5.5, 4.5, 3.0, 2.25] ... [0.75, 4.75, 4.0, 5.75, 2.5]
# Literature: [5.5, 5.25, 5.5, 6.0, 4.75] ... [5.0, 5.75, 5.5, 6.0, 4.25]
# Geography: [5.0, 5.5, 3.75, 5.5, 5.25] ... [nan, nan, nan, nan, nan]
# History: [3.0, nan, nan, nan, nan] ... [nan, nan, nan, nan, nan]
# English: [nan, 3.68, 2.25, 1.5, 2.0] ... [nan, 3.33, 3.6, 2.88, 3.0]
# Biology: [nan, nan, nan, nan, nan] ... [5.2, 4.6, nan, nan, 4.4]
# Physics: [nan, nan, nan, nan, nan] ... [nan, 6.8, 5.6, 7.4, 4.2]
# Chemistry: [nan, nan, nan, nan, nan] ... [4.8, 4.6, nan, 4.8, 4.4]

df_subjects_score = (
    df_bac
    .copy() # Create a copy of df_bac
    .assign(**dict_subjects_score) # Add new subject score columns
    .drop(columns=['SCORE', 'BIRTHDAY', 'EXAM_LOCATION']) # Drop SCORE column
    .set_index('ID') # Set ID as index
)

print(df_subjects_score.head())
#           FULL_NAME  GENDER  Math  Literature  Geography  History  English  Biology  Physics  Chemistry
# ID
# ID_00001  NAME_00001    Male  2.00        5.50       5.00      3.0      NaN      NaN      NaN        NaN
# ID_00002  NAME_00002    Male  5.50        5.25       5.50      NaN     3.68      NaN      NaN        NaN
# ID_00003  NAME_00003    Male  4.50        5.50       3.75      NaN     2.25      NaN      NaN        NaN
# ID_00004  NAME_00004  Female  3.00        6.00       5.50      NaN     1.50      NaN      NaN        NaN
# ID_00005  NAME_00005    Male  2.25        4.75       5.25      NaN     2.00      NaN      NaN        NaN

print(df_subjects_score.notna().sum()) # Count non-null values in each column
# FULL_NAME     34826
# GENDER        34826
# Math          34500
# Literature    33894
# Geography     22171
# History        3235
# English       30200
# Biology        3573
# Physics       10157
# Chemistry      8098
# dtype: int64

# =========================================================================================
# All-in-one workflow
# =========================================================================================

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

##-------------------##

df_bac = (
    pd.read_excel(data_dir/"Baccalaureate_2016.xlsx")
    .rename(columns = { # Change column names to English
        "SOBAODANH": "ID",
        "HO_TEN": "FULL_NAME",
        "NGAY_SINH": "BIRTHDAY",
        "TEN_CUMTHI": "EXAM_LOCATION",
        "GIOI_TINH": "GENDER",
        "DIEM_THI": "SCORE",
    })
    .assign(SCORE = c('SCORE').replace(dict_subjects, regex=True)) # Change subject names into English
    .replace(to_replace=dict_translate) # Translate other values into English
    .assign(
        BIRTHDAY = lambda df: pd.to_datetime(df['BIRTHDAY'], format='%d/%m/%Y', errors='coerce'), # Convert BIRTHDAY to datetime
        EXAM_LOCATION = c('EXAM_LOCATION').astype('category'), # Convert EXAM_LOCATION to category
        GENDER = c('GENDER').astype('category'), # Convert GENDER to category
    )
    .assign(**{
        subj: c('SCORE').str.extract(fr'{subj}:\s*(\d+\.*\d*)', expand=False).astype(float) for subj in dict_subjects.values()
    })
    .drop(columns=['SCORE', 'BIRTHDAY', 'EXAM_LOCATION'])
    .set_index('ID')
    # .assign(**{col: c(col).fillna('not_attend') for col in dict_subjects.values()})
)

print(df_bac.head())
#     FULL_NAME  GENDER  Math  Literature  Geography  History  English  Biology  Physics  Chemistry
# ID
# ID_00001  NAME_00001    Male  2.00        5.50       5.00      3.0      NaN      NaN      NaN        NaN
# ID_00002  NAME_00002    Male  5.50        5.25       5.50      NaN     3.68      NaN      NaN        NaN
# ID_00003  NAME_00003    Male  4.50        5.50       3.75      NaN     2.25      NaN      NaN        NaN
# ID_00004  NAME_00004  Female  3.00        6.00       5.50      NaN     1.50      NaN      NaN        NaN
# ID_00005  NAME_00005    Male  2.25        4.75       5.25      NaN     2.00      NaN      NaN        NaN
