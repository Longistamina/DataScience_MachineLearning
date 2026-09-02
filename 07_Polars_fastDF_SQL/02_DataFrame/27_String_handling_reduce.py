from functools import reduce
from pathlib import Path

import polars as pl
from polars import col as c
from polars import selectors as cs

data_dir = Path("/home").rglob("*/DataScience_MachineLearning/data")
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
# $ ID            <str> '018000001', '018000002', '018000003', '018000004', '018000005', '018000006', '018000007', '018000008', '018000009', '018000010'
# $ FULL_NAME     <str> 'DƯƠNG VIỆT AN', 'ĐỖ VĂN AN', 'ĐỖ XUÂN AN', 'ĐẶNG PHÚC AN', 'ĐẶNG VĂN AN', 'HÀ THỊ AN', 'HÀ THỊ AN', 'HỨA VĂN AN', 'HOÀNG VĂN AN', 'LA VĂN AN'
# $ BIRTHDAY      <str> '12/03/1998', '09/12/1998', '12/08/1997', '19/03/1998', '25/10/1998', '22/06/1998', '23/04/1997', '25/05/1998', '22/02/1998', '19/08/1998'
# $ EXAM_LOCATION <str> 'Sở GDĐT Bắc Giang', 'Sở GDĐT Bắc Giang', 'Sở GDĐT Bắc Giang', 'Sở GDĐT Bắc Giang', 'Sở GDĐT Bắc Giang', 'Sở GDĐT Bắc Giang', 'Sở GDĐT Bắc Giang', 'Sở GDĐT Bắc Giang', 'Sở GDĐT Bắc Giang', 'Sở GDĐT Bắc Giang'
# $ GENDER        <str> 'Nam', 'Nam', 'Nam', 'Nữ', 'Nam', 'Nữ', 'Nữ', 'Nam', 'Nam', 'Nam'
# $ SCORE         <str> 'Toán:   2.00   Ngữ văn:   5.50   Lịch sử:   3.00   Địa lí:   5.00', 'Toán:   5.50   Ngữ văn:   5.25   Địa lí:   5.50   Tiếng Anh:   3.68', 'Toán:   4.50   Ngữ văn:   5.50   Địa lí:   3.75   Tiếng Anh:   2.25', 'Toán:   3.00   Ngữ văn:   6.00   Địa lí:   5.50   Tiếng Anh:   1.50', 'Toán:   2.25   Ngữ văn:   4.75   Địa lí:   5.25   Tiếng Anh:   2.00', 'Toán:   5.75   Ngữ văn:   5.50   Địa lí:   5.50   Tiếng Anh:   3.55', 'Toán:   1.75   Ngữ văn:   5.25   Địa lí:   4.75   Tiếng Anh:   1.75', 'Toán:   2.00   Ngữ văn:   4.75   Địa lí:   5.50   Tiếng Anh:   1.13', 'Toán:   3.75   Ngữ văn:   5.00   Địa lí:   6.50   Tiếng Anh:   2.75', 'Toán:   3.50   Ngữ văn:   5.00   Địa lí:   4.25   Tiếng Anh:   2.13'
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

