## <span style="font-size: 20px;">The Hadamard Product (Element-wise Multiplication)</span>

The **Hadamard product** (also called the **Schur product**) is the element-wise multiplication of two matrices. Given two matrices $A$ and $B$ of the **same shape** $(m \times n)$, their Hadamard product $A \odot B$ is defined as:

$$(A \odot B)_{ij} = A_{ij} \cdot B_{ij}$$

Each element in the result is simply the product of the corresponding elements from $A$ and $B$. This operation is conceptually simpler than standard matrix multiplication, yet it plays an equally important role in modern machine learning architectures.

---

## Shape Requirement

Unlike matrix multiplication, the Hadamard product requires both operands to have **identical shapes**. If $A$ is $(m \times n)$, then $B$ must also be $(m \times n)$. This is a strict requirement - there is no "inner dimension" matching as in standard matrix multiplication.

**Contrast with matrix multiplication:** For the product $AB$ to be valid, $A$ must be $(m \times k)$ and $B$ must be $(k \times n)$ - only the inner dimensions must match, and the result has shape $(m \times n)$. For $A \odot B$, both dimensions must match exactly, and the result has the same shape as the inputs.

---

## Algebraic Properties

The Hadamard product satisfies several useful algebraic properties:

- **Commutative:** $A \odot B = B \odot A$
- **Associative:** $(A \odot B) \odot C = A \odot (B \odot C)$
- **Distributive over addition:** $A \odot (B + C) = A \odot B + A \odot C$
- **Identity element:** A matrix of all ones $J$ satisfies $A \odot J = A$
- **Zero element:** A matrix of all zeros $O$ satisfies $A \odot O = O$
- **Preserves symmetry:** If $A$ and $B$ are both symmetric, then $A \odot B$ is symmetric

Note that standard matrix multiplication is **not commutative** in general, while the Hadamard product always is. This makes reasoning about Hadamard products significantly simpler in many algebraic manipulations.

---

## Connection to the Schur Product

The Hadamard product is named after Jacques Hadamard, but it is also frequently called the **Schur product** after Issai Schur, who proved a fundamental theorem: if $A$ and $B$ are both **positive semidefinite**, then their Hadamard product $A \odot B$ is also positive semidefinite. This result (the Schur product theorem) has deep implications in kernel methods, covariance matrix operations, and quantum information theory. It guarantees that element-wise multiplication preserves the positive semidefinite structure that is essential in many optimization problems.

---

## NumPy Implementation

In NumPy, element-wise multiplication is the **default behavior** of the `*` operator on arrays:

$`C = A * B`$

This is in contrast to matrix multiplication, which requires `A @ B` or `np.dot(A, B)`. You can also use `np.multiply(A, B)` for explicit element-wise multiplication. When broadcasting rules apply, NumPy will automatically expand dimensions, but for a true Hadamard product, the shapes should match exactly.

---

## Applications in Machine Learning

The Hadamard product appears throughout modern ML architectures:

**Attention Mechanisms and Masking:** In transformers, attention masks are applied via element-wise multiplication. A binary mask $M$ is multiplied with the attention scores: $\text{scores} \odot M$, where $M_{ij} = 0$ blocks attention from position $i$ to position $j$. This is how causal (autoregressive) masking and padding masking are implemented.

**Feature Gating in LSTMs and GRUs:** Recurrent networks use sigmoid gates that produce values in $[0, 1]$, which are then Hadamard-multiplied with candidate values. For example, the LSTM update: $c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$, where $f_t$ and $i_t$ are forget and input gates respectively.

**Dropout Regularization:** Dropout creates a binary mask $M$ (each entry is 0 or 1 with probability $p$) and applies it as $h_{\text{dropped}} = h \odot M$. This randomly zeroes out activations during training to prevent co-adaptation of neurons.

**Gradient Computation:** When computing gradients of element-wise operations like $\text{ReLU}$ or $\text{sigmoid}$, the chain rule produces Hadamard products. If $y = f(x)$ element-wise, then $\frac{\partial L}{\partial x} = \frac{\partial L}{\partial y} \odot f'(x)$.

**Normalization Layers:** Batch normalization and layer normalization use element-wise multiplication by learned scale parameters: $y = \gamma \odot \hat{x} + \beta$, where $\gamma$ and $\beta$ are learnable vectors broadcast across the batch dimension.