## <span style="font-size: 20px;">Matrix Rank</span>

The rank of a matrix quantifies the amount of "independent information" it contains. It is one of the most important structural properties of a matrix, determining whether systems of equations have solutions and how much a linear transformation compresses its input space.

---

## Definition

The **rank** of a matrix $A$ is the maximum number of **linearly independent rows** (or equivalently, the maximum number of **linearly independent columns**). For a matrix $A \in \mathbb{R}^{m \times n}$:

$$\text{rank}(A) \leq \min(m, n)$$

A key theorem in linear algebra states that **row rank equals column rank** for any matrix. This is not obvious at first glance, but it is deeply important: no matter whether you count independent rows or independent columns, you get the same number. This common value is simply called the rank.

---

## Full Rank vs. Rank-Deficient

A matrix has **full rank** when $\text{rank}(A) = \min(m, n)$. This means it has as many independent rows or columns as possible given its dimensions.

A matrix is **rank-deficient** when $\text{rank}(A) < \min(m, n)$. This means some rows or columns can be written as linear combinations of others. Rank deficiency implies:

- For square matrices: the matrix is singular (non-invertible, $\det(A) = 0$)
- For overdetermined systems ($m > n$): the system $Ax = b$ may have no exact solution
- For underdetermined systems ($m < n$): the system $Ax = b$ has infinitely many solutions
- Geometrically: the linear transformation collapses at least one dimension of the input space

---

## Rank-Nullity Theorem

For a matrix $A \in \mathbb{R}^{m \times n}$:

$$\text{rank}(A) + \text{nullity}(A) = n$$

The **nullity** is the dimension of the null space (kernel) - the set of all vectors $x$ such that $Ax = 0$. This theorem says the number of "useful" dimensions (rank) plus the number of "wasted" dimensions (nullity) equals the total number of input dimensions. It is one of the most fundamental relationships in linear algebra.

---

## SVD Reveals Rank

The **Singular Value Decomposition** $A = U\Sigma V^T$ provides the cleanest and most numerically stable way to determine rank. The rank equals the **number of nonzero singular values** $\sigma_i$:

$$\text{rank}(A) = |\{i : \sigma_i > 0\}|$$

In practice, due to floating-point arithmetic, we count singular values above a small tolerance $\epsilon$ (typically $\epsilon = \max(m, n) \cdot \sigma_1 \cdot \varepsilon_{\text{machine}}$, where $\sigma_1$ is the largest singular value). This is exactly what `np.linalg.matrix_rank` does internally.

The singular values also tell you "how close" a matrix is to being rank-deficient. A very small singular value (relative to the largest) means the matrix is **ill-conditioned** - nearly rank-deficient - and numerical computations involving it may be unreliable.

---

## Checking System Solvability

The rank determines the solution structure of $Ax = b$:

- If $\text{rank}(A) = \text{rank}([A|b])$ and equals $n$: **unique solution**
- If $\text{rank}(A) = \text{rank}([A|b])$ but is less than $n$: **infinitely many solutions** (the solution space has dimension $n - \text{rank}(A)$)
- If $\text{rank}(A) < \text{rank}([A|b])$: **no solution** (the system is inconsistent)

Here $[A|b]$ denotes the augmented matrix with $b$ appended as an extra column. This is a direct application of the Rouche-Capelli theorem.

---

## Applications in Machine Learning

**Data Dimensionality:** The rank of a data matrix reveals the true dimensionality of the data. If a dataset $X \in \mathbb{R}^{n \times d}$ has $\text{rank}(X) = k < d$, the data actually lives in a $k$-dimensional subspace, and dimension reduction techniques can exploit this structure.

**Low-Rank Matrix Factorization:** Recommender systems approximate a sparse user-item rating matrix $R \approx UV^T$ where $U \in \mathbb{R}^{m \times k}$ and $V \in \mathbb{R}^{n \times k}$ with $k \ll \min(m, n)$. This assumes the full matrix has approximately low rank, meaning user preferences can be described by a small number of latent factors.

**PCA (Principal Component Analysis):** PCA selects the top-$k$ singular values and their corresponding singular vectors, effectively finding the best rank-$k$ approximation to the data matrix. The Eckart-Young theorem guarantees this is optimal in the Frobenius norm: no other rank-$k$ matrix is closer to $A$.

**Weight Matrix Compression:** In deep learning, LoRA (Low-Rank Adaptation) fine-tunes large language models by learning low-rank updates $\Delta W = BA$ where $B \in \mathbb{R}^{d \times r}$ and $A \in \mathbb{R}^{r \times d}$ with $r \ll d$. This drastically reduces the number of trainable parameters while preserving most of the model's expressivity.