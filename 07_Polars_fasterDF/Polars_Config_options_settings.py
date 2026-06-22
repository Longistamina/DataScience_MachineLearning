'''
In Polars, display options and a small number of global behavior options are
controlled through pl.Config.

Polars does NOT have the pandas options API:
    pandas: pd.describe_option(), pd.get_option(), pd.set_option(), pd.reset_option()
    polars: pl.Config.state(), pl.Config.set_*(), pl.Config.restore_defaults()

Pandas -> Polars equivalents:
1. pd.describe_option()
   + Polars: inspect dir(pl.Config) for set_* methods, or read pl.Config docs
   + Runtime state: pl.Config.state()

2. pd.get_option("display.max_rows")
   + Polars has no direct one-option getter.
   + Use pl.Config.state() / pl.Config.state(if_set=True) and inspect the returned dict.

3. pd.set_option("display.max_rows", n)
   + Polars: pl.Config.set_tbl_rows(n)
   + Or temporary/local: with pl.Config(tbl_rows=n): ...

4. pd.reset_option("display.max_rows")
   + Polars: pl.Config.set_tbl_rows(None)
   + Reset everything: pl.Config.restore_defaults()

5. pd.option_context(...)
   + Polars: with pl.Config(...): ...

6. pd.set_eng_float_format(...)
   + Polars: pl.Config.set_float_precision(), set_fmt_float(),
     set_thousands_separator(), set_decimal_separator()

######################################################
1. All available Config options
2. Getting, Setting, and Resetting options
3. Temporary options with context manager and decorator
4. Setting startup options in Python/IPython
5. Frequently used display options
   + tbl_rows, tbl_cols, tbl_width_chars
   + fmt_str_lengths, fmt_table_cell_list_len
   + table shape, data types, table formatting, alignment
6. Number formatting
   + float precision, full/mixed float mode
   + thousands and decimal separators
   + Decimal trailing zeros
7. Unicode / ASCII table formatting
8. Less common global behavior options
'''

from decimal import Decimal as D
from pathlib import Path
import sys

import polars as pl


#-------------------------------------------------------------------------------------------------------#
#----------------------------------------- Data setup --------------------------------------------------#
#-------------------------------------------------------------------------------------------------------#

'''
This guide is self-contained. It creates a small medals-like DataFrame instead
of reading from a CSV file, so the examples work even when the external
"medals.csv" file is unavailable.
'''

df_seed = pl.DataFrame(
    {
        "Year": [1924, 1924, 1924, 1924, 1924, 1928, 1928, 1928],
        "City": [
            "Chamonix",
            "Chamonix",
            "Chamonix",
            "Chamonix",
            "Chamonix",
            "St. Moritz",
            "St. Moritz",
            "St. Moritz",
        ],
        "Sport": [
            "Skating",
            "Skating",
            "Skating",
            "Bobsleigh",
            "Ice Hockey",
            "Skating",
            "Skiing",
            "Skiing",
        ],
        "Discipline": [
            "Figure skating",
            "Figure skating",
            "Figure skating",
            "Bobsleigh",
            "Ice Hockey",
            "Speed skating",
            "Cross Country Skiing",
            "Ski Jumping",
        ],
        "NOC": ["AUT", "AUT", "AUT", "BEL", "CAN", "NOR", "SWE", "NOR"],
        "Event": [
            "individual",
            "individual",
            "pairs",
            "four-man",
            "ice hockey",
            "500m",
            "18km",
            "normal hill individual",
        ],
        "Event gender": ["M", "W", "X", "M", "M", "M", "M", "M"],
        "Medal": ["Silver", "Gold", "Gold", "Bronze", "Gold", "Gold", "Silver", "Bronze"],
        "Score": [4.512345, 4.981234, 4.777777, 3.123456, 5.000000, 4.543210, 4.111111, 3.987654],
        "Prize": [1200, 1500, 1500, 750, 2000, 1700, 900, 800],
        "Tags": [
            ["winter", "ice", "solo"],
            ["winter", "ice", "solo"],
            ["winter", "ice", "pair"],
            ["winter", "sled", "team"],
            ["winter", "ice", "team"],
            ["winter", "ice", "speed"],
            ["winter", "snow", "distance"],
            ["winter", "snow", "jump"],
        ],
        "Notes": [
            "Short note",
            "A longer note that may be truncated in table display",
            "Pairs event",
            "Bobsleigh team competition",
            "Ice hockey team event",
            "Speed skating sprint race",
            "Cross country distance race",
            "Ski jumping normal hill individual event",
        ],
    }
)

