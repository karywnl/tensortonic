# <span style="font-size: 20px;">Fancy Indexing</span>

<span style="font-size: 14px;">Fancy indexing (also called advanced indexing) selects array elements using integer arrays or lists as indices, rather than slices. Unlike basic indexing which selects contiguous regions, fancy indexing can select arbitrary elements in any order, with repetition. This makes it essential for operations like reordering rows, extracting non-contiguous elements, and implementing lookup tables.</span>

---

## <span style="font-size: 16px;">Integer Array Indexing</span>

<span style="font-size: 14px;">Pass an array (or list) of integers to select elements at those positions:</span>

```python
a = np.array([10, 20, 30, 40, 50])
indices = np.array([0, 3, 1, 4])
a[indices]  # [10, 40, 20, 50]
```

<span style="font-size: 14px;">The result has the same shape as the index array. Elements can be selected in any order and repeated:</span>

```python
a[[2, 2, 0]]  # [30, 30, 10] - element at index 2 appears twice
```

---

## <span style="font-size: 16px;">2D Fancy Indexing</span>

### <span style="font-size: 14px;">Selecting Rows</span>

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]])

arr[[0, 2]]        # rows 0 and 2: [[1,2,3], [7,8,9]]
arr[[2, 0, 1]]     # reorder rows: [[7,8,9], [1,2,3], [4,5,6]]
```

### <span style="font-size: 14px;">Selecting Along an Axis</span>

```python
arr[:, [0, 2]]     # columns 0 and 2
arr[[0, 2], :]     # rows 0 and 2 (same as arr[[0, 2]])
```

### <span style="font-size: 14px;">Element-wise Selection</span>

```python
rows = np.array([0, 1, 2])
cols = np.array([2, 0, 1])
arr[rows, cols]    # [arr[0,2], arr[1,0], arr[2,1]] = [3, 4, 8]
```

<span style="font-size: 14px;">When two index arrays are provided for different axes, they are paired element-wise. Both arrays must have the same shape or be broadcastable.</span>

---

## <span style="font-size: 16px;">Fancy Indexing Always Returns a Copy</span>

<span style="font-size: 14px;">Unlike basic indexing (slicing), which returns a view, fancy indexing always returns a copy:</span>

```python
a = np.array([1, 2, 3, 4, 5])
b = a[[0, 2, 4]]   # copy, not a view
b[0] = 99          # does NOT modify a
```

<span style="font-size: 14px;">This means fancy indexing is safer (no accidental mutation) but slower (memory allocation and copying).</span>

---

## <span style="font-size: 16px;">np.take() and np.take_along_axis()</span>

<span style="font-size: 14px;">Functional alternatives to fancy indexing:</span>

```python
np.take(arr, [0, 2], axis=0)        # take rows 0, 2 (like arr[[0, 2]])
np.take(arr, [0, 2], axis=1)        # take columns 0, 2

# take_along_axis: useful with argsort results
sorted_indices = np.argsort(arr, axis=1)
np.take_along_axis(arr, sorted_indices, axis=1)  # sort each row
```

---

## <span style="font-size: 16px;">Assignment with Fancy Indexing</span>

```python
a = np.zeros(5)
a[[0, 2, 4]] = [10, 30, 50]   # set specific elements
a[[1, 1, 1]] = [10, 20, 30]   # duplicate index: last value wins (30)
```

<span style="font-size: 14px;">For duplicate indices, use `np.add.at()` for accumulation instead of assignment:</span>

```python
np.add.at(a, [1, 1, 1], [10, 20, 30])  # a[1] becomes 60 (accumulated)
```

---

## <span style="font-size: 16px;">Practical Applications</span>

### <span style="font-size: 14px;">Batch Selection in ML</span>

```python
batch_indices = rng.choice(len(X), size=32, replace=False)
X_batch = X[batch_indices]
y_batch = y[batch_indices]
```

### <span style="font-size: 14px;">Embedding Lookup</span>

```python
embeddings = np.random.randn(10000, 128)  # 10k words, 128-dim
token_ids = [42, 7, 256, 42]
selected = embeddings[token_ids]           # shape (4, 128)
```

### <span style="font-size: 14px;">Reordering by Sort</span>

```python
a = np.array([30, 10, 20])
order = np.argsort(a)       # [1, 2, 0]
a[order]                    # [10, 20, 30]
```

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**Copy, not view**: Unlike slicing, fancy indexing copies data. Modifying the result does not affect the original.</span>
* <span style="font-size: 14px;">**Duplicate index assignment**: `a[[0, 0]] = [1, 2]` sets `a[0] = 2` (last value wins), not `a[0] = 3` (not summed). Use `np.add.at` for accumulation.</span>
* <span style="font-size: 14px;">**Shape of result**: The result shape matches the index array shape, not the source array shape. `a[np.array([[0,1],[2,3]])]` returns a $(2, 2)$ array.</span>
* <span style="font-size: 14px;">**Out of bounds**: Indices outside $[0, n)$ raise `IndexError`. Use `np.clip` to clamp indices safely.</span>