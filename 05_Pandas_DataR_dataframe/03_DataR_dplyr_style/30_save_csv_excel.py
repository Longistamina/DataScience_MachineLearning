'''
datar does not support saving DataR dataframes to CSV or Excel files directly.

However, can use dr.pipe() to apply Pandas methods for saving dataframes.

############################

1. Save to CSV: dr.pipe(lambda f: f.to_csv('file.csv'))

2. Save to EXCEL: dr.pipe(lambda f: f.to_excel('file.xlsx', sheet_name='Sheet1'))
'''

import datar.all as dr
from datar import f
import pandas as pd


#-----------------------------------------------------------------------------------------------------------#
#----------------------------------------- 1. Save to CSV --------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#

(
    pd.read_csv("05_Pandas_DataR_dataframe/data/baseball.csv")
    >> dr.select(f.Name, f.Position, f.Height, f.Weight)
    >> dr.mutate(
        Position = dr.as_factor(f.Position),
        Height = f.Height * 0.0254,  # convert to m
        Weight = f.Weight * 0.453592,  # convert to kg
        BMI = f.Weight / (f.Height ** 2)
    )
    >> dr.pipe(lambda df: df.to_csv("05_Pandas_DataR_dataframe/save/tb_to.csv", index = False)) # Save to CSV
)


#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------- 2. Save to EXCEL -------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#

#---------
## Define dictionaries and functions
#---------

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

#---------
## Load and process data, then save to Excel
#---------

(
    pd.read_excel("05_Pandas_DataR_dataframe/data/Baccalaureate_2016.xlsx")
    >> dr.rename( # Rename columns from Vietnamese to English
        ID = f.SOBAODANH,
        FULL_NAME = f.HO_TEN,
        BIRTHDAY = f.NGAY_SINH,
        EXAM_LOCATION = f.TEN_CUMTHI,
        GENDER = f.GIOI_TINH,
        SCORE = f.DIEM_THI
    )
    >> dr.mutate(SCORE = f.SCORE.apply(rename_subjects))
    >> dr.pipe(lambda f: f.replace(to_replace = dict_translate))
    >> dr.mutate(
        BIRTHDAY = dr.as_date(f.BIRTHDAY, format = "%d/%m/%Y", optional = True),
        EXAM_LOCATION = dr.as_factor(f.EXAM_LOCATION),
        GENDER = dr.as_factor(f.GENDER)
    )
    >> dr.mutate(
        **{subject: dr.as_numeric(f.SCORE.str.extract(fr'{subject}:\s*(\d+\.\d+)', expand=False)) for subject in dict_subjects.values()}    
    )
    >> dr.select(~f.SCORE, ~f.BIRTHDAY, ~f.EXAM_LOCATION)
    >> dr.pipe(lambda f: f.set_index('ID'))

    >> dr.mutate(
        dr.across(
            ~f.FULL_NAME & ~f.GENDER,
            lambda col: col.fillna('not_attend') 
        )
    )
    >> dr.pipe(lambda df: df.to_excel("05_Pandas_DataR_dataframe/save/tb_baccalaureat_to.xlsx", sheet_name='Baccalaureate_2016'))
                          # Save to EXCEL
)