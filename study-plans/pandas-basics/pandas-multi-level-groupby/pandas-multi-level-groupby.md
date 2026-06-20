# <span style="font-size: 20px;">Multi-Level GroupBy</span>

<span style="font-size: 14px;">Multi-level GroupBy extends the split-apply-combine pattern to hierarchical groupings. Instead of grouping by a single column, you group by two or more columns to compute statistics at finer granularity: average salary by department and seniority level, total sales by region and product category, or error counts by service and error type. This produces MultiIndex results that can be reshaped, drilled into, and visualized.</span>

---

## <span style="font-size: 16px;">Creating Multi-Level Groups</span>

```python
grouped = df.groupby(['department', 'seniority'])['salary'].mean()
```

<span style="font-size: 14px;">This creates groups for every unique (department, seniority) combination. The result is a Series with a MultiIndex:</span>

```
department   seniority
Engineering  Junior       75000
             Senior      120000
Marketing    Junior       55000
             Senior       90000
Name: salary, dtype: float64
```

---

## <span style="font-size: 16px;">Accessing Multi-Level Results</span>

<span style="font-size: 14px;">MultiIndex results support hierarchical slicing:</span>

```python
result = df.groupby(['dept', 'year'])['revenue'].sum()

result.loc['Engineering']           # all years for Engineering
result.loc[('Engineering', 2024)]   # specific (dept, year)
result.xs('Engineering', level='dept')  # cross-section
result.xs(2024, level='year')       # all departments in 2024
```

---

## <span style="font-size: 16px;">Reshaping with unstack()</span>

<span style="font-size: 14px;">The most common post-processing step is unstacking one level into columns:</span>

```python
result = df.groupby(['dept', 'quarter'])['revenue'].sum()
wide = result.unstack('quarter')
# quarter     Q1    Q2    Q3    Q4
# dept
# Engineering 100   150   130   170
# Marketing    80   120   110   140
```

<span style="font-size: 14px;">This converts the MultiIndex Series into a DataFrame suitable for comparison across quarters.</span>

---

## <span style="font-size: 16px;">Multiple Aggregations</span>

```python
df.groupby(['dept', 'year']).agg(
    avg_salary=('salary', 'mean'),
    headcount=('employee_id', 'count'),
    total_bonus=('bonus', 'sum')
)
```

<span style="font-size: 14px;">Named aggregation works identically with multi-level groups. The result has a MultiIndex on rows and flat columns.</span>

---

## <span style="font-size: 16px;">Group Size and Distribution</span>

```python
# Number of rows in each group
df.groupby(['dept', 'seniority']).size()

# Groups with fewer than 5 members
sizes = df.groupby(['dept', 'seniority']).size()
small_groups = sizes[sizes < 5]
```

<span style="font-size: 14px;">Checking group sizes is essential for statistical validity. Groups with very few members produce unreliable means and standard deviations.</span>

---

## <span style="font-size: 16px;">Iterating Over Groups</span>

```python
for (dept, year), group_df in df.groupby(['department', 'year']):
    print(f'{dept} {year}: {len(group_df)} rows, avg salary: {group_df["salary"].mean():.0f}')
```

<span style="font-size: 14px;">The group name is a tuple when grouping by multiple columns.</span>

---

## <span style="font-size: 16px;">Transform with Multi-Level Groups</span>

<span style="font-size: 14px;">`transform()` broadcasts group-level statistics back to each row:</span>

```python
df['dept_year_avg'] = df.groupby(['dept', 'year'])['salary'].transform('mean')
df['pct_of_group'] = df['salary'] / df.groupby(['dept', 'year'])['salary'].transform('sum')
```

<span style="font-size: 14px;">This is useful for creating features like "employee's salary as a percentage of their department-year total."</span>

---

## <span style="font-size: 16px;">Resetting the MultiIndex</span>

```python
result = df.groupby(['dept', 'year'])['revenue'].sum()

# Reset all levels
result.reset_index()

# Reset one level
result.reset_index(level='year')

# Avoid MultiIndex entirely
df.groupby(['dept', 'year'], as_index=False)['revenue'].sum()
```

---

## <span style="font-size: 16px;">Group-Level Filtering</span>

```python
# Keep only (dept, year) groups with total revenue > 1M
df.groupby(['dept', 'year']).filter(lambda x: x['revenue'].sum() > 1_000_000)
```

<span style="font-size: 14px;">`filter()` returns the original rows (not aggregated), keeping only those belonging to qualifying groups.</span>

---

## <span style="font-size: 16px;">Ordering of Group Levels</span>

<span style="font-size: 14px;">The order of columns in the `groupby()` list determines the MultiIndex level order:</span>

```python
df.groupby(['year', 'dept'])  # year is level 0, dept is level 1
df.groupby(['dept', 'year'])  # dept is level 0, year is level 1
```

<span style="font-size: 14px;">Choose the order based on how you want to slice the results. `loc['Engineering']` works when 'dept' is level 0.</span>

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**Confusing MultiIndex levels**: With many levels, it is easy to slice the wrong level. Use `xs()` with explicit level names for clarity.</span>
* <span style="font-size: 14px;">**Sparse groups**: Not all (dept, year) combinations may exist. NaN appears after unstacking.</span>
* <span style="font-size: 14px;">**Performance with many groups**: Grouping by high-cardinality columns (e.g., user_id with millions of unique values) creates millions of groups. Custom aggregation functions become very slow.</span>
* <span style="font-size: 14px;">**Forgetting as_index=False**: If you do not want a MultiIndex result, set `as_index=False` in the groupby call instead of resetting afterward.</span>