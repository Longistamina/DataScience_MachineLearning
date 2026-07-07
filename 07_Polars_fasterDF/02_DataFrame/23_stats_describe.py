'''
DataFrame description / summary statistics in Polars.

Pandas reference ideas:
1. df.describe(): summary statistics for numeric columns by default.
2. df.describe(include=[...]): include specific data types.
3. df.describe(exclude=[...]): exclude specific data types.

Polars equivalent ideas:
1. df.describe(): summary statistics for all columns, with dtype-dependent output.
2. Use `polars.selectors` to choose columns by dtype before calling `.describe()`.
3. Use selectors like `cs.numeric()`, `cs.string()`, `cs.categorical()`, `cs.boolean()`,
   and selector set operations (`|`, `&`, `~`) to emulate include/exclude behavior.

Important difference:
Polars does not have pandas-style `include=` or `exclude=` arguments inside `.describe()`.
Instead, select the columns first, then call `.describe()`.
'''

import polars as pl
from polars import selectors as cs
from polars import col as c
from pathlib import Path

# Optional display settings
pl.Config.set_tbl_rows(20)
pl.Config.set_tbl_cols(20)
pl.Config.set_tbl_width_chars(120)


data_dir = next(Path('/home').rglob('*/DataScience_MachineLearning/data'))


 #--------------------------------------------------------------------------------------------------------------#
 #------------------------------------------- 0. Setup Data ----------------------------------------------------#
 #--------------------------------------------------------------------------------------------------------------#

