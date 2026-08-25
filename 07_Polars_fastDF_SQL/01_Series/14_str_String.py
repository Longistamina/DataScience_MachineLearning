'''
The Polars `.str` namespace provides highly optimized, vectorized string operations
backed by Rust's `regex` and `arrow2` crates.

Key Differences from Pandas:
1. Polars `.str.slice()` takes (offset, length), NOT (start, stop).
2. Element-wise concatenation of multiple Series uses `pl.concat_str()`, not `.str.cat()`.
3. Splitting strings into columns uses `.str.split_exact()` or `.str.extract_groups()`.
4. Methods like `.isalpha()`, `.isdigit()` do not exist natively; use Regex with `.str.contains()`.

##--------------------------------------------------##
1. Slicing and Indexing
2. Basic Transformations
3. Checking methods (Regex required for some)
4. Split and List Indexing
5. Concatenation (pl.concat_str & .list.join)
6. Replacement and Stripping
7. RegEx, Matching, Finding, Extracting
8. Prefix, Suffix, Padding and Alignment
9. Categorical Encoding
10. Real applications
'''

import polars as pl


# =========================================================================================
# 0. Polars .str namespace
# =========================================================================================
'''
Just like pandas, Polars uses the `.str` namespace for string operations.
However, Polars is strictly typed. You MUST cast numeric Series to `pl.String` first.
Note: Unlike pandas (which converts NaN to the string 'nan'), Polars preserves `null` values.
'''

s = pl.Series(['hello', 'world'])
print(s.str.to_uppercase())
# shape: (2,)
# Series: '' [str]
# [
# 	"HELLO"
# 	"WORLD"
# ]

s_nums = pl.Series([1, 2, 3, None, 5])
print(s_nums.cast(pl.String))
# shape: (5,)
# Series: '' [str]
# [
# 	"1"
# 	"2"
# 	"3"
# 	null
# 	"5"
# ]


# =========================================================================================
# 1. Slicing and Indexing
# =========================================================================================

s_heroes = pl.Series(["Tony_Stark", "Steve_Rogers", "Bruce_Banner", "Pietro_Maximoff"])

##--------------##
## .str.slice() ##
##--------------##
'''
CRITICAL DIFFERENCE:
Pandas: .str.slice(start, stop, step)
Polars: .str.slice(offset, length)
'''

# Get first 4 characters (offset=0, length=4)
print(s_heroes.str.slice(0, 4))
# ["Tony", "Stev", "Bruc", "Piet"]

# Get from index 5 to the end (offset=5, length omitted)
print(s_heroes.str.slice(5))
# ["_Stark", "_Rogers", "_Banner", "o_Maximoff"]

# Get last 3 characters using negative offset
print(s_heroes.str.slice(-3))
# ["ark", "ers", "ner", "off"]

##------------##
## .str.get() ##
##------------##
'''
Polars does not have a direct `.str.get(i)` for single characters.
Instead, use `.str.slice(index, 1)` or extract via regex.
'''

print(s_heroes.str.slice(0, 1)) # First character
# ["T", "S", "B", "P"]


# =========================================================================================
# 2. Basic Transformations
# =========================================================================================

s_mixed = pl.Series(['Hello World', 'pandas is FUN', 'Data Science 101'])

##----------------------##
## Case transformations ##
##----------------------##

print(s_mixed.str.to_lowercase())
print(s_mixed.str.to_uppercase())
print(s_mixed.str.to_titlecase()) # Equivalent to pandas .title()
# Note: Polars does not have a direct .capitalize() or .swapcase() method.

##-----------------------##
## Information retrieval ##
##-----------------------##

# Length of strings (Polars distinguishes between bytes and unicode characters)
print(s_mixed.str.len_chars())

# Count occurrences of a substring (literal=True prevents regex parsing)
print(s_mixed.str.count_matches('a', literal=True))
print(s_mixed.str.count_matches(r'\d', literal=False)) # Count digits using regex

##------------------##
##     Stripping    ##
##------------------##

s_spaced = pl.Series(['  hello  ', '  pandas  ', '  data science  '])
print(s_spaced.str.strip_chars())       # Equivalent to .strip()
print(s_spaced.str.strip_chars_start()) # Equivalent to .lstrip()
print(s_spaced.str.strip_chars_end())   # Equivalent to .rstrip()


