Neural network forward passes combine matrix multiplication, element-wise operations, and broadcasting. Understanding the mathematics behind each is essential for building and debugging models.

## Matrix Multiplication

For two matrices $A \in \mathbb{R}^{m \times k}$ and $B \in \mathbb{R}^{k \times n}$, their product $C = AB$ has shape $(m, n)$ where each element is the dot product of a row of $A$ with a column of $B$:

$$
C_{ij} = \sum_{l=1}^{k} A_{il} \cdot B_{lj}
$$

For example, with $A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$ and $B = \begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}$:

$$
C_{11} = 1 \cdot 5 + 2 \cdot 7 = 19
$$

$$
C_{12} = 1 \cdot 6 + 2 \cdot 8 = 22
$$

The inner dimensions must match: $A$ has $k$ columns and $B$ has $k$ rows. In PyTorch, several functions perform this operation.

## Element-wise Operations

Element-wise operations apply a function independently to each element. For a tensor $A \in \mathbb{R}^{m \times n}$, the element-wise square produces a new tensor of the same shape:

$$
(A^2)_{ij} = (A_{ij})^2
$$

For example:

$$
\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}^2 = \begin{bmatrix} 1 & 4 \\ 9 & 16 \end{bmatrix}
$$

Other common element-wise operations include addition, subtraction, multiplication, and division between same-shaped tensors. The key property is that no interaction occurs between elements at different positions.

## Broadcasting

Broadcasting allows operations between tensors of different shapes by automatically expanding the smaller tensor. PyTorch follows NumPy broadcasting rules:

* Dimensions are compared from the trailing (rightmost) side
* Two dimensions are compatible if they are equal, or one of them is 1
* A missing dimension (fewer total dims) is treated as size 1

When adding a 1D tensor $c \in \mathbb{R}^{n}$ to a 2D tensor $A \in \mathbb{R}^{m \times n}$, the vector $c$ is conceptually replicated across rows:

$$
(A + c)_{ij} = A_{ij} + c_j
$$

For example:

$$
\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix} + \begin{bmatrix} 10 & 20 \end{bmatrix} = \begin{bmatrix} 11 & 22 \\ 13 & 24 \end{bmatrix}
$$

No actual memory copy occurs: PyTorch uses stride tricks to virtually expand the tensor, making broadcasting both memory-efficient and fast.

## Why These Three Operations Matter

* A linear layer computes $y = Xw + b$: matrix multiplication for $Xw$, broadcasting for adding bias $b$
* Activation functions apply element-wise nonlinearities
* Loss functions often combine element-wise differences with reductions (sums, means)
