'''
In Polars, binary data is handled using the strictly typed `pl.Binary` data type.
Unlike strings (which are strictly UTF-8 encoded text), Binary Series hold raw,
arbitrary byte sequences. This is highly useful for handling serialized data,
cryptography, images, or low-level memory manipulation.

The `.bin` namespace provides vectorized operations specifically for raw bytes.
The `.str` namespace provides operations for text strings (including decoding text into bytes).

######################################################
0. Creation: Byte strings (b"...") and casting
1. Transfer Encodings: Hex and Base64 (.str.decode vs .bin.encode)
2. UTF-8 String Conversion (Casting)
3. Searching & Matching (.bin.contains, .starts_with, .ends_with)
4. Slicing & Extraction (.bin.slice, .head, .tail, .bin.get)
5. Size & Information (.bin.size)
6. Low-Level Memory Casting (.bin.reinterpret)
'''

import polars as pl
import struct

#-------------------------------------------------------------------------------------------------#
#--------------------------------------- 0. Creation ---------------------------------------------#
#-------------------------------------------------------------------------------------------------#
'''
You can create a Binary Series by passing Python byte strings (prefixed with `b`),
or by casting a standard String Series to `pl.Binary`.
'''

# Method 1: Direct byte strings
s_bin_raw = pl.Series([b"\x00\x01\x02", b"\xff\xfe\xfd"])
print(s_bin_raw)
# shape: (2,)
# Series: '' [binary]
# [
# 	b"\x00\x01\x02"
# 	b"\xff\xfe\xfd"
# ]

# Method 2: Casting standard UTF-8 strings to raw binary bytes
s_str = pl.Series(["hello", "world", "polars", "data"])
s_bin = s_str.cast(pl.Binary)
print(s_bin)
# shape: (4,)
# Series: '' [binary]
# [
# 	b"hello"
# 	b"world"
# 	b"polars"
# 	b"data"
# ]

#-------------------------------------------------------------------------------------------------#
#----------------------------- 1. Transfer Encodings (Hex & Base64) ------------------------------#
#-------------------------------------------------------------------------------------------------#
'''
IMPORTANT: The namespace you use depends strictly on the CURRENT data type of the Series!
- If you have a String Series (text) and want to decode it into raw Binary bytes,
  you MUST use the `.str` namespace: `.str.decode("hex")` or `.str.decode("base64")`.
- If you have a Binary Series (raw bytes) and want to encode it into a text String,
  you MUST use the `.bin` namespace: `.bin.encode("hex")` or `.bin.encode("base64")`.
'''

# 1. Convert Hex String -> Raw Binary (using .str.decode)
s_hex_strings = pl.Series(["68656c6c6f", "776f726c64"]) # This is a pl.String Series
s_bin_from_hex = s_hex_strings.str.decode("hex")        # Use .str namespace to decode string into binary
print(s_bin_from_hex)
# shape: (2,)
# Series: '' [binary]
# [
# 	b"hello"
# 	b"world"
# ]

# 2. Convert Raw Binary -> Base64 String (using .bin.encode)
# s_bin_from_hex is now a pl.Binary Series, so we use the .bin namespace to encode it into a string
s_base64_str = s_bin_from_hex.bin.encode("base64")
print(s_base64_str)
# shape: (2,)
# Series: '' [str]
# [
# 	"aGVsbG8="
# 	"d29ybGQ="
# ]


#-------------------------------------------------------------------------------------------------#
#-------------------------------- 2. UTF-8 String Conversion -------------------------------------#
#-------------------------------------------------------------------------------------------------#
'''
To convert raw UTF-8 bytes to a Polars String (or vice versa), you simply use `.cast()`.
Polars natively assumes `pl.Binary` <-> `pl.String` casting uses UTF-8.
'''

# Raw bytes to UTF-8 String
s_valid_bytes = pl.Series([b"hello", b"world"])
print(s_valid_bytes.cast(pl.String))
# shape: (2,)
# Series: '' [str]
# [
# 	"hello"
# 	"world"
# ]

# Handling invalid UTF-8 bytes (strict=False replaces invalid sequences with null)
s_bad_bytes = pl.Series([b"valid", b"\xff\xfe\xfd"])
print(s_bad_bytes.cast(pl.String))
# Note: Depending on the Polars version, invalid bytes might raise an error or become null.
# To be safe with messy byte data, you can use map_elements or handle it at ingestion.


