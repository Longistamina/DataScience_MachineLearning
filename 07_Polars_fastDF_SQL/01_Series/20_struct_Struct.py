'''
In Polars, pl.Struct is a nested data type that stores multiple NAMED fields
inside one Series value. Think of it like a typed Python dict / TypedDict:
field names and field dtypes belong to the dtype, while each row stores values
for those fields.

Struct columns commonly appear when:
1. You build a Series/DataFrame from dictionaries.
2. You collect columns with pl.struct(...).
3. You call expression methods that need to return multiple values, such as
   value_counts(), str.extract_groups(), and str.split_exact().

Key Differences from pl.List and pl.Array:
1. pl.Struct stores named fields, not positional elements only.
2. Fields can have different dtypes, e.g. string + float + bool in one value.
3. You usually extract fields with .struct.field("name") or expand them with
   .struct.unnest().
4. The Series.struct namespace is intentionally small compared with .list/.arr.

Covered commands from polars.Series.struct:
field, json_encode, rename_fields, unnest, fields, schema

######################################################
0. Creation: dictionaries, pl.Struct dtype, and pl.struct()
1. Inspecting Struct Metadata (fields, schema)
2. Field Extraction (field, struct[...] convenience)
3. Renaming Fields (rename_fields)
4. Expanding Structs (unnest)
5. Encoding Structs (json_encode)
6. Common Struct Producers
7. Real applications
'''

import polars as pl
pl.Config(fmt_str_lengths=1000)

#-------------------------------------------------------------------------------------------------#
#-------------------------------------- 0. Creation ----------------------------------------------#
#-------------------------------------------------------------------------------------------------#
'''
Polars can infer a Struct dtype from dictionaries.
The field order is inferred from the first dictionary and retained by the Struct dtype.
'''

s_ratings = pl.Series(
    "ratings",
    [
        {"movie": "Cars", "theatre": "NE", "avg_rating": 4.5},
        {"movie": "Toy Story", "theatre": "ME", "avg_rating": 4.9},
        {"movie": "Snow White", "theatre": "IL", "avg_rating": 4.7},
    ],
)
print(s_ratings)
# shape: (3,)
# Series: 'ratings' [struct[3]]
# [
#     {"Cars","NE",4.5}
#     {"Toy Story","ME",4.9}
#     {"Snow White","IL",4.7}
# ]

##############################
## Explicit pl.Struct dtype ##
##############################
'''
For production code, explicitly defining the struct schema can be clearer.
A Struct schema is a mapping from field names to Polars dtypes.
'''

rating_dtype = pl.Struct(
    {
        "movie": pl.String,
        "theatre": pl.String,
        "avg_rating": pl.Float64,
    }
)

s_typed = pl.Series(
    "ratings",
    [
        {"movie": "Cars", "theatre": "NE", "avg_rating": 4.5},
        {"movie": "Toy Story", "theatre": "ME", "avg_rating": 4.9},
    ],
    dtype=rating_dtype,
)
print(s_typed)
# shape: (2,)
# Series: 'ratings' [struct[3]]
# [
# 	{"Cars","NE",4.5}
# 	{"Toy Story","ME",4.9}
# ]
# Same logical values, but the dtype/schema is explicitly controlled.

##########################################
## Creating Structs from DataFrame cols ##
##########################################
'''
Use pl.struct(...) to pack multiple columns into one Struct column.
This is the most common DataFrame workflow.
'''

df_movies = pl.DataFrame(
    {
        "movie": ["Cars", "Toy Story", "Snow White"],
        "theatre": ["NE", "ME", "IL"],
        "avg_rating": [4.5, 4.9, 4.7],
        "votes": [120, 98, 75],
    }
)

df_packed = df_movies.select(
    pl.struct("movie", "theatre", "avg_rating").alias("rating_info")
)
print(df_packed)
# shape: (3, 1)
# ┌─────────────────────────┐
# │ rating_info             │
# │ ---                     │
# │ struct[3]               │
# ╞═════════════════════════╡
# │ {"Cars","NE",4.5}       │
# │ {"Toy Story","ME",4.9}  │
# │ {"Snow White","IL",4.7} │
# └─────────────────────────┘

