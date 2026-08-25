"""
Topic: pl.api.register_series_namespace
----------------------------------------
Polars lets you attach your own custom methods to Series (and DataFrame,
LazyFrame, Expr) via a "namespace". Once registered, your method behaves
just like a built-in one (e.g. .str.xxx(), .dt.xxx()) and can be chained.

Why: Series has no .pipe(), so this is the idiomatic way to add reusable,
chainable, custom logic to a Series.

How it works:
1. Define a class that takes the Series (or DataFrame/Expr) in __init__.
2. Add whatever methods you want on that class.
3. Decorate the class with @pl.api.register_series_namespace("your_name").
4. Call it as: some_series.your_name.your_method(...)

Rules / gotchas:
- Namespace name can't collide with a built-in one (e.g. "str", "dt").
- Registration happens once per session/import; put it in a shared module.
- Works the same way for DataFrame/LazyFrame/Expr via the matching
  register_dataframe_namespace / register_lazyframe_namespace /
  register_expr_namespace decorators.
"""

import polars as pl


@pl.api.register_series_namespace("mystr")
class MyStrNamespace:
    def __init__(self, s: pl.Series):
        self._s = s

    def radd(self, prefixes) -> pl.Series:
        """Prepend each element of `prefixes` to the matching Series element."""
        return pl.Series(prefixes, dtype=pl.Utf8) + self._s


if __name__ == "__main__":
    s = pl.Series(["Vietnam", "Philipines", "Malaysia", "Myanmar"])
    prefixes = ["VN_", "PH_", "MY_", "MM_"]

    # Usable like any built-in method, and chainable
    result = s.mystr.radd(prefixes)
    print(result)