# Repeat the seed rows to make a DataFrame large enough to demonstrate row truncation.
df_medals = pl.concat([df_seed] * 4, how="vertical").with_row_index("row_id")

# Make selected string columns categorical, similar to the pandas guide.
df_medals = df_medals.with_columns(
    pl.col(["City", "Sport", "Discipline", "NOC", "Event", "Event gender", "Medal"]).cast(pl.Categorical)
)

print(df_medals.head(3))
# shape: (3, 13)
# ┌────────┬──────┬──────────┬─────────┬───┬──────────┬───────┬───────────────────┬───────────────┐
# │ row_id ┆ Year ┆ City     ┆ Sport   ┆ … ┆ Score    ┆ Prize ┆ Tags              ┆ Notes         │
# │ ---    ┆ ---  ┆ ---      ┆ ---     ┆   ┆ ---      ┆ ---   ┆ ---               ┆ ---           │
# │ u32    ┆ i64  ┆ cat      ┆ cat     ┆   ┆ f64      ┆ i64   ┆ list[str]         ┆ str           │
# ╞════════╪══════╪══════════╪═════════╪═══╪══════════╪═══════╪═══════════════════╪═══════════════╡
# │ 0      ┆ 1924 ┆ Chamonix ┆ Skating ┆ … ┆ 4.512345 ┆ 1200  ┆ ["winter", "ice", ┆ Short note    │
# │        ┆      ┆          ┆         ┆   ┆          ┆       ┆ "solo"]           ┆               │
# │ 1      ┆ 1924 ┆ Chamonix ┆ Skating ┆ … ┆ 4.981234 ┆ 1500  ┆ ["winter", "ice", ┆ A longer note │
# │        ┆      ┆          ┆         ┆   ┆          ┆       ┆ "solo"]           ┆ that may be   │
# │        ┆      ┆          ┆         ┆   ┆          ┆       ┆                   ┆ trun…         │
# │ 2      ┆ 1924 ┆ Chamonix ┆ Skating ┆ … ┆ 4.777777 ┆ 1500  ┆ ["winter", "ice", ┆ Pairs event   │
# │        ┆      ┆          ┆         ┆   ┆          ┆       ┆ "pair"]           ┆               │
# └────────┴──────┴──────────┴─────────┴───┴──────────┴───────┴───────────────────┴───────────────┘

print(df_medals.schema)
# Schema({'row_id': UInt32, 'Year': Int64, 'City': Categorical, 'Sport': Categorical, 'Discipline': Categorical, 'NOC': Categorical, 'Event': Categorical, 'Event gender': Categorical, 'Medal': Categorical, 'Score': Float64, 'Prize': Int64, 'Tags': List(String), 'Notes': String})


#-------------------------------------------------------------------------------------------------------#
#----------------------------------- 1. All available Config options -----------------------------------#
#-------------------------------------------------------------------------------------------------------#
'''
Pandas has pd.describe_option().
Polars does not have a direct describe_option() equivalent.

The closest runtime tools are:
1. dir(pl.Config): inspect available methods.
2. pl.Config.state(): inspect current configuration values.
3. pl.Config.state(if_set=True): inspect only options explicitly set in this process.
'''

#####################
## Inspect methods ##
#####################

config_set_methods = sorted(name for name in dir(pl.Config) if name.startswith("set_"))
print(config_set_methods)
# Example method names:
# ['set_ascii_tables', 'set_auto_structify', 'set_decimal_separator',
#  'set_engine_affinity', 'set_float_precision', 'set_fmt_float',
#  'set_fmt_str_lengths', 'set_fmt_table_cell_list_len', 'set_tbl_cols',
#  'set_tbl_rows', 'set_tbl_width_chars', 'set_verbose', ...]

config_state_methods = ["state", "save", "save_to_file", "load", "load_from_file", "restore_defaults"]
print(config_state_methods)

###################
## Current state ##
###################

