# <span style="font-size: 20px;">Outer Sum</span>

<span style="font-size: 14px;">The outer sum of two vectors $a$ and $b$ produces a matrix where element $(i, j) = a_i + b_j$. It is the additive analog of the outer product $a_i \cdot b_j$. Outer sums appear in distance computation, kernel construction, grid generation, and anywhere you need to evaluate a function over all pairs of two sets of values. NumPy's broadcasting makes this operation both concise and efficient.</span>

---

## <span style="font-size: 16px;">Broadcasting Construction</span>

```python
a = np.array([1, 2, 3])     # shape (3,)
b = np.array([10, 20])      # shape (2,)

outer = a[:, np.newaxis] + b[np.newaxis, :]
# shape (3, 2):
# [[11, 21],
#  [12, 22],
#  [13, 23]]
```

<span style="font-size: 14px;">The reshape creates a column vector $(3, 1)$ and a row vector $(1, 2)$. Broadcasting expands both to $(3, 2)$ and adds element-wise.</span>

---

## <span style="font-size: 16px;">np.add.outer()</span>

<span style="font-size: 14px;">NumPy provides a dedicated method. For inputs of shape</span> $(m,)$ <span style="font-size: 14px;">and</span> $(n,)$<span style="font-size: 14px;">, the result has shape</span> $(m, n)$ <span style="font-size: 14px;">where entry</span> $[i, j] = a_i + b_j$<span style="font-size: 14px;">:</span>

```python
a = np.array([1, 2, 3])      # shape (3,)
b = np.array([10, 20])       # shape (2,)
np.add.outer(a, b)           # shape (3, 2)
# [[11, 21],
#  [12, 22],
#  [13, 23]]
```

<span style="font-size: 14px;">This is more readable and avoids manual reshaping. The `.outer` method exists for all universal functions:</span>

```python
np.multiply.outer(a, b)   # outer product: a_i * b_j
np.subtract.outer(a, b)   # outer difference: a_i - b_j
np.maximum.outer(a, b)    # element-wise max: max(a_i, b_j)
```

---

## <span style="font-size: 16px;">Mathematical Definition</span>

<span style="font-size: 14px;">For vectors $a \in \mathbb{R}^m$ and $b \in \mathbb{R}^n$, the outer sum is:</span>

$$S_{ij} = a_i + b_j, \quad i \in [0, m), \; j \in [0, n)$$

<span style="font-size: 14px;">In matrix form: $S = a \mathbf{1}^T + \mathbf{1} b^T$ where $\mathbf{1}$ is the all-ones vector of appropriate size.</span>

---

## <span style="font-size: 16px;">Applications</span>

### <span style="font-size: 14px;">Distance Matrix Construction</span>

<span style="font-size: 14px;">The squared Euclidean distance matrix can be decomposed using outer sums:</span>

$$\|x_i - x_j\|^2 = \|x_i\|^2 + \|x_j\|^2 - 2 x_i^T x_j$$

```python
sq_norms = np.sum(X**2, axis=1)
dist_sq = np.add.outer(sq_norms, sq_norms) - 2 * X @ X.T
```

### <span style="font-size: 14px;">Grid Evaluation</span>

```python
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
Z = np.add.outer(x**2, y**2)  # z = x^2 + y^2 on a grid
```

### <span style="font-size: 14px;">Log-Probability Tables</span>

<span style="font-size: 14px;">In probabilistic models, $\log p(x, y) = \log p(x) + \log p(y)$ for independent variables. The outer sum of log-probabilities gives the joint log-probability table.</span>

---

## <span style="font-size: 16px;">Memory and Performance</span>

<span style="font-size: 14px;">The outer sum of vectors of length $m$ and $n$ produces an $m \times n$ matrix. For $m = n = 10{,}000$, this is $10^8$ elements = 800 MB in float64. Consider batch computation for large vectors.</span>

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**Forgetting reshape**: `a + b` gives element-wise addition (requires same shape), not outer sum. Use `a[:, None] + b[None, :]` or `np.add.outer(a, b)`.</span>
* <span style="font-size: 14px;">**Memory explosion**: The output is $m \times n$ regardless of input sizes. Large vectors produce huge matrices.</span>
* <span style="font-size: 14px;">**Axis order**: `np.add.outer(a, b)` puts $a$ along rows and $b$ along columns. Swapping $a$ and $b$ transposes the result.</span>