# =========================================================================================
# 3. Checking methods
# =========================================================================================
'''
NOTE: Polars DOES NOT have native .isalpha(), .isdigit(), .isnumeric() methods.
Because Polars is heavily optimized for Regex and Arrow strings, you achieve this
using .str.contains() with Unicode Regex properties.
'''

s_check = pl.Series(['Hello', 'WORLD', '123', 'Hello123', '   '])

# Equivalent to .isalpha() (Match only Unicode letters)
print(s_check.str.contains(r'^\p{L}+$'))

# Equivalent to .isdigit() (Match only digits)
print(s_check.str.contains(r'^\d+$'))

# Equivalent to .isalnum() (Match letters and numbers)
print(s_check.str.contains(r'^[\p{L}\d]+$'))

# Equivalent to .isspace()
print(s_check.str.contains(r'^\s+$'))

##------------------------##
##     Pattern checks     ##
##------------------------##

s_start = pl.Series(['bat', 'Bear', 'cat', None])

# .starts_with() and .ends_with() are native and highly optimized
print(s_start.str.starts_with('b'))
print(s_start.str.ends_with('t'))

# .contains() (Regex by default, use literal=True for exact substrings)
s_contain = pl.Series(['Mouse', 'dog', 'house and parrot', '23', None])
print(s_contain.str.contains('og', literal=True))
print(s_contain.str.contains(r'\d|parrot|Mo', literal=False)) # Regex pattern


# =========================================================================================
# 4. Split and List Indexing
# =========================================================================================

s_split = pl.Series(['apple_banana_cherry', 'dog_cat', 'one_two_three_four', None])

##-------------------##
##     Splitting     ##
##-------------------##

# .str.split() returns a Series of type List(String)
print(s_split.str.split('_'))
# [["apple", "banana", "cherry"], ["dog", "cat"], ["one", "two", "three", "four"], null]

# Split up to 2 delimiters (n=3 parts max)
print(s_split.str.splitn('_', 3))

##------------------------##
##     SPLIT INDEXING     ##
##------------------------##
'''
In pandas: s.str.split('_').str[1]
In Polars: Because .str.split() returns a List, you use the `.list` namespace!
'''

print(s_split.str.split('_').list.get(0)) # Get first element
print(s_split.str.split('_').list.get(1)) # Get second element

##---------------------##
##  Expand to Columns  ##
##---------------------##
'''
In pandas: s.str.split('_', expand=True)
In Polars: Use .str.split_exact() which returns a Struct, then .unnest() in a DataFrame.
'''

df_split = pl.DataFrame({"text": s_split})
print(
    df_split.with_columns(
        pl.col("text").str.split_exact('_', 2).alias("fields")
    ).unnest("fields")
)
# shape: (4, 4)
# ┌──────────────────────┬────────┬────────┬────────────┐
# │ text                 ┆ field_0┆ field_1┆ field_2    │
# │ ---                  ┆ ---    ┆ ---    ┆ ---        │
# │ str                  ┆ str    ┆ str    ┆ str        │
# ╞══════════════════════╪════════╪════════╪════════════╡
# │ apple_banana_cherry  ┆ apple  ┆ banana ┆ cherry     │
# │ dog_cat              ┆ dog    ┆ cat    ┆ null       │
# │ one_two_three_four   ┆ one    ┆ two    ┆ three_four │
# │ null                 ┆ null   ┆ null   ┆ null       │
# └──────────────────────┴────────┴────────┴────────────┘


# =========================================================================================
# 5. Concatenation
# =========================================================================================
'''
Pandas: .str.cat(others) or .str.join()
Polars: pl.concat_str() for Series, .list.join() for Lists
'''

s1 = pl.Series(['a', 'b', 'c'])
s2 = pl.Series(['1', '2', '3'])

# Element-wise concatenation of multiple Series
print(pl.select(pl.concat_str([s1, s2], separator='_'))) # pl.concat_str([s1, s2], separator='_') returns an expr, use pl.select() to display in DF form
# ["a_1", "b_2", "c_3"]

# Joining elements inside a List column
s_lists = pl.Series([['apple', 'banana'], ['dog', 'cat']])
print(s_lists.list.join('-'))
# ["apple-banana", "dog-cat"]


# =========================================================================================
# 6. Replacement, Removal, Repeat
# =========================================================================================

s_replace = pl.Series(['apple_banana_cherry', 'dog_cat', '1234', None])

