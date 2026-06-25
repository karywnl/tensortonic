# <span style="font-size: 20px;">Create Arrays from Lists</span>

<span style="font-size: 14px;">The NumPy array (`ndarray`) is the fundamental data structure for numerical computing in Python. Converting Python lists to NumPy arrays is the first step in almost every scientific computing pipeline. Understanding how the constructor handles nested lists, infers data types, and allocates memory is essential for writing correct and efficient numerical code.</span>

---

## <span style="font-size: 16px;">The np.array() Constructor</span>

<span style="font-size: 14px;">The primary function for creating arrays from existing data:</span>

```python
import numpy as np

# 1D array from a flat list
a = np.array([1, 2, 3, 4])
# shape: (4,), dtype: int64

# 2D array from a list of lists
b = np.array([[1, 2, 3], [4, 5, 6]])
# shape: (2, 3), dtype: int64
```

<span style="font-size: 14px;">Each inner list becomes a row. All inner lists must have the same length, or NumPy creates a ragged array of dtype `object` (which defeats the purpose of using NumPy).</span>

---

## <span style="font-size: 16px;">Type Inference</span>

<span style="font-size: 14px;">NumPy infers the data type from the input values using upcasting rules:</span>

* <span style="font-size: 14px;">All integers: `int64` on 64-bit systems</span>
* <span style="font-size: 14px;">Any float present: `float64` (all values upcast to float)</span>
* <span style="font-size: 14px;">Any complex number: `complex128`</span>
* <span style="font-size: 14px;">Mixed numeric and string: `object` (avoid this)</span>

```python
np.array([1, 2, 3]).dtype          # int64
np.array([1, 2, 3.0]).dtype        # float64 (int upcast to float)
np.array([1, 2, 3+0j]).dtype       # complex128
```

### <span style="font-size: 14px;">Explicit dtype</span>

<span style="font-size: 14px;">Override inference with the `dtype` parameter:</span>

```python
np.array([1, 2, 3], dtype=np.float64)   # force float64
np.array([1, 2, 3], dtype=np.float32)   # use less memory
np.array([1.9, 2.7], dtype=np.int32)    # truncates to [1, 2]
```

<span style="font-size: 14px;">Specifying `dtype` is important for reproducibility (same behavior on 32-bit and 64-bit systems) and for memory optimization (float32 uses half the memory of float64).</span>

---

## <span style="font-size: 16px;">Memory Layout</span>

<span style="font-size: 14px;">NumPy arrays store data in a contiguous block of memory, unlike Python lists which store pointers to scattered objects:</span>

$$\text{Memory} = \text{shape[0]} \times \text{shape[1]} \times \text{itemsize}$$

<span style="font-size: 14px;">A $(1000, 1000)$ float64 array uses exactly $1000 \times 1000 \times 8 = 8$ MB. The same data in a Python list of lists would use roughly 80-100 MB due to object overhead.</span>

### <span style="font-size: 14px;">Row-Major (C) vs. Column-Major (Fortran) Order</span>

<span style="font-size: 14px;">By default, NumPy stores arrays in row-major (C) order: elements of each row are contiguous in memory. This means iterating across columns within a row is fast (cache-friendly), while iterating down rows within a column is slower.</span>

```python
a = np.array([[1, 2, 3], [4, 5, 6]], order='C')  # row-major (default)
b = np.array([[1, 2, 3], [4, 5, 6]], order='F')  # column-major
```

---

## <span style="font-size: 16px;">Homogeneity Requirement</span>

<span style="font-size: 14px;">Unlike Python lists, NumPy arrays are homogeneous: every element has the same type. This constraint enables:</span>

* <span style="font-size: 14px;">**Vectorized operations**: The CPU can process elements in bulk using SIMD instructions because all elements have the same size and type.</span>
* <span style="font-size: 14px;">**Predictable memory layout**: Element $i$ is at memory offset $i \times \text{itemsize}$, enabling $O(1)$ random access.</span>
* <span style="font-size: 14px;">**Efficient broadcasting**: Operations between arrays of different shapes work because element sizes are uniform.</span>

<span style="font-size: 14px;">If you pass mixed types, NumPy upcasts everything to the most general type. Avoid creating `object` arrays, which lose all performance benefits.</span>

---

## <span style="font-size: 16px;">Array Attributes</span>

<span style="font-size: 14px;">After creating an array, inspect its properties:</span>

```python
a = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])

a.shape      # (3, 2) - dimensions
a.ndim       # 2 - number of dimensions
a.size       # 6 - total element count
a.dtype      # float64 - element type
a.itemsize   # 8 - bytes per element
a.nbytes     # 48 - total bytes (size * itemsize)
a.strides    # (16, 8) - bytes between elements along each axis
```

### <span style="font-size: 14px;">Strides</span>

<span style="font-size: 14px;">Strides tell NumPy how many bytes to skip to reach the next element along each axis. For a $(3, 2)$ float64 array in C order:</span>

* <span style="font-size: 14px;">Stride along axis 0 (rows): $2 \times 8 = 16$ bytes (skip one full row)</span>
* <span style="font-size: 14px;">Stride along axis 1 (columns): $8$ bytes (skip one element)</span>

<span style="font-size: 14px;">Understanding strides is key to understanding views, broadcasting, and performance.</span>

---

## <span style="font-size: 16px;">Copy vs. View Behavior</span>

<span style="font-size: 14px;">`np.array()` always creates a new copy of the data. If you want to avoid copying:</span>

```python
a = np.asarray(my_list)   # avoids copy if input is already an ndarray
a = np.asarray(my_list, dtype=np.float64)  # still avoids copy if dtype matches
```

<span style="font-size: 14px;">`np.asarray()` returns the input unchanged if it is already an array with the correct dtype. `np.array()` always copies. Use `asarray` in function signatures to accept both arrays and lists efficiently.</span>

---

## <span style="font-size: 16px;">Common Creation Patterns</span>

```python
# From a range or any iterable (no need to convert to list)
np.array(range(100))

# From a generator (generators DO need list() first)
np.array(list(x for x in range(100)))

# From a tuple
np.array((1, 2, 3))

# Nested tuples/lists can be mixed
np.array([(1, 2), [3, 4]])  # works, produces (2, 2) array

# Empty array with specific shape
np.empty((3, 4))  # uninitialized, fastest creation
np.zeros((3, 4))  # all zeros
np.ones((3, 4))   # all ones
```

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**Ragged lists**: `np.array([[1,2], [3,4,5]])` raises `ValueError: inhomogeneous shape`. To create a ragged array, you must explicitly pass `dtype=object`: `np.array([[1,2], [3,4,5]], dtype=object)`.</span>
* <span style="font-size: 14px;">**Silent upcasting**: `np.array([1, 2, 3.0])` silently converts all integers to float64. Check dtype if integer precision matters.</span>
* <span style="font-size: 14px;">**Object arrays**: Arrays with dtype `object` have no performance advantage over Python lists. They arise from mixed types or ragged inputs.</span>
* <span style="font-size: 14px;">**Mutating shared data**: `np.asarray` can return a view that shares memory with the input. Modifying the view modifies the original.</span>