##########################################
## Handling missing / inconsistent keys ##
##########################################
'''
If later dictionaries are missing a field from the first dictionary, that field
can become null. If types are inconsistent, Polars may raise unless strict=False
or an explicit dtype can coerce the values.
'''

s_missing = pl.Series(
    "ratings",
    [
        {"movie": "Cars", "theatre": "NE", "avg_rating": 4.5},
        {"movie": "Toy Story", "theatre": "ME"},  # missing avg_rating
    ],
    strict=False,
)
print(s_missing)
# shape: (2,)
# Series: 'ratings' [struct[3]]
# [
# 	{"Cars","NE",4.5}
# 	{"Toy Story","ME",null}
# ]
# The second row has null for avg_rating.


#-------------------------------------------------------------------------------------------------#
#------------------------------- 1. Inspecting Struct Metadata -----------------------------------#
#-------------------------------------------------------------------------------------------------#

s_ratings = pl.Series(
    "ratings",
    [
        {"movie": "Cars", "theatre": "NE", "avg_rating": 4.5},
        {"movie": "Toy Story", "theatre": "ME", "avg_rating": 4.9},
        {"movie": "Snow White", "theatre": "IL", "avg_rating": 4.7},
    ],
)

####################
## .struct.fields ##
####################
'''
.struct.fields returns the field names as a Python list.
This is an ATTRIBUTE, not a method, so do not add parentheses.
'''

print(s_ratings.struct.fields)
# ['movie', 'theatre', 'avg_rating']

####################
## .struct.schema ##
####################
'''
.struct.schema returns the full struct definition as a Polars Schema object.
It maps field names to dtypes.
This is also an ATTRIBUTE, not a method.
'''

print(s_ratings.struct.schema)
# Schema({'movie': String, 'theatre': String, 'avg_rating': Float64})

# Use metadata checks before extracting fields.
if "avg_rating" in s_ratings.struct.fields:
    print("avg_rating exists")


#-------------------------------------------------------------------------------------------------#
#----------------------------------- 2. Field Extraction -----------------------------------------#
#-------------------------------------------------------------------------------------------------#

#########################
## .struct.field(name) ##
#########################
'''
.struct.field(name) extracts one named field from every struct row and returns
a normal Series with that field's dtype.
'''

print(s_ratings.struct.field("movie"))
# shape: (3,)
# Series: 'movie' [str]
# [
#     "Cars"
#     "Toy Story"
#     "Snow White"
# ]

print(s_ratings.struct.field("avg_rating"))
# shape: (3,)
# Series: 'avg_rating' [f64]
# [
#     4.5
#     4.9
#     4.7
# ]

########################################
## Convenience: .struct[...] indexing ##
########################################
'''
Polars also supports convenient struct indexing on Series:
+ s.struct["field_name"] extracts by field name.
+ s.struct[index] extracts by field position.

Prefer .struct.field("name") in guide/example code because it is explicit.
'''

print(s_ratings.struct["theatre"])
# Same as s_ratings.struct.field("theatre")

print(s_ratings.struct[0])
# Same as s_ratings.struct.field("movie") because movie is field position 0.

##########################################
## Extracting in a DataFrame expression ##
##########################################
'''
Inside DataFrame workflows, use the expression namespace:
pl.col("struct_col").struct.field("field_name")
'''

df_ratings = pl.DataFrame({"ratings": s_ratings})

print(
    df_ratings.with_columns(
        pl.col("ratings").struct.field("movie").alias("movie"),
        pl.col("ratings").struct.field("avg_rating").alias("rating"),
    )
)
# shape: (3, 3)
# ┌─────────────────────────┬────────────┬────────┐
# │ ratings                 ┆ movie      ┆ rating │
# │ ---                     ┆ ---        ┆ ---    │
# │ struct[3]               ┆ str        ┆ f64    │
# ╞═════════════════════════╪════════════╪════════╡
# │ {"Cars","NE",4.5}       ┆ Cars       ┆ 4.5    │
# │ {"Toy Story","ME",4.9}  ┆ Toy Story  ┆ 4.9    │
# │ {"Snow White","IL",4.7} ┆ Snow White ┆ 4.7    │
# └─────────────────────────┴────────────┴────────┘


