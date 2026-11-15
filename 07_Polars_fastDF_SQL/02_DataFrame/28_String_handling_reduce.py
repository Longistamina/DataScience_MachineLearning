from functools import reduce
from pathlib import Path

import polars as pl
from polars import col as c
from polars import selectors as cs

data_dir = Path.home().rglob("*/DataScience_MachineLearning/data")
data_dir = next(data_dir)

# Optional display settings
pl.Config.set_tbl_rows(10)
pl.Config.set_tbl_cols(10)
pl.Config.set_tbl_width_chars(120)

# =========================================================================================
# Step-by-step workflow
# =========================================================================================

##------------------##
### Read Excel file ##
##------------------##

df_bac = (
    pl.read_excel(data_dir/"Baccalaureate_2016.xlsx") # read into an eager dataframe
    .rename(mapping={ # Change column names to English
        "SOBAODANH": "ID",
        "HO_TEN": "FULL_NAME",
        "NGAY_SINH": "BIRTHDAY",
        "TEN_CUMTHI": "EXAM_LOCATION",
        "GIOI_TINH": "GENDER",
        "DIEM_THI": "SCORE",
    })
)

# Create a lazyframe
lf_bac = df_bac.lazy()

# glimpse the info
print(df_bac.glimpse())
# Rows: 34826
# Columns: 6
# $ ID            <str> 'ID_00001', 'ID_00002', 'ID_00003', 'ID_00004', 'ID_00005', 'ID_00006', 'ID_00007', 'ID_00008', 'ID_00009' , 'ID_00010'
# $ FULL_NAME     <str> 'NAME_00001', 'NAME_00002', 'NAME_00003', 'NAME_00004', 'NAME_00005', 'NAME_00006', 'NAME_00007', 'NAME_00 008', 'NAME_00009', 'NAME_00010'
# $ BIRTHDAY      <str> '16/01/1998', '20/05/1998', '02/03/1998', '15/02/1998', '23/06/1998', '15/02/1998', '02/04/1997', '09/12/1 998', '28/06/1997', '01/06/1998'
# $ EXAM_LOCATION <str> 'Sở GDĐT Bắc Giang', 'Sở GDĐT Bắc Giang', 'Sở GDĐT Bắc Giang', 'Sở GDĐT Bắc Giang', 'Sở GDĐT Bắc Giang', 'Sở GDĐT Bắc Giang', 'Sở GDĐT Bắc Giang', 'Sở GDĐT Bắc Giang', 'Sở GDĐT Bắc Giang', 'Sở GDĐT Bắc Giang'
# $ GENDER        <str> 'Nam', 'Nam', 'Nam', 'Nữ', 'Nam', 'Nữ', 'Nữ', 'Nam', 'Nam', 'Nam'
# $ SCORE         <str> 'Toán:   2.00   Ngữ văn:   5.50   Lịch sử:   3.00   Địa lí:   5.00', 'Toán:   5.50   Ngữ văn:   5.25   Địa
#  lí:   5.50   Tiếng Anh:   3.68', 'Toán:   4.50   Ngữ văn:   5.50   Địa lí:   3.75   Tiếng Anh:   2.25', 'Toán:   3.00   Ngữ văn
# :   6.00   Địa lí:   5.50   Tiếng Anh:   1.50', 'Toán:   2.25   Ngữ văn:   4.75   Địa lí:   5.25   Tiếng Anh:   2.00', 'Toán:
# 5.75   Ngữ văn:   5.50   Địa lí:   5.50   Tiếng Anh:   3.55', 'Toán:   1.75   Ngữ văn:   5.25   Địa lí:   4.75   Tiếng Anh:   1.
# 75', 'Toán:   2.00   Ngữ văn:   4.75   Địa lí:   5.50   Tiếng Anh:   1.13', 'Toán:   3.75   Ngữ văn:   5.00   Địa lí:   6.50   T
# iếng Anh:   2.75', 'Toán:   3.50   Ngữ văn:   5.00   Địa lí:   4.25   Tiếng Anh:   2.13'
# None

##----------------------------------##
## Change subject name into English ##
##----------------------------------##

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