# Show all Config state values.
print(pl.Config.state())
# Returns a dictionary of Config values, mostly backed by environment variables.

# Show only options that have been explicitly set.
print(pl.Config.state(if_set=True))
# Usually {} at the start of a clean session.


#-------------------------------------------------------------------------------------------------------#
#---------------------------- 2. Getting, Setting and Resetting options --------------------------------#
#-------------------------------------------------------------------------------------------------------#

################################
## Getting: pl.Config.state() ##
################################
'''
Polars has no pd.get_option("...") equivalent that fetches one option by a
friendly pandas-style key.

Use pl.Config.state() or pl.Config.state(if_set=True), then inspect the returned
dictionary. In normal Polars code, it is often cleaner to avoid reading global
state and use a temporary context manager instead.
'''

pl.Config.restore_defaults()

print(pl.Config.state(if_set=True))
# {}

################################
## Setting: pl.Config.set_*() ##
################################

# Equivalent idea to: pd.set_option("display.max_rows", 6)
pl.Config.set_tbl_rows(6)

print(pl.Config.state(if_set=True))
# Example output contains a row-display setting, such as:
# {'POLARS_FMT_MAX_ROWS': '6'}

# Set multiple options by calling multiple set_* methods.
pl.Config.set_tbl_cols(6)
pl.Config.set_fmt_str_lengths(30)

print(pl.Config.state(if_set=True))
# Example output contains row, column, and string-length settings.

####################################
## Resetting one option with None ##
####################################
'''
To reset one Config option, call the related setter with None.
This is the Polars equivalent idea of pd.reset_option("...").
'''

pl.Config.set_tbl_rows(None)
print(pl.Config.state(if_set=True))
# The row-display setting is removed/reset, but other settings remain.

###########################
## Resetting all options ##
###########################

pl.Config.restore_defaults()
print(pl.Config.state(if_set=True))
# {}


#-------------------------------------------------------------------------------------------------------#
#-------------------------- 3. Temporary options: context manager / decorator --------------------------#
#-------------------------------------------------------------------------------------------------------#

####################################
## Context manager: with Config() ##
####################################
'''
Polars Config is often best used as a context manager.
The settings are active only inside the with-block and are restored on exit.

This is the closest Polars equivalent to pandas option_context().
'''

print(df_medals.head(8))
# Default display settings.

with pl.Config(tbl_rows=4, tbl_cols=5, fmt_str_lengths=18):
    print(df_medals)
    # Only the first/last rows and limited columns/string width are displayed.

print(df_medals.head(8))
# Outside the with-block, the previous display settings are restored.

#######################################
## Context manager with method calls ##
#######################################

with pl.Config() as cfg:
    cfg.set_tbl_rows(5)
    cfg.set_tbl_cols(4)
    cfg.set_ascii_tables(True)
    print(df_medals)
# On scope exit, the previous settings are restored.

#####################
## Decorator style ##
#####################
'''
You can also create a reusable Config object and use it as a decorator.
Use apply_on_context_enter=True when you want the settings applied when the
function is called, not immediately when the Config object is created.
'''

cfg_markdown = pl.Config(tbl_formatting="MARKDOWN", apply_on_context_enter=True)

@cfg_markdown
def write_markdown_frame_to_stdout(df: pl.DataFrame) -> None:
    sys.stdout.write(str(df) + "\n")

write_markdown_frame_to_stdout(df_medals.head(3))
# The function prints the DataFrame using Markdown-style table formatting.


#-------------------------------------------------------------------------------------------------------#
#----------------------- 4. Setting startup options in Python/IPython environment ----------------------#
#-------------------------------------------------------------------------------------------------------#
'''
Polars does not require a dedicated startup-options file.
The usual pattern is to put Config calls at the top of a notebook/script, or in
an IPython startup file if you want the same display preferences every session.

Example IPython startup file:

    ~/.ipython/profile_default/startup/00-polars-config.py

Example contents:

    import polars as pl
    pl.Config.set_tbl_rows(20)
    pl.Config.set_tbl_cols(12)
    pl.Config.set_fmt_str_lengths(100)
    pl.Config.set_tbl_width_chars(120)

For a project, you can also save and reload a Config JSON file.
'''

cfg_path = Path("polars_display_config.json")