#-------------------------------------------------------------------------------------------------#
#----------------------------------- 3. Renaming Fields ------------------------------------------#
#-------------------------------------------------------------------------------------------------#

#############################
## .struct.rename_fields() ##
#############################
'''
.rename_fields(names) renames the fields of the Struct Series.
The new names must be given in the SAME ORDER as the current fields.
It does not change the values; it only changes the struct field names.
'''

s_renamed = s_ratings.struct.rename_fields(["title", "state", "rating"])

print(s_renamed.struct.fields)
# ['title', 'state', 'rating']

print(s_renamed.struct.schema)
# Schema({'title': String, 'state': String, 'rating': Float64})

print(s_renamed.struct.field("title"))
# shape: (3,)
# Series: 'title' [str]
# [
#     "Cars"
#     "Toy Story"
#     "Snow White"
# ]

#######################################
## Rename before unnesting if needed ##
#######################################
'''
If a DataFrame already has columns with the same names as struct fields,
renaming the struct fields before unnesting avoids name collisions.
'''

df_with_conflict = pl.DataFrame(
    {
        "movie": ["original_1", "original_2", "original_3"], # This will conflict with s_ratings.struct["movie"]
        "ratings": s_ratings,
    }
)

df_no_conflict = df_with_conflict.with_columns(
    pl.col("ratings")
    .struct.rename_fields(["rating_movie", "rating_theatre", "rating_value"]) # Rename struct file "movie" -> "rating_movie" to avoid conflict
    .alias("ratings")
)

print(df_no_conflict.unnest("ratings"))
# shape: (3, 4)
# ┌────────────┬──────────────┬────────────────┬──────────────┐
# │ movie      ┆ rating_movie ┆ rating_theatre ┆ rating_value │
# │ ---        ┆ ---          ┆ ---            ┆ ---          │
# │ str        ┆ str          ┆ str            ┆ f64          │
# ╞════════════╪══════════════╪════════════════╪══════════════╡
# │ original_1 ┆ Cars         ┆ NE             ┆ 4.5          │
# │ original_2 ┆ Toy Story    ┆ ME             ┆ 4.9          │
# │ original_3 ┆ Snow White   ┆ IL             ┆ 4.7          │
# └────────────┴──────────────┴────────────────┴──────────────┘


#-------------------------------------------------------------------------------------------------#
#------------------------------------ 4. Expanding Structs ---------------------------------------#
#-------------------------------------------------------------------------------------------------#

######################
## .struct.unnest() ##
######################
'''
.struct.unnest() converts a Struct Series into a DataFrame with one column per field.
This is the Series-level equivalent of DataFrame.unnest("struct_col").
'''

print(s_ratings.struct.unnest())
# shape: (3, 3)
# ┌────────────┬─────────┬────────────┐
# │ movie      ┆ theatre ┆ avg_rating │
# │ ---        ┆ ---     ┆ ---        │
# │ str        ┆ str     ┆ f64        │
# ╞════════════╪═════════╪════════════╡
# │ Cars       ┆ NE      ┆ 4.5        │
# │ Toy Story  ┆ ME      ┆ 4.9        │
# │ Snow White ┆ IL      ┆ 4.7        │
# └────────────┴─────────┴────────────┘

####################################
## DataFrame.unnest() equivalent  ##
####################################
'''
When the struct is a column in a DataFrame, use DataFrame.unnest().
That operation expands the struct column in-place into its fields.
'''

df_ratings = pl.DataFrame(
    {
        "row_id": [1, 2, 3],
        "ratings": s_ratings,
    }
)

print(df_ratings.unnest("ratings"))
# shape: (3, 4)
# ┌────────┬────────────┬─────────┬────────────┐
# │ row_id ┆ movie      ┆ theatre ┆ avg_rating │
# │ ---    ┆ ---        ┆ ---     ┆ ---        │
# │ i64    ┆ str        ┆ str     ┆ f64        │
# ╞════════╪════════════╪═════════╪════════════╡
# │ 1      ┆ Cars       ┆ NE      ┆ 4.5        │
# │ 2      ┆ Toy Story  ┆ ME      ┆ 4.9        │
# │ 3      ┆ Snow White ┆ IL      ┆ 4.7        │
# └────────┴────────────┴─────────┴────────────┘