lf_pokemon = (
    pl.scan_csv(data_dir / "pokemon.csv")
    .drop('#')
    .rename(lambda name: name.strip()) # remove trailing space characters
    .select(
        pl.all()
        .name.replace(r"\s+", "_") # replace " " or "  " (or more consecutive space characters) with just one "_"
        .name.replace(".", "", literal=True) # replace "." with empty string (remove it), literal=True to deactive regex
    )
    .with_columns(cs.string().exclude("Name").cast(pl.Categorical))
    .pipe(lambda lf: lf.with_columns(
        c.Generation.cast(pl.String).cast(pl.Enum(lf.select("Generation").collect().to_series().cast(pl.String).unique().sort())))
    )
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

print(lf_pokemon.collect_schema())


#----------------------------------------------------------------------------------------------------------#
#----------------------------------------- 1. DataFrame.describe() ----------------------------------------#
#----------------------------------------------------------------------------------------------------------#

###################
## Default usage ##
###################
'''
Polars `DataFrame.describe()` returns summary statistics for the DataFrame.
Unlike pandas, Polars includes all columns by default, and fills unsupported
statistics with nulls depending on the dtype.
'''

print(lf_pokemon.describe())
# shape: (9, 13)
# ┌─────────┬─────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┐
# │ statist ┆ Name    ┆ Type_1 ┆ Type_2 ┆ Total  ┆ HP     ┆ Attack ┆ Defens ┆ Sp_Atk ┆ Sp_Def ┆ Speed  ┆ Genera ┆ Legend │
# │ ic      ┆ ---     ┆ ---    ┆ ---    ┆ ---    ┆ ---    ┆ ---    ┆ e      ┆ ---    ┆ ---    ┆ ---    ┆ tion   ┆ ary    │
# │ ---     ┆ str     ┆ str    ┆ str    ┆ f64    ┆ f64    ┆ f64    ┆ ---    ┆ f64    ┆ f64    ┆ f64    ┆ ---    ┆ ---    │
# │ str     ┆         ┆        ┆        ┆        ┆        ┆        ┆ f64    ┆        ┆        ┆        ┆ str    ┆ f64    │
# ╞═════════╪═════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╡
# │ count   ┆ 800     ┆ 800    ┆ 414    ┆ 800.0  ┆ 800.0  ┆ 800.0  ┆ 800.0  ┆ 800.0  ┆ 800.0  ┆ 800.0  ┆ 800    ┆ 800.0  │
# │ null_co ┆ 0       ┆ 0      ┆ 386    ┆ 0.0    ┆ 0.0    ┆ 0.0    ┆ 0.0    ┆ 0.0    ┆ 0.0    ┆ 0.0    ┆ 0      ┆ 0.0    │
# │ unt     ┆         ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        │
# │ mean    ┆ null    ┆ null   ┆ null   ┆ 435.10 ┆ 69.258 ┆ 79.001 ┆ 73.842 ┆ 72.82  ┆ 71.902 ┆ 68.277 ┆ null   ┆ 0.0812 │
# │         ┆         ┆        ┆        ┆ 25     ┆ 75     ┆ 25     ┆ 5      ┆        ┆ 5      ┆ 5      ┆        ┆ 5      │
# │ std     ┆ null    ┆ null   ┆ null   ┆ 119.96 ┆ 25.534 ┆ 32.457 ┆ 31.183 ┆ 32.722 ┆ 27.828 ┆ 29.060 ┆ null   ┆ null   │
# │         ┆         ┆        ┆        ┆ 304    ┆ 669    ┆ 366    ┆ 501    ┆ 294    ┆ 916    ┆ 474    ┆        ┆        │
# │ min     ┆ Abomasn ┆ null   ┆ null   ┆ 180.0  ┆ 1.0    ┆ 5.0    ┆ 5.0    ┆ 10.0   ┆ 20.0   ┆ 5.0    ┆ null   ┆ 0.0    │
# │         ┆ ow      ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        │
# │ 25%     ┆ null    ┆ null   ┆ null   ┆ 330.0  ┆ 50.0   ┆ 55.0   ┆ 50.0   ┆ 50.0   ┆ 50.0   ┆ 45.0   ┆ null   ┆ null   │
# │ 50%     ┆ null    ┆ null   ┆ null   ┆ 450.0  ┆ 65.0   ┆ 75.0   ┆ 70.0   ┆ 65.0   ┆ 70.0   ┆ 65.0   ┆ null   ┆ null   │
# │ 75%     ┆ null    ┆ null   ┆ null   ┆ 515.0  ┆ 80.0   ┆ 100.0  ┆ 90.0   ┆ 95.0   ┆ 90.0   ┆ 90.0   ┆ null   ┆ null   │
# │ max     ┆ Zygarde ┆ null   ┆ null   ┆ 780.0  ┆ 255.0  ┆ 190.0  ┆ 230.0  ┆ 194.0  ┆ 230.0  ┆ 180.0  ┆ null   ┆ 1.0    │
# │         ┆ 50%     ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        │
# │         ┆ Forme   ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        │
# └─────────┴─────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┘



#----------------------------------------------------------------------------------------------------------#
#--------------------------------- 2. Describe only numeric columns ---------------------------------------#
#----------------------------------------------------------------------------------------------------------#

#########################################################
## Equivalent idea: df.describe() for numeric columns  ##
## Polars way: select numeric columns, then describe() ##
#########################################################

print(
    lf_pokemon
    .select(cs.numeric())
    .describe()
)
# shape: (9, 8)
# ┌────────────┬───────────┬───────────┬───────────┬───────────┬───────────┬───────────┬───────────┐
# │ statistic  ┆ Total     ┆ HP        ┆ Attack    ┆ Defense   ┆ Sp_Atk    ┆ Sp_Def    ┆ Speed     │
# │ ---        ┆ ---       ┆ ---       ┆ ---       ┆ ---       ┆ ---       ┆ ---       ┆ ---       │
# │ str        ┆ f64       ┆ f64       ┆ f64       ┆ f64       ┆ f64       ┆ f64       ┆ f64       │
# ╞════════════╪═══════════╪═══════════╪═══════════╪═══════════╪═══════════╪═══════════╪═══════════╡
# │ count      ┆ 800.0     ┆ 800.0     ┆ 800.0     ┆ 800.0     ┆ 800.0     ┆ 800.0     ┆ 800.0     │
# │ null_count ┆ 0.0       ┆ 0.0       ┆ 0.0       ┆ 0.0       ┆ 0.0       ┆ 0.0       ┆ 0.0       │
# │ mean       ┆ 435.1025  ┆ 69.25875  ┆ 79.00125  ┆ 73.8425   ┆ 72.82     ┆ 71.9025   ┆ 68.2775   │
# │ std        ┆ 119.96304 ┆ 25.534669 ┆ 32.457366 ┆ 31.183501 ┆ 32.722294 ┆ 27.828916 ┆ 29.060474 │
# │ min        ┆ 180.0     ┆ 1.0       ┆ 5.0       ┆ 5.0       ┆ 10.0      ┆ 20.0      ┆ 5.0       │
# │ 25%        ┆ 330.0     ┆ 50.0      ┆ 55.0      ┆ 50.0      ┆ 50.0      ┆ 50.0      ┆ 45.0      │
# │ 50%        ┆ 450.0     ┆ 65.0      ┆ 75.0      ┆ 70.0      ┆ 65.0      ┆ 70.0      ┆ 65.0      │
# │ 75%        ┆ 515.0     ┆ 80.0      ┆ 100.0     ┆ 90.0      ┆ 95.0      ┆ 90.0      ┆ 90.0      │
# │ max        ┆ 780.0     ┆ 255.0     ┆ 190.0     ┆ 230.0     ┆ 194.0     ┆ 230.0     ┆ 180.0     │
# └────────────┴───────────┴───────────┴───────────┴───────────┴───────────┴───────────┴───────────┘


#----------------------------------------------------------------------------------------------------------#
#---------------------------- 3. Describe string and categorical columns ----------------------------------#
#----------------------------------------------------------------------------------------------------------#

########################################################################
## Equivalent idea: describe(include=['object', 'category'])          ##
## Polars way: select string and categorical columns, then describe() ##
########################################################################

print(
    lf_pokemon
    .select(cs.string() | cs.categorical())
    .describe()
)
# shape: (9, 4)
# ┌────────────┬──────────────────┬────────┬────────┐
# │ statistic  ┆ Name             ┆ Type_1 ┆ Type_2 │
# │ ---        ┆ ---              ┆ ---    ┆ ---    │
# │ str        ┆ str              ┆ str    ┆ str    │
# ╞════════════╪══════════════════╪════════╪════════╡
# │ count      ┆ 800              ┆ 800    ┆ 414    │
# │ null_count ┆ 0                ┆ 0      ┆ 386    │
# │ mean       ┆ null             ┆ null   ┆ null   │
# │ std        ┆ null             ┆ null   ┆ null   │
# │ min        ┆ Abomasnow        ┆ null   ┆ null   │
# │ 25%        ┆ null             ┆ null   ┆ null   │
# │ 50%        ┆ null             ┆ null   ┆ null   │
# │ 75%        ┆ null             ┆ null   ┆ null   │
# │ max        ┆ Zygarde50% Forme ┆ null   ┆ null   │
# └────────────┴──────────────────┴────────┴────────┘


#----------------------------------------------------------------------------------------------------------#
#-------------------------------- 4. Include all columns explicitly ---------------------------------------#
#----------------------------------------------------------------------------------------------------------#

#############################################################
## Equivalent idea: df.describe(include='all')             ##
## Polars way: df.describe() already describes all columns ##
#############################################################

print(lf_pokemon.describe())


#----------------------------------------------------------------------------------------------------------#
#-------------------------------- 5. Exclude specific dtypes ----------------------------------------------#
#----------------------------------------------------------------------------------------------------------#

#################################################################################
## Equivalent idea: df.describe(exclude=['category', 'bool'])                  ##
## Polars way: use selector negation to remove categorical and boolean columns ##
#################################################################################

print(
    lf_pokemon
    .select(~(cs.categorical() | cs.boolean()))
    .describe()
)
# Keeps string + numeric columns, excludes categorical + boolean columns.


#----------------------------------------------------------------------------------------------------------#
#--------------------------- 6. Custom describe for categorical columns -----------------------------------#
#----------------------------------------------------------------------------------------------------------#
'''
Polars `describe()` does not return pandas-style `unique`, `top`, and `freq` rows
for categorical/string columns. If you specifically want those statistics, compute
them directly with expressions.
'''

print(
    lf_pokemon
    .select(cs.string() | cs.categorical())
    .pipe(lambda lf: # use this to avoid typing ``lf_pokemon`` many times
        lf.select(
            [
                pl.col(col).count().alias(f"{col}_count")
                for col in lf.select(cs.string() | cs.categorical()).collect_schema().names()
            ]
            + [
                pl.col(col).n_unique().alias(f"{col}_unique")
                for col in lf.select(cs.string() | cs.categorical()).collect_schema().names()
            ]
            + [
                pl.col(col).mode().first().alias(f"{col}_top")
                for col in lf.select(cs.string() | cs.categorical()).collect_schema().names()
            ]
        )
    )
    .collect()
)
# shape: (1, 9)
# ┌────────────┬─────────────┬─────────────┬─────────────┬─────────────┬────────────┬──────────┬────────────┬────────────┐
# │ Name_count ┆ Type_1_coun ┆ Type_2_coun ┆ Name_unique ┆ Type_1_uniq ┆ Type_2_uni ┆ Name_top ┆ Type_1_top ┆ Type_2_top │
# │ ---        ┆ t           ┆ t           ┆ ---         ┆ ue          ┆ que        ┆ ---      ┆ ---        ┆ ---        │
# │ u32        ┆ ---         ┆ ---         ┆ u32         ┆ ---         ┆ ---        ┆ str      ┆ cat        ┆ cat        │
# │            ┆ u32         ┆ u32         ┆             ┆ u32         ┆ u32        ┆          ┆            ┆            │
# ╞════════════╪═════════════╪═════════════╪═════════════╪═════════════╪════════════╪══════════╪════════════╪════════════╡
# │ 800        ┆ 800         ┆ 414         ┆ 800         ┆ 18          ┆ 19         ┆ Scraggy  ┆ Water      ┆ null       │
# └────────────┴─────────────┴─────────────┴─────────────┴─────────────┴────────────┴──────────┴────────────┴────────────┘


#----------------------------------------------------------------------------------------------------------#
#--------------------------- 7. Custom pandas-like describe(include='all') --------------------------------#
#----------------------------------------------------------------------------------------------------------#

'''
If you want a pandas-like mixed summary table, it is usually clearer to build it
manually. Below is a compact version that creates:

- numeric summaries: count, mean, std, min, q25, q50, q75, max
- categorical/string summaries: count, unique, top, freq

This is not the default Polars style, but it demonstrates how flexible expression
construction can reproduce pandas-like output when needed.
'''

numeric_cols = df_pokemon.select(cs.numeric()).columns
categorical_like_cols = df_pokemon.select(cs.string() | cs.categorical() | cs.boolean()).columns

numeric_summary = pl.DataFrame({
    "statistic": ["count", "mean", "std", "min", "25%", "50%", "75%", "max"],
    **{
        col: [
            df_pokemon[col].count(),
            df_pokemon[col].mean(),
            df_pokemon[col].std(),
            df_pokemon[col].min(),
            df_pokemon[col].quantile(0.25),
            df_pokemon[col].quantile(0.50),
            df_pokemon[col].quantile(0.75),
            df_pokemon[col].max(),
        ]
        for col in numeric_cols
    }
})

categorical_summary = pl.DataFrame({
    "statistic": ["count", "unique", "top", "freq"],
    **{
        col: [
            df_pokemon[col].count(),
            df_pokemon[col].n_unique(),
            df_pokemon[col].mode().first(),
            df_pokemon[col].value_counts(sort=True)["count"].first(),
        ]
        for col in categorical_like_cols
    }
})

print(numeric_summary)
print(categorical_summary)
