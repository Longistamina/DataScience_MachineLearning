'''
Polars DataFrame attributes and close replacements for common pandas attributes.

This file is adapted from the pandas workflow:
    df.shape
    df.size
    df.ndim
    df.dtypes
    df.columns
    df.index
    df.axes
    df.values
    df.T
    df.empty
    df.attrs
    df.style
    df.flags

Important Polars differences:
1. Polars does NOT have a pandas-style row index or MultiIndex.
   Rows are addressed by integer position, and index-like values should be stored
   as normal columns.

2. Polars has a smaller and more explicit attribute surface for DataFrames.
   The core DataFrame attributes are:
      + df.shape
      + df.height
      + df.width
      + df.columns
      + df.dtypes
      + df.schema
      + df.flags
      + df.plot
      + df.style

3. Some pandas attributes are methods in Polars:
      + pandas df.values  -> Polars df.to_numpy()
      + pandas df.T       -> Polars df.transpose()
      + pandas df.empty   -> Polars df.is_empty()

4. Some pandas attributes do not exist in Polars:
      + df.size  -> use df.height * df.width
      + df.ndim  -> DataFrames are 2D, so use 2 conceptually
      + df.index -> no special row index; use df.with_row_index() if needed
      + df.axes  -> no row/column axes object; use row positions + df.columns
      + df.attrs -> keep metadata in a separate Python dict or normal columns
'''

import polars as pl
from pathlib import Path


#------------------------------------------------------------------------------------------------------#
#------------------------------------- 0. Example DataFrame -------------------------------------------#
#------------------------------------------------------------------------------------------------------#
'''
This guide uses the same baseball.csv dataset as the pandas attributes guide when available.
If the teaching data directory is not found, a small fallback DataFrame is created so that
this file is still easy to read and test elsewhere.
'''

try:
    data_dir = next(Path("/home").rglob("*/DataScience_MachineLearning/data"))

    df_baseball = pl.read_csv(
        data_dir / "baseball.csv",
        schema_overrides={
            "Team": pl.Categorical,
            "Position": pl.Categorical,
            "PosCategory": pl.Categorical,
        },
    )

except StopIteration:
    # Small fallback dataset with the same column names as baseball.csv.
    df_baseball = pl.DataFrame(
        {
            "Name": ["Adam_Donachie", "Paul_Bako", "Ramon_Hernandez", "Kevin_Millar", "Chris_Gomez"],
            "Team": ["BAL", "BAL", "BAL", "BAL", "BAL"],
            "Position": ["Catcher", "Catcher", "Catcher", "First_Baseman", "First_Baseman"],
            "Height": [74, 74, 72, 72, 73],
            "Weight": [180, 215, 210, 210, 188],
            "Age": [22.99, 34.69, 30.78, 35.43, 35.71],
            "PosCategory": ["Catcher", "Catcher", "Catcher", "Infielder", "Infielder"],
        }
    ).with_columns(
        pl.col(["Team", "Position", "PosCategory"]).cast(pl.Categorical)
    )


print(df_baseball.head())
# shape: (5, 7)
# ┌─────────────────┬──────┬───────────────┬────────┬────────┬───────┬─────────────┐
# │ Name            ┆ Team ┆ Position      ┆ Height ┆ Weight ┆ Age   ┆ PosCategory │
# │ ---             ┆ ---  ┆ ---           ┆ ---    ┆ ---    ┆ ---   ┆ ---         │
# │ str             ┆ cat  ┆ cat           ┆ i64    ┆ i64    ┆ f64   ┆ cat         │
# ╞═════════════════╪══════╪═══════════════╪════════╪════════╪═══════╪═════════════╡
# │ Adam_Donachie   ┆ BAL  ┆ Catcher       ┆ 74     ┆ 180    ┆ 22.99 ┆ Catcher     │
# │ Paul_Bako       ┆ BAL  ┆ Catcher       ┆ 74     ┆ 215    ┆ 34.69 ┆ Catcher     │
# │ Ramon_Hernandez ┆ BAL  ┆ Catcher       ┆ 72     ┆ 210    ┆ 30.78 ┆ Catcher     │
# │ Kevin_Millar    ┆ BAL  ┆ First_Baseman ┆ 72     ┆ 210    ┆ 35.43 ┆ Infielder   │
# │ Chris_Gomez     ┆ BAL  ┆ First_Baseman ┆ 73     ┆ 188    ┆ 35.71 ┆ Infielder   │
# └─────────────────┴──────┴───────────────┴────────┴────────┴───────┴─────────────┘
# Polars output has no pandas-style row index at the left.
# The column data types are displayed under the column names.

