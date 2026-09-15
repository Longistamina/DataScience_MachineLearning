'''
The idea of selecting and reordering columns
in tidypyrs is similar to polars.
=> The center is `tf.select()`

Content flow:
1. Explicit column selection and reordering
   -> tl.select([...]), tl.select("col1", "col2"), eager bracket selection,
      tl.select(f.colnames[slice_of_indices]) to select columns by slice of indices
      tl.select(pl.nth(list_of_indices)) to select columns by discrete indices
      f("*"), f("*").exclude(...), and regex column-name selection

2. Selecting all except some columns
   -> tl.drop(...)
   -> tp.exclude(...)
   => f.all().exclude(...)

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

5. f() column-expression styles
   -> f("name"), f.name, f("*"),
      f("*").exclude(...), regex patterns such as f("^ham.*$"),
      and special-character column names

Note:
Selectors are not covered here. They are powerful enough to deserve a separate selectors script.
'''
