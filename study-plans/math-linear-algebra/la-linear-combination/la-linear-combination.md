## <span style="font-size: 20px;">Linear Combinations</span>

A **linear combination** takes a set of vectors, scales each by a scalar coefficient, and sums the results. It is arguably the single most important operation in linear algebra - matrix multiplication, change of basis, projections, and neural network layers are all linear combinations in disguise.

### Definition

Given vectors $v_1, v_2, \ldots, v_k \in \mathbb{R}^n$ and scalars $\alpha_1, \alpha_2, \ldots, \alpha_k \in \mathbb{R}$, their linear combination is:

$$w = \sum_{i=1}^{k} \alpha_i v_i = \alpha_1 v_1 + \alpha_2 v_2 + \cdots + \alpha_k v_k$$

Each scalar $\alpha_i$ (called a **coefficient** or **weight**) controls how much of vector $v_i$ to include in the result. A positive coefficient includes the vector as-is; a negative coefficient includes it in the opposite direction; zero excludes it entirely.

---

### Span of Vectors

The **span** of a set of vectors is the set of all possible linear combinations:

$$\text{span}(v_1, \ldots, v_k) = \left\{ \sum_{i=1}^{k} \alpha_i v_i \;\middle|\; \alpha_i \in \mathbb{R} \right\}$$

The span is always a **subspace** (it contains the zero vector and is closed under addition and scalar multiplication). Examples:
- One non-zero vector spans a line through the origin
- Two non-parallel vectors in $\mathbb{R}^3$ span a plane through the origin
- Three linearly independent vectors in $\mathbb{R}^3$ span all of $\mathbb{R}^3$

---

### Linear Independence

Vectors $v_1, \ldots, v_k$ are **linearly independent** if no vector can be written as a linear combination of the others. Formally, the only solution to:

$$\alpha_1 v_1 + \alpha_2 v_2 + \cdots + \alpha_k v_k = 0$$

is $\alpha_1 = \alpha_2 = \cdots = \alpha_k = 0$ (the trivial solution).

If the vectors are linearly dependent, at least one is redundant - it lies in the span of the others and can be removed without shrinking the span. In ML terms, linearly dependent features carry redundant information.

---

### Basis

A **basis** for a vector space $V$ is a set of linearly independent vectors that spans $V$. Key facts:
- Every basis for $\mathbb{R}^n$ has exactly $n$ vectors (this number is the **dimension**)
- Any vector in $V$ can be written as a *unique* linear combination of basis vectors
- The standard basis for $\mathbb{R}^3$ is $\{e_1, e_2, e_3\}$ where $e_i$ has a 1 in position $i$ and 0 elsewhere
- Different bases represent the same space from different "viewpoints" - PCA finds the basis that aligns with directions of maximum variance

---

### Connection to Matrix-Vector Multiplication

Matrix-vector multiplication $Ax$ is a linear combination of the columns of $A$:

$$Ax = x_1 a_1 + x_2 a_2 + \cdots + x_n a_n$$

where $a_j$ is the $j$-th column of $A$ and $x_j$ is the $j$-th entry of $x$. This **column-centric view** is one of the most important perspectives in linear algebra. It reveals that multiplying a matrix by a vector simply blends the columns of the matrix, with the vector entries serving as the blending weights.

This means that the range (column space) of $A$ is exactly the span of its columns - the set of all possible outputs $Ax$.

---

### Geometric Interpretation

Scaling a vector stretches or shrinks it along its direction (and flips it if the scalar is negative). Adding two scaled vectors follows the **parallelogram law**: place them tail-to-tail, and the sum is the diagonal of the parallelogram they form.

A linear combination $\alpha v_1 + \beta v_2$ traces out a plane as $\alpha$ and $\beta$ range over all reals (assuming $v_1$ and $v_2$ are not parallel). Every point in this plane is reachable by choosing the right coefficients. Adding a third independent vector opens up all of 3D space.

---

### Applications in Machine Learning

**Feature Representation**: A data point can be viewed as a linear combination of basis features. In PCA, data is re-expressed as a linear combination of principal components: $x \approx \sum_{i=1}^{k} \alpha_i p_i$, keeping only the $k$ most informative directions. The coefficients $\alpha_i$ become the new, lower-dimensional representation.

**Neural Network Layers**: A fully connected layer computes $z = Wx + b$, where $Wx$ is a linear combination of input features weighted by learned parameters. Each output neuron computes its own linear combination with different weights. The bias $b$ shifts the result. Stacking these layers with nonlinear activations builds powerful function approximators.

**Word Embeddings**: The classic example $\text{king} - \text{man} + \text{woman} \approx \text{queen}$ is a linear combination of embedding vectors with coefficients $+1, -1, +1$. This works because well-trained embedding spaces encode semantic relationships as approximately linear directions: the "royalty" direction and the "gender" direction are separable.

**Ensemble Methods**: A weighted ensemble prediction $\hat{y} = \sum_i \alpha_i f_i(x)$ is a linear combination of base model outputs. Methods like stacking and blending learn the optimal coefficients $\alpha_i$ to combine diverse models.