print(df_baseball.glimpse(return_type="string"))
# Rows: 1015
# Columns: 7
# $ Name        <str> 'Adam_Donachie', 'Paul_Bako', ...
# $ Team        <cat> 'BAL', 'BAL', ...
# $ Position    <cat> 'Catcher', 'Catcher', ...
# $ Height      <i64> 74, 74, ...
# $ Weight      <i64> 180, 215, ...
# $ Age         <f64> 22.99, 34.69, ...
# $ PosCategory <cat> 'Catcher', 'Catcher', ...


#------------------------------------------------------------------------------------------------------#
#------------------------------- 1. Shape and size-like attributes ------------------------------------#
#------------------------------------------------------------------------------------------------------#

##############
## df.shape ##
##############
'''
df.shape returns a tuple representing the dimensionality of the DataFrame:
    (number_of_rows, number_of_columns)

This is the direct Polars equivalent of pandas df.shape.
'''

print(df_baseball.shape)
# (1015, 7)
# There are 1015 rows and 7 columns in the full baseball DataFrame.

###############
## df.height ##
###############
'''
df.height returns the number of rows only.

This is more explicit than df.shape[0].
'''

print(df_baseball.height)
# 1015

print(df_baseball.shape[0])
# 1015

###############
## df.width  ##
###############
'''
df.width returns the number of columns only.

This is more explicit than df.shape[1].
'''

print(df_baseball.width)
# 7

print(df_baseball.shape[1])
# 7

#######################
## No direct df.size ##
#######################
'''
Pandas df.size returns the total number of elements:
    number_of_rows * number_of_columns

Polars does not expose df.size as a documented DataFrame attribute.
Use df.height * df.width instead.
'''

total_elements = df_baseball.height * df_baseball.width
print(total_elements)
# 7105

print(hasattr(df_baseball, "size"))
# False

#######################
## No direct df.ndim ##
#######################
'''
Pandas df.ndim returns 2 for DataFrames.

Polars DataFrames are also two-dimensional tables, but df.ndim is not a documented
DataFrame attribute. Treat the number of dimensions as conceptually 2.

Can use ``len(df.shape)`` to get the ndim
'''

print(hasattr(df_baseball, "ndim"))
# False

print(len(df_baseball.shape))
# 2


#------------------------------------------------------------------------------------------------------#
#------------------------------- 2. Data types and structure attributes -------------------------------#
#------------------------------------------------------------------------------------------------------#

###############
## df.dtypes ##
###############
'''
df.dtypes returns a list of Polars data types, in column order.

Unlike pandas, this is a plain list, not a Series indexed by column names.
Use zip(df.columns, df.dtypes) or df.schema when you want names and dtypes together.
'''

print(df_baseball.dtypes)
# [String, Categorical, Categorical, Int64, Int64, Float64, Categorical]

print(list(zip(df_baseball.columns, df_baseball.dtypes)))
# [('Name', String), ('Team', Categorical), ('Position', Categorical), ...]

################
## df.columns ##
################
'''
df.columns returns a Python list containing the column names in order.

In Polars, df.columns can also be assigned to rename all columns at once.
For selective renaming, df.rename({...}) is usually clearer.
'''

print(df_baseball.columns)
# ['Name', 'Team', 'Position', 'Height', 'Weight', 'Age', 'PosCategory']

# Rename all columns on a small clone.
df_upper = df_baseball.head(3).clone()
df_upper.columns = [name.upper() for name in df_upper.columns]
print(df_upper.columns)
# ['NAME', 'TEAM', 'POSITION', 'HEIGHT', 'WEIGHT', 'AGE', 'POSCATEGORY']

# Selective renaming.
df_renamed = df_baseball.head(3).rename({"Name": "Player", "Team": "Club"})
print(df_renamed.columns)
# ['Player', 'Club', 'Position', 'Height', 'Weight', 'Age', 'PosCategory']

###############
## df.schema ##
###############
'''
df.schema returns an ordered mapping from column names to Polars data types.

This is often the best Polars replacement for the dtype portion of pandas df.info().
'''

