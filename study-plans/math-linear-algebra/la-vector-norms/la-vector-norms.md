## <span style="font-size: 20px;">Vector Norms</span>

A **norm** assigns a non-negative "size" or "length" to every vector. Norms answer the question: *how big is this vector?* Different norms measure size differently, and the choice of norm has real consequences in machine learning - from which features survive regularization to how gradients are clipped during training.

### Formal Definition

A function $\|\cdot\|$ is a norm on $\mathbb{R}^n$ if it satisfies three axioms for all vectors $x, y$ and scalars $\alpha$:

1. **Non-negativity**: $\|x\| \geq 0$, with $\|x\| = 0$ if and only if $x = 0$
2. **Absolute homogeneity**: $\|\alpha x\| = |\alpha| \cdot \|x\|$ - scaling a vector scales its norm
3. **Triangle inequality**: $\|x + y\| \leq \|x\| + \|y\|$ - the norm of a sum is at most the sum of the norms

These axioms ensure that norms behave like a reasonable notion of "length."

---

### The L1 Norm (Manhattan Norm)

$$\|v\|_1 = \sum_{i=1}^{n} |v_i|$$

The L1 norm sums the absolute values of all components. It is called the **Manhattan distance** because it measures the distance you would travel on a grid of city blocks - only horizontal and vertical moves are allowed, no diagonal shortcuts.

**ML Application - Lasso Regularization**: Adding $\lambda \|w\|_1$ to a loss function (L1 penalty) drives many weights to exactly zero, producing **sparse** models. This performs automatic feature selection: irrelevant features get weight 0 and are effectively removed. The sparsity arises because the L1 unit ball has corners at the axes, and the loss contours are likely to intersect these corners.

---

### The L2 Norm (Euclidean Norm)

$$\|v\|_2 = \sqrt{\sum_{i=1}^{n} v_i^2}$$

The L2 norm is the straight-line length of the vector - the most intuitive notion of "size." It corresponds to the Euclidean distance from the origin to the point $v$ and is the default norm in most of linear algebra and machine learning.

**ML Application - Ridge Regularization**: Adding $\lambda \|w\|_2^2$ to a loss function (L2 penalty) shrinks all weights toward zero but rarely sets them exactly to zero. This reduces overfitting while keeping all features in the model. The L2 unit ball is a smooth hypersphere, so the loss contours generally intersect it at a point where all weights are small but non-zero.

---

### The L-infinity Norm (Max Norm)

$$\|v\|_\infty = \max_{i} |v_i|$$

The L-infinity norm picks out the single largest absolute component. Geometrically, the unit ball under $\|\cdot\|_\infty$ is a hypercube (a square in 2D, a cube in 3D) rather than a sphere.

This corresponds to **Chebyshev distance**: on a chessboard, the minimum number of moves a king needs to travel between two squares. It is useful when you care about the worst-case deviation across all dimensions.

---

### The General Lp Norm

All three norms above are special cases of the Lp norm:

$$\|v\|_p = \left(\sum_{i=1}^{n} |v_i|^p\right)^{1/p}, \quad p \geq 1$$

- $p = 1$: L1 norm (diamond-shaped unit ball)
- $p = 2$: L2 norm (circular unit ball)
- $p \to \infty$: L-infinity norm (square unit ball)

As $p$ increases, the norm pays more attention to the largest component and less to the smaller ones. The shape of the unit ball transitions from a diamond ($p = 1$) to a circle ($p = 2$) to a square ($p = \infty$).

---

### Unit Vectors and Normalization

A **unit vector** has norm equal to 1. To normalize any non-zero vector $v$:

$$\hat{v} = \frac{v}{\|v\|}$$

The result points in the same direction as $v$ but has unit length. Normalization is essential when you care about *direction* rather than *magnitude*. Cosine similarity, for example, is just the dot product of two L2-normalized vectors. In practice, normalizing feature vectors before feeding them to a model can improve training stability and convergence.

---

### ML Applications

**Gradient Clipping**: During training, if the gradient norm exceeds a threshold, rescale it: $g \leftarrow g \cdot \frac{\text{max\_norm}}{\|g\|_2}$. This prevents exploding gradients in RNNs and deep networks, keeping optimization stable without changing the gradient direction.

**Batch Normalization**: Normalizes activations within a mini-batch so they have zero mean and unit variance. This stabilizes training, allows higher learning rates, and acts as a mild regularizer. It operates on the statistics of activation norms across the batch.

**Weight Decay**: Equivalent to L2 regularization in standard SGD. Each step multiplies weights by a factor slightly less than 1, steadily shrinking them toward zero. This prevents any single weight from growing too large and dominating the model's predictions.

---

### Properties at a Glance

| Property | Holds for all Lp norms? |
|----------|------------------------|
| $\|v\| \geq 0$ | Yes |
| $\|v\| = 0 \Leftrightarrow v = 0$ | Yes |
| $\|\alpha v\| = |\alpha| \|v\|$ | Yes |
| $\|u + v\| \leq \|u\| + \|v\|$ | Yes |

These properties guarantee that Lp norms define valid distance metrics via $d(x, y) = \|x - y\|_p$. Any algorithm that requires a proper metric (ball trees, cover trees, metric-based clustering) can use Lp distances.