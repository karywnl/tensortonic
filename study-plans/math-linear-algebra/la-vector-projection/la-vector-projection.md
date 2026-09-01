## <span style="font-size: 20px;">Vector Projection</span>

Projection is one of the most fundamental operations in linear algebra. It lets you decompose a vector into components along and perpendicular to a given direction - essentially answering the question: "How much of $v$ lies in the direction of $u$?"

---

## Scalar and Vector Projection

Given two vectors $v$ and $u$, the **scalar projection** (also called the component) of $v$ onto $u$ is:

$$
\text{comp}_u v = \frac{v \cdot u}{\|u\|}
$$

This gives a signed scalar: positive if $v$ has a component in the same direction as $u$, negative if opposite. Its magnitude equals the length of the "shadow" of $v$ along $u$.

The **vector projection** of $v$ onto $u$ is:

$$
\text{proj}_u v = \frac{v \cdot u}{u \cdot u} u
$$

This is a vector that lies along $u$ and represents the shadow of $v$ cast onto the line defined by $u$. Note the denominator is $u \cdot u = \|u\|^2$, not just $\|u\|$.

---

## Geometric Interpretation

Imagine a light shining perpendicular to the direction of $u$. The shadow of $v$ on the line through $u$ is exactly $\text{proj}_u v$. The remaining piece, $v - \text{proj}_u v$, is perpendicular to $u$. This gives the **orthogonal decomposition**:

$$
v = \text{proj}_u v + (v - \text{proj}_u v)
$$

where the two components are orthogonal. You can verify: $(v - \text{proj}_u v) \cdot u = 0$. This decomposition is unique and fundamental - every vector can be split into a component along any direction and a component perpendicular to it.

---

## Projection Matrix

For a column vector $u$, the projection onto the line spanned by $u$ can be written as a matrix operation:

$$
P = \frac{u u^T}{u^T u}
$$

Then $\text{proj}_u v = Pv$. This matrix $P$ has key properties:

- **Idempotent**: $P^2 = P$ (projecting twice gives the same result)
- **Symmetric**: $P^T = P$ (the projection is self-adjoint)
- **Rank 1**: it maps everything onto a one-dimensional subspace
- **Eigenvalues**: only 0 and 1 (eigenvectors along $u$ get eigenvalue 1, perpendicular ones get 0)

More generally, the projection onto the column space of a matrix $A$ (with linearly independent columns) is:

$$
P = A(A^T A)^{-1} A^T
$$

This generalizes from projecting onto a line to projecting onto a multi-dimensional subspace. The same properties hold: $P^2 = P$ and $P^T = P$.

---

## Orthogonal Complement

The vector $v - \text{proj}_u v$ is called the **rejection** of $v$ from $u$, or the component in the orthogonal complement. This is useful for:

- Removing unwanted components from a signal or dataset
- The Gram-Schmidt process (repeatedly projecting and subtracting to build orthogonal bases)
- Constructing orthonormal coordinate systems
- Deflation methods in eigenvalue computation

The rejection matrix is $I - P$, and it is itself a projection matrix: $(I - P)^2 = I - P$ and $(I - P)^T = I - P$. It projects onto the orthogonal complement of the column space of $A$.

---

## Connection to Least Squares

When you solve the least-squares problem $\min_x \|Ax - b\|^2$, the solution gives $\hat{b} = A\hat{x}$ which is exactly the projection of $b$ onto the column space of $A$:

$$
\hat{b} = A(A^T A)^{-1} A^T b = Pb
$$

The residual $b - \hat{b}$ is orthogonal to every column of $A$, which yields the normal equation $A^T(b - A\hat{x}) = 0$. This geometric view makes least squares intuitive: you find the closest point in the column space to $b$, and "closest" means the perpendicular distance is minimized.

---

## Projection in Higher Dimensions

When projecting onto a $k$-dimensional subspace spanned by orthonormal vectors $\{q_1, q_2, \ldots, q_k\}$, the projection simplifies to:

$$
\text{proj} \, v = \sum_{i=1}^{k} (v \cdot q_i) q_i = QQ^T v
$$

where $Q = [q_1 | q_2 | \cdots | q_k]$. When the basis vectors are orthonormal, no matrix inversion is needed - this is one reason orthogonal bases are so valuable.

---

## Applications in ML and Data Science

- **Feature decomposition**: Splitting data into components along meaningful directions
- **Removing confounders**: Project out unwanted variation (e.g., batch effects in genomics)
- **Gram-Schmidt process**: Iteratively projects and subtracts to build orthogonal bases
- **PCA interpretation**: Principal components define projection directions that capture maximum variance
- **Regression geometry**: The fitted values $\hat{y}$ are the projection of $y$ onto the column space of the design matrix
- **Word embeddings**: Removing bias directions from word vectors uses orthogonal projection

---

## NumPy Implementation

For vector projection:
```python
proj = (np.dot(v, u) / np.dot(u, u)) * u
rejection = v - proj  # orthogonal component
```

For the projection matrix onto column space of $A$:
```python
P = A @ np.linalg.inv(A.T @ A) @ A.T
projected = P @ v
```