##----------------##
## .str.replace() ##
##----------------##

# Replace first occurrence (literal=True for exact string match)
print(s_replace.str.replace('_', ' || ', literal=True))

# Replace ALL occurrences
print(s_replace.str.replace_all('_', ' || ', literal=True))

# Replace using Regex
print(s_replace.str.replace_all(r'\d', '#', literal=False))

##-----------------------##
## .str.strip_prefix()   ##
##-----------------------##

s_prefix = pl.Series(['pre_apple', 'pre_banana', 'cat'])
print(s_prefix.str.strip_prefix('pre_'))

##-----------------------##
## .str.strip_suffix()   ##
##-----------------------##

s_suffix = pl.Series(['apple_suf', 'banana_suf', 'dog'])
print(s_suffix.str.strip_suffix('_suf'))


# =========================================================================================
# 7. RegEx, Matching, Finding, Extracting
# =========================================================================================

s_match = pl.Series(['abc123', 'def456', 'ghi789', '123abc', None])

##--------------------------------------##
##               Finding                ##
##--------------------------------------##

# Find index of first occurrence
print(s_match.str.find('123', literal=True))
# [3, null, null, 0, null]

##--------------------------------------##
##              Extracting              ##
##--------------------------------------##

s_extract = pl.Series(['a1', 'b2', 'c3'])

# Extract single group
print(s_extract.str.extract(r'[ab](\d)', 1))
# ["1", "2", null]

# Extract MULTIPLE groups into columns (Equivalent to pandas expand=True)
# .str.extract_groups() returns a Struct containing all capture groups
df_ext = pl.DataFrame({"text": s_extract})
print(
    df_ext.with_columns(
        pl.col("text").str.extract_groups(r'([ab])(\d)').alias("groups")
    ).unnest("groups")
)
# shape: (3, 3)
# ┌──────┬───────┬───────┐
# │ text ┆ 1     ┆ 2     │
# │ ---  ┆ ---   ┆ ---   │
# │ str  ┆ str   ┆ str   │
# ╞══════╪═══════╪═══════╡
# │ a1   ┆ a     ┆ 1     │
# │ b2   ┆ b     ┆ 2     │
# │ c3   ┆ null  ┆ null  │
# └──────┴───────┴───────┘

# Extract ALL matches (Returns List of Strings)
s_extall = pl.Series(["a2a4", "b63", "ccc"])
print(s_extall.str.extract_all(r'[ab]\d'))
# [["a2", "a4"], ["b6"], []]


# =========================================================================================
# 8. Prefix, Suffix, Padding and Alignment
# =========================================================================================
'''
Polars Series does not have ``add()`` or ``radd()`` methods natively like Pandas,
so we need to register it like this.
'''

@pl.api.register_series_namespace("mystr")
class MyStrNamespace:
    def __init__(self, s: pl.Series):
        self._s = s

    def radd(self, prefixes) -> pl.Series:
        """Prepend each element of `prefixes` to the corresponding element of the Series."""
        return pl.Series(prefixes, dtype=pl.Utf8) + self._s

    def add(self, suffixes) -> pl.Series:
        """Append each element of `suffixes` to the corresponding element of the Series."""
        return self._s + pl.Series(suffixes, dtype=pl.Utf8)

##-------------------------------------------------------##
## add prefix: Use + operator, or register new namespace ##
##-------------------------------------------------------##

s_asean = pl.Series(["Vietnam", "Philipines", "Malaysia", "Myanmar"])

print(s_asean.mystr.radd(["ASEAN_"])) #  pl.Series(["ASEAN_"]) + s_asean
# shape: (4,)
# Series: '' [str]
# [
# 	"ASEAN_Vietnam"
# 	"ASEAN_Philipines"
# 	"ASEAN_Malaysia"
# 	"ASEAN_Myanmar"
# ]

print(s_asean.mystr.radd(["VN_", "PH_", "MY_", "MM_"])) # pl.Series(["VN_", "PH_", "MY_", "MM_"]) + s_asean
# shape: (4,)
# Series: '' [str]
# [
# 	"VN_Vietnam"
# 	"PH_Philipines"
# 	"MY_Malaysia"
# 	"MM_Myanmar"
# ]

##-------------------------------------------------------##
## add suffix: Use + operator, or register new namespace ##
##-------------------------------------------------------##

