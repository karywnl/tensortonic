# <span style="font-size: 20px;">Zeros and Ones</span>

<span style="font-size: 14px;">Creating arrays filled with zeros or ones is one of the most frequent operations in numerical computing. These arrays serve as initializers for accumulators, masks, identity-like constructs, and placeholder tensors. NumPy provides `np.zeros()`, `np.ones()`, `np.zeros_like()`, and `np.ones_like()` for this purpose, along with the related `np.full()` for arbitrary fill values and `np.empty()` for uninitialized memory.</span>

---

## <span style="font-size: 16px;">np.zeros()</span>

<span style="font-size: 14px;">Creates an array filled with zeros:</span>

```python
np.zeros(5)            # 1D: [0. 0. 0. 0. 0.], dtype float64
np.zeros((3, 4))       # 2D: shape (3, 4), all zeros
np.zeros((2, 3, 4))    # 3D: shape (2, 3, 4)
```

<span style="font-size: 14px;">The default dtype is `float64`. Pass `dtype` to change:</span>

```python
np.zeros(5, dtype=np.int32)     # [0, 0, 0, 0, 0] as int32
np.zeros(5, dtype=bool)         # [False, False, False, False, False]
np.zeros(5, dtype=np.complex64) # [0.+0.j, ...]
```

### <span style="font-size: 14px;">Use Cases</span>

* <span style="font-size: 14px;">**Accumulators**: Initialize a sum/count array before a loop: `totals = np.zeros(n_classes)`</span>
* <span style="font-size: 14px;">**Padding**: Create a zero-padded version of an array for convolution or FFT</span>
* <span style="font-size: 14px;">**Masks**: Boolean arrays initialized to False (all zeros) for selective operations</span>
* <span style="font-size: 14px;">**Neural network weights**: Some initialization schemes set biases to zero</span>

---

## <span style="font-size: 16px;">np.ones()</span>

<span style="font-size: 14px;">Creates an array filled with ones:</span>

```python
np.ones(5)           # [1. 1. 1. 1. 1.]
np.ones((3, 4))      # shape (3, 4), all ones
```

### <span style="font-size: 14px;">Use Cases</span>

* <span style="font-size: 14px;">**Multiplicative identity**: Initialize a product accumulator</span>
* <span style="font-size: 14px;">**Bias vectors**: Neural network bias terms often initialize to ones</span>
* <span style="font-size: 14px;">**Homogeneous coordinates**: Append a column of ones to a feature matrix for linear regression: $X_{aug} = [X | \mathbf{1}]$</span>
* <span style="font-size: 14px;">**Scaling factors**: Initialize per-feature scaling to identity</span>

---

## <span style="font-size: 16px;">np.full()</span>

<span style="font-size: 14px;">Creates an array filled with an arbitrary constant:</span>

```python
np.full((3, 4), 7)           # shape (3, 4), all 7s
np.full((2, 3), np.nan)      # shape (2, 3), all NaN
np.full((5,), -1, dtype=int) # [-1, -1, -1, -1, -1]
```

<span style="font-size: 14px;">`np.full()` is more readable than `np.ones(shape) * value` and avoids the unnecessary multiplication.</span>

---

## <span style="font-size: 16px;">np.empty()</span>

<span style="font-size: 14px;">Allocates memory without initializing it:</span>

```python
a = np.empty((1000, 1000))  # fastest creation, garbage values
```

<span style="font-size: 14px;">The array contains whatever was in memory at that location. This is useful when you are going to fill every element immediately (e.g., in a computation loop), because it skips the cost of writing zeros. Never read from an `empty` array before writing to it.</span>

---

## <span style="font-size: 16px;">_like() Variants</span>

<span style="font-size: 14px;">Create arrays with the same shape and dtype as an existing array:</span>

```python
template = np.array([[1.0, 2.0], [3.0, 4.0]])

np.zeros_like(template)   # same shape (2, 2), same dtype float64, all zeros
np.ones_like(template)    # same shape, all ones
np.full_like(template, 5) # same shape, all fives
np.empty_like(template)   # same shape, uninitialized
```

<span style="font-size: 14px;">The `_like` variants are convenient because you do not need to manually extract shape and dtype from the template. They are commonly used to create output arrays that match an input array:</span>

```python
def normalize(x):
    result = np.zeros_like(x)
    for i in range(x.shape[0]):
        result[i] = x[i] / np.linalg.norm(x[i])
    return result
```

---

## <span style="font-size: 16px;">np.eye() and np.identity()</span>

<span style="font-size: 14px;">Create identity matrices:</span>

```python
np.eye(3)       # 3x3 identity matrix
np.eye(3, 5)    # 3x5 matrix with 1s on diagonal
np.eye(3, k=1)  # 1s on the superdiagonal
np.identity(3)  # always square, always main diagonal
```

<span style="font-size: 14px;">`np.eye()` is more flexible (supports non-square and off-diagonal). `np.identity()` is a convenience for the common case.</span>

<span style="font-size: 14px;">**Fun fact:** the name `eye` is a phonetic play on the letter **I**, which is how mathematicians denote the identity matrix ($I$). So `np.eye(3)` literally reads as "I of 3".</span>

---

## <span style="font-size: 16px;">Performance Comparison</span>

<span style="font-size: 14px;">For a $(1000, 1000)$ float64 array:</span>

| Function | Relative Time |
|----------|--------------|
| `np.empty()` | 1x (baseline) |
| `np.zeros()` | ~1x (OS provides zeroed pages) |
| `np.ones()` | ~2-3x (must write to every element) |
| `np.full(value)` | ~2-3x (must write to every element) |
| `np.ones() * value` | ~4-5x (write + multiply) |

<span style="font-size: 14px;">`np.zeros()` is nearly as fast as `np.empty()` because the operating system provides pre-zeroed memory pages. `np.ones()` and `np.full()` must explicitly write to every element.</span>

---

## <span style="font-size: 16px;">Practical Patterns</span>

### <span style="font-size: 14px;">One-Hot Encoding</span>

```python
n_classes = 10
label = 3
one_hot = np.zeros(n_classes)
one_hot[label] = 1.0  # [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
```

### <span style="font-size: 14px;">Confusion Matrix Initialization</span>

```python
cm = np.zeros((n_classes, n_classes), dtype=np.int64)
for true, pred in zip(y_true, y_pred):
    cm[true, pred] += 1
```

### <span style="font-size: 14px;">Feature Matrix with Bias Column</span>

```python
X_augmented = np.column_stack([X, np.ones(X.shape[0])])
```

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**Reading from np.empty**: Uninitialized memory contains garbage values. Always fill before reading.</span>
* <span style="font-size: 14px;">**Shape as int vs. tuple**: `np.zeros(5)` creates 1D; `np.zeros((5,))` is equivalent. But `np.zeros(5, 3)` is an error - use `np.zeros((5, 3))` for 2D.</span>
* <span style="font-size: 14px;">**Default float64**: `np.zeros(5)` creates float64, not int. Specify `dtype=int` if you need integers.</span>
* <span style="font-size: 14px;">**ones * value vs. full**: `np.ones(shape) * 7` creates a temporary array and multiplies. `np.full(shape, 7)` is more efficient and readable.</span>