lf_bac = lf_bac.with_columns(
    # c.SCORE.str.replace_all(viet, eng) for viet, eng in dict_subjects.items() # this will fail because it creates 8 separate expressions, and each one outputs a column named "SCORE":
    reduce( # "Toán:  2.5  Ngữ Văn:  3.2..." => "Math:  2.5  Ngữ Văn:  3.2..." => "Math:  2.5  Literature:  3.2..."
        lambda expr, item: expr.str.replace_all(item[0], item[1]), # the function to apply
        dict_subjects.items(), # the iterable
        c.SCORE # the initial (initializer)
    ).alias("SCORE")
)
# c.SCORE.str.replace_all('Toán', 'Math').str.replace('Ngữ văn', 'Literature').str.replace(...).str.replace(...)
'''
`.str.replace_all()` modify the root column
so it is not allowed to use for loop to generate multiple parallel expressions,
because it risks of data race
'''

print(lf_bac.collect())
# shape: (34_826, 6)
# ┌──────────┬────────────┬────────────┬─────────────────────────────────┬────────┬─────────────────────────────────┐
# │ ID       ┆ FULL_NAME  ┆ BIRTHDAY   ┆ EXAM_LOCATION                   ┆ GENDER ┆ SCORE                           │
# │ ---      ┆ ---        ┆ ---        ┆ ---                             ┆ ---    ┆ ---                             │
# │ str      ┆ str        ┆ str        ┆ str                             ┆ str    ┆ str                             │
# ╞══════════╪════════════╪════════════╪═════════════════════════════════╪════════╪═════════════════════════════════╡
# │ ID_00001 ┆ NAME_00001 ┆ 16/01/1998 ┆ Sở GDĐT Bắc Giang               ┆ Nam    ┆ Math:   2.00   Literature:   5… │
# │ ID_00002 ┆ NAME_00002 ┆ 20/05/1998 ┆ Sở GDĐT Bắc Giang               ┆ Nam    ┆ Math:   5.50   Literature:   5… │
# │ ID_00003 ┆ NAME_00003 ┆ 02/03/1998 ┆ Sở GDĐT Bắc Giang               ┆ Nam    ┆ Math:   4.50   Literature:   5… │
# │ ID_00004 ┆ NAME_00004 ┆ 15/02/1998 ┆ Sở GDĐT Bắc Giang               ┆ Nữ     ┆ Math:   3.00   Literature:   6… │
# │ ID_00005 ┆ NAME_00005 ┆ 23/06/1998 ┆ Sở GDĐT Bắc Giang               ┆ Nam    ┆ Math:   2.25   Literature:   4… │
# │ …        ┆ …          ┆ …          ┆ …                               ┆ …      ┆ …                               │
# │ ID_34822 ┆ NAME_34822 ┆ 26/12/1998 ┆ Trường Đại học Công nghiệp Tp.… ┆ Nữ     ┆ Math:   0.75   Literature:   5… │
# │ ID_34823 ┆ NAME_34823 ┆ 11/04/1998 ┆ Trường Đại học Công nghiệp Tp.… ┆ Nữ     ┆ Math:   4.75   Literature:   5… │
# │ ID_34824 ┆ NAME_34824 ┆ 13/10/1998 ┆ Trường Đại học Công nghiệp Tp.… ┆ Nữ     ┆ Math:   4.00   Literature:   5… │
# │ ID_34825 ┆ NAME_34825 ┆ 24/07/1998 ┆ Trường Đại học Công nghiệp Tp.… ┆ Nữ     ┆ Math:   5.75   Literature:   6… │
# │ ID_34826 ┆ NAME_34826 ┆ 25/10/1998 ┆ Trường Đại học Công nghiệp Tp.… ┆ Nữ     ┆ Math:   2.50   Literature:   4… │
# └──────────┴────────────┴────────────┴─────────────────────────────────┴────────┴─────────────────────────────────┘

##----------------------------------##
## Change other values into English ##
##----------------------------------##

print(lf_bac.select("GENDER").unique().collect())
# ['Nam' 'Nữ']

print(lf_bac.select("EXAM_LOCATION").unique().collect())
# ['Sở GDĐT Bắc Giang' 'Sở GDĐT Hoà Bình' 'Sở GDĐT Thừa Thiên -Huế', 'Trường Đại học Công nghiệp Tp. HCM']

