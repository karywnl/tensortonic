## <span style="font-size: 20px;">Matrix Multiplication</span>

Matrix multiplication is the composition of linear transformations and one of the most important operations in all of mathematics and machine learning. Unlike element-wise multiplication, matrix multiplication combines rows of the first matrix with columns of the second in a structured way that encodes function composition.

---

## Definition

Given matrices $A$ of shape $(m, n)$ and $B$ of shape $(n, p)$, their product $C = AB$ has shape $(m, p)$ with entries:

$$(AB)_{ij} = \sum_{k=1}^{n} A_{ik} B_{kj}$$

Each entry $C_{ij}$ is the dot product of the $i$-th row of $A$ with the $j$-th column of $B$. The **inner dimensions must match**: if $A$ is $(m, n)$ then $B$ must have $n$ rows. Computing all $mp$ entries requires $mnp$ multiply-add operations.

---

## Shape Rules

$$\underset{(m \times n)}{A} \cdot \underset{(n \times p)}{B} = \underset{(m \times p)}{C}$$

The result takes the outer dimensions: $m$ rows from $A$ and $p$ columns from $B$. If the inner dimensions do not match, the multiplication is undefined. A helpful mnemonic: the shapes must form a chain where adjacent inner numbers match: $(m, \mathbf{n}) \times (\mathbf{n}, p) \to (m, p)$.

---

## Geometric Interpretation

Matrix multiplication represents the **composition of linear transformations**. If $A$ represents transformation $T_A$ and $B$ represents transformation $T_B$, then $AB$ represents applying $T_B$ first, then $T_A$:

$$(AB)x = A(Bx)$$

This is why the order matters: applying rotation then scaling is different from scaling then rotation. The composition interpretation also explains why matrix multiplication is associative but not commutative.

---

## Key Properties

- **Not commutative:** $AB \neq BA$ in general. Even when both products are defined (e.g., both are square), the results typically differ. This is perhaps the most important distinction from scalar multiplication.
- **Associative:** $(AB)C = A(BC)$. You can group multiplications however you like without changing the result. This allows optimization of computation order.
- **Distributive:** $A(B + C) = AB + AC$ and $(A + B)C = AC + BC$.
- **Transpose rule:** $(AB)^T = B^T A^T$. The transpose reverses the order of multiplication.
- **Identity:** $AI = IA = A$ where $I$ is the identity matrix of appropriate size.
- **Determinant rule:** $\det(AB) = \det(A) \det(B)$ for square matrices.
- **Rank:** $\text{rank}(AB) \leq \min(\text{rank}(A), \text{rank}(B))$.

---

## Computational Complexity

The naive algorithm for multiplying an $(m, n)$ matrix by an $(n, p)$ matrix requires $O(mnp)$ scalar multiplications. For two $n \times n$ matrices, this is $O(n^3)$.

Strassen's algorithm reduces this to approximately $O(n^{2.807})$ by cleverly reducing the number of recursive multiplications from 8 to 7. The best known theoretical bound is around $O(n^{2.373})$, though these sub-cubic algorithms have large constant factors and are rarely used in practice.

In practice, highly optimized BLAS libraries (like Intel MKL on CPUs and cuBLAS on GPUs) use blocking, cache-aware tiling, and SIMD vectorization strategies to achieve near-peak hardware throughput for the standard $O(n^3)$ algorithm.

---

## Applications in Deep Learning

**Layer computation:** Every fully connected layer computes $Y = XW + B$ where $X$ is the batch of inputs with shape $(\text{batch}, \text{in\_features})$ and $W$ has shape $(\text{in\_features}, \text{out\_features})$. A single forward pass through a deep network chains together many such matrix multiplications.

**Batch matrix multiply:** When processing batches of sequences (e.g., in transformers), we often need $C_b = A_b B_b$ for each batch element $b$. PyTorch provides `torch.bmm` and `torch.matmul` for this. The attention mechanism computes $\text{softmax}(QK^T / \sqrt{d_k})V$, which involves two batch matrix multiplications.

**Backpropagation:** Gradients flow backward through matrix multiplications. If the forward pass computes $Y = XW$, then the gradient with respect to $W$ is $X^T \frac{\partial L}{\partial Y}$ and with respect to $X$ is $\frac{\partial L}{\partial Y} W^T$. This symmetry is a direct consequence of the chain rule applied to matrix operations.

**Convolutional layers** can be reformulated as matrix multiplications using the im2col trick, which reshapes input patches into rows of a matrix. This allows convolutions to leverage fast GEMM (General Matrix Multiply) routines, which is why GPU-accelerated convolutions are so efficient.