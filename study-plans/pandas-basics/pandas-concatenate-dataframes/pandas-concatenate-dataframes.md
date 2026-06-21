# <span style="font-size: 20px;">Concatenate DataFrames</span>

<span style="font-size: 14px;">Concatenation stacks DataFrames along an axis: vertically (adding rows) or horizontally (adding columns). Unlike merging, which combines DataFrames based on key columns, concatenation is a structural operation that places DataFrames next to or on top of each other. It is the standard tool for combining data from multiple files, appending new observations, or assembling feature matrices.</span>

---

## <span style="font-size: 16px;">The concat() Function</span>

<span style="font-size: 14px;">The basic syntax takes a list of DataFrames:</span>

```python
result = pd.concat([df1, df2, df3])
```

<span style="font-size: 14px;">By default, this stacks vertically (`axis=0`), adding rows. All DataFrames must have compatible columns; columns that exist in only some DataFrames are filled with NaN in the others.</span>

---

## <span style="font-size: 16px;">Vertical Concatenation (axis=0)</span>

<span style="font-size: 14px;">Stacking rows is the most common use case:</span>

```python
# Combine monthly data files
jan = pd.read_csv('jan.csv')
feb = pd.read_csv('feb.csv')
mar = pd.read_csv('mar.csv')
full_quarter = pd.concat([jan, feb, mar])
```

### <span style="font-size: 14px;">Column Alignment</span>

<span style="font-size: 14px;">Concatenation aligns on column names. If DataFrames have different columns, the result has the union of all columns:</span>

```python
df1 = pd.DataFrame({'a': [1], 'b': [2]})
df2 = pd.DataFrame({'b': [3], 'c': [4]})
pd.concat([df1, df2])
#      a  b    c
# 0  1.0  2  NaN
# 0  NaN  3  4.0
```

<span style="font-size: 14px;">Pass `join='inner'` to keep only shared columns:</span>

```python
pd.concat([df1, df2], join='inner')
#    b
# 0  2
# 0  3
```

---

## <span style="font-size: 16px;">Horizontal Concatenation (axis=1)</span>

<span style="font-size: 14px;">Adding columns side by side:</span>

```python
pd.concat([df1, df2], axis=1)
```

<span style="font-size: 14px;">This aligns on the row index. If indices do not match, NaN is inserted for missing rows. Ensure indices are aligned before horizontal concatenation, or reset both indices first.</span>

---

## <span style="font-size: 16px;">Index Handling</span>

### <span style="font-size: 14px;">ignore_index</span>

<span style="font-size: 14px;">After vertical concatenation, the original indices are preserved, creating duplicates:</span>

```python
df1 = pd.DataFrame({'a': [1, 2]})  # index [0, 1]
df2 = pd.DataFrame({'a': [3, 4]})  # index [0, 1]
pd.concat([df1, df2])
# index: [0, 1, 0, 1] - duplicates!
```

<span style="font-size: 14px;">Use `ignore_index=True` to reset:</span>

```python
pd.concat([df1, df2], ignore_index=True)
# index: [0, 1, 2, 3]
```

### <span style="font-size: 14px;">keys Parameter</span>

<span style="font-size: 14px;">Add a hierarchical index to identify the source DataFrame:</span>

```python
pd.concat([df1, df2], keys=['jan', 'feb'])
# MultiIndex: [('jan', 0), ('jan', 1), ('feb', 0), ('feb', 1)]
```

<span style="font-size: 14px;">This is useful for tracking which original DataFrame each row came from.</span>

---

## <span style="font-size: 16px;">Performance: concat vs. Append in Loops</span>

<span style="font-size: 14px;">A critical performance pattern: never concatenate inside a loop. Each concatenation creates a new DataFrame and copies all previous data:</span>

```python
# WRONG: O(n^2) total copying
result = pd.DataFrame()
for file in files:
    df = pd.read_csv(file)
    result = pd.concat([result, df])

# RIGHT: O(n) total copying
dfs = [pd.read_csv(file) for file in files]
result = pd.concat(dfs)
```

<span style="font-size: 14px;">The wrong pattern copies $1 + 2 + 3 + ... + n$ rows = $O(n^2)$. The right pattern copies each row exactly once = $O(n)$. For 100 files of 10,000 rows each, the wrong pattern is roughly 50x slower.</span>

---

## <span style="font-size: 16px;">concat vs. merge</span>

| Feature | `concat` | `merge` |
|---------|-----------|----------|
| Purpose | Stack DataFrames structurally | Join on key columns |
| Alignment | By column names (axis=0) or index (axis=1) | By key column values |
| Number of inputs | Any number | Two |
| Key columns | Not used | Required |
| Use case | Combining same-schema data | Combining related data |

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**Duplicate indices**: Without `ignore_index=True`, concatenated DataFrames have duplicate index values, which breaks `loc`-based lookups.</span>
* <span style="font-size: 14px;">**Column mismatch**: Mismatched column names (e.g., "Name" vs "name") produce NaN instead of merging. Normalize column names first.</span>
* <span style="font-size: 14px;">**Type coercion**: Concatenating an int column with a float column upcasts to float. Concatenating int with str produces object.</span>
* <span style="font-size: 14px;">**Loop concatenation**: Building a DataFrame by concatenating in a loop is quadratic. Always collect into a list first.</span>