# <span style="font-size: 20px;">Pairwise Differences</span>

<span style="font-size: 14px;">Computing the pairwise difference matrix - where element $(i, j)$ is $a_i - a_j$ - is a fundamental operation in distance computation, kernel methods, and data analysis. For a vector of $n$ elements, the result is an $n \times n$ matrix that encodes all relative differences. NumPy's broadcasting makes this computation elegant and vectorized. The complexity is still $O(n^2)$ since there are $n \times n$ pairs, but NumPy performs the arithmetic in compiled C code instead of a Python-level nested loop, which is typically 10-100x faster.</span>

---

## <span style="font-size: 16px;">The Broadcasting Approach</span>

<span style="font-size: 14px;">The key insight is reshaping the vector to enable broadcasting:</span>

```python
a = np.array([10, 20, 30, 40])

# Reshape to column vector (4, 1) and row vector (1, 4)
diff = a[:, np.newaxis] - a[np.newaxis, :]
# or equivalently:
diff = a[:, None] - a[None, :]
```

<span style="font-size: 14px;">This produces a $(4, 4)$ matrix:</span>

$$D_{ij} = a_i - a_j$$

```
[[ 0, -10, -20, -30],
 [10,   0, -10, -20],
 [20,  10,   0, -10],
 [30,  20,  10,   0]]
```

### <span style="font-size: 14px;">How Broadcasting Works Here</span>

1. <span style="font-size: 14px;">`a[:, None]` has shape $(4, 1)$ - a column vector</span>
2. <span style="font-size: 14px;">`a[None, :]` has shape $(1, 4)$ - a row vector</span>
3. <span style="font-size: 14px;">Subtraction broadcasts both to $(4, 4)$ by replicating the column across columns and the row across rows</span>
4. <span style="font-size: 14px;">Result: element $(i, j) = a_i - a_j$</span>

---

## <span style="font-size: 16px;">Properties of the Pairwise Difference Matrix</span>

* <span style="font-size: 14px;">**Antisymmetric**: $D_{ij} = -D_{ji}$</span>
* <span style="font-size: 14px;">**Zero diagonal**: $D_{ii} = 0$</span>
* <span style="font-size: 14px;">**Rank 1**: The matrix has rank at most 1 (it is an outer product minus its transpose)</span>

---

## <span style="font-size: 16px;">Pairwise Distance Matrix</span>

<span style="font-size: 14px;">The absolute pairwise differences give a distance matrix:</span>

```python
dist = np.abs(a[:, None] - a[None, :])
```

<span style="font-size: 14px;">For Euclidean distance between vectors in a matrix $X$ of shape $(n, d)$:</span>

```python
# Squared Euclidean distance matrix
diff = X[:, np.newaxis, :] - X[np.newaxis, :, :]  # (n, n, d)
dist_sq = np.sum(diff**2, axis=2)                  # (n, n)
dist = np.sqrt(dist_sq)
```

<span style="font-size: 14px;">A more numerically stable computation uses the identity $\|a - b\|^2 = \|a\|^2 + \|b\|^2 - 2a^Tb$:</span>

```python
sq_norms = np.sum(X**2, axis=1)
dist_sq = sq_norms[:, None] + sq_norms[None, :] - 2 * X @ X.T
dist_sq = np.maximum(dist_sq, 0)  # clamp negative values from floating-point error
dist = np.sqrt(dist_sq)
```

---

## <span style="font-size: 16px;">Applications</span>

* <span style="font-size: 14px;">**k-NN**: Compute all pairwise distances, then find the k smallest per row</span>
* <span style="font-size: 14px;">**RBF kernel**: $K_{ij} = \exp(-\gamma \|x_i - x_j\|^2)$ requires pairwise squared distances</span>
* <span style="font-size: 14px;">**Time series**: Pairwise differences of timestamps give all inter-event intervals</span>
* <span style="font-size: 14px;">**Sorting verification**: If all pairwise differences $D_{ij}$ with $i < j$ are positive, the array is sorted ascending</span>

---

## <span style="font-size: 16px;">Memory Considerations</span>

<span style="font-size: 14px;">The pairwise difference matrix has $n^2$ elements. For $n = 10{,}000$ float64 values:</span>

$$10{,}000^2 \times 8 \text{ bytes} = 800 \text{ MB}$$

<span style="font-size: 14px;">For large $n$, compute distances in batches or use scipy's `cdist`/`pdist` which store only the upper triangle.</span>

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**Memory explosion**: $O(n^2)$ memory for $n$ elements. For $n > 50{,}000$, consider batch computation.</span>
* <span style="font-size: 14px;">**axis confusion**: `a[:, None] - a[None, :]` gives differences. Swapping the order gives the transpose (negated).</span>
* <span style="font-size: 14px;">**Floating-point errors**: Squared distances can be slightly negative due to rounding. Use `np.maximum(0, dist_sq)` before taking sqrt.</span>
* <span style="font-size: 14px;">**Forgetting newaxis**: `a - a` gives all zeros (element-wise), not pairwise differences. The newaxis reshape is essential.</span>