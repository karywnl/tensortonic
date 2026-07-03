# <span style="font-size: 20px;">Reshaping Arrays</span>

<span style="font-size: 14px;">Reshaping changes the dimensions of an array without altering its data. A $(6,)$ array can become $(2, 3)$ or $(3, 2)$ or $(1, 6)$ or $(6, 1)$, as long as the total number of elements remains the same. Reshaping is one of the most frequently used operations in machine learning preprocessing, where data must be converted between 1D vectors, 2D matrices, and higher-dimensional tensors.</span>

---

## <span style="font-size: 16px;">The reshape() Method</span>

```python
a = np.arange(12)        # [0, 1, 2, ..., 11], shape (12,)
b = a.reshape(3, 4)      # shape (3, 4)
c = a.reshape(4, 3)      # shape (4, 3)
d = a.reshape(2, 2, 3)   # shape (2, 2, 3)
```

<span style="font-size: 14px;">The constraint is that the product of the new dimensions must equal the product of the old dimensions:</span>

$$\prod_{i} \text{new\_shape}[i] = \prod_{j} \text{old\_shape}[j]$$

<span style="font-size: 14px;">If this constraint is violated, NumPy raises a `ValueError`.</span>

### <span style="font-size: 14px;">The -1 Wildcard</span>

<span style="font-size: 14px;">Use $-1$ for one dimension to let NumPy infer it:</span>

```python
a = np.arange(12)
a.reshape(3, -1)    # (3, 4) - NumPy computes 12/3 = 4
a.reshape(-1, 6)    # (2, 6) - NumPy computes 12/6 = 2
a.reshape(-1)       # (12,) - flatten to 1D
```

<span style="font-size: 14px;">Only one dimension can be $-1$. This is extremely common in practice because you often know one dimension (e.g., batch size) but not the other.</span>

---

## <span style="font-size: 16px;">Views vs. Copies in Reshape</span>

<span style="font-size: 14px;">`reshape()` returns a view when possible. A view shares memory with the original:</span>

```python
a = np.arange(12)
b = a.reshape(3, 4)
b[0, 0] = 99       # also changes a[0]
```

<span style="font-size: 14px;">A view is possible when the new shape is compatible with the array's memory layout (strides). If the array is non-contiguous (e.g., after a transpose), reshape may need to copy:</span>

```python
a = np.arange(12).reshape(3, 4)
t = a.T              # shape (4, 3), non-contiguous
r = t.reshape(12)    # must copy because strides are incompatible
```

---

## <span style="font-size: 16px;">flatten() vs. ravel()</span>

<span style="font-size: 14px;">Two methods for converting to 1D:</span>

```python
a = np.array([[1, 2], [3, 4]])

a.flatten()   # [1, 2, 3, 4] - always returns a COPY
a.ravel()     # [1, 2, 3, 4] - returns a VIEW when possible
```

* <span style="font-size: 14px;">`flatten()`: Always creates a new array. Safe to modify without affecting the original.</span>
* <span style="font-size: 14px;">`ravel()`: Returns a view when possible. Faster and more memory-efficient, but modifications may affect the original.</span>

<span style="font-size: 14px;">`a.reshape(-1)` is equivalent to `a.ravel()`.</span>

---

## <span style="font-size: 16px;">Transpose</span>

<span style="font-size: 14px;">`.T` swaps rows and columns (more generally, reverses all axes):</span>

```python
a = np.array([[1, 2, 3], [4, 5, 6]])  # shape (2, 3)
a.T   # shape (3, 2)
```

<span style="font-size: 14px;">Transpose returns a view by manipulating strides, not by moving data. For higher-dimensional arrays, use `np.transpose()` with an explicit axis order:</span>

```python
a = np.zeros((2, 3, 4))
np.transpose(a, (1, 2, 0))  # shape (3, 4, 2)
```

---

## <span style="font-size: 16px;">Adding and Removing Dimensions</span>

### <span style="font-size: 14px;">np.expand_dims()</span>

```python
a = np.array([1, 2, 3])        # shape (3,)
np.expand_dims(a, axis=0)      # shape (1, 3) - add row dimension
np.expand_dims(a, axis=1)      # shape (3, 1) - add column dimension
```

### <span style="font-size: 14px;">np.squeeze()</span>

```python
a = np.array([[[1, 2, 3]]])    # shape (1, 1, 3)
np.squeeze(a)                   # shape (3,) - remove all length-1 dimensions
np.squeeze(a, axis=0)           # shape (1, 3) - remove only axis 0
```

---

## <span style="font-size: 16px;">Machine Learning Reshape Patterns</span>

### <span style="font-size: 14px;">Flattening Images for Dense Layers</span>

```python
images = np.random.randn(100, 28, 28)  # 100 grayscale 28x28 images
flat = images.reshape(100, -1)          # shape (100, 784)
```

### <span style="font-size: 14px;">Adding Channel Dimension for CNNs</span>

```python
images = np.random.randn(100, 28, 28)         # (batch, height, width)
images_4d = images.reshape(100, 1, 28, 28)    # (batch, channels, height, width)
# or equivalently:
images_4d = images[:, np.newaxis, :, :]
```

### <span style="font-size: 14px;">Reshaping Predictions</span>

```python
predictions = model.predict(X)      # shape (1000, 1)
predictions = predictions.ravel()    # shape (1000,) - for comparison with y
```

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**Size mismatch**: Reshaping (12,) to (3, 5) raises ValueError because $3 \times 5 = 15 \neq 12$.</span>
* <span style="font-size: 14px;">**View mutation**: `reshape()` often returns a view. Modifying the reshaped array may modify the original.</span>
* <span style="font-size: 14px;">**Row-major element order**: Reshape fills elements in row-major (C) order by default. `[1,2,3,4,5,6].reshape(2,3)` gives `[[1,2,3],[4,5,6]]`, not `[[1,3,5],[2,4,6]]`.</span>
* <span style="font-size: 14px;">**Confusing reshape and transpose**: Reshape changes dimensions but not element order. Transpose changes the axis ordering. To convert a $(2, 3)$ array to $(3, 2)$ by swapping axes, use `.T`, not `.reshape(3, 2)`.</span>