pl.Config.restore_defaults()
pl.Config.set_tbl_rows(12)
pl.Config.set_tbl_cols(8)
pl.Config.set_fmt_str_lengths(60)

# Save all Config settings as JSON.
json_state = pl.Config.save()
print(type(json_state))
# <class 'str'>

# Save to a file.
pl.Config.save_to_file(cfg_path)

# Restore and reload.
pl.Config.restore_defaults()
pl.Config.load(json_state)

# Or load from file.
pl.Config.restore_defaults()
pl.Config.load_from_file(cfg_path)

# Clean up the demo file.
cfg_path.unlink(missing_ok=True)

# Reset after the demo.
pl.Config.restore_defaults()


#-------------------------------------------------------------------------------------------------------#
#------------------------------------- 5. Frequently used options --------------------------------------#
#-------------------------------------------------------------------------------------------------------#

########################
## tbl_rows: max rows ##
########################
'''
Pandas:
    pd.set_option("display.max_rows", 5)

Polars:
    pl.Config.set_tbl_rows(5)
    with pl.Config(tbl_rows=5): ...

Notes:
1. Applies to DataFrame and Series display.
2. Use a negative value, such as -1, to display all rows/elements.
3. Use None to reset to default.
'''

with pl.Config(tbl_rows=5):
    print(df_medals)
    # Displays a truncated table with first rows, an ellipsis row, and last rows.

with pl.Config(tbl_rows=-1):
    print(df_medals.select("row_id", "Year", "City", "Medal"))
    # Displays all rows because tbl_rows is negative.

###########################
## tbl_cols: max columns ##
###########################
'''
Pandas:
    pd.set_option("display.max_columns", 5)

Polars:
    pl.Config.set_tbl_cols(5)
    with pl.Config(tbl_cols=5): ...

Use -1 to display all columns.
'''

with pl.Config(tbl_cols=5):
    print(df_medals)
    # Displays a subset of columns with an ellipsis column.

with pl.Config(tbl_cols=-1, tbl_width_chars=-1):
    print(df_medals.head(3))
    # Displays all columns and full table width.

################################
## tbl_width_chars: max width ##
################################
'''
Pandas:
    pd.set_option("display.width", 100)

Polars:
    pl.Config.set_tbl_width_chars(100)
    with pl.Config(tbl_width_chars=100): ...

Use -1 to display full width.
'''

df_text = pl.DataFrame(
    {
        "id": ["SEQ1", "SEQ2"],
        "sequence": ["ATGATAAAGGAG", "GCAACGCATATA"],
        "note": [
            "A long text value that will often be truncated in a narrow table",
            "Another long value that is easier to inspect with a wider table",
        ],
    }
)

with pl.Config(tbl_width_chars=40):
    print(df_text)
    # Narrow table; columns/cells may be abbreviated.

with pl.Config(tbl_width_chars=-1, fmt_str_lengths=100):
    print(df_text)
    # Full width plus longer string cell display.

#####################
## fmt_str_lengths ##
#####################
'''
Pandas:
    pd.set_option("display.max_colwidth", 100)

Polars:
    pl.Config.set_fmt_str_lengths(100)
    with pl.Config(fmt_str_lengths=100): ...
'''

with pl.Config(fmt_str_lengths=12):
    print(df_text)
    # Long strings are abbreviated.

with pl.Config(fmt_str_lengths=100):
    print(df_text)
    # Longer strings are displayed.

#######################################
## fmt_table_cell_list_len for lists ##
#######################################
'''
Controls how many list elements are displayed inside a List cell.

Useful with nested Polars data such as pl.List.
Negative values display all list items.
'''

df_lists = pl.DataFrame(
    {
        "id": ["a", "b", "c"],
        "nums": [[1, 2, 3, 4, 5, 6], [10, 20, 30, 40, 50, 60], []],
    }
)

with pl.Config(fmt_table_cell_list_len=2):
    print(df_lists)
    # Shows a shortened list representation.

with pl.Config(fmt_table_cell_list_len=-1):
    print(df_lists)
    # Shows every element in the list cells.

