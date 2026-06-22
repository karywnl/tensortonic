# <span style="font-size: 20px;">Unstack Long to Wide</span>

<span style="font-size: 14px;">The `unstack()` method pivots a level of a row MultiIndex into columns, converting long-format data to wide-format. It is the index-based counterpart of `pivot()` and the inverse of `stack()`. Understanding `unstack()` is essential for reshaping GroupBy results, creating cross-tabulations, and preparing data for wide-format consumers like spreadsheets and heatmaps.</span>

---

## <span style="font-size: 16px;">What unstack() Does</span>

<span style="font-size: 14px;">`unstack()` takes the innermost level of a MultiIndex and rotates it into columns:</span>

```python
# Start with long format (MultiIndex)
#                    value
# category  month
# A         Jan        10
# A         Feb        20
# B         Jan        30
# B         Feb        40

result = df.unstack()
#           value
# month    Jan  Feb
# category
# A         10   20
# B         30   40
```

<span style="font-size: 14px;">The MultiIndex level "month" became column headers. Each unique value in that level becomes a separate column.</span>

---

## <span style="font-size: 16px;">Choosing Which Level to Unstack</span>

```python
df.unstack()           # unstack innermost level (default, level=-1)
df.unstack(level=0)    # unstack outermost level
df.unstack('month')    # unstack by level name
```

<span style="font-size: 14px;">For a MultiIndex with three levels (A, B, C), `unstack(level=1)` rotates level B into columns while keeping A and C as row index levels.</span>

---

## <span style="font-size: 16px;">unstack() After GroupBy</span>

<span style="font-size: 14px;">The most common use case is reshaping grouped aggregations:</span>

```python
# GroupBy produces a Series with MultiIndex
result = df.groupby(['department', 'quarter'])['revenue'].sum()
# department  quarter
# Engineering Q1         100
#             Q2         150
# Marketing   Q1          80
#             Q2         120

# Unstack to get quarters as columns
wide = result.unstack()
# quarter     Q1   Q2
# department
# Engineering 100  150
# Marketing    80  120
```

<span style="font-size: 14px;">This is equivalent to using a pivot table but works directly on the GroupBy result.</span>

---

## <span style="font-size: 16px;">Handling Missing Values</span>

<span style="font-size: 14px;">If not all combinations of (row, column) exist, `unstack()` fills gaps with NaN:</span>

```python
df.unstack(fill_value=0)  # fill missing combinations with 0
```

<span style="font-size: 14px;">The `fill_value` parameter is essential for producing clean pivot tables without NaN.</span>

---

## <span style="font-size: 16px;">stack() as the Inverse</span>

<span style="font-size: 14px;">`stack()` is the inverse of `unstack()`: it pivots columns back into a MultiIndex level:</span>

```python
long = wide.stack()     # wide -> long
wide = long.unstack()   # long -> wide (round-trip)
```

---

## <span style="font-size: 16px;">Comparison with pivot()</span>

| Feature | `unstack()` | `pivot()` |
|---------|------------|----------|
| Input | MultiIndex rows | Regular columns |
| Column source | Index level | Column values |
| Requires unique values | Yes | Yes |
| Typical use | After groupby | On raw data |

<span style="font-size: 14px;">`unstack()` works on the index; `pivot()` works on regular columns. After a GroupBy (which sets groups as the index), `unstack()` is the natural choice.</span>

---

## <span style="font-size: 16px;">Multiple Value Columns</span>

<span style="font-size: 14px;">When the DataFrame has multiple value columns, `unstack()` creates hierarchical columns:</span>

```python
# MultiIndex result with multiple aggregations
result = df.groupby(['dept', 'year']).agg({'salary': 'mean', 'headcount': 'sum'})
wide = result.unstack()
# Columns become MultiIndex: (salary, 2022), (salary, 2023), (headcount, 2022), ...
```

<span style="font-size: 14px;">Flatten with:</span>

```python
wide.columns = [f'{col}_{year}' for col, year in wide.columns]
```

---

## <span style="font-size: 16px;">Practical Applications</span>

* <span style="font-size: 14px;">**Report tables**: Unstack time periods into columns for quarterly/monthly reports.</span>
* <span style="font-size: 14px;">**Heatmaps**: Seaborn's `heatmap()` expects a 2D DataFrame where rows and columns are categories.</span>
* <span style="font-size: 14px;">**Correlation analysis**: Unstack to get a matrix format suitable for correlation computation.</span>
* <span style="font-size: 14px;">**Excel export**: Spreadsheet users expect wide format with time periods as columns.</span>

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**Duplicate index values**: If the (remaining index, unstacked level) combination is not unique, `unstack()` raises a `ValueError`. Aggregate first to ensure uniqueness.</span>
* <span style="font-size: 14px;">**NaN in results**: Missing combinations produce NaN. Use `fill_value` to handle this.</span>
* <span style="font-size: 14px;">**MultiIndex columns**: After unstacking, columns may have a MultiIndex that complicates further operations. Flatten column names when needed.</span>
* <span style="font-size: 14px;">**Confusing unstack direction**: `unstack()` moves a row level into columns. `stack()` moves a column level into rows. Mixing these up produces the wrong shape.</span>