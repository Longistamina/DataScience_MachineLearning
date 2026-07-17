'''
Chaining methods is a style that lets you express a complete DataFrame workflow as a
sequence of transformations instead of creating many intermediate variables.

In Polars, this style works especially well with LazyFrame pipelines:

(
    lf
    .method1()
    .method2()
    .method3()
    .collect()
)

Important Polars ideas:
+ Prefer LazyFrame workflows with pl.scan_csv(...) when possible.
+ Use .collect() only when you need an eager result, such as plotting or calling external Python/SciPy functions.
+ Use .pipe(...) when a custom transformation does not fit neatly as a built-in method.
+ Polars does not have a pandas-style index; keep identifier/time columns as normal columns.

##################################
1. General chaining methods
2. Apply with .pipe() for custom functions
3. Apply with .group_by()
4. Apply with .plot
5. All-in-one workflow example
'''

from pathlib import Path
from functools import reduce

import altair as alt
import polars as pl
from polars import col as c
from polars import selectors as cs
from scipy import stats

# Optional display settings
pl.Config.set_tbl_rows(12)
pl.Config.set_tbl_cols(12)
pl.Config.set_tbl_width_chars(120)
pl.Config.set_float_precision(4)

data_dir = next(Path("/home").rglob("*/DataScience_MachineLearning/data"))
alt.renderers.enable("browser")


#-------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 1. General Chaining Methods -----------------------------------------#
#-------------------------------------------------------------------------------------------------------------#
'''
Use scan_csv(...) to start a lazy query.
Then chain rename, parsing, filtering, sorting, and selecting operations.

Unlike pandas, Polars does not use a datetime index. The date column remains a normal column.
'''

lf_aq = (
    pl.scan_csv(data_dir / "air_quality_no2_long.csv")
    .rename({"date.utc": "date"})
    .with_columns(
        c("date")
        .str.strptime(
            dtype=pl.Datetime(time_zone="UTC"),
            format="%Y-%m-%d %H:%M:%S%z",
            strict=False,
        )
        .alias("date")
    )
)

lf_aq_paris = (
    lf_aq
    .filter((c("country") == "FR") & (c("city") == "Paris"))
    .select("date", "value")
    .sort("date")
)

print(lf_aq_paris.head().collect())
# shape: (5, 2)
# ┌─────────────────────────┬─────────┐
# │ date                    ┆ value   │
# │ ---                     ┆ ---     │
# │ datetime[μs, UTC]       ┆ f64     │
# ╞═════════════════════════╪═════════╡
# │ 2019-05-07 01:00:00 UTC ┆ 25.0000 │
# │ 2019-05-07 02:00:00 UTC ┆ 27.7000 │
# │ 2019-05-07 03:00:00 UTC ┆ 50.4000 │
# │ 2019-05-07 04:00:00 UTC ┆ 61.9000 │
# │ 2019-05-07 05:00:00 UTC ┆ 72.4000 │
# └─────────────────────────┴─────────┘


#-------------------------------------------------------------------------------------------------------------#
#--------------------------------- 2. Apply with .pipe() for custom functions --------------------------------#
#-------------------------------------------------------------------------------------------------------------#
'''
.pipe(...) passes the current DataFrame/LazyFrame as the first argument to a function.
It is useful when you want to keep method chaining but need custom logic.

Polars LazyFrame.pipe(...) is still part of the lazy chain if the function returns a LazyFrame.
For external Python libraries like SciPy, collect first, then use pipe on the eager DataFrame.
'''

# Example with the Pokemon dataset: clean columns and cast selected columns.
lf_pokemon = (
    pl.scan_csv(data_dir / "pokemon.csv")
    .drop("#")
    .rename(lambda name: name.strip())
    .select(pl.all().name.replace(r"\s+", "_").name.replace(".", "", literal=True))
    .with_columns(
        c("Type_1", "Type_2").cast(pl.Categorical),
        c("Legendary").cast(pl.Boolean),
    )
    .pipe(lambda f: f.with_columns(
        c("Generation").cast(pl.String).cast(pl.Enum(f.select("Generation").collect().to_series().cast(pl.String).unique().sort())),
    ))                                               # Must use .collect() to realize the dataframe, to access the values for Enum casting
)

print(lf_pokemon.head().collect())
# shape: (5, 12)
# ┌────────────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ Name           ┆ Type_1 ┆ Type_2 ┆ Total ┆ HP  ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed ┆ Generation ┆ Legendary │
# │ ---            ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ str            ┆ cat    ┆ cat    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞════════════════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ Bulbasaur      ┆ Grass  ┆ Poison ┆ 318   ┆ 45  ┆ 49     ┆ 49      ┆ 65     ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ Ivysaur        ┆ Grass  ┆ Poison ┆ 405   ┆ 60  ┆ 62     ┆ 63      ┆ 80     ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ Venusaur       ┆ Grass  ┆ Poison ┆ 525   ┆ 80  ┆ 82     ┆ 83      ┆ 100    ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# │ VenusaurMega   ┆ Grass  ┆ Poison ┆ 625   ┆ 80  ┆ 100    ┆ 123     ┆ 122    ┆ 120    ┆ 80    ┆ 1          ┆ false     │
# │ Venusaur       ┆        ┆        ┆       ┆     ┆        ┆         ┆        ┆        ┆       ┆            ┆           │
# │ Charmander     ┆ Fire   ┆ null   ┆ 309   ┆ 39  ┆ 52     ┆ 43      ┆ 60     ┆ 50     ┆ 65    ┆ 1          ┆ false     │
# └────────────────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘


