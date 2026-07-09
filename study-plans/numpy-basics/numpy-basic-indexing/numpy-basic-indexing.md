# <span style="font-size: 20px;">Basic Indexing</span>

<span style="font-size: 14px;">NumPy's indexing system lets you extract any rectangular region from an array using slice notation. Understanding how slices, negative indices, and the stop-exclusive convention interact is essential for writing correct data pipeline code. Basic indexing always returns a view of the original array, meaning changes to the view affect the original data.</span>

---

## <span style="font-size: 16px;">2D Indexing with Comma Notation</span>

<span style="font-size: 14px;">A 2D NumPy array is indexed with two coordinates inside a single bracket pair, separated by a comma:</span>

```python
arr = np.array([[10, 20, 30],
                [40, 50, 60],
                [70, 80, 90]])

arr[0, 0]    # 10 (scalar: first row, first column)
arr[1, 2]    # 60 (scalar: second row, third column)
arr[0]       # [10, 20, 30] (entire first row)
arr[:, 1]    # [20, 50, 80] (entire second column)
```

<span style="font-size: 14px;">The syntax `arr[row, col]` is equivalent to `arr[row][col]` but more efficient: the single-bracket form selects the element in one operation, while the double-bracket form creates an intermediate row array.</span>

---

## <span style="font-size: 16px;">Slice Notation: start:stop:step</span>

<span style="font-size: 14px;">NumPy slicing follows Python conventions:</span>

```python
arr[0:2, :]     # rows 0, 1 (stop is exclusive)
arr[:, 1:3]     # columns 1, 2
arr[::2, :]     # every other row (step=2)
arr[::-1, :]    # rows in reverse order
```

### <span style="font-size: 14px;">Key Rules</span>

* <span style="font-size: 14px;">`start:stop` selects indices from start up to (but not including) stop</span>
* <span style="font-size: 14px;">Omitting start defaults to 0; omitting stop defaults to the axis length</span>
* <span style="font-size: 14px;">`start:stop:step` takes every step-th element</span>
* <span style="font-size: 14px;">Negative step reverses direction: `::-1` reverses the axis</span>

### <span style="font-size: 14px;">Subarray Shape</span>

<span style="font-size: 14px;">The shape of a slice `arr[r0:r1, c0:c1]` is:</span>

$$(\texttt{r1} - \texttt{r0}, \; \texttt{c1} - \texttt{c0})$$

---

## <span style="font-size: 16px;">Negative Indexing</span>

<span style="font-size: 14px;">Negative indices count from the end:</span>

```python
arr[-1]       # last row: [70, 80, 90]
arr[-1, -1]   # bottom-right element: 90
arr[-2:, :]   # last two rows
arr[:, -1]    # last column: [30, 60, 90]
```

<span style="font-size: 14px;">Negative index $-k$ refers to position $N - k$, where $N$ is the axis length. This is especially useful for accessing the last element without knowing the array size.</span>

---

## <span style="font-size: 16px;">Views vs. Copies</span>

<span style="font-size: 14px;">Basic indexing (slicing) returns a view, not a copy:</span>

```python
a = np.array([[1, 2], [3, 4]])
b = a[0, :]    # b is a VIEW of a's first row
b[0] = 99      # modifies a[0, 0] as well!
print(a)       # [[99, 2], [3, 4]]
```

<span style="font-size: 14px;">This is a deliberate design choice for performance: views share memory with the original, avoiding expensive copies for large arrays. To get an independent copy:</span>

```python
b = a[0, :].copy()
b[0] = 99      # a is unchanged
```

### <span style="font-size: 14px;">How to Check if Something is a View</span>

```python
b = a[0:2, :]
b.base is a    # True: b shares memory with a
b.flags.owndata  # False: b does not own its data
```

---

## <span style="font-size: 16px;">Ellipsis (...)</span>

<span style="font-size: 14px;">The ellipsis expands to as many colons as needed to fill remaining dimensions:</span>

```python
# For a 4D array of shape (2, 3, 4, 5):
a[..., 0]       # equivalent to a[:, :, :, 0] - shape (2, 3, 4)
a[0, ...]       # equivalent to a[0, :, :, :] - shape (3, 4, 5)
a[0, ..., -1]   # equivalent to a[0, :, :, -1] - shape (3, 4)
```

<span style="font-size: 14px;">Ellipsis is essential for writing dimension-agnostic code that works on arrays with any number of dimensions.</span>

---

## <span style="font-size: 16px;">np.newaxis for Adding Dimensions</span>

<span style="font-size: 14px;">`np.newaxis` (alias for `None`) inserts a new axis of length 1:</span>

```python
v = np.array([1, 2, 3])       # shape (3,)
row = v[np.newaxis, :]         # shape (1, 3) - row vector
col = v[:, np.newaxis]         # shape (3, 1) - column vector
```

<span style="font-size: 14px;">This is critical for broadcasting: converting a 1D vector to a 2D row or column vector enables element-wise operations with 2D arrays.</span>

---

## <span style="font-size: 16px;">Assignment with Indexing</span>

<span style="font-size: 14px;">You can assign to slices to modify portions of an array in-place:</span>

```python
arr[0, :] = 0          # set first row to zeros
arr[:, -1] = [1, 2, 3] # set last column
arr[1:3, 1:3] = [[99, 99], [99, 99]]  # set a subregion
```

<span style="font-size: 14px;">The right-hand side must be broadcastable to the selected region's shape.</span>

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**View mutation**: Slicing returns a view. Modifying the slice modifies the original. Use `.copy()` if you need independence.</span>
* <span style="font-size: 14px;">**Off-by-one with stop**: `arr[0:2]` includes indices 0, 1 but not 2. This is consistent with Python but catches newcomers.</span>
* <span style="font-size: 14px;">**Single int vs. slice**: `arr[0]` reduces dimensionality (returns a 1D array from 2D). `arr[0:1]` preserves dimensionality.</span>
* <span style="font-size: 14px;">**Negative index with slice**: `arr[-1:0]` returns an empty array because -1 comes after 0 in the forward direction. Use `arr[-1:]` to get the last element.</span>