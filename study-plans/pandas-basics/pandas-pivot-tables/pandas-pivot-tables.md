# <span style="font-size: 20px;">Pivot Tables</span>

<span style="font-size: 14px;">Pivot tables are one of the most powerful summarization tools in data analysis. They group data by one or more row and column variables, apply an aggregation function, and present the results in a two-dimensional matrix. If you have used pivot tables in Excel, the pandas `pivot_table()` function provides the same capability with full programmatic control, additional aggregation options, and seamless integration with the rest of the pandas ecosystem.</span>

---

## <span style="font-size: 16px;">The pivot_table() Function</span>

```python
pd.pivot_table(
    df,
    values='revenue',        # column to aggregate
    index='department',      # row labels
    columns='quarter',       # column labels
    aggfunc='sum'            # aggregation function
)
```

<span style="font-size: 14px;">This produces a matrix where rows are departments, columns are quarters, and cells contain the sum of revenue for each (department, quarter) combination.</span>

---

## <span style="font-size: 16px;">pivot_table vs. pivot</span>

<span style="font-size: 14px;">`pivot()` reshapes without aggregation and requires unique (index, column) pairs. `pivot_table()` handles duplicates by applying an aggregation:</span>

```python
# pivot: raises ValueError if duplicates exist
df.pivot(index='dept', columns='quarter', values='revenue')

# pivot_table: aggregates duplicates
df.pivot_table(index='dept', columns='quarter', values='revenue', aggfunc='sum')
```

<span style="font-size: 14px;">Use `pivot()` for pure reshaping (no data reduction). Use `pivot_table()` when summarization is needed.</span>

---

## <span style="font-size: 16px;">Aggregation Functions</span>

<span style="font-size: 14px;">The `aggfunc` parameter accepts:</span>

```python
aggfunc='mean'                    # single function (string)
aggfunc=np.sum                    # single function (callable)
aggfunc=['mean', 'std', 'count']  # multiple functions
aggfunc={'revenue': 'sum', 'headcount': 'mean'}  # per-column functions
```

<span style="font-size: 14px;">The default aggregation is `mean`. Multiple functions produce MultiIndex columns.</span>

---

## <span style="font-size: 16px;">Multiple Index and Column Levels</span>

```python
pd.pivot_table(df,
    values='revenue',
    index=['region', 'department'],
    columns=['year', 'quarter'],
    aggfunc='sum'
)
```

<span style="font-size: 14px;">This creates a nested row index (region/department) and nested column headers (year/quarter). The result is a multi-dimensional summary table.</span>

---

## <span style="font-size: 16px;">Margins (Totals)</span>

```python
pd.pivot_table(df,
    values='revenue',
    index='department',
    columns='quarter',
    aggfunc='sum',
    margins=True,
    margins_name='Total'
)
```

<span style="font-size: 14px;">`margins=True` adds a row and column of totals. The margin applies the same aggregation function to the subtotals. This is equivalent to Excel's "Grand Total" row and column.</span>

---

## <span style="font-size: 16px;">Handling Missing Values</span>

```python
pd.pivot_table(df,
    values='revenue',
    index='department',
    columns='quarter',
    fill_value=0  # replace NaN with 0
)
```

<span style="font-size: 14px;">Missing (department, quarter) combinations appear as NaN in the pivot table. Use `fill_value` to replace them. Choose the fill value carefully: 0 is appropriate for sums, but misleading for means.</span>

---

## <span style="font-size: 16px;">Post-Processing</span>

<span style="font-size: 14px;">Pivot table results are regular DataFrames, so you can chain any operation:</span>

```python
pt = pd.pivot_table(df, values='revenue', index='dept', columns='quarter', aggfunc='sum')

# Sort by total revenue
pt['Total'] = pt.sum(axis=1)
pt = pt.sort_values('Total', ascending=False)

# Percentage of total
pt_pct = pt.div(pt.sum(axis=0), axis=1) * 100

# Heatmap
import seaborn as sns
sns.heatmap(pt, annot=True, fmt='.0f')
```

---

## <span style="font-size: 16px;">Pivot Table vs. GroupBy + Unstack</span>

<span style="font-size: 14px;">A pivot table is functionally equivalent to a GroupBy followed by unstack:</span>

```python
# These produce identical results:
pd.pivot_table(df, values='revenue', index='dept', columns='quarter', aggfunc='sum')

df.groupby(['dept', 'quarter'])['revenue'].sum().unstack(fill_value=0)
```

<span style="font-size: 14px;">`pivot_table()` is more concise and handles margins. GroupBy + unstack is more flexible for complex aggregation chains.</span>

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**Default aggfunc is mean**: If you forget to specify `aggfunc`, you get means instead of sums. This is a common source of incorrect totals.</span>
* <span style="font-size: 14px;">**MultiIndex columns with multiple aggfuncs**: Using a list of aggregation functions creates MultiIndex columns that need flattening for downstream use.</span>
* <span style="font-size: 14px;">**NaN fill value misleading for means**: Filling NaN with 0 in a mean pivot table makes it look like a (department, quarter) had zero average, when really it had no data.</span>
* <span style="font-size: 14px;">**Margin aggregation**: Margins apply the same function as the cells. For a sum table, margins are sums. For a mean table, margins are means of the group, not grand means.</span>