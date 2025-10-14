import pandas as pd

#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------- Step-by-step workflow -----------------------------------------#
#-----------------------------------------------------------------------------------------------------------#

######################
### Read Excel file ##
######################

df_bac = (
    pd.read_excel("05_Pandas_DataR_dataframe/data/Baccalaureate_2016.xlsx")
    .rename(columns = { # Change column names to English
        "SOBAODANH": "ID",
        "HO_TEN": "FULL_NAME",
        "NGAY_SINH": "BIRTHDAY",
        "TEN_CUMTHI": "EXAM_LOCATION",
        "GIOI_TINH": "GENDER",
        "DIEM_THI": "SCORE",
    })
)

print(df_bac.info())
# RangeIndex: 34826 entries, 0 to 34825
# Data columns (total 6 columns):
#  #   Column         Non-Null Count  Dtype 
# ---  ------         --------------  ----- 
#  0   ID             34826 non-null  object
#  1   FULL_NAME      34826 non-null  object
#  2   BIRTHDAY       34826 non-null  object
#  3   EXAM_LOCATION  34826 non-null  object
#  4   GENDER         34826 non-null  object
#  5   SCORE          34826 non-null  object
# dtypes: object(6)
# memory usage: 1.6+ MB

######################################
## Change subject name into English ##
######################################

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

def rename_subjects(subjects_str):
    for viet, eng in dict_subjects.items():
        subjects_str = subjects_str.replace(viet, eng)
    return subjects_str

df_bac['SCORE'] = df_bac['SCORE'].apply(rename_subjects)

print(df_bac['SCORE'].head(3))
# 0    Math:   2.00   Literature:   5.50   History:  ...
# 1    Math:   5.50   Literature:   5.25   Geography:...
# 2    Math:   4.50   Literature:   5.50   Geography:...
# Name: SCORE, dtype: object

######################################
## Change other values into English ##
######################################

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
    df_bac.replace(to_replace = dict_translate) # Translate values into English
    .assign(
        BIRTHDAY = lambda df: pd.to_datetime(df['BIRTHDAY'], format='%d/%m/%Y', errors='coerce'), # Convert BIRTHDAY to datetime
        EXAM_LOCATION = lambda df: df['EXAM_LOCATION'].astype('category'), # Convert EXAM_LOCATION to category
        GENDER = lambda df: df['GENDER'].astype('category'), # Convert GENDER to category
    )
)

print(df_bac.head())
#           ID      FULL_NAME   BIRTHDAY  EXAM_LOCATION  GENDER                                              SCORE
# 0  018000001  DƯƠNG VIỆT AN 1998-03-12  Bac Giang DET    Male  Toán:   2.00   Ngữ văn:   5.50   Lịch sử:   3....
# 1  018000002      ĐỖ VĂN AN 1998-12-09  Bac Giang DET    Male  Toán:   5.50   Ngữ văn:   5.25   Địa lí:   5.5...
# 2  018000003     ĐỖ XUÂN AN 1997-08-12  Bac Giang DET    Male  Toán:   4.50   Ngữ văn:   5.50   Địa lí:   3.7...
# 3  018000004   ĐẶNG PHÚC AN 1998-03-19  Bac Giang DET  Female  Toán:   3.00   Ngữ văn:   6.00   Địa lí:   5.5...
# 4  018000005    ĐẶNG VĂN AN 1998-10-25  Bac Giang DET    Male  Toán:   2.25   Ngữ văn:   4.75   Địa lí:   5.2...

print(df_bac.info())
# RangeIndex: 34826 entries, 0 to 34825
# Data columns (total 6 columns):
#  #   Column         Non-Null Count  Dtype         
# ---  ------         --------------  -----         
#  0   ID             34826 non-null  object        
#  1   FULL_NAME      34826 non-null  object        
#  2   BIRTHDAY       34806 non-null  datetime64[ns]
#  3   EXAM_LOCATION  34826 non-null  category      
#  4   GENDER         34826 non-null  category      
#  5   SCORE          34826 non-null  object        
# dtypes: category(2), datetime64[ns](1), object(3)
# memory usage: 1.1+ MB

###################################
## Check invalid BIRTHDAY values ##
###################################

s_birthday = (
    pd.read_excel("05_Pandas_DataR_dataframe/data/Baccalaureate_2016.xlsx", usecols=['NGAY_SINH'])
    .rename(columns = {"NGAY_SINH": "BIRTHDAY"})
    .squeeze() # Convert single-column DataFrame to Series
)

s_date_check = pd.to_datetime(df_bac['BIRTHDAY'], format='%d/%m/%Y', errors='coerce')

print(s_date_check[s_date_check.isna()])
# 2341    NaT
# 3256    NaT
# 7493    NaT
# 7766    NaT
# 7888    NaT
# 10388   NaT

print(s_date_check[s_date_check.isna()].index)
# Index([ 2341,  3256,  7493,  7766,  7888, 10388, 12531, 15166, 18312, 18346,
#        18592, 18672, 19383, 22353, 23517, 24212, 25567, 29375, 32122, 32812],
#       dtype='int64')

invalid_idx = s_date_check[s_date_check.isna()].index

print(s_birthday.iloc[invalid_idx])
# 2341     29/02/1998
# 3256     29/02/1998
# 7493     29/02/1997
# 7766     00/07/1996
# 7888     29/02/1998
# 10388    29/02/1998
# 12531    29/02/1985
# 15166    29/02/1998
# 18312    00/01/1998
# 18346    00/00/1998
# 18592    00/00/1982
# 18672    00/00/1998
# 19383    31/11/1997
# 22353    29/02/1998
# 23517    29/02/1997
# 24212    00/10/1997
# 25567    00/03/1997
# 29375    29/02/1998
# 32122    29/02/1998
# 32812    29/02/1997
# Name: BIRTHDAY, dtype: object

'''
######################################################
## Split SCORE column into multiple subject columns ##
######################################################
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
    df_bac.copy() # Create a copy of df_bac
    .assign(**dict_subjects_score) # Add new subject score columns
    .drop(columns=['SCORE', 'BIRTHDAY', 'EXAM_LOCATION']) # Drop SCORE column
    .set_index('ID') # Set ID as index
)

print(df_subjects_score.head())
#                FULL_NAME  GENDER  Math  Literature  Geography  History  English  Biology  Physics  Chemistry
# ID                                                                                                          
# 018000001  DƯƠNG VIỆT AN    Male  2.00        5.50       5.00      3.0      NaN      NaN      NaN        NaN
# 018000002      ĐỖ VĂN AN    Male  5.50        5.25       5.50      NaN     3.68      NaN      NaN        NaN
# 018000003     ĐỖ XUÂN AN    Male  4.50        5.50       3.75      NaN     2.25      NaN      NaN        NaN
# 018000004   ĐẶNG PHÚC AN  Female  3.00        6.00       5.50      NaN     1.50      NaN      NaN        NaN
# 018000005    ĐẶNG VĂN AN    Male  2.25        4.75       5.25      NaN     2.00      NaN      NaN        NaN

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


#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------------- All-in-one workflow ------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#

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
    .rename(columns = { # Change column names to English
        "SOBAODANH": "ID",
        "HO_TEN": "FULL_NAME",
        "NGAY_SINH": "BIRTHDAY",
        "TEN_CUMTHI": "EXAM_LOCATION",
        "GIOI_TINH": "GENDER",
        "DIEM_THI": "SCORE",
    })
    .assign(SCORE = lambda df: df['SCORE'].apply(rename_subjects)) # Change subject names into English
    .replace(to_replace = dict_translate) # Translate other values into English
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