#-------------------------------------------------------------------------------------------------#
#------------------------------------ 5. Encoding Structs ----------------------------------------#
#-------------------------------------------------------------------------------------------------#

###########################
## .struct.json_encode() ##
###########################
'''
.struct.json_encode() serializes each struct value into a JSON string.
This is useful for logging, exporting payload columns, or passing nested data
to systems that expect JSON text.
'''

s_payload = pl.Series(
    "payload",
    [
        {"id": 1, "tags": ["family", "pixar"], "score": 4.5},
        {"id": 2, "tags": ["classic"], "score": None},
    ],
)

print(s_payload.struct.json_encode())
# shape: (2,)
# Series: 'payload' [str]
# [
# 	"{"id":1,"tags":["family","pixar"],"score":4.5}"
# 	"{"id":2,"tags":["classic"],"score":null}"
# ]

##########################################
## JSON encode after field manipulation ##
##########################################

s_api_payload = s_ratings.struct.rename_fields(["title", "region", "rating"])
print(s_api_payload.struct.json_encode())
# shape: (3,)
# Series: 'ratings' [str]
# [
# 	"{"title":"Cars","region":"NE","rating":4.5}"
# 	"{"title":"Toy Story","region":"ME","rating":4.9}"
# 	"{"title":"Snow White","region":"IL","rating":4.7}"
# ]
# JSON strings use the renamed field names.



#-------------------------------------------------------------------------------------------------#
#---------------------------------- 6. Common Struct Producers -----------------------------------#
#-------------------------------------------------------------------------------------------------#
'''
Several Polars operations produce Struct data because Polars expressions return
one Series. Struct is how Polars can represent multiple output values inside
that one Series.
'''

###################################
## value_counts() in expressions ##
###################################

df_theatres = pl.DataFrame(
    {
        "theatre": ["NE", "IL", "NE", "ND", "IL", "NE", "ME"],
    }
)

counts_as_struct = df_theatres.select(
    pl.col("theatre").value_counts(sort=True).alias("counts")
)
print(counts_as_struct)
# shape: (4, 1)
# ┌───────────┐
# │ counts    │
# │ ---       │
# │ struct[2] │
# ╞═══════════╡
# │ {"NE",3}  │
# │ {"IL",2}  │
# │ {"ND",1}  │
# │ {"ME",1}  │
# └───────────┘

# Convert the Series of structs into a normal two-column DataFrame.
print(counts_as_struct["counts"].struct.unnest())
# shape: (4, 2)
# ┌─────────┬───────┐
# │ theatre ┆ count │
# │ ---     ┆ ---   │
# │ str     ┆ u32   │
# ╞═════════╪═══════╡
# │ NE      ┆ 3     │
# │ IL      ┆ 2     │
# │ ND      ┆ 1     │
# │ ME      ┆ 1     │
# └─────────┴───────┘

####################################
## str.extract_groups() -> Struct ##
####################################

s_codes = pl.Series("code", ["A-001", "B-014", "bad"])

s_groups = s_codes.str.extract_groups(r"(?P<prefix>[A-Z])-(?P<number>\d+)")
print(s_groups)
# shape: (3,)
# Series: 'code' [struct[2]]
# [
# 	{"A","001"}
# 	{"B","014"}
# 	{null,null}
# ]

print(s_groups.struct.fields)
# ['prefix', 'number']

print(s_groups.struct.unnest())
# shape: (3, 2)
# ┌────────┬────────┐
# │ prefix ┆ number │
# │ ---    ┆ ---    │
# │ str    ┆ str    │
# ╞════════╪════════╡
# │ A      ┆ 001    │
# │ B      ┆ 014    │
# │ null   ┆ null   │
# └────────┴────────┘

#################################
## str.split_exact() -> Struct ##
#################################

s_names = pl.Series("name", ["Tony_Stark", "Steve_Rogers", "Cher"])

s_split = s_names.str.split_exact("_", 1)
print(s_split.struct.fields)
# ['field_0', 'field_1']

