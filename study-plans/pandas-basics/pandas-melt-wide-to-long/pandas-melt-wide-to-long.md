# <span style="font-size: 20px;">Melt Wide to Long</span>

<span style="font-size: 14px;">Data comes in two fundamental shapes: wide format (one column per variable) and long format (one row per observation). The `melt()` function converts wide-format data to long-format data by "unpivoting" columns into rows. This transformation is essential for visualization libraries like seaborn and plotly (which expect long format), for tidy data principles, and for normalizing denormalized datasets.</span>

---

## <span style="font-size: 16px;">Wide vs. Long Format</span>

### <span style="font-size: 14px;">Wide Format</span>

```
  name    math  english  science
  Alice     90       85       88
  Bob       78       92       81
```

### <span style="font-size: 14px;">Long Format</span>

```
  name    subject    score
  Alice   math          90
  Alice   english       85
  Alice   science       88
  Bob     math          78
  Bob     english       92
  Bob     science       81
```

<span style="font-size: 14px;">Long format has more rows but fewer columns. Each row represents a single observation (one student's score in one subject), making it easier to filter, group, and plot.</span>

---

## <span style="font-size: 16px;">The melt() Function</span>

```python
long = pd.melt(
    df,
    id_vars=['name'],           # columns to keep as-is
    value_vars=['math', 'english', 'science'],  # columns to unpivot
    var_name='subject',         # name for the new variable column
    value_name='score'          # name for the new value column
)
```

### <span style="font-size: 14px;">Parameters</span>

* <span style="font-size: 14px;">`id_vars`: Columns that identify each observation (kept as-is, repeated for each unpivoted value)</span>
* <span style="font-size: 14px;">`value_vars`: Columns to unpivot into rows. If omitted, all columns not in `id_vars` are used.</span>
* <span style="font-size: 14px;">`var_name`: Name for the new column holding the original column names. Defaults to "variable".</span>
* <span style="font-size: 14px;">`value_name`: Name for the new column holding the values. Defaults to "value".</span>

---

## <span style="font-size: 16px;">Row Count After Melting</span>

<span style="font-size: 14px;">If the original has $n$ rows and you melt $k$ value columns, the result has $n \times k$ rows:</span>

$$\text{result rows} = n \times k$$

<span style="font-size: 14px;">For 100 students and 5 subjects, the melted result has 500 rows. This row multiplication is expected, not a bug.</span>

---

## <span style="font-size: 16px;">Omitting value_vars</span>

<span style="font-size: 14px;">If `value_vars` is not specified, all columns not in `id_vars` are melted:</span>

```python
pd.melt(df, id_vars=['name'])
# Melts math, english, science (all remaining columns)
```

<span style="font-size: 14px;">This is convenient but can be surprising if the DataFrame has columns you did not intend to melt. Explicitly listing `value_vars` is safer.</span>

---

## <span style="font-size: 16px;">Tidy Data Principles</span>

<span style="font-size: 14px;">The "tidy data" framework (Hadley Wickham) defines three rules:</span>

1. <span style="font-size: 14px;">Each variable forms a column</span>
2. <span style="font-size: 14px;">Each observation forms a row</span>
3. <span style="font-size: 14px;">Each type of observational unit forms a table</span>

<span style="font-size: 14px;">Wide format violates rule 1: "subject" is a variable, but its values (math, english, science) are spread across column names instead of being stored in a column. Melting converts to tidy format by making "subject" an explicit column.</span>

---

## <span style="font-size: 16px;">Melting with Multiple ID Variables</span>

```python
pd.melt(df, id_vars=['student_id', 'name', 'grade_level'],
        value_vars=['q1_score', 'q2_score', 'q3_score'],
        var_name='quarter', value_name='score')
```

<span style="font-size: 14px;">All id_vars columns are preserved and repeated. This is common in longitudinal datasets where each time period is stored as a separate column.</span>

---

## <span style="font-size: 16px;">Post-Melt Cleanup</span>

<span style="font-size: 14px;">After melting, the variable column often contains column names that need cleaning:</span>

```python
long = pd.melt(df, id_vars=['id'], value_vars=['q1_score', 'q2_score'])
long['variable'] = long['variable'].str.replace('_score', '')
# 'q1_score' -> 'q1', 'q2_score' -> 'q2'
```

---

## <span style="font-size: 16px;">Melt as the Inverse of Pivot</span>

<span style="font-size: 14px;">`melt()` and `pivot()` are inverse operations:</span>

```python
# Wide -> Long
long = pd.melt(wide, id_vars=['name'], var_name='subject', value_name='score')

# Long -> Wide
wide = long.pivot(index='name', columns='subject', values='score')
```

<span style="font-size: 14px;">However, the round-trip is not always lossless: pivot requires unique (index, column) pairs, and the column order may change.</span>

---

## <span style="font-size: 16px;">Use Cases</span>

* <span style="font-size: 14px;">**Visualization**: Seaborn's `catplot()`, `boxplot()`, and `lineplot()` expect a "hue" column, which requires long format.</span>
* <span style="font-size: 14px;">**Database normalization**: Wide-format CSVs need to be melted before loading into normalized database tables.</span>
* <span style="font-size: 14px;">**Statistical analysis**: Libraries like statsmodels expect long format for repeated-measures ANOVA.</span>
* <span style="font-size: 14px;">**Feature engineering**: Converting wide features to long format before encoding can simplify the pipeline.</span>

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**Forgetting id_vars**: Without `id_vars`, there is no way to trace which original row each value came from.</span>
* <span style="font-size: 14px;">**Mixed types in value columns**: If the melted columns have different types (e.g., one int and one string), the value column becomes object type.</span>
* <span style="font-size: 14px;">**Row explosion**: Melting many columns creates a large result. 100 rows with 50 columns becomes 5,000 rows.</span>
* <span style="font-size: 14px;">**Default column names**: Without `var_name` and `value_name`, the result has generic "variable" and "value" columns that are uninformative.</span>