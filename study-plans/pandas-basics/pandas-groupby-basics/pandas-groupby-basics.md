# <span style="font-size: 20px;">GroupBy Basics</span>

<span style="font-size: 14px;">The GroupBy operation is one of the most powerful concepts in data analysis. It implements the "split-apply-combine" paradigm: split the data into groups based on some criteria, apply a function to each group independently, and combine the results into a new data structure. This pattern handles questions like "what is the average salary per department?" or "what is the total revenue per region per quarter?" that would require nested loops in plain Python.</span>

---

## <span style="font-size: 16px;">The Split-Apply-Combine Pattern</span>

<span style="font-size: 14px;">Every GroupBy operation follows three steps:</span>

1. <span style="font-size: 14px;">**Split**: Partition the DataFrame into groups based on the values of one or more columns.</span>
2. <span style="font-size: 14px;">**Apply**: Execute a function (aggregation, transformation, or filter) on each group.</span>
3. <span style="font-size: 14px;">**Combine**: Merge the results back into a single DataFrame or Series.</span>

```python
# Split by 'department', apply mean(), combine into a new DataFrame
result = df.groupby('department')['salary'].mean()
```

<span style="font-size: 14px;">The `groupby()` call itself does not compute anything. It returns a `GroupBy` object that is lazy: computation happens only when you call an aggregation method like `mean()`, `sum()`, or `count()`.</span>

---

## <span style="font-size: 16px;">Creating Groups</span>

<span style="font-size: 14px;">Group by a single column:</span>

```python
grouped = df.groupby('department')
```

<span style="font-size: 14px;">Group by multiple columns:</span>

```python
grouped = df.groupby(['department', 'year'])
```

<span style="font-size: 14px;">The GroupBy object supports iteration, which is useful for inspection:</span>

```python
for name, group_df in df.groupby('department'):
    print(f'{name}: {len(group_df)} rows')
```

---

## <span style="font-size: 16px;">Aggregation Functions</span>

<span style="font-size: 14px;">Built-in aggregation methods are optimized in C and run much faster than custom Python functions:</span>

| Method | Description |
|--------|-------------|
| `sum()` | Sum of values |
| `mean()` | Arithmetic mean |
| `median()` | Median value |
| `min()`, `max()` | Minimum/maximum |
| `count()` | Number of non-null values |
| `size()` | Number of rows (including null) |
| `std()`, `var()` | Standard deviation/variance |
| `first()`, `last()` | First/last non-null value |
| `nunique()` | Count of unique values |

```python
df.groupby('dept')['salary'].mean()
df.groupby('dept')['salary'].agg(['mean', 'median', 'std'])
```

---

## <span style="font-size: 16px;">The agg() Method</span>

<span style="font-size: 14px;">`agg()` (alias for `aggregate()`) provides flexible aggregation:</span>

### <span style="font-size: 14px;">Multiple Functions on One Column</span>

```python
df.groupby('dept')['salary'].agg(['mean', 'std', 'count'])
```

### <span style="font-size: 14px;">Different Functions per Column</span>

```python
df.groupby('dept').agg({
    'salary': ['mean', 'max'],
    'age': 'median',
    'name': 'count'
})
```

### <span style="font-size: 14px;">Named Aggregations</span>

```python
df.groupby('dept').agg(
    avg_salary=('salary', 'mean'),
    max_salary=('salary', 'max'),
    headcount=('name', 'count')
)
```

<span style="font-size: 14px;">Named aggregations produce flat column names instead of MultiIndex columns, making the result easier to work with.</span>

---

## <span style="font-size: 16px;">Custom Aggregation Functions</span>

<span style="font-size: 14px;">For operations not covered by built-in methods, pass a custom function:</span>

```python
df.groupby('dept')['salary'].agg(lambda x: x.max() - x.min())
```

<span style="font-size: 14px;">Custom functions receive a Series (the group's values) and must return a scalar. They are significantly slower than built-in methods because they execute in Python rather than C.</span>

---

## <span style="font-size: 16px;">GroupBy Index Behavior</span>

<span style="font-size: 14px;">By default, the grouping columns become the index of the result:</span>

```python
result = df.groupby('dept')['salary'].mean()
# dept
# Engineering    85000
# Marketing      72000
# Name: salary, dtype: float64
```

<span style="font-size: 14px;">Use `as_index=False` to keep the grouping columns as regular columns:</span>

```python
result = df.groupby('dept', as_index=False)['salary'].mean()
# Returns a DataFrame with 'dept' and 'salary' as columns
```

<span style="font-size: 14px;">Alternatively, chain `.reset_index()` after the aggregation.</span>

---

## <span style="font-size: 16px;">Selecting Columns After GroupBy</span>

<span style="font-size: 14px;">You can select columns before or after grouping:</span>

```python
df.groupby('dept')['salary'].mean()           # Series result
df.groupby('dept')[['salary', 'age']].mean()  # DataFrame result
df.groupby('dept').mean(numeric_only=True)     # all numeric columns
```

<span style="font-size: 14px;">Selecting specific columns before aggregation is more efficient because pandas only computes the aggregation for the selected columns.</span>

---

## <span style="font-size: 16px;">Handling Missing Values</span>

<span style="font-size: 14px;">By default, `groupby()` excludes NaN keys:</span>

```python
df = pd.DataFrame({'dept': ['A', 'B', None, 'A'], 'val': [1, 2, 3, 4]})
df.groupby('dept')['val'].sum()
# dept
# A    5
# B    2
# (NaN group is excluded)
```

<span style="font-size: 14px;">Pass `dropna=False` to include NaN as a group:</span>

```python
df.groupby('dept', dropna=False)['val'].sum()
```

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**Forgetting to select a column**: `df.groupby('dept').mean()` aggregates ALL numeric columns. Select specific columns to avoid unexpected results.</span>
* <span style="font-size: 14px;">**count vs size**: `count()` excludes NaN; `size()` includes NaN. For row counts, `size()` is usually what you want.</span>
* <span style="font-size: 14px;">**MultiIndex columns from agg**: Using `agg(['mean', 'std'])` produces MultiIndex columns. Use named aggregation to get flat columns.</span>
* <span style="font-size: 14px;">**Slow custom functions**: Custom lambda functions in `agg()` are 10-100x slower than built-in methods. Always check if a built-in covers your case first.</span>