#-------------------------------------------------------------------------------------------------#
#----------------------------- 3. Searching & Matching -------------------------------------------#
#-------------------------------------------------------------------------------------------------#
'''
You can search for specific byte substrings using `.bin.contains()`,
`.bin.starts_with()`, and `.bin.ends_with()`.
Note: The search patterns MUST be byte strings (e.g., b"or").
'''

s_bin = pl.Series([b"hello", b"world", b"polars", b"data"])

# Check if binary contains a specific byte sequence
print(s_bin.bin.contains(b"or"))
# [false, false, true, false]

# Check if binary starts with a specific byte sequence
print(s_bin.bin.starts_with(b"he"))
# [true, false, false, false]

# Check if binary ends with a specific byte sequence
print(s_bin.bin.ends_with(b"ld"))
# [false, true, false, false]


#-------------------------------------------------------------------------------------------------#
#---------------------------------- 4. Slicing & Extraction --------------------------------------#
#-------------------------------------------------------------------------------------------------#
'''
Just like strings, binary data can be sliced. However, the operations are strictly
byte-based, not character-based (which matters for multi-byte UTF-8 characters).
'''

s_bin = pl.Series([b"hello", b"world", b"polars"])

# .bin.slice(offset, length)
print(s_bin.bin.slice(0, 2)) # First 2 bytes
# [b"he", b"wo", b"po"]

print(s_bin.bin.slice(-2)) # Last 2 bytes
# [b"lo", b"ld", b"rs"]

# .bin.head(n) and .bin.tail(n)
print(s_bin.bin.head(3))
# [b"hel", b"wor", b"pol"]

print(s_bin.bin.tail(2))
# [b"lo", b"ld", b"rs"]

# .bin.get(index): Retrieves the integer value of the byte at the specific index
# (e.g., ASCII value of 'h' is 104, 'w' is 119, 'p' is 112)
print(s_bin.bin.get(0))
# [104, 119, 112]


#-------------------------------------------------------------------------------------------------#
#------------------------------------ 5. Size & Information --------------------------------------#
#-------------------------------------------------------------------------------------------------#
'''
.bin.size() returns the exact number of bytes in each binary element.
You can optionally pass a unit like "kb", "mb", etc., but "b" (bytes) is the default.
'''

s_bin = pl.Series([b"hello", b"\x00\x01\x02", b""])

print(s_bin.bin.size()) # Equivalent to .bin.size("b")
# shape: (3,)
# Series: '' [u32]
# [
# 	5
# 	3
# 	0
# ]

# Filter out empty binary payloads
print(s_bin.filter(s_bin.bin.size() > 0))
# [b"hello", b"\x00\x01\x02"]


#-------------------------------------------------------------------------------------------------#
#----------------------------- 6. Low-Level Memory Casting (.bin.reinterpret) --------------------#
#-------------------------------------------------------------------------------------------------#
'''
One of the most powerful features of the `.bin` namespace is `.reinterpret()`.
It allows you to take raw, unstructured bytes and cast them directly into
structured numeric types (Int32, Float64, etc.) WITHOUT copying the underlying
memory buffer. This is heavily used in high-performance computing and parsing
binary file formats (like Parquet, Arrow, or custom C-structs).

NOTE: The `dtype` argument MUST be passed as a keyword argument.
The byte length MUST perfectly match the target dtype size
(e.g., 4 bytes for Int32, 8 bytes for Float64). Endianness matters!
'''

# Create 4-byte sequences representing little-endian 32-bit integers:
# b"\x01\x00\x00\x00" -> 1
# b"\x00\x01\x00\x00" -> 256
# b"\xff\xff\xff\xff" -> -1
s_raw_int_bytes = pl.Series([
    b"\x01\x00\x00\x00",
    b"\x00\x01\x00\x00",
    b"\xff\xff\xff\xff"
])

# Reinterpret the raw bytes directly as Polars Int32 (MUST use dtype= keyword)
s_integers = s_raw_int_bytes.bin.reinterpret(dtype=pl.Int32)
print(s_integers)
# shape: (3,)
# Series: '' [i32]
# [
# 	1
# 	256
# 	-1
# ]

# Reinterpreting 8-byte sequences as Float64
# Pack Python floats into 8-byte raw binary sequences (little-endian)
float_bytes = [struct.pack('<d', 3.14), struct.pack('<d', -99.9)]
s_raw_float_bytes = pl.Series(float_bytes)

s_floats = s_raw_float_bytes.bin.reinterpret(dtype=pl.Float64)
print(s_floats)
# shape: (2,)
# Series: '' [f64]
# [
# 	3.14
# 	-99.9
# ]