###########################################
## Hide/show shape, dtypes, column names ##
###########################################
'''
Polars tables normally show:
1. DataFrame shape.
2. Column names.
3. A dtype row, such as i64, f64, str, cat.
4. A separator row between column names and dtypes.

You can hide or move some of this display metadata.
'''

with pl.Config(tbl_hide_dataframe_shape=True):
    print(df_medals.head(3))
    # Shape line is hidden.

with pl.Config(tbl_dataframe_shape_below=True):
    print(df_medals.head(3))
    # Shape is printed below the table.

with pl.Config(tbl_hide_column_data_types=True):
    print(df_medals.head(3))
    # Dtype row is hidden.

with pl.Config(tbl_hide_column_names=True):
    print(df_medals.head(3))
    # Column names are hidden.

with pl.Config(tbl_hide_dtype_separator=True):
    print(df_medals.head(3))
    # The '---' dtype separator row is hidden.

with pl.Config(tbl_column_data_type_inline=True):
    print(df_medals.head(3))
    # Dtypes are displayed next to column names.

############################
## Table formatting style ##
############################
'''
Polars can change the table frame style.
Common values include:
1. "UTF8_FULL" / "UTF8_FULL_CONDENSED"
2. "ASCII_FULL" / "ASCII_FULL_CONDENSED"
3. "ASCII_MARKDOWN" / "MARKDOWN"
4. "NOTHING"

The exact visual result depends on the display environment.
'''

with pl.Config(tbl_formatting="ASCII_FULL"):
    print(df_medals.head(3))

with pl.Config(tbl_formatting="ASCII_MARKDOWN"):
    print(df_medals.head(3))

with pl.Config(tbl_formatting="MARKDOWN"):
    print(df_medals.head(3))

# Shortcut for ASCII table borders.
with pl.Config(ascii_tables=True):
    print(df_medals.head(3))

####################
## Cell alignment ##
####################
'''
Alignment options use strings:
    "LEFT", "CENTER", "RIGHT"

Use tbl_cell_alignment for all cells.
Use tbl_cell_numeric_alignment for numeric cells only.
'''

df_align = pl.DataFrame(
    {
        "name": ["Alice", "Bob", "Charlie"],
        "score": [95.25, 88.5, 100.0],
        "passed": [True, True, True],
    }
)

with pl.Config(tbl_cell_alignment="CENTER"):
    print(df_align)

with pl.Config(tbl_cell_numeric_alignment="RIGHT"):
    print(df_align)


#-------------------------------------------------------------------------------------------------------#
#--------------------------------------- 6. Number formatting ------------------------------------------#
#-------------------------------------------------------------------------------------------------------#
'''
Polars number formatting is controlled through pl.Config.
These options affect DISPLAY only. They do not change the underlying values.
'''

df_numbers = pl.DataFrame(
    {
        "raw": [1.0 / 3.0, 1234567.89123, 0.0000012345, -9876.54321],
        "count": [1000, 2500000, 42, -123456],
    }
)

#########################
## set_float_precision ##
#########################

with pl.Config(float_precision=3):
    print(df_numbers)
    # Floating point values are displayed with 3 decimal places.

with pl.Config(float_precision=6):
    print(df_numbers)
    # Floating point values are displayed with 6 decimal places.

###################
## set_fmt_float ##
###################
'''
fmt_float controls the general float display mode.
Common values:
1. "mixed": limited decimal places and scientific notation for very small/large values.
2. "full": print full precision.
'''

with pl.Config(fmt_float="mixed", float_precision=4):
    print(df_numbers)

with pl.Config(fmt_float="full"):
    print(df_numbers)

######################################
## Thousands and decimal separators ##
######################################
'''
Use thousands_separator to group large numbers.
Use decimal_separator to change the decimal point character.

This is a display feature only.
'''

with pl.Config(
    thousands_separator=True,
    float_precision=2,
    tbl_cell_numeric_alignment="RIGHT",
):
    print(df_numbers)
    # Uses the default thousands separator.

with pl.Config(
    thousands_separator=".",
    decimal_separator=",",
    float_precision=3,
    tbl_cell_numeric_alignment="RIGHT",
):
    print(df_numbers)
    # European-style display: 1.234.567,891

############################
## Decimal trailing zeros ##
############################
'''
set_trim_decimal_zeros applies to pl.Decimal display.
It strips trailing zeros from Decimal values when active.
'''

