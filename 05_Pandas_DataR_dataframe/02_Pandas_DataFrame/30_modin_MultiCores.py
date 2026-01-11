'''
modin helps to speed up pandas operations by utilizing all available CPU cores.
Just need to change a single line of code to import modin instead of pandas.

########################

1. Example Code

2. Check supported APIs

3. Config the number of CPU cores
'''


#-----------------------------------------------------------------------------------------------#
#------------------------------------- 1. Example Code -----------------------------------------#
#-----------------------------------------------------------------------------------------------#

import modin.pandas as pd # Change only this line to use modin instead of pandas

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
    .assign(SCORE=lambda df: df['SCORE'].apply(rename_subjects)) # Change subject names into English
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
    .pipe(lambda df: df.assign(**{col: df[col].fillna('not_attend') for col in dict_subjects.values()})) # Dummy pipe to end the chain
)

print(df_bac.head())
#               FULL_NAME  GENDER  Math Literature  ...     English     Biology     Physics   Chemistry
# ID                                                ...                                                
# 18000001  DƯƠNG VIỆT AN    Male  2.00        5.5  ...  not_attend  not_attend  not_attend  not_attend
# 18000002      ĐỖ VĂN AN    Male  5.50       5.25  ...        3.68  not_attend  not_attend  not_attend
# 18000003     ĐỖ XUÂN AN    Male  4.50        5.5  ...        2.25  not_attend  not_attend  not_attend
# 18000004   ĐẶNG PHÚC AN  Female  3.00        6.0  ...         1.5  not_attend  not_attend  not_attend
# 18000005    ĐẶNG VĂN AN    Male  2.25       4.75  ...         2.0  not_attend  not_attend  not_attend
'''
UserWarning: <function Series.extract> is not currently supported by PandasOnRay, defaulting to pandas implementation.

=> So Modin converts to pandas, runs the operation, then converts back.
=> This may lead to performance degradation due to data transfer overhead.
'''


#-------------------------------------------------------------------------------------------------------#
#------------------------------------- 2. Check supported APIs -----------------------------------------#
#-------------------------------------------------------------------------------------------------------#
'''
Not all pandas APIs are supported by modin.

You can check the supported APIs at:
# pd.DataFrame: https://modin.readthedocs.io/en/latest/supported_apis/dataframe_supported.html
# pd.Series: https://modin.readthedocs.io/en/latest/supported_apis/series_supported.html
# pd Utilities: https://modin.readthedocs.io/en/latest/supported_apis/utilities_supported.html
# pd.read_* functions: https://modin.readthedocs.io/en/latest/supported_apis/io_supported.html
'''


#-------------------------------------------------------------------------------------------------------#
#-------------------------------- 3. Config the number of CPU cores ------------------------------------#
#-------------------------------------------------------------------------------------------------------#

import modin

'''Check the current number of partitions (CPU cores) that modin recognizes'''
print(modin.config.NPartitions.get())
# 32

'''Set the specific number of partitions (CPU cores) to be used by modin'''
import os
os.environ["MODIN_CPUS"] = "10" # Set to use 10 CPU cores

'''If you are using modin[ray]'''
import ray
ray.shutdown() # Shut down current process if already running
ray.init(num_cpus=10) # Set to use 10 CPU cores