print(df_baseball.schema)
# Schema({
#     'Name': String,
#     'Team': Categorical,
#     'Position': Categorical,
#     'Height': Int64,
#     'Weight': Int64,
#     'Age': Float64,
#     'PosCategory': Categorical,
# })

print(df_baseball.schema["Age"])
# Float64

print(df_baseball.schema.names())
# ['Name', 'Team', 'Position', 'Height', 'Weight', 'Age', 'PosCategory']

print(df_baseball.schema.dtypes())
# [String, Categorical, Categorical, Int64, Int64, Float64, Categorical]

print(df_baseball.schema.len())
# 7

#########################
## df.collect_schema() ##
#########################
'''
df.collect_schema() also returns a Schema object.

This method is especially useful because LazyFrame has the same method, allowing
you to inspect a lazy query schema without collecting the data.
'''

schema = df_baseball.collect_schema()
print(schema)
# Schema({'Name': String, 'Team': Categorical, ...})

########################
## No direct df.index ##
########################
'''
Polars does not have a pandas-style row index.

If you need row numbers, add them as a normal column with df.with_row_index().
This is not a special index axis; it is just another column.
'''

print(hasattr(df_baseball, "index"))
# False

print(df_baseball.head(5).with_row_index(name="row_nr"))
# shape: (5, 8)
# ┌────────┬─────────────────┬──────┬───────────────┬────────┬────────┬───────┬─────────────┐
# │ row_nr ┆ Name            ┆ Team ┆ Position      ┆ Height ┆ Weight ┆ Age   ┆ PosCategory │
# │ ---    ┆ ---             ┆ ---  ┆ ---           ┆ ---    ┆ ---    ┆ ---   ┆ ---         │
# │ u32    ┆ str             ┆ cat  ┆ cat           ┆ i64    ┆ i64    ┆ f64   ┆ cat         │
# ╞════════╪═════════════════╪══════╪═══════════════╪════════╪════════╪═══════╪═════════════╡
# │ 0      ┆ Adam_Donachie   ┆ BAL  ┆ Catcher       ┆ 74     ┆ 180    ┆ 22.99 ┆ Catcher     │
# │ 1      ┆ Paul_Bako       ┆ BAL  ┆ Catcher       ┆ 74     ┆ 215    ┆ 34.69 ┆ Catcher     │
# │ 2      ┆ Ramon_Hernandez ┆ BAL  ┆ Catcher       ┆ 72     ┆ 210    ┆ 30.78 ┆ Catcher     │
# │ 3      ┆ Kevin_Millar    ┆ BAL  ┆ First_Baseman ┆ 72     ┆ 210    ┆ 35.43 ┆ Infielder   │
# │ 4      ┆ Chris_Gomez     ┆ BAL  ┆ First_Baseman ┆ 73     ┆ 188    ┆ 35.71 ┆ Infielder   │
# └────────┴─────────────────┴──────┴───────────────┴────────┴────────┴───────┴─────────────┘

#######################
## No direct df.axes ##
#######################
'''
Pandas df.axes returns [row_index, column_index].

Polars does not maintain row/column axes objects. If you need similar information,
combine a range of row positions with df.columns.
'''

row_positions = range(df_baseball.height)
column_names = df_baseball.columns

print(row_positions)
# range(0, 1015)

print(column_names)
# ['Name', 'Team', 'Position', 'Height', 'Weight', 'Age', 'PosCategory']

print(hasattr(df_baseball, "axes"))
# False


#------------------------------------------------------------------------------------------------------#
#----------------------------- 3. Data access and conversion replacements -----------------------------#
#------------------------------------------------------------------------------------------------------#

#########################
## No direct df.values ##
#########################
'''
Pandas df.values returns the underlying NumPy array.

Polars does not use a df.values attribute. Use df.to_numpy() when you explicitly
want a NumPy array.

Tip:
+ Numeric columns can often convert more efficiently.
+ Mixed-type DataFrames usually convert to a NumPy object array.
+ structured=True preserves column names and per-column dtypes better.
'''

print(hasattr(df_baseball, "values"))
# False

arr_numeric = df_baseball.select(["Height", "Weight", "Age"]).to_numpy()
print(type(arr_numeric))
# <class 'numpy.ndarray'>

