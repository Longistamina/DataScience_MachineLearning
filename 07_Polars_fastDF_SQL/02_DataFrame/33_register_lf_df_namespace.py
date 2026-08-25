"""
Topic: pl.api.register_dataframe_namespace / register_lazyframe_namespace
---------------------------------------------------------------------------
Same idea as register_series_namespace, but for DataFrame and LazyFrame.
Lets you attach custom, chainable methods instead of relying only on .pipe().

How it works:
1. Define a class that takes the DataFrame/LazyFrame in __init__.
2. Add whatever methods you want on that class.
3. Decorate with @pl.api.register_dataframe_namespace("name")
   or @pl.api.register_lazyframe_namespace("name").
4. Call it as: df.name.method(...) / lf.name.method(...)

Rules / gotchas:
- Namespace name can't collide with a built-in one.
- DataFrame and LazyFrame namespaces are registered separately — if you
  want the method on both, register it twice (or share a mixin class).
- Registration happens once per session/import; put it in a shared module.
"""

import polars as pl


@pl.api.register_dataframe_namespace("mytools")
class MyDataFrameNamespace:
    def __init__(self, df: pl.DataFrame):
        self._df = df

    def with_prefix(self, col: str, prefixes) -> pl.DataFrame:
        """Prepend elementwise prefixes onto a string column."""
        return self._df.with_columns(
            (pl.Series(prefixes, dtype=pl.Utf8) + self._df[col]).alias(col)
        )


@pl.api.register_lazyframe_namespace("mytools")
class MyLazyFrameNamespace:
    def __init__(self, lf: pl.LazyFrame):
        self._lf = lf

    def with_prefix(self, col: str, prefixes) -> pl.LazyFrame:
        """Prepend elementwise prefixes onto a string column (lazy version)."""
        prefix_expr = pl.Series(prefixes, dtype=pl.Utf8)
        return self._lf.with_columns((prefix_expr + pl.col(col)).alias(col))


if __name__ == "__main__":
    df = pl.DataFrame(
        {"country": ["Vietnam", "Philipines", "Malaysia", "Myanmar"]}
    )
    prefixes = ["VN_", "PH_", "MY_", "MM_"]

    # DataFrame usage — chainable like any built-in method
    print(df.mytools.with_prefix("country", prefixes))

    # LazyFrame usage — same call, stays lazy until .collect()
    print(df.lazy().mytools.with_prefix("country", prefixes).collect())