print(s_split.struct.rename_fields(["first", "last"]).struct.unnest())
# ['field_0', 'field_1']
# shape: (3, 2)
# ┌───────┬────────┐
# │ first ┆ last   │
# │ ---   ┆ ---    │
# │ str   ┆ str    │
# ╞═══════╪════════╡
# │ Tony  ┆ Stark  │
# │ Steve ┆ Rogers │
# │ Cher  ┆ null   │
# └───────┴────────┘


#-------------------------------------------------------------------------------------------------#
#------------------------------------ 7. Real applications ---------------------------------------#
#-------------------------------------------------------------------------------------------------#

#########################################
## Pack nested payload, export as JSON ##
#########################################

df_events = pl.DataFrame(
    {
        "event_id": [101, 102, 103],
        "user": ["u1", "u2", "u1"],
        "action": ["view", "click", "purchase"],
        "amount": [None, None, 39.99],
    }
)

api_ready = df_events.select(
    "event_id",
    pl.struct("user", "action", "amount").alias("payload"),
).with_columns(
    pl.col("payload").struct.json_encode().alias("payload_json")
)
print(api_ready)
# shape: (3, 3)
# ┌──────────┬─────────────────────────┬──────────────────────────────────────────────────┐
# │ event_id ┆ payload                 ┆ payload_json                                     │
# │ ---      ┆ ---                     ┆ ---                                              │
# │ i64      ┆ struct[3]               ┆ str                                              │
# ╞══════════╪═════════════════════════╪══════════════════════════════════════════════════╡
# │ 101      ┆ {"u1","view",null}      ┆ {"user":"u1","action":"view","amount":null}      │
# │ 102      ┆ {"u2","click",null}     ┆ {"user":"u2","action":"click","amount":null}     │
# │ 103      ┆ {"u1","purchase",39.99} ┆ {"user":"u1","action":"purchase","amount":39.99} │
# └──────────┴─────────────────────────┴──────────────────────────────────────────────────┘

######################################
## Multi-column duplicate detection ##
######################################
'''
Structs are useful when you need to treat multiple columns as one composite key.
Here, pl.struct("user", "action") lets Polars compare/hash both columns together.
'''

df_dupes = df_events.with_columns(
    pl.struct("user", "action").is_duplicated().alias("duplicate_user_action")
)
print(df_dupes)
# shape: (3, 5)
# ┌──────────┬──────┬──────────┬────────┬───────────────────────┐
# │ event_id ┆ user ┆ action   ┆ amount ┆ duplicate_user_action │
# │ ---      ┆ ---  ┆ ---      ┆ ---    ┆ ---                   │
# │ i64      ┆ str  ┆ str      ┆ f64    ┆ bool                  │
# ╞══════════╪══════╪══════════╪════════╪═══════════════════════╡
# │ 101      ┆ u1   ┆ view     ┆ null   ┆ false                 │
# │ 102      ┆ u2   ┆ click    ┆ null   ┆ false                 │
# │ 103      ┆ u1   ┆ purchase ┆ 39.99  ┆ false                 │
# └──────────┴──────┴──────────┴────────┴───────────────────────┘

###########################################
## Normalize nested records into columns ##
###########################################

df_nested = pl.DataFrame(
    {
        "id": [1, 2],
        "contact": pl.Series(
            "contact",
            [
                {"email": "a@example.com", "phone": "111-222"},
                {"email": "b@example.com", "phone": None},
            ],
        ),
    }
)

# Step 1: inspect fields before expanding.
print(df_nested["contact"].struct.fields)
# ['email', 'phone']

# Step 2: unnest into normal columns.
print(df_nested.unnest("contact"))
# shape: (2, 3)
# ┌─────┬───────────────┬─────────┐
# │ id  ┆ email         ┆ phone   │
# │ --- ┆ ---           ┆ ---     │
# │ i64 ┆ str           ┆ str     │
# ╞═════╪═══════════════╪═════════╡
# │ 1   ┆ a@example.com ┆ 111-222 │
# │ 2   ┆ b@example.com ┆ null    │
# └─────┴───────────────┴─────────┘