print(arr_numeric.shape)
# (1015, 3)

print(arr_numeric[:3])
# [[ 74.   180.    22.99]
#  [ 74.   215.    34.69]
#  [ 72.   210.    30.78]]

arr_structured = df_baseball.select(["Height", "Weight", "Age"]).to_numpy(structured=True)
print(arr_structured.dtype)
# [('Height', '<i8'), ('Weight', '<i8'), ('Age', '<f8')]

#######################
## Other data access ##
#######################
'''
When you need Python-native output, Polars provides several explicit methods.
Use these only when you really need to leave Polars, because materializing data
as Python objects can be expensive for large DataFrames.
'''

print(df_baseball.head(3).rows())
# [
#     ('Adam_Donachie', 'BAL', 'Catcher', 74, 180, 22.99, 'Catcher'),
#     ('Paul_Bako', 'BAL', 'Catcher', 74, 215, 34.69, 'Catcher'),
#     ('Ramon_Hernandez', 'BAL', 'Catcher', 72, 210, 30.78, 'Catcher'),
# ]

print(df_baseball.head(2).rows(named=True))
# [
#     {'Name': 'Adam_Donachie', 'Team': 'BAL', ...},
#     {'Name': 'Paul_Bako', 'Team': 'BAL', ...},
# ]

print(df_baseball.head(2).to_dict(as_series=False))
# {
#     'Name': ['Adam_Donachie', 'Paul_Bako'],
#     'Team': ['BAL', 'BAL'],
#     ...
# }

####################
## No direct df.T ##
####################
'''
Pandas df.T is an attribute that returns the transpose.

Polars uses the explicit method df.transpose().
Transposing a DataFrame is usually expensive, so avoid it in performance-critical
pipelines unless you really need it.
'''

print(hasattr(df_baseball, "T"))
# False

# Use a tiny numeric DataFrame so the output is easy to read.
df_small = pl.DataFrame(
    {
        "a": [1, 2, 3],
        "b": [4, 5, 6],
    }
)

print(df_small.transpose(include_header=True))
# shape: (2, 4)
# ┌────────┬──────────┬──────────┬──────────┐
# │ column ┆ column_0 ┆ column_1 ┆ column_2 │
# │ ---    ┆ ---      ┆ ---      ┆ ---      │
# │ str    ┆ i64      ┆ i64      ┆ i64      │
# ╞════════╪══════════╪══════════╪══════════╡
# │ a      ┆ 1        ┆ 2        ┆ 3        │
# │ b      ┆ 4        ┆ 5        ┆ 6        │
# └────────┴──────────┴──────────┴──────────┘


print(df_small.transpose(include_header=True, header_name="original_column", column_names=["row_0", "row_1", "row_2"]))
# shape: (2, 4)
# ┌─────────────────┬───────┬───────┬───────┐
# │ original_column ┆ row_0 ┆ row_1 ┆ row_2 │
# │ ---             ┆ ---   ┆ ---   ┆ ---   │
# │ str             ┆ i64   ┆ i64   ┆ i64   │
# ╞═════════════════╪═══════╪═══════╪═══════╡
# │ a               ┆ 1     ┆ 2     ┆ 3     │
# │ b               ┆ 4     ┆ 5     ┆ 6     │
# └─────────────────┴───────┴───────┴───────┘

########################
## No direct df.empty ##
########################
'''
Pandas df.empty is an attribute.

Polars uses df.is_empty(), which returns True if the DataFrame contains no rows.
A DataFrame with zero columns but some rows is not a common Polars workflow;
for normal data-analysis use, think of emptiness as having no rows.
'''

print(hasattr(df_baseball, "empty"))
# False

print(df_baseball.is_empty())
# False

print(df_baseball.filter(pl.col("Age") > 200).is_empty())
# True

print(pl.DataFrame().is_empty())
# True


#------------------------------------------------------------------------------------------------------#
#------------------------------------- 4. Advanced attributes -----------------------------------------#
#------------------------------------------------------------------------------------------------------#

##############
## df.flags ##
##############
'''
df.flags returns a dictionary mapping each column name to column flags.

The most common flags are related to sortedness. These flags are metadata that
can help Polars optimize certain operations, but they must be correct.
Only use set_sorted() when the data is truly sorted.
'''

print(df_baseball.flags)
# A dictionary mapping column names to flags, for example sortedness flags.

