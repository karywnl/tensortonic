# <span style="font-size: 20px;">Filter and Extract</span>

<span style="font-size: 14px;">Filtering extracts a subset of array elements that satisfy a condition. NumPy's boolean indexing, combined with slicing and conditional operations, provides a powerful toolkit for selecting, masking, and extracting data without writing loops. These operations run at C speed and are the foundation of data preprocessing in scientific computing.</span>

---

## <span style="font-size: 16px;">Boolean Masking</span>

<span style="font-size: 14px;">The core pattern: create a boolean mask, then use it to index:</span>

```python
a = np.array([1, 5, 3, 8, 2, 7])
mask = a > 4        # [False, True, False, True, False, True]
a[mask]             # [5, 8, 7]
```

<span style="font-size: 14px;">The comparison `a > 4` broadcasts the scalar across every element, producing a boolean array. Using this array as an index selects only the True elements.</span>

### <span style="font-size: 14px;">Combining Conditions</span>

```python
(a > 2) & (a < 7)   # AND: [False, True, True, False, False, True]
(a < 2) | (a > 7)   # OR: [True, False, False, True, False, False]
~(a > 4)             # NOT: [True, False, True, False, True, False]
```

<span style="font-size: 14px;">Use `\&`, `|`, `\~` for element-wise boolean operations. Parentheses are required because bitwise operators have higher precedence than comparison operators.</span>

---

## <span style="font-size: 16px;">2D Boolean Filtering</span>

<span style="font-size: 14px;">Boolean indexing on 2D arrays returns a 1D result (the matching elements flattened):</span>

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]])

arr[arr > 5]  # [6, 7, 8, 9] - 1D result
```

<span style="font-size: 14px;">To filter entire rows based on a condition on one column:</span>

```python
row_mask = arr[:, 0] > 3   # condition on first column
arr[row_mask]               # [[4,5,6], [7,8,9]] - filtered rows
```

---

## <span style="font-size: 16px;">np.where()</span>

<span style="font-size: 14px;">`np.where` has two modes:</span>

### <span style="font-size: 14px;">Find Indices</span>

```python
indices = np.where(a > 4)  # tuple of index arrays
a[indices]                  # same as a[a > 4]
```

### <span style="font-size: 14px;">Conditional Selection (Ternary)</span>

```python
np.where(a > 4, a, 0)  # keep values > 4, replace others with 0
np.where(a > 4, 'big', 'small')  # element-wise if/else
```

<span style="font-size: 14px;">The three-argument form is a vectorized ternary operator: `np.where(cond, x, y)` returns $x_i$ when $\texttt{cond}_i$ is True, else $y_i$.</span>

---

## <span style="font-size: 16px;">np.extract() and np.compress()</span>

```python
np.extract(a > 4, a)         # same as a[a > 4]
np.compress(mask, a)          # same as a[mask]
np.compress([True, False, True], arr, axis=0)  # select rows 0, 2
```

---

## <span style="font-size: 16px;">Counting and Summarizing Matches</span>

```python
np.count_nonzero(a > 4)   # how many elements > 4
np.any(a > 4)              # True if any element > 4
np.all(a > 0)              # True if all elements > 0
np.sum(a > 4)              # count (True = 1, False = 0)
```

---

## <span style="font-size: 16px;">Slicing Then Filtering</span>

<span style="font-size: 14px;">A common pattern is to slice a contiguous block of rows, then filter within that block:</span>

```python
block = arr[2:5, :]        # rows 2-4
values = block[block > threshold]  # elements exceeding threshold
```

<span style="font-size: 14px;">The slice returns a view (fast, no copy), and the boolean filter returns a copy of the matching elements.</span>

---

## <span style="font-size: 16px;">Performance</span>

<span style="font-size: 14px;">Boolean indexing is highly optimized:</span>

* <span style="font-size: 14px;">The comparison runs as a single vectorized C operation</span>
* <span style="font-size: 14px;">The selection uses the boolean mask to compute offsets efficiently</span>
* <span style="font-size: 14px;">For large arrays, this is 10-100x faster than a Python for-loop</span>

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**2D flattening**: `arr[arr > 5]` returns a 1D array, not a 2D subarray. Use row-based masking for structured results.</span>
* <span style="font-size: 14px;">**Parentheses required**: `a > 2 \& a < 7` is parsed as `a > (2 \& a) < 7` due to operator precedence. Use `(a > 2) \& (a < 7)`.</span>
* <span style="font-size: 14px;">**NaN in comparisons**: `np.nan > 0` is False. Use `np.isnan()` to detect NaN values.</span>
* <span style="font-size: 14px;">**Boolean mask returns a copy**: Unlike slicing, boolean-indexed results are copies. Modifying them does not modify the original.</span>