dict_translate = {
    'Nam': 'Male',
    'Nữ': 'Female',
    'Sở GDĐT Bắc Giang': 'Bac Giang DET', # DET: Dept of Education and Training
    'Sở GDĐT Hoà Bình': 'Hoa Binh DET',
    'Sở GDĐT Thừa Thiên -Huế': 'Thua Thien - Hue DET',
    'Trường Đại học Công nghiệp Tp. HCM': 'IUH' # IUH: Industrial University of Ho Chi Minh City
}

lf_bac = (
    lf_bac
    .with_columns(cs.string().replace(dict_translate)) # Must separate to avoid duplicate name
    .with_columns(
        c("EXAM_LOCATION").cast(pl.Categorical),
        c.GENDER.cast(pl.Categorical),
        c.BIRTHDAY.str.strptime(dtype=pl.Date, format='%d/%m/%Y', strict=False) # Convert BIRTHDAY to Datetime
    )
)

print(lf_bac.collect())
# shape: (34_826, 6)
# ┌──────────┬────────────┬────────────┬───────────────┬────────┬─────────────────────────────────┐
# │ ID       ┆ FULL_NAME  ┆ BIRTHDAY   ┆ EXAM_LOCATION ┆ GENDER ┆ SCORE                           │
# │ ---      ┆ ---        ┆ ---        ┆ ---           ┆ ---    ┆ ---                             │
# │ str      ┆ str        ┆ date       ┆ cat           ┆ cat    ┆ str                             │
# ╞══════════╪════════════╪════════════╪═══════════════╪════════╪═════════════════════════════════╡
# │ ID_00001 ┆ NAME_00001 ┆ 1998-01-16 ┆ Bac Giang DET ┆ Male   ┆ Math:   2.00   Literature:   5… │
# │ ID_00002 ┆ NAME_00002 ┆ 1998-05-20 ┆ Bac Giang DET ┆ Male   ┆ Math:   5.50   Literature:   5… │
# │ ID_00003 ┆ NAME_00003 ┆ 1998-03-02 ┆ Bac Giang DET ┆ Male   ┆ Math:   4.50   Literature:   5… │
# │ ID_00004 ┆ NAME_00004 ┆ 1998-02-15 ┆ Bac Giang DET ┆ Female ┆ Math:   3.00   Literature:   6… │
# │ ID_00005 ┆ NAME_00005 ┆ 1998-06-23 ┆ Bac Giang DET ┆ Male   ┆ Math:   2.25   Literature:   4… │
# │ …        ┆ …          ┆ …          ┆ …             ┆ …      ┆ …                               │
# │ ID_34822 ┆ NAME_34822 ┆ 1998-12-26 ┆ IUH           ┆ Female ┆ Math:   0.75   Literature:   5… │
# │ ID_34823 ┆ NAME_34823 ┆ 1998-04-11 ┆ IUH           ┆ Female ┆ Math:   4.75   Literature:   5… │
# │ ID_34824 ┆ NAME_34824 ┆ 1998-10-13 ┆ IUH           ┆ Female ┆ Math:   4.00   Literature:   5… │
# │ ID_34825 ┆ NAME_34825 ┆ 1998-07-24 ┆ IUH           ┆ Female ┆ Math:   5.75   Literature:   6… │
# │ ID_34826 ┆ NAME_34826 ┆ 1998-10-25 ┆ IUH           ┆ Female ┆ Math:   2.50   Literature:   4… │
# └──────────┴────────────┴────────────┴───────────────┴────────┴─────────────────────────────────┘

##-------------------------------##
## Check invalid BIRTHDAY values ##
##-------------------------------##

s_birthday = df_bac["BIRTHDAY"]
# 34_826 observations

s_date_check = s_birthday.str.strptime(dtype=pl.Date, format='%d/%m/%Y', strict=False)
print(s_date_check.filter(s_date_check.is_null()))
# shape: (20,)
# Series: 'BIRTHDAY' [date]
# [
# 	null
# 	null
# 	null
# 	null
# 	null
# 	…
# 	null
# 	null
# 	null
# 	null
# 	null
# ]

print(s_birthday.filter(s_date_check.is_null()))
# shape: (20,)
# Series: 'BIRTHDAY' [str]
# [
# 	"00/07/1996"
# 	"31/11/1997"
# 	"29/02/1998"
# 	"29/02/1998"
# 	"29/02/1985"
# 	…
# 	"00/03/1997"
# 	"29/02/1997"
# 	"29/02/1998"
# 	"00/00/1998"
# 	"00/00/1998"
# ]