# Correct usage: sort first, then mark the sorted column.
df_by_age = df_baseball.sort("Age").set_sorted("Age")
print(df_by_age.flags["Age"])
# Example: {'SORTED_ASC': True, 'SORTED_DESC': False, ...}

########################
## No direct df.attrs ##
########################
'''
Pandas df.attrs stores custom metadata on the DataFrame object.

Polars does not expose df.attrs as a documented DataFrame attribute.
Use a separate Python dictionary for teaching notes, provenance, or metadata,
or store important metadata as normal columns if it should travel with the data.
'''

print(hasattr(df_baseball, "attrs"))
# False

baseball_metadata = {
    "source": "Baseball dataset",
    "description": "Player statistics including height, weight, age, team, and position.",
}

print(baseball_metadata)
# {'source': 'Baseball dataset', 'description': 'Player statistics including height, weight, age, team, and position.'}

##############
## df.style ##
##############
'''
Polars now has a df.style namespace for table styling.

Important difference from pandas:
+ pandas df.style returns a pandas Styler.
+ Polars df.style delegates to the optional Great Tables package.

This is useful for presentation output, not for computation.
If the optional package is not installed, install it first:
    pip install great-tables
'''

try:
    styled_table = df_baseball.head(5).style.tab_header(title="Baseball preview")
    print(type(styled_table))
    # <class 'great_tables.gt.GT'>
except (ImportError, ModuleNotFoundError) as err:
    print("Install great-tables to use df.style:", err)
except AttributeError as err:
    print("Your Polars version does not expose df.style:", err)

#############
## df.plot ##
#############
'''
Polars also has a df.plot namespace for quick plotting.

Important difference from pandas:
+ pandas implements a plotting accessor around matplotlib.
+ Polars delegates plotting to the optional Altair ecosystem.

This is useful in notebooks and reports, not in core transformation pipelines.
If the optional package is not installed, install it first:
    pip install altair
'''

try:
    chart = df_baseball.head(50).plot.point(x="Height", y="Weight", color="Position")
    print(type(chart))
    # <class 'altair.vegalite.v5.api.Chart'>
except (ImportError, ModuleNotFoundError) as err:
    print("Install altair to use df.plot:", err)
except AttributeError as err:
    print("Your Polars version does not expose df.plot:", err)


#------------------------------------------------------------------------------------------------------#
#--------------------------- 5. Pandas-to-Polars attributes cheat sheet -------------------------------#
#------------------------------------------------------------------------------------------------------#

'''
Pandas attribute / concept        Polars equivalent
------------------------------------------------------------------------------------------
df.shape                         df.shape
df.shape[0]                      df.height
df.shape[1]                      df.width
df.size                          df.height * df.width
df.ndim                          2 conceptually; no documented df.ndim attribute
df.dtypes                        df.dtypes, or df.schema for name + dtype mapping
df.columns                       df.columns
df.index                         no special index; use df.with_row_index() if needed
df.axes                          no axes object; use range(df.height) and df.columns
df.values                        df.to_numpy()
df.T                             df.transpose()
df.empty                         df.is_empty()
df.attrs                         no documented df.attrs; use a separate metadata dict
df.style                         df.style, backed by optional Great Tables
df.flags                         df.flags
df.plot                          df.plot, backed by optional Altair
'''


#------------------------------------------------------------------------------------------------------#
#--------------------------- 6. Current Polars DataFrame attributes list ------------------------------#
#------------------------------------------------------------------------------------------------------#

'''
Categorized list of current Polars DataFrame attributes
======================================================

A. Shape / dimensions
   + df.shape
   + df.height
   + df.width

B. Names / types / schema
   + df.columns
   + df.dtypes
   + df.schema

C. Column metadata
   + df.flags

D. Presentation namespaces
   + df.style
   + df.plot

Related methods that often replace pandas attributes
====================================================

A. Index-like row numbers
   + df.with_row_index(name="index")

B. Data export / materialization
   + df.to_numpy()
   + df.to_dict()
   + df.rows()
   + df.rows(named=True)

C. Transpose / emptiness
   + df.transpose()
   + df.is_empty()

D. Info-like inspection
   + df.glimpse()
   + df.collect_schema()
   + df.null_count()
   + df.count()
   + df.describe()
   + df.estimated_size()
'''
