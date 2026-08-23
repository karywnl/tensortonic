## <span style="font-size: 20px;">Matrix Determinant</span>

The determinant is a scalar value that encodes fundamental properties of a square matrix. It tells you whether the matrix is invertible, how it scales areas and volumes, and connects to eigenvalues and systems of equations.

---

## Definition for Small Matrices

For a $2 \times 2$ matrix:

$$\det\begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc$$

For a $3 \times 3$ matrix, expansion along the first row gives:

$$\det(A) = a_{11}(a_{22}a_{33} - a_{23}a_{32}) - a_{12}(a_{21}a_{33} - a_{23}a_{31}) + a_{13}(a_{21}a_{32} - a_{22}a_{31})$$

These formulas can be memorized, but more importantly they illustrate the recursive pattern that generalizes to any size.

---

## General Definition via Cofactor Expansion

For an $n \times n$ matrix, the determinant is computed by **cofactor expansion** along any row or column. Expanding along row $i$:

$$\det(A) = \sum_{j=1}^{n} (-1)^{i+j} a_{ij} M_{ij}$$

where $M_{ij}$ is the **minor** - the determinant of the $(n-1) \times (n-1)$ submatrix obtained by deleting row $i$ and column $j$. The factor $(-1)^{i+j} M_{ij}$ is called the **cofactor**. You may expand along any row or column and get the same result; choosing a row or column with many zeros reduces computation.

In practice, numerical algorithms use **LU decomposition** rather than cofactor expansion, reducing complexity from $O(n!)$ to $O(n^3)$. The determinant is then the product of the diagonal entries of the upper triangular factor $U$, with a sign adjustment for row swaps.

---

## Geometric Interpretation

The determinant measures the **signed volume scaling factor** of the linear transformation represented by the matrix:

- $|\det(A)| > 1$: the transformation expands volumes
- $|\det(A)| < 1$: the transformation shrinks volumes
- $|\det(A)| = 1$: the transformation preserves volumes (e.g., rotations)
- $\det(A) < 0$: the transformation reverses orientation (like a reflection)
- $\det(A) = 0$: the transformation collapses space to a lower dimension

For a $2 \times 2$ matrix, $|\det(A)|$ gives the area of the parallelogram formed by the column vectors. For a $3 \times 3$ matrix, it gives the volume of the parallelepiped spanned by the three column vectors.

---

## Key Properties

- **Multiplicative:** $\det(AB) = \det(A)\det(B)$
- **Transpose invariance:** $\det(A^T) = \det(A)$
- **Row swap:** Swapping two rows flips the sign of the determinant
- **Row scaling:** Multiplying a single row by scalar $c$ multiplies the determinant by $c$
- **Scalar multiplication:** $\det(cA) = c^n \det(A)$ for an $n \times n$ matrix
- **Inverse:** $\det(A^{-1}) = 1/\det(A)$ when $A$ is invertible
- **Triangular matrices:** The determinant equals the product of the diagonal entries
- **Block diagonal:** $\det\begin{pmatrix} A & 0 \\ 0 & B \end{pmatrix} = \det(A)\det(B)$

---

## Singular Matrices

A matrix with $\det(A) = 0$ is called **singular** (non-invertible). This means:

- The columns (or rows) are linearly dependent
- The system $Ax = b$ either has no solution or infinitely many solutions
- The matrix maps some nonzero vector to the zero vector (has a nontrivial null space)
- The matrix has at least one zero eigenvalue
- The matrix has rank less than $n$

Detecting singularity is one of the most common uses of the determinant in practice, though checking the condition number is often more numerically reliable.

---

## Connection to Eigenvalues

The determinant equals the **product of all eigenvalues**:

$$\det(A) = \prod_{i=1}^{n} \lambda_i$$

Similarly, the trace equals the sum of eigenvalues: $\text{tr}(A) = \sum_i \lambda_i$. Together, the trace and determinant provide quick spectral information about a matrix. The characteristic polynomial $\det(A - \lambda I) = 0$ is the equation whose roots are the eigenvalues.

---

## Cramer's Rule

For a system $Ax = b$ where $A$ is $n \times n$ with $\det(A) \neq 0$, each component of the solution is:

$$x_i = \frac{\det(A_i)}{\det(A)}$$

where $A_i$ is the matrix $A$ with its $i$-th column replaced by $b$. While theoretically elegant, this method requires computing $n + 1$ determinants and is computationally impractical for large systems compared to Gaussian elimination.

---

## Applications in Machine Learning

**Multivariate Gaussian distribution:** The probability density function is:

$$p(x) = \frac{1}{(2\pi)^{n/2} |\Sigma|^{1/2}} \exp\left(-\frac{1}{2}(x-\mu)^T \Sigma^{-1} (x-\mu)\right)$$

The determinant $|\Sigma|$ of the covariance matrix appears in the normalization constant. Taking the log gives $-\frac{1}{2}\log|\Sigma|$, which is needed for log-likelihood computations in Gaussian mixture models, variational autoencoders, and normalizing flows. In normalizing flows specifically, computing $\log|\det(J)|$ of the Jacobian is a core operation for density estimation.