# <span style="font-size: 20px;">Aggregation Functions</span>

<span style="font-size: 14px;">Aggregation reduces a group of values to a single summary statistic. In the context of pandas GroupBy, aggregation is the "apply" step that transforms each group into a single row. Mastering the various ways to specify aggregations - built-in methods, named aggregations, custom functions, and multi-function application - is essential for producing clean, efficient summary tables.</span>

---

## <span style="font-size: 16px;">Built-in Aggregation Methods</span>

<span style="font-size: 14px;">Pandas provides optimized C-level implementations for common statistics:</span>

```python
grouped = df.groupby('category')['value']

grouped.sum()       # total per group
grouped.mean()      # average per group
grouped.median()    # median per group
grouped.std()       # standard deviation (ddof=1 by default)
grouped.var()       # variance
grouped.min()       # minimum
grouped.max()       # maximum
grouped.count()     # non-null count
grouped.nunique()   # unique value count
grouped.first()     # first non-null value
grouped.last()      # last non-null value
```

<span style="font-size: 14px;">These methods are vectorized and run at native speed. They should always be preferred over custom Python functions when available.</span>

---

## <span style="font-size: 16px;">The agg() Method</span>

<span style="font-size: 14px;">The `agg()` method provides maximum flexibility for specifying aggregations:</span>

### <span style="font-size: 14px;">String Specification</span>

```python
grouped.agg('mean')          # same as grouped.mean()
grouped.agg(['mean', 'std']) # multiple functions, MultiIndex columns
```

### <span style="font-size: 14px;">Dictionary Specification (Different Functions per Column)</span>

```python
df.groupby('dept').agg({
    'salary': 'mean',
    'bonus': 'sum',
    'name': 'count'
})
```

<span style="font-size: 14px;">This is the most common pattern for producing summary tables where different columns need different aggregations.</span>

### <span style="font-size: 14px;">Named Aggregation (Recommended)</span>

```python
df.groupby('dept').agg(
    avg_salary=('salary', 'mean'),
    total_bonus=('bonus', 'sum'),
    headcount=('name', 'count'),
    salary_range=('salary', lambda x: x.max() - x.min())
)
```

<span style="font-size: 14px;">Named aggregation (introduced in pandas 0.25) produces clean, flat column names instead of MultiIndex columns. Each argument is a tuple of (column, function). This is the recommended approach for new code.</span>

---

## <span style="font-size: 16px;">Custom Aggregation Functions</span>

<span style="font-size: 14px;">Any function that takes a Series and returns a scalar can be used as an aggregation:</span>

```python
def coefficient_of_variation(x):
    return x.std() / x.mean() if x.mean() != 0 else 0

df.groupby('dept')['salary'].agg(coefficient_of_variation)
```

### <span style="font-size: 14px;">Lambda Functions</span>

```python
df.groupby('dept')['salary'].agg(lambda x: x.quantile(0.9))
df.groupby('dept')['salary'].agg(lambda x: (x > 100000).sum())
```

<span style="font-size: 14px;">Lambda functions are concise but cannot be named in the output. For named output, use named aggregation with the lambda.</span>

### <span style="font-size: 14px;">Performance Warning</span>

<span style="font-size: 14px;">Custom Python functions are called once per group and execute in the Python interpreter. For a DataFrame with 10,000 groups, this means 10,000 Python function calls. Built-in methods process all groups in a single C loop. The performance difference can be 10-100x.</span>

---

## <span style="font-size: 16px;">Multiple Aggregations on One Column</span>

```python
df.groupby('dept')['salary'].agg(['mean', 'median', 'std', 'count'])
```

<span style="font-size: 14px;">This produces a DataFrame with MultiIndex columns (one level for the column name, one for the aggregation). To flatten:</span>

```python
result = df.groupby('dept')['salary'].agg(['mean', 'median', 'std'])
result.columns = ['salary_mean', 'salary_median', 'salary_std']
```

<span style="font-size: 14px;">Or use named aggregation to avoid MultiIndex entirely.</span>

---

## <span style="font-size: 16px;">describe() as Aggregation</span>

<span style="font-size: 14px;">The `describe()` method provides a comprehensive statistical summary per group:</span>

```python
df.groupby('dept')['salary'].describe()
# Returns: count, mean, std, min, 25%, 50%, 75%, max per group
```

<span style="font-size: 14px;">This is useful for quick exploration but produces a fixed set of statistics. For custom summaries, use `agg()`.</span>

---

## <span style="font-size: 16px;">Transform vs. Aggregate</span>

<span style="font-size: 14px;">`agg()` reduces each group to a single row (output has one row per group). `transform()` returns a value for every row in the original DataFrame (output has the same shape):</span>

```python
# Aggregation: one value per department
df.groupby('dept')['salary'].mean()

# Transform: group mean broadcast to every row
df['dept_avg'] = df.groupby('dept')['salary'].transform('mean')
```

<span style="font-size: 14px;">Transform is used for creating group-level features while preserving the original row structure.</span>

---

## <span style="font-size: 16px;">Filtering Groups</span>

<span style="font-size: 14px;">`filter()` keeps or removes entire groups based on a condition:</span>

```python
# Keep only departments with more than 5 employees
df.groupby('dept').filter(lambda x: len(x) > 5)

# Keep only departments where average salary exceeds 80000
df.groupby('dept').filter(lambda x: x['salary'].mean() > 80000)
```

---

## <span style="font-size: 16px;">Pivot Table as Aggregation</span>

<span style="font-size: 14px;">`pivot_table()` is essentially a GroupBy + reshape in one step:</span>

```python
pd.pivot_table(df, values='salary', index='dept', columns='year', aggfunc='mean')
```

<span style="font-size: 14px;">This groups by (dept, year), computes the mean salary, and reshapes the result into a matrix with departments as rows and years as columns.</span>

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**Confusing count and size**: `count()` excludes NaN values; `size()` includes them. Use `size()` for row counts.</span>
* <span style="font-size: 14px;">**MultiIndex columns**: Using `agg(['func1', 'func2'])` creates MultiIndex columns that complicate downstream code. Use named aggregation.</span>
* <span style="font-size: 14px;">**Slow custom functions**: Always check if a built-in method exists before writing a custom function.</span>
* <span style="font-size: 14px;">**std() with ddof**: By default, `std()` uses `ddof=1` (sample standard deviation). For population standard deviation, pass `ddof=0`.</span>