print(lf_bac.collect())

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
# ┌───────────┬────────────────┬────────────┬───────────────┬────────┬─────────────────────────────────┐
# │ ID        ┆ FULL_NAME      ┆ BIRTHDAY   ┆ EXAM_LOCATION ┆ GENDER ┆ SCORE                           │
# │ ---       ┆ ---            ┆ ---        ┆ ---           ┆ ---    ┆ ---                             │
# │ str       ┆ str            ┆ date       ┆ cat           ┆ cat    ┆ str                             │
# ╞═══════════╪════════════════╪════════════╪═══════════════╪════════╪═════════════════════════════════╡
# │ 018000001 ┆ DƯƠNG VIỆT AN  ┆ 1998-03-12 ┆ Bac Giang DET ┆ Male   ┆ Toán:   2.00   Ngữ văn:   5.50… │
# │ 018000002 ┆ ĐỖ VĂN AN      ┆ 1998-12-09 ┆ Bac Giang DET ┆ Male   ┆ Toán:   5.50   Ngữ văn:   5.25… │
# │ 018000003 ┆ ĐỖ XUÂN AN     ┆ 1997-08-12 ┆ Bac Giang DET ┆ Male   ┆ Toán:   4.50   Ngữ văn:   5.50… │
# │ 018000004 ┆ ĐẶNG PHÚC AN   ┆ 1998-03-19 ┆ Bac Giang DET ┆ Female ┆ Toán:   3.00   Ngữ văn:   6.00… │
# │ 018000005 ┆ ĐẶNG VĂN AN    ┆ 1998-10-25 ┆ Bac Giang DET ┆ Male   ┆ Toán:   2.25   Ngữ văn:   4.75… │
# │ …         ┆ …              ┆ …          ┆ …             ┆ …      ┆ …                               │
# │ HUI014539 ┆ VÒNG NGỌC YẾN  ┆ 1998-05-15 ┆ IUH           ┆ Female ┆ Toán:   0.75   Ngữ văn:   5.00… │
# │ HUI014540 ┆ VÒNG THANH YẾN ┆ 1998-09-09 ┆ IUH           ┆ Female ┆ Toán:   4.75   Ngữ văn:   5.75… │
# │ HUI014541 ┆ VŨ THỊ BẢO YẾN ┆ 1998-05-19 ┆ IUH           ┆ Female ┆ Toán:   4.00   Ngữ văn:   5.50… │
# │ HUI014542 ┆ VŨ THỊ YẾN     ┆ 1998-01-13 ┆ IUH           ┆ Female ┆ Toán:   5.75   Ngữ văn:   6.00… │
# │ HUI014543 ┆ VƯƠNG THỊ YẾN  ┆ 1998-02-05 ┆ IUH           ┆ Female ┆ Toán:   2.50   Ngữ văn:   4.25… │
# └───────────┴────────────────┴────────────┴───────────────┴────────┴─────────────────────────────────┘


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
# 	"29/02/1998"
# 	"29/02/1998"
# 	"29/02/1997"
# 	"00/07/1996"
# 	"29/02/1998"
# 	…
# 	"00/10/1997"
# 	"00/03/1997"
# 	"29/02/1998"
# 	"29/02/1998"
# 	"29/02/1997"
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

