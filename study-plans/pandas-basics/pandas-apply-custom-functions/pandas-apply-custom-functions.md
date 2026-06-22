# <span style="font-size: 20px;">Apply Custom Transforms</span>

<span style="font-size: 14px;">The `apply()` method lets you run any Python function on a DataFrame, Series, or GroupBy object. It is the escape hatch for operations that cannot be expressed with built-in vectorized methods. While powerful, `apply()` comes with a significant performance cost because it executes Python code per element or per group rather than using optimized C code. Understanding when to use `apply()`, when to use vectorized alternatives, and how to minimize its overhead is essential for writing efficient pandas code.</span>

---

## <span style="font-size: 16px;">apply() on a Series</span>

<span style="font-size: 14px;">Apply a function to each element of a Series:</span>

```python
df['name_length'] = df['name'].apply(len)
df['category'] = df['score'].apply(lambda x: 'pass' if x >= 60 else 'fail')
```

<span style="font-size: 14px;">The function receives a single value and returns a single value. This is equivalent to `map()` for Series.</span>

---

## <span style="font-size: 16px;">apply() on a DataFrame</span>

<span style="font-size: 14px;">Apply a function to each column (default) or each row:</span>

```python
# Per column (axis=0): function receives a Series (the column)
df.apply(np.sum)                  # sum of each column
df.apply(lambda col: col.max() - col.min())  # range of each column

# Per row (axis=1): function receives a Series (the row)
df.apply(lambda row: row['salary'] * row['bonus_pct'], axis=1)
```

<span style="font-size: 14px;">With `axis=0`, the function receives one column at a time. With `axis=1`, the function receives one row at a time. Row-wise apply is significantly slower because DataFrames are stored column-major.</span>

---

## <span style="font-size: 16px;">apply() vs. Vectorized Operations</span>

<span style="font-size: 14px;">Many uses of `apply()` can be replaced with vectorized operations that are 10-100x faster:</span>

```python
# SLOW: apply with lambda
df['total'] = df.apply(lambda row: row['price'] * row['quantity'], axis=1)

# FAST: vectorized multiplication
df['total'] = df['price'] * df['quantity']
```

```python
# SLOW: apply for conditional
df['category'] = df['score'].apply(lambda x: 'A' if x >= 90 else 'B')

# FAST: np.where
df['category'] = np.where(df['score'] >= 90, 'A', 'B')

# FAST: pd.cut for multiple bins
df['category'] = pd.cut(df['score'], bins=[0, 60, 80, 90, 100], labels=['F', 'C', 'B', 'A'])
```

### <span style="font-size: 14px;">When apply() is Necessary</span>

* <span style="font-size: 14px;">Complex string parsing that `.str` accessor cannot express</span>
* <span style="font-size: 14px;">Functions that depend on multiple columns in non-trivial ways</span>
* <span style="font-size: 14px;">External library calls that only accept scalars</span>
* <span style="font-size: 14px;">Logic with multiple conditional branches that `np.select` cannot express cleanly</span>

---

## <span style="font-size: 16px;">map() vs. apply() vs. applymap()</span>

| Method | Works on | Input to function | Use case |
|--------|----------|------------------|----------|
| `map()` | Series | Single value | Element-wise transformation or dictionary lookup |
| `apply()` | Series/DataFrame | Single value (Series) or row/column (DataFrame) | Custom transforms |
| `map()` (DataFrame) | DataFrame | Single value | Element-wise (replaces deprecated `applymap`) |

---

## <span style="font-size: 16px;">apply() with GroupBy</span>

<span style="font-size: 14px;">GroupBy `apply()` receives each group as a DataFrame and can return a scalar, Series, or DataFrame:</span>

```python
# Return a scalar per group (like agg)
df.groupby('dept').apply(lambda g: g['salary'].max() - g['salary'].min())

# Return a DataFrame per group (like transform but more flexible)
def normalize_group(g):
    g['salary_z'] = (g['salary'] - g['salary'].mean()) / g['salary'].std()
    return g

df.groupby('dept').apply(normalize_group)
```

<span style="font-size: 14px;">GroupBy `apply()` is the most flexible but slowest GroupBy method. Use `agg()` or `transform()` when possible.</span>

---

## <span style="font-size: 16px;">Returning Multiple Values</span>

<span style="font-size: 14px;">A function can return a Series to create multiple new columns:</span>

```python
def parse_full_name(name):
    parts = name.split()
    return pd.Series({'first': parts[0], 'last': parts[-1]})

df[['first_name', 'last_name']] = df['full_name'].apply(parse_full_name)
```

---

## <span style="font-size: 16px;">Error Handling in apply()</span>

<span style="font-size: 14px;">If the function fails on any element, the entire apply fails. Handle errors within the function:</span>

```python
def safe_parse(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan

df['value'] = df['raw_value'].apply(safe_parse)
```

<span style="font-size: 14px;">For numeric parsing specifically, `pd.to_numeric(errors='coerce')` is faster and more idiomatic.</span>

---

## <span style="font-size: 16px;">Performance Optimization</span>

<span style="font-size: 14px;">If you must use `apply()`, minimize the overhead:</span>

* <span style="font-size: 14px;">**Use raw=True**: `df.apply(func, raw=True)` passes numpy arrays instead of Series, eliminating Series construction overhead. Only works when the function does not need index or column names.</span>
* <span style="font-size: 14px;">**Use result_type='expand'**: When returning multiple values, this avoids the overhead of constructing intermediate Series objects.</span>
* <span style="font-size: 14px;">**Numba or Cython**: For computationally intensive functions, compile the inner function with numba for near-C performance.</span>

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**Using apply when vectorized alternatives exist**: This is the most common pandas performance mistake. Always check for a vectorized solution first.</span>
* <span style="font-size: 14px;">**Axis confusion**: `axis=0` applies to columns; `axis=1` applies to rows. This is counterintuitive because `axis=0` processes along the vertical axis.</span>
* <span style="font-size: 14px;">**Side effects in apply functions**: Functions passed to `apply()` should be pure (no side effects). Pandas may call the function more than once per element for type inference.</span>
* <span style="font-size: 14px;">**GroupBy apply double-calling**: In older pandas versions, GroupBy `apply()` calls the function on the first group twice (for type inference). Do not rely on side effects.</span>