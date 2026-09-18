<span style="font-size: 14px;">Neural network forward passes combine matrix multiplication, element-wise operations, and broadcasting. Understanding the mathematics behind each is essential for building and debugging models.</span>

## <span style="font-size: 14px;">Matrix Multiplication</span>

<span style="font-size: 14px;">For two matrices</span> $A \in \mathbb{R}^{m \times k}$ <span style="font-size: 14px;">and</span> $B \in \mathbb{R}^{k \times n}$<span style="font-size: 14px;">, their product</span> $C = AB$ <span style="font-size: 14px;">has shape</span> $(m, n)$ <span style="font-size: 14px;">where each element is the dot product of a row of</span> $A$ <span style="font-size: 14px;">with a column of</span> $B$<span style="font-size: 14px;">:</span>

$$
C_{ij} = \sum_{l=1}^{k} A_{il} \cdot B_{lj}
$$

<span style="font-size: 14px;">For example, with</span> $A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$ <span style="font-size: 14px;">and</span> $B = \begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}$<span style="font-size: 14px;">:</span>

$$
C_{11} = 1 \cdot 5 + 2 \cdot 7 = 19, \quad C_{12} = 1 \cdot 6 + 2 \cdot 8 = 22
$$

<span style="font-size: 14px;">The inner dimensions must match:</span> $A$ <span style="font-size: 14px;">has</span> $k$ <span style="font-size: 14px;">columns and</span> $B$ <span style="font-size: 14px;">has</span> $k$ <span style="font-size: 14px;">rows. In PyTorch, several functions perform this operation.</span>

## <span style="font-size: 14px;">Element-wise Operations</span>

<span style="font-size: 14px;">Element-wise operations apply a function independently to each element. For a tensor</span> $A \in \mathbb{R}^{m \times n}$<span style="font-size: 14px;">, the element-wise square produces a new tensor of the same shape:</span>

$$
(A^2)_{ij} = (A_{ij})^2
$$

<span style="font-size: 14px;">For example:</span>

$$
\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}^2 = \begin{bmatrix} 1 & 4 \\ 9 & 16 \end{bmatrix}
$$

<span style="font-size: 14px;">Other common element-wise operations include addition, subtraction, multiplication, and division between same-shaped tensors. The key property is that no interaction occurs between elements at different positions.</span>

## <span style="font-size: 14px;">Broadcasting</span>

<span style="font-size: 14px;">Broadcasting allows operations between tensors of different shapes by automatically expanding the smaller tensor. PyTorch follows NumPy broadcasting rules:</span>

* <span style="font-size: 14px;">Dimensions are compared from the trailing (rightmost) side</span>
* <span style="font-size: 14px;">Two dimensions are compatible if they are equal, or one of them is 1</span>
* <span style="font-size: 14px;">A missing dimension (fewer total dims) is treated as size 1</span>

<span style="font-size: 14px;">When adding a 1D tensor</span> $c \in \mathbb{R}^{n}$ <span style="font-size: 14px;">to a 2D tensor</span> $A \in \mathbb{R}^{m \times n}$<span style="font-size: 14px;">, the vector</span> $c$ <span style="font-size: 14px;">is conceptually replicated across rows:</span>

$$
(A + c)_{ij} = A_{ij} + c_j
$$

<span style="font-size: 14px;">For example:</span>

$$
\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix} + \begin{bmatrix} 10 & 20 \end{bmatrix} = \begin{bmatrix} 11 & 22 \\ 13 & 24 \end{bmatrix}
$$

<span style="font-size: 14px;">No actual memory copy occurs: PyTorch uses stride tricks to virtually expand the tensor, making broadcasting both memory-efficient and fast.</span>

## <span style="font-size: 14px;">Why These Three Operations Matter</span>

* <span style="font-size: 14px;">A linear layer computes</span> $y = Xw + b$<span style="font-size: 14px;">: matrix multiplication for</span> $Xw$<span style="font-size: 14px;">, broadcasting for adding bias</span> $b$
* <span style="font-size: 14px;">Activation functions apply element-wise nonlinearities</span>
* <span style="font-size: 14px;">Loss functions often combine element-wise differences with reductions (sums, means)</span>
