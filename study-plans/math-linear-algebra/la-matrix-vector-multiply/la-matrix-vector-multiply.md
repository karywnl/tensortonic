## <span style="font-size: 20px;">Matrix-Vector Multiplication</span>

Matrix-vector multiplication is one of the most fundamental operations in linear algebra and the backbone of nearly every neural network computation. Given a matrix $A$ of shape $(m, n)$ and a vector $x$ of shape $(n,)$, the product $Ax$ is a new vector of shape $(m,)$.

---

## Definition

The matrix-vector product $y = Ax$ is defined component-wise as:

$$y_i = \sum_{j=1}^{n} A_{ij} x_j \quad \text{for } i = 1, 2, \ldots, m$$

Each element of the output vector $y$ is the **dot product** of the corresponding row of $A$ with the vector $x$. This means computing $m$ separate dot products, one for each row. The computational cost is $O(mn)$ - we perform $m$ dot products, each involving $n$ multiply-add operations.

---

## Column Interpretation

An equivalent and often more insightful way to view $Ax$ is as a **linear combination of the columns** of $A$:

$$Ax = x_1 \mathbf{a}_1 + x_2 \mathbf{a}_2 + \cdots + x_n \mathbf{a}_n$$

where $\mathbf{a}_j$ denotes the $j$-th column of $A$. The entries of $x$ serve as scalar weights on the columns of $A$. This perspective is central to understanding the **column space** of a matrix: the set of all possible outputs $Ax$ (as $x$ ranges over all of $\mathbb{R}^n$) is exactly the span of the columns of $A$. If the columns are linearly independent, the column space has dimension $n$; otherwise it has dimension equal to the rank of $A$.

---

## Geometric Interpretation

Multiplying by a matrix $A$ applies a **linear transformation** to the vector $x$. This transformation can include:

- **Rotation:** changing the direction of $x$ without altering its magnitude
- **Scaling:** stretching or compressing $x$ along certain axes (eigenvalue directions)
- **Shearing:** skewing the space so that perpendicular axes become non-perpendicular
- **Projection:** collapsing dimensions when $m < n$ (the output lives in a lower-dimensional space)
- **Embedding:** expanding into higher dimensions when $m > n$ (the output lives in a higher-dimensional space)

The matrix $A$ encodes all of these geometric operations simultaneously. When $A$ is square and invertible, the transformation is reversible via $A^{-1}$. The eigenvalues of $A$ reveal the scaling factors, and the eigenvectors reveal the directions along which the scaling occurs.

---

## Shape Rules and Common Errors

For $Ax$ to be valid, the number of columns of $A$ must equal the length of $x$:

$$A \in \mathbb{R}^{m \times n}, \quad x \in \mathbb{R}^{n} \quad \Rightarrow \quad Ax \in \mathbb{R}^{m}$$

Common mistakes include:

- **Dimension mismatch:** Passing a vector of length $k \neq n$, which raises a shape error
- **Confusing $Ax$ with $xA$:** The latter requires $x$ to be a row vector of shape $(1, m)$, and produces a result of shape $(1, n)$
- **Output shape confusion:** The result has the number of rows of $A$ (not the length of $x$)
- **1-D vs 2-D vectors:** In NumPy, a 1-D array of shape $(n,)$ is treated differently from a 2-D column vector of shape $(n, 1)$

---

## Connection to Neural Networks

The core computation in a neural network layer is:

$$z = Wx + b$$

where $W$ is the weight matrix of shape $(\text{out\_features}, \text{in\_features})$, $x$ is the input feature vector of shape $(\text{in\_features},)$, and $b$ is the bias vector of shape $(\text{out\_features},)$. This is a matrix-vector multiplication followed by vector addition. The activation function is then applied element-wise: $a = \sigma(z)$.

In **linear regression**, the prediction for a single sample is $\hat{y} = w^T x + b$, which is a special case where $W$ is a single row vector (the weights form a $1 \times n$ matrix).

---

## Applications

- **Feature transformation:** Projecting data from one feature space to another (e.g., PCA, random projections)
- **Linear regression prediction:** Computing $X\beta$ for a design matrix $X$ and coefficient vector $\beta$
- **Coordinate transformations:** Rotating, scaling, or translating points in computer graphics and robotics
- **Graph operations:** Multiplying the adjacency matrix with a node feature vector to aggregate neighborhood information (the basis of graph neural networks)
- **Signal processing:** Applying discrete transforms (DFT, DCT) which can be expressed as matrix-vector products