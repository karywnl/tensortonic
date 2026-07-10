# <span style="font-size: 20px;">Boolean Masking</span>

<span style="font-size: 14px;">Boolean masking is the NumPy technique for selecting elements based on conditions. A boolean mask is an array of True/False values. For plain indexing (`arr[mask]`) the mask must have the same shape as the data; for functions like `np.where(cond, x, y)` and `np.select(conditions, choices)`, the condition broadcasts against `x` and `y` following NumPy's standard broadcasting rules, so a `(n,)` mask can apply to `(m, n)` data. Masking enables element-level filtering, row or column selection, and conditional computation without Python loops.</span>

---

## <span style="font-size: 16px;">Element-Level Masking</span>

```python
arr = np.array([[1, 8, 3],
                [7, 2, 9],
                [4, 6, 5]])

mask = arr > 5
# [[False, True, False],
#  [ True, False, True],
#  [False, True, False]]

arr[mask]  # [8, 7, 9, 6] - 1D array of matching elements
```

<span style="font-size: 14px;">Boolean indexing on a 2D array always returns a 1D array of the matching elements, regardless of the mask pattern.</span>

---

## <span style="font-size: 16px;">Row-Level Masking</span>

<span style="font-size: 14px;">To select entire rows based on a condition on one column or a per-row condition:</span>

```python
# Keep rows where ANY element exceeds threshold
row_mask = np.any(arr > 5, axis=1)  # [True, True, True]
arr[row_mask]

# Keep rows where the first column exceeds threshold
row_mask = arr[:, 0] > 3
arr[row_mask]  # rows where first element > 3

# Keep rows where the row sum exceeds a threshold
row_mask = arr.sum(axis=1) > 15
arr[row_mask]
```

### <span style="font-size: 14px;">np.any() and np.all() Along Axes</span>

```python
np.any(arr > 5, axis=1)   # True if ANY element in row > 5
np.all(arr > 0, axis=1)   # True if ALL elements in row > 0
np.any(arr > 5, axis=0)   # True if ANY element in column > 5
```

---

## <span style="font-size: 16px;">Combining Multiple Conditions</span>

```python
mask = (arr > 2) & (arr < 8)   # AND
mask = (arr < 2) | (arr > 8)   # OR
mask = ~(arr > 5)               # NOT
```

<span style="font-size: 14px;">Parentheses are required because `&` and `|` have higher precedence than comparison operators in Python.</span>

---

## <span style="font-size: 16px;">Row vs Column Filtering</span>

<span style="font-size: 14px;">For a 2D array of shape</span> $(m, n)$<span style="font-size: 14px;">, you can filter by rows or by columns using a 1D mask and the `:` slice in the other axis:</span>

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]])

# Keep rows where the first column is > 3
row_mask = arr[:, 0] > 3        # shape (m,)
arr[row_mask, :]                # shape (k, n) - rows that passed

# Keep columns where the first row is even
col_mask = arr[0, :] % 2 == 0   # shape (n,)
arr[:, col_mask]                # shape (m, k) - columns that passed
```

<span style="font-size: 14px;">The 1D mask is applied to the axis it matches in shape; the `:` in the other axis means "keep everything on that axis".</span>

---

## <span style="font-size: 16px;">Conditional Assignment</span>

<span style="font-size: 14px;">Boolean masks enable selective modification:</span>

```python
arr[arr < 0] = 0              # clip negatives to zero
arr[arr > 100] = 100          # clip to max
arr[np.isnan(arr)] = 0        # replace NaN with 0
```

---

## <span style="font-size: 16px;">np.where() for Conditional Selection</span>

```python
result = np.where(arr > 5, arr, 0)     # keep > 5, else 0
result = np.where(arr > 5, arr, -arr)  # negate elements <= 5
```

<span style="font-size: 14px;">`np.where(cond, x, y)` is the vectorized equivalent of `x if cond else y` applied element-wise.</span>

---

## <span style="font-size: 16px;">np.select() for Multiple Conditions</span>

<span style="font-size: 14px;">`np.select(conditions, choices, default)` takes three arguments:</span>

* <span style="font-size: 14px;">`conditions`: a list of boolean arrays, all the same shape as the input. Each element says "does this position match this condition?"</span>
* <span style="font-size: 14px;">`choices`: a list of values (or arrays) to pick from. `choices[i]` is used wherever `conditions[i]` is True. Conditions and choices must have the same length.</span>
* <span style="font-size: 14px;">`default`: the fallback value used at positions where none of the conditions are True.</span>

```python
arr = np.array([1, 5, 9, 2, 8])
conditions = [arr < 3, arr < 7]          # [True,False,False,True,False], [True,True,False,True,False]
choices    = ['low', 'medium']
result = np.select(conditions, choices, default='high')
# ['low', 'medium', 'high', 'low', 'high']
```

<span style="font-size: 14px;">`np.select` evaluates conditions in order: the first matching condition wins, later ones are ignored at that position. This is the vectorized equivalent of an if-elif-else chain. `default` is used where none of the conditions are True (never use `'unknown'` unless you literally want the string "unknown" there).</span>

---

## <span style="font-size: 16px;">Masked Arrays</span>

<span style="font-size: 14px;">NumPy's `ma` module provides masked arrays that carry their mask with the data:</span>

```python
masked = np.ma.masked_where(arr < 0, arr)
masked.mean()    # ignores masked elements
masked.sum()     # ignores masked elements
```

<span style="font-size: 14px;">Masked arrays are useful when you need to propagate the mask through multiple operations without repeatedly applying it.</span>

---

## <span style="font-size: 16px;">Performance</span>

<span style="font-size: 14px;">Boolean operations are highly optimized in NumPy:</span>

* <span style="font-size: 14px;">Comparison creates the mask in a single vectorized pass</span>
* <span style="font-size: 14px;">The mask is stored as a byte array (1 byte per element)</span>
* <span style="font-size: 14px;">Selection using the mask runs at C speed</span>
* <span style="font-size: 14px;">For 10 million elements, boolean filtering takes milliseconds</span>

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**Parentheses with boolean operators**: `arr > 2 & arr < 8` fails due to operator precedence. Use `(arr > 2) & (arr < 8)`.</span>
* <span style="font-size: 14px;">**2D masking returns 1D**: Applying an element-wise mask to a 2D array produces a flat 1D result. Use row-level masking to preserve structure.</span>
* <span style="font-size: 14px;">**NaN comparison**: `np.nan > 5` is False. Use `np.isnan()` to detect NaN.</span>
* <span style="font-size: 14px;">**and/or vs. &/|**: Python `and` and `or` do not work element-wise on arrays. Use `&` and `|`.</span>