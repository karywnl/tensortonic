# <span style="font-size: 20px;">Row Scaling</span>

<span style="font-size: 14px;">Row scaling multiplies (or divides) each row of a matrix by a corresponding scalar. This operation appears constantly in data preprocessing: normalizing samples by their total, applying per-observation weights, computing diagonal matrix products, and rescaling probability distributions. The key to implementing it efficiently in NumPy is understanding broadcasting and the `np.newaxis` (or `None`) trick.</span>

---

## <span style="font-size: 16px;">The Broadcasting Approach</span>

<span style="font-size: 14px;">Given a 2D array $A$ of shape $(m, n)$ and a weight vector $s$ of shape $(m,)$, multiply each row $i$ by $s_i$:</span>

```python
A = np.array([[1, 2, 3],
              [4, 5, 6]])   # shape (2, 3)
s = np.array([10, 100])     # shape (2,)

# Reshape s to (2, 1) for broadcasting
result = A * s[:, np.newaxis]
# [[10, 20, 30],
#  [400, 500, 600]]
```

### <span style="font-size: 14px;">Why the Reshape is Needed</span>

<span style="font-size: 14px;">Without reshaping, $A * s$ tries to broadcast $(2, 3)$ and $(2,)$. NumPy aligns from the right: the last dimensions (3 and 2) do not match and cannot broadcast. By reshaping $s$ to $(2, 1)$, the shapes $(2, 3)$ and $(2, 1)$ are compatible: the 1 broadcasts to 3.</span>

$$\begin{pmatrix} s_0 \\ s_1 \end{pmatrix}_{(2,1)} \odot \begin{pmatrix} a_{00} & a_{01} & a_{02} \\ a_{10} & a_{11} & a_{12} \end{pmatrix}_{(2,3)} = \begin{pmatrix} s_0 a_{00} & s_0 a_{01} & s_0 a_{02} \\ s_1 a_{10} & s_1 a_{11} & s_1 a_{12} \end{pmatrix}$$

---

## <span style="font-size: 16px;">Division for Normalization</span>

```python
row_sums = A.sum(axis=1, keepdims=True)  # shape (2, 1)
normalized = A / row_sums
```

<span style="font-size: 14px;">Using `keepdims=True` preserves the column dimension as 1, enabling broadcasting without manual reshaping.</span>

---

## <span style="font-size: 16px;">Equivalent Matrix Operation</span>

<span style="font-size: 14px;">Row scaling by $s$ is equivalent to left-multiplication by a diagonal matrix:</span>

$$\text{diag}(s) \cdot A$$

```python
np.diag(s) @ A  # correct but creates a full (m, m) matrix
A * s[:, None]   # same result, no temporary matrix
```

<span style="font-size: 14px;">The broadcasting approach is much more memory-efficient: it uses $O(m)$ for the weight vector instead of $O(m^2)$ for the diagonal matrix.</span>

---

## <span style="font-size: 16px;">Applications</span>

* <span style="font-size: 14px;">**Sample weighting**: Weight each observation by its importance: $X_w = \text{diag}(w) \cdot X$</span>
* <span style="font-size: 14px;">**Row normalization**: Divide each row by its L2 norm for unit-length vectors</span>
* <span style="font-size: 14px;">**Probability normalization**: Divide each row by its sum to get valid probability distributions</span>
* <span style="font-size: 14px;">**Inverse scaling**: Divide by per-row statistics to undo a previous scaling</span>

---

## <span style="font-size: 16px;">Common Pitfalls</span>

* <span style="font-size: 14px;">**Forgetting newaxis**: `A * s` fails or broadcasts incorrectly. Always reshape $s$ to $(m, 1)$ with `s[:, None]` or `s[:, np.newaxis]`.</span>
* <span style="font-size: 14px;">**axis confusion**: Row sums use `axis=1`; column sums use `axis=0`. Mixing these up scales the wrong direction.</span>
* <span style="font-size: 14px;">**Division by zero**: If any row sum is zero, division produces inf or nan. Check for zero denominators.</span>
* <span style="font-size: 14px;">**Integer truncation**: Scaling an integer array by a float weight may truncate. Cast to float first.</span>