df_decimal = pl.DataFrame(
    data={"amount": [D("1.01000"), D("-5.67890"), D("1000.00000")]},
    schema={"amount": pl.Decimal(scale=5)},
)

with pl.Config(trim_decimal_zeros=False):
    print(df_decimal)
    # Decimal scale is visible, including trailing zeros.

with pl.Config(trim_decimal_zeros=True):
    print(df_decimal)
    # Trailing decimal zeros are trimmed in display.


#-------------------------------------------------------------------------------------------------------#
#------------------------------------ 7. Unicode / ASCII formatting ------------------------------------#
#-------------------------------------------------------------------------------------------------------#
'''
Pandas has display.unicode.east_asian_width for aligning some East Asian
characters.

Polars does not expose the same pandas-style option. Polars display formatting
is mainly controlled by table style, width, string length, and ASCII/UTF8 table
borders.

To keep this file ASCII-only while still demonstrating Unicode strings, the
Unicode values below are written with Python escape sequences.
'''

df_unicode = pl.DataFrame(
    {
        "country": ["UK", "\u65e5\u672c", "\ub300\ud55c\ubbfc\uad6d"],
        "name": ["Alice", "\u3057\u306e\u3076", "\ubbfc\uc218"],
    }
)

print(df_unicode)
# shape: (3, 2)
# ┌──────────┬────────┐
# │ country  ┆ name   │
# │ ---      ┆ ---    │
# │ str      ┆ str    │
# ╞══════════╪════════╡
# │ UK       ┆ Alice  │
# │ 日本      ┆ しのぶ  │
# │ 대한민국   ┆ 민수    │
# └──────────┴────────┘
# Default Polars output uses UTF8 table borders in many terminals.

with pl.Config(ascii_tables=True):
    print(df_unicode)
    # ASCII borders are useful for plain-text logs or environments with poor UTF8 support.

with pl.Config(tbl_formatting="ASCII_MARKDOWN"):
    print(df_unicode)
    # Markdown-like ASCII table formatting.

with pl.Config(tbl_width_chars=60, fmt_str_lengths=20):
    print(df_unicode)
    # Width and string-length options can help with display readability.


#-------------------------------------------------------------------------------------------------------#
#------------------------------- 8. Less common global behavior options --------------------------------#
#-------------------------------------------------------------------------------------------------------#
'''
The options below are not direct equivalents of pandas display options, but they
are part of pl.Config and can affect execution, debugging, or advanced behavior.
'''

###########################
## Verbose/debug logging ##
###########################

with pl.Config(verbose=True):
    result = (
        df_medals.lazy()
        .filter(pl.col("Medal") == "Gold")
        .group_by("NOC")
        .agg(pl.len().alias("gold_count"))
        .collect()
    )
    print(result)
    # Depending on the query and Polars version, verbose mode may print extra debug information.

##########################
## Streaming chunk size ##
##########################
'''
Advanced: set_streaming_chunk_size can override the chunk size used by Polars'
streaming engine. Most users do not need to change it.
'''

pl.Config.set_streaming_chunk_size(100_000)
print(pl.Config.state(if_set=True))
pl.Config.set_streaming_chunk_size(None)

####################
## Auto structify ##
####################
'''
Advanced: set_auto_structify controls whether multi-output expressions are
automatically turned into Struct columns. The current Polars docs mark this
option as deprecated since 1.32.0, so treat it as legacy/awareness material
rather than a recommended setting for new code.
'''

with pl.Config(set_auto_structify=True):
    df_struct_demo = pl.DataFrame({"v": [1, 2, 3], "v2": [4, 5, 6]}).select(pl.all())
    print(df_struct_demo)

#####################
## Engine affinity ##
#####################
'''
Advanced: set_engine_affinity sets the preferred default execution engine.
Most users should leave this unset and let Polars choose.

Examples of why you might care:
1. Debugging a query with a specific engine.
2. Working in an environment configured for GPU/distributed execution.
3. Testing behavior differences across engines.

Because supported engine names depend on your Polars installation and enabled
features, this guide does not force a specific engine value.
'''

print(pl.Config.state(if_set=True))

# Final cleanup so this script does not leave global display settings behind.
pl.Config.restore_defaults()