'''
##--------------------------------------------------##
## Split SCORE column into multiple subject columns ##
##--------------------------------------------------##
'''

lf_bac_subjects = (
    lf_bac
    .with_columns(
        c.SCORE.str.extract(rf"{subject}:\s*(\d+\.\d+)").cast(pl.Float32).alias(f"{subject}")
        for subject in dict_subjects.values()
    )
)
'''
`.str.extract()` don't modify the root column
so it is able to use for loop to generate multiple parallel expressions.
'''

print(
    lf_bac_subjects
    .drop("SCORE")
    .tail(5)
    .collect()
)
# shape: (5, 13)
# ┌──────────┬────────────┬────────────┬───────────────┬────────┬───┬─────────┬─────────┬─────────┬─────────┬───────────┐
# │ ID       ┆ FULL_NAME  ┆ BIRTHDAY   ┆ EXAM_LOCATION ┆ GENDER ┆ … ┆ History ┆ English ┆ Biology ┆ Physics ┆ Chemistry │
# │ ---      ┆ ---        ┆ ---        ┆ ---           ┆ ---    ┆   ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---       │
# │ str      ┆ str        ┆ date       ┆ cat           ┆ cat    ┆   ┆ f32     ┆ f32     ┆ f32     ┆ f32     ┆ f32       │
# ╞══════════╪════════════╪════════════╪═══════════════╪════════╪═══╪═════════╪═════════╪═════════╪═════════╪═══════════╡
# │ ID_34822 ┆ NAME_34822 ┆ 1998-12-26 ┆ IUH           ┆ Female ┆ … ┆ null    ┆ null    ┆ 5.2     ┆ null    ┆ 4.8       │
# │ ID_34823 ┆ NAME_34823 ┆ 1998-04-11 ┆ IUH           ┆ Female ┆ … ┆ null    ┆ 3.33    ┆ 4.6     ┆ 6.8     ┆ 4.6       │
# │ ID_34824 ┆ NAME_34824 ┆ 1998-10-13 ┆ IUH           ┆ Female ┆ … ┆ null    ┆ 3.6     ┆ null    ┆ 5.6     ┆ null      │
# │ ID_34825 ┆ NAME_34825 ┆ 1998-07-24 ┆ IUH           ┆ Female ┆ … ┆ null    ┆ 2.88    ┆ null    ┆ 7.4     ┆ 4.8       │
# │ ID_34826 ┆ NAME_34826 ┆ 1998-10-25 ┆ IUH           ┆ Female ┆ … ┆ null    ┆ 3.0     ┆ 4.4     ┆ 4.2     ┆ 4.4       │
# └──────────┴────────────┴────────────┴───────────────┴────────┴───┴─────────┴─────────┴─────────┴─────────┴───────────┘

print(
    lf_bac_subjects
    .select(pl.all().is_null().sum())
    .unpivot(variable_name="column", value_name="null_count")
    .collect()
)
# shape: (14, 2)
# ┌───────────────┬────────────┐
# │ column        ┆ null_count │
# │ ---           ┆ ---        │
# │ str           ┆ u32        │
# ╞═══════════════╪════════════╡
# │ ID            ┆ 0          │
# │ FULL_NAME     ┆ 0          │
# │ BIRTHDAY      ┆ 20         │
# │ EXAM_LOCATION ┆ 0          │
# │ GENDER        ┆ 0          │
# │ …             ┆ …          │
# │ History       ┆ 31591      │
# │ English       ┆ 4626       │
# │ Biology       ┆ 31253      │
# │ Physics       ┆ 24669      │
# │ Chemistry     ┆ 26728      │
# └───────────────┴────────────┘

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