s_vn = pl.Series(["Vietnam"]*3)

print(s_vn.mystr.add(["_1975"])) # s_vn + pl.Series(["_1975"])
# shape: (3,)
# Series: '' [str]
# [
# 	"Vietnam_1975"
# 	"Vietnam_1975"
# 	"Vietnam_1975"
# ]

print(s_vn.mystr.add(["_north", "_center", "_south"])) # s_vn + pl.Series(["_north", "_center", "_south"])
# shape: (3,)
# Series: '' [str]
# [
# 	"Vietnam_north"
# 	"Vietnam_center"
# 	"Vietnam_south"
# ]

##-----------------------##
## Padding and Alignment ##
##-----------------------##

s_align = pl.Series(['dog', 'bird', 'mouse'])

# Right-align (pad on left) -> Equivalent to pandas .rjust()
print(s_align.str.pad_start(8, '.'))
# [".....dog", "....bird", "...mouse"]

# Left-align (pad on right) -> Equivalent to pandas .ljust()
print(s_align.str.pad_end(8, '.'))
# ["dog.....", "bird....", "mouse..."]

# Zero-fill
print(pl.Series(['1', '22', '333']).str.zfill(5))
# ["00001", "00022", "00333"]

# Note: Polars does not have a native .center() method.


# =========================================================================================
# 9. Categorical Encoding
# =========================================================================================

s_gender = pl.Series(["M", "M", "F", "M", "LGBTQ", "F", "M", "F", "LGBTQ", "M"])

##-----------------------------------##
##            Factorize              ##
##-----------------------------------##
'''
In Polars, casting to Categorical and then calling .to_physical() yields the integer codes.
'''

codes = s_gender.cast(pl.Categorical).to_physical()
print(codes)
# shape: (10,)
# Series: '' [u32]
# [
# 	0
# 	0
# 	1
# ...

##-------------------------------------##
##            .to_dummies()            ##
##-------------------------------------##
'''
.to_dummies() return one-hot encoder
'''

print(s_gender.to_dummies(separator="gender_"))
# shape: (10, 3)
# ┌───────────┬────────────┬──────────────┐
# │ gender_M  ┆ gender_F   ┆ gender_LGBTQ │
# │ ---       ┆ ---        ┆ ---          │
# │ u8        ┆ u8         ┆ u8           │
# ╞═══════════╪════════════╪══════════════╡
# │ 1         ┆ 0          ┆ 0            │
# │ 1         ┆ 0          ┆ 0            │
# │ 0         ┆ 1          ┆ 0            │
# ...


# =========================================================================================
# 10. Real applications
# =========================================================================================

##---------------##
## Data cleaning ##
##---------------##

messy_names = pl.Series(['  john doe  ', 'JANE SMITH', 'bob-johnson'])

# Polars expression chaining is incredibly clean for data pipelines
clean_names = (
    messy_names
    .str.strip_chars()
    .str.replace_all('-', ' ', literal=True)
    .str.to_titlecase()
    .str.replace_all(r'\s+', ' ', literal=False) # Regex to collapse multiple spaces
)
print(clean_names)
# ["John Doe", "Jane Smith", "Bob Johnson"]

##------------------##
## Email processing ##
##------------------##

emails = pl.Series(['user@example.com', 'ADMIN@SITE.ORG', 'invalid.email'])
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

df_emails = pl.DataFrame({"email": emails})
print(
    df_emails.with_columns(
        pl.col("email").str.contains(email_pattern).alias("is_valid"),
        pl.col("email").str.extract(r'@([^.]+\..*)', 1).alias("domain"),
        pl.col("email").str.extract(r'^([^@]+)@', 1).alias("username")
    )
)
# shape: (3, 4)
# ┌──────────────────┬──────────┬──────────────┬──────────┐
# │ email            ┆ is_valid ┆ domain       ┆ username │
# │ ---              ┆ ---      ┆ ---          ┆ ---      │
# │ str              ┆ bool     ┆ str          ┆ str      │
# ╞══════════════════╪══════════╪══════════════╪══════════╡
# │ user@example.com ┆ true     ┆ example.com  ┆ user     │
# │ ADMIN@SITE.ORG   ┆ true     ┆ SITE.ORG     ┆ ADMIN    │
# │ invalid.email    ┆ false    ┆ null         ┆ null     │
# └──────────────────┴──────────┴──────────────┴──────────┘