# Example with Boston Housing dataset and reframing technique.
# SciPy functions need materialized scalar inputs, so this is a deliberate collect() + pipe() fallback.
lf_boston_stats = (
    pl.scan_csv(data_dir / "BostonHousing.csv")
    .rename(lambda col: col.lower())
    .select("rm", "lstat", "medv")
    .collect()
    .pipe(
        lambda df: pl.LazyFrame({
            "index": ["ppf_25th", "ppf_50th", "ppf_75th", "ppf_100th"],
            "rm_norm": stats.norm.ppf(
                q=[0.25, 0.5, 0.75, 1],
                loc=df["rm"].mean(),
                scale=df["rm"].std(),
            ),
            "lstat_expon": stats.expon.ppf(
                q=[0.25, 0.5, 0.75, 1],
                scale=df["lstat"].mean(),
            ),
            "medv_gamma": stats.gamma.ppf(
                q=[0.25, 0.5, 0.75, 1],
                a=2,
                scale=df["medv"].mean() / 2,
            ),
        })
    )
)

print(lf_boston_stats.collect())
# shape: (4, 4)
# columns: index, rm_norm, lstat_expon, medv_gamma
# q=1 gives inf for these continuous distributions.


#-------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 3. Apply with .group_by() ------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#
'''
Polars group_by().agg(...) keeps grouping keys as normal columns.
There is no need for pandas-style reset_index().

If you want pandas dropna=True behavior for group keys, drop null keys before group_by(...).
'''

print(
    lf_pokemon
    .drop_nulls(["Type_1", "Type_2"])
    .group_by("Type_1", "Type_2")
    .agg(
        c("HP").min().alias("min_HP"),
        c("HP").max().alias("max_HP"),
        c("HP").mean().alias("mean_HP"),
    )
    .sort("Type_1", "Type_2")
    .collect()
)
# shape: depends on observed Type_1 + Type_2 combinations
# columns: Type_1, Type_2, min_HP, max_HP, mean_HP


#-------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 4. Apply with .plot -----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#
'''
Polars DataFrame.plot uses Altair-style charts.
LazyFrame does not plot directly, so collect the data needed for the chart first.

In a notebook, returning the chart object as the last line may render it.
In a normal editor such as Zed, saving to HTML is usually the most reliable workflow.
'''

# Box plot of Attack by Generation.
df_plot_attack = (
    lf_pokemon
    .select("Generation", "Attack")
    .collect()
)

chart_attack_box = (
    df_plot_attack
    .plot
    .boxplot(
        x=alt.X("Generation:N", title="Generation"),
        y=alt.Y("Attack:Q", title="Attack"),
    )
    .properties(
        width=650,
        height=350,
        title="Box Plot of Pokemon Attack by Generation",
    )
)
chart_attack_box.show()

# Scatter plot of Attack vs Defense.
chart_attack_defense = (
    lf_pokemon
    .select("Attack", "Defense", "Legendary")
    .collect()
    .plot
    .point(
        x=alt.X("Attack:Q", title="Attack"),
        y=alt.Y("Defense:Q", title="Defense"),
        color=alt.Color("Legendary:N", title="Legendary"),
    )
    .properties(
        width=650,
        height=350,
        title="Scatter Plot of Pokemon Attack vs Defense",
    )
)
chart_attack_defense.show()


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 5. All-in-one workflow --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
This is a larger workflow that chains several ideas:
+ read Excel eagerly, then convert to LazyFrame
+ rename columns
+ replace subject names using reduce(...)
+ translate selected values
+ parse string dates into pl.Date
+ cast categorical columns
+ split a packed SCORE string into multiple numeric subject columns
+ drop columns that are no longer needed

Polars does not have a pandas-style index, so ID remains a normal column.
'''

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

#######################

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



#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 6. Quick summary ------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Pandas -> Polars mental map

1. General chaining
   pandas: df.method1().method2().method3()
   polars: lf.method1().method2().method3().collect()

2. Custom pipeline step
   pandas: df.pipe(lambda df: ...)
   polars: lf.pipe(lambda lf: ...) or df.pipe(lambda df: ...)

3. Grouped aggregation
   pandas: df.groupby(...).agg(...).reset_index()
   polars: lf.group_by(...).agg(...).collect()

4. Plotting
   pandas: df.plot(...)
   polars: df.plot.<mark>(...) after collecting to eager DataFrame

5. Index
   pandas: df.set_index("ID")
   polars: keep ID as a normal column

6. External Python/SciPy
   pandas: often works directly on Series/DataFrame
   polars: use native expressions first; collect + pipe only when the external function needs Python objects
'''