lf_bac = (
    pl.read_excel(data_dir/"Baccalaureate_2016.xlsx")
    .lazy()
    .rename({ # Change column names to English
        "SOBAODANH": "ID",
        "HO_TEN": "FULL_NAME",
        "NGAY_SINH": "BIRTHDAY",
        "TEN_CUMTHI": "EXAM_LOCATION",
        "GIOI_TINH": "GENDER",
        "DIEM_THI": "SCORE",
    })
    .with_columns( # "Toán:  2.5  Ngữ Văn:  3.2..." => "Math:  2.5  Ngữ Văn:  3.2..." => "Math:  2.5  Literature:  3.2..."
        reduce(
            lambda expr, item: expr.str.replace_all(item[0], item[1]),
            dict_subjects.items(),
            c.SCORE
        ).alias("SCORE")
    )
    .with_columns(cs.string().replace(dict_translate))
    .with_columns(
        c("EXAM_LOCATION").cast(pl.Categorical),
        c.GENDER.cast(pl.Categorical),
        c.BIRTHDAY.str.strptime(dtype=pl.Date, format='%d/%m/%Y', strict=False) # Convert BIRTHDAY to Datetime
    )
    .with_columns(
        #c.SCORE.str.extract(rf"{subject}:\s*(\d+\.\d+)").cast(pl.Float32).fill_null("not_attend").alias(f"{subject}")
        c.SCORE.str.extract(rf"{subject}:\s*(\d+\.\d+)").cast(pl.Float32).alias(f"{subject}")
        for subject in dict_subjects.values()
    )
    .drop('SCORE', 'BIRTHDAY', 'EXAM_LOCATION')
)

print(lf_bac.collect())
# shape: (34_826, 11)
# ┌──────────┬────────────┬────────┬──────┬────────────┬───┬─────────┬─────────┬─────────┬─────────┬───────────┐
# │ ID       ┆ FULL_NAME  ┆ GENDER ┆ Math ┆ Literature ┆ … ┆ History ┆ English ┆ Biology ┆ Physics ┆ Chemistry │
# │ ---      ┆ ---        ┆ ---    ┆ ---  ┆ ---        ┆   ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---       │
# │ str      ┆ str        ┆ cat    ┆ f32  ┆ f32        ┆   ┆ f32     ┆ f32     ┆ f32     ┆ f32     ┆ f32       │
# ╞══════════╪════════════╪════════╪══════╪════════════╪═══╪═════════╪═════════╪═════════╪═════════╪═══════════╡
# │ ID_00001 ┆ NAME_00001 ┆ Male   ┆ 2.0  ┆ 5.5        ┆ … ┆ 3.0     ┆ null    ┆ null    ┆ null    ┆ null      │
# │ ID_00002 ┆ NAME_00002 ┆ Male   ┆ 5.5  ┆ 5.25       ┆ … ┆ null    ┆ 3.68    ┆ null    ┆ null    ┆ null      │
# │ ID_00003 ┆ NAME_00003 ┆ Male   ┆ 4.5  ┆ 5.5        ┆ … ┆ null    ┆ 2.25    ┆ null    ┆ null    ┆ null      │
# │ ID_00004 ┆ NAME_00004 ┆ Female ┆ 3.0  ┆ 6.0        ┆ … ┆ null    ┆ 1.5     ┆ null    ┆ null    ┆ null      │
# │ ID_00005 ┆ NAME_00005 ┆ Male   ┆ 2.25 ┆ 4.75       ┆ … ┆ null    ┆ 2.0     ┆ null    ┆ null    ┆ null      │
# │ …        ┆ …          ┆ …      ┆ …    ┆ …          ┆ … ┆ …       ┆ …       ┆ …       ┆ …       ┆ …         │
# │ ID_34822 ┆ NAME_34822 ┆ Female ┆ 0.75 ┆ 5.0        ┆ … ┆ null    ┆ null    ┆ 5.2     ┆ null    ┆ 4.8       │
# │ ID_34823 ┆ NAME_34823 ┆ Female ┆ 4.75 ┆ 5.75       ┆ … ┆ null    ┆ 3.33    ┆ 4.6     ┆ 6.8     ┆ 4.6       │
# │ ID_34824 ┆ NAME_34824 ┆ Female ┆ 4.0  ┆ 5.5        ┆ … ┆ null    ┆ 3.6     ┆ null    ┆ 5.6     ┆ null      │
# │ ID_34825 ┆ NAME_34825 ┆ Female ┆ 5.75 ┆ 6.0        ┆ … ┆ null    ┆ 2.88    ┆ null    ┆ 7.4     ┆ 4.8       │
# │ ID_34826 ┆ NAME_34826 ┆ Female ┆ 2.5  ┆ 4.25       ┆ … ┆ null    ┆ 3.0     ┆ 4.4     ┆ 4.2     ┆ 4.4       │
# └──────────┴────────────┴────────┴──────┴────────────┴───┴─────────┴─────────┴─────────┴─────────┴───────────┘
