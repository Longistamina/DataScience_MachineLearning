'''
The idea of selecting and reordering columns
in tidypyrs is similar to polars.
=> The center is `tf.select()`

Content flow:
1. Explicit column selection and reordering
   -> lf.select([...]), lf.select("col1", "col2"), eager bracket selection,
      lf.select(lf.collect_schema().names()[slice_of_indices]) to select columns by slice of indices
      lf.select(pl.nth(list_of_indices)) to select columns by discrete indices
      pl.col("*"), pl.col("*").exclude(...), and regex column-name selection

2. Selecting all except some columns
   -> lf.drop(...)
   -> pl.exclude(...)
   => pl.all().exclude(...)

3. Programmatic reordering patterns
   -> move columns to the front/end
   -> alphabetical ordering
   -> reverse ordering
   -> rule-based ordering

4. Expression selection and light transformation
   -> select raw columns
   -> transform columns
   -> rename with alias()
   -> rename all outputs

5. pl.col() column-expression styles
   -> pl.col("name"), pl.col.name, c("name"), c.name, pl.col("*"),
      pl.col("*").exclude(...), regex patterns such as pl.col("^ham.*$"),
      and special-character column names

Note:
Selectors are not covered here. They are powerful enough to deserve a separate selectors script.
'''