print(
    lf_bac_subjects
    .drop("SCORE")
    .tail(5)
    .collect()
)
# shape: (5, 13)
# ┌───────────┬──────────────┬────────────┬─────────────┬────────┬───┬─────────┬─────────┬─────────┬─────────┬───────────┐
# │ ID        ┆ FULL_NAME    ┆ BIRTHDAY   ┆ EXAM_LOCATI ┆ GENDER ┆ … ┆ History ┆ English ┆ Biology ┆ Physics ┆ Chemistry │
# │ ---       ┆ ---          ┆ ---        ┆ ON          ┆ ---    ┆   ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---       │
# │ str       ┆ str          ┆ date       ┆ ---         ┆ cat    ┆   ┆ f32     ┆ f32     ┆ f32     ┆ f32     ┆ f32       │
# │           ┆              ┆            ┆ cat         ┆        ┆   ┆         ┆         ┆         ┆         ┆           │
# ╞═══════════╪══════════════╪════════════╪═════════════╪════════╪═══╪═════════╪═════════╪═════════╪═════════╪═══════════╡
# │ HUI014539 ┆ VÒNG NGỌC    ┆ 1998-05-15 ┆ IUH         ┆ Nữ     ┆ … ┆ null    ┆ null    ┆ 5.2     ┆ null    ┆ 4.8       │
# │           ┆ YẾN         ┆            ┆             ┆        ┆   ┆         ┆         ┆         ┆         ┆           │
# │ HUI014540 ┆ VÒNG THANH   ┆ 1998-09-09 ┆ IUH         ┆ Nữ     ┆ … ┆ null    ┆ 3.33    ┆ 4.6     ┆ 6.8     ┆ 4.6       │
# │           ┆ YẾN         ┆            ┆             ┆        ┆   ┆         ┆         ┆         ┆         ┆           │
# │ HUI014541 ┆ VŨ THỊ BẢO  ┆ 1998-05-19 ┆ IUH         ┆ Nữ     ┆ … ┆ null    ┆ 3.6     ┆ null    ┆ 5.6     ┆ null      │
# │           ┆ YẾN         ┆            ┆             ┆        ┆   ┆         ┆         ┆         ┆         ┆           │
# │ HUI014542 ┆ VŨ THỊ YẾN  ┆ 1998-01-13 ┆ IUH         ┆ Nữ     ┆ … ┆ null    ┆ 2.88    ┆ null    ┆ 7.4     ┆ 4.8       │
# │ HUI014543 ┆ VƯƠNG THỊ    ┆ 1998-02-05 ┆ IUH         ┆ Nữ     ┆ … ┆ null    ┆ 3.0     ┆ 4.4     ┆ 4.2     ┆ 4.4       │
# │           ┆ YẾN         ┆            ┆             ┆        ┆   ┆         ┆         ┆         ┆         ┆           │
# └───────────┴──────────────┴────────────┴─────────────┴────────┴───┴─────────┴─────────┴─────────┴─────────┴───────────┘

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
# ┌───────────┬─────────────────┬────────┬──────┬────────────┬───┬─────────┬─────────┬─────────┬─────────┬───────────┐
# │ ID        ┆ FULL_NAME       ┆ GENDER ┆ Math ┆ Literature ┆ … ┆ History ┆ English ┆ Biology ┆ Physics ┆ Chemistry │
# │ ---       ┆ ---             ┆ ---    ┆ ---  ┆ ---        ┆   ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---       │
# │ str       ┆ str             ┆ cat    ┆ f32  ┆ f32        ┆   ┆ f32     ┆ f32     ┆ f32     ┆ f32     ┆ f32       │
# ╞═══════════╪═════════════════╪════════╪══════╪════════════╪═══╪═════════╪═════════╪═════════╪═════════╪═══════════╡
# │ 018000001 ┆ DƯƠNG VIỆT AN   ┆ Male   ┆ 2.0  ┆ 5.5        ┆ … ┆ 3.0     ┆ null    ┆ null    ┆ null    ┆ null      │
# │ 018000002 ┆ ĐỖ VĂN AN      ┆ Male   ┆ 5.5  ┆ 5.25       ┆ … ┆ null    ┆ 3.68    ┆ null    ┆ null    ┆ null      │
# │ 018000003 ┆ ĐỖ XUÂN AN     ┆ Male   ┆ 4.5  ┆ 5.5        ┆ … ┆ null    ┆ 2.25    ┆ null    ┆ null    ┆ null      │
# │ 018000004 ┆ ĐẶNG PHÚC AN    ┆ Female ┆ 3.0  ┆ 6.0        ┆ … ┆ null    ┆ 1.5     ┆ null    ┆ null    ┆ null      │
# │ 018000005 ┆ ĐẶNG VĂN AN     ┆ Male   ┆ 2.25 ┆ 4.75       ┆ … ┆ null    ┆ 2.0     ┆ null    ┆ null    ┆ null      │
# │ …         ┆ …               ┆ …      ┆ …    ┆ …          ┆ … ┆ …       ┆ …       ┆ …       ┆ …       ┆ …         │
# │ HUI014539 ┆ VÒNG NGỌC YẾN  ┆ Female ┆ 0.75 ┆ 5.0        ┆ … ┆ null    ┆ null    ┆ 5.2     ┆ null    ┆ 4.8       │
# │ HUI014540 ┆ VÒNG THANH YẾN ┆ Female ┆ 4.75 ┆ 5.75       ┆ … ┆ null    ┆ 3.33    ┆ 4.6     ┆ 6.8     ┆ 4.6       │
# │ HUI014541 ┆ VŨ THỊ BẢO YẾN┆ Female ┆ 4.0  ┆ 5.5        ┆ … ┆ null    ┆ 3.6     ┆ null    ┆ 5.6     ┆ null      │
# │ HUI014542 ┆ VŨ THỊ YẾN     ┆ Female ┆ 5.75 ┆ 6.0        ┆ … ┆ null    ┆ 2.88    ┆ null    ┆ 7.4     ┆ 4.8       │
# │ HUI014543 ┆ VƯƠNG THỊ YẾN  ┆ Female ┆ 2.5  ┆ 4.25       ┆ … ┆ null    ┆ 3.0     ┆ 4.4     ┆ 4.2     ┆ 4.4       │
# └───────────┴─────────────────┴────────┴──────┴────────────┴───┴─────────┴─────────┴─────────┴─────────┴───────────┘
