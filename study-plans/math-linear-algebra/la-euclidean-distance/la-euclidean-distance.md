## <span style="font-size: 20px;">Euclidean Distance</span>

The **Euclidean distance** between two vectors measures the straight-line distance between them in space - the length of the shortest path connecting two points. It is the most natural and widely used distance metric in machine learning.

### Definition

For vectors $x = (x_1, x_2, \ldots, x_n)$ and $y = (y_1, y_2, \ldots, y_n)$ in $\mathbb{R}^n$:

$$d(x, y) = \|x - y\|_2 = \sqrt{\sum_{i=1}^{n}(x_i - y_i)^2}$$

In 2D this reduces to the familiar formula $\sqrt{(x_1 - y_1)^2 + (x_2 - y_2)^2}$. In 3D, you simply add the third squared difference under the radical.

---

### Connection to the Pythagorean Theorem

Euclidean distance is a direct generalization of the Pythagorean theorem. In 2D, the distance between two points equals the hypotenuse of a right triangle whose legs are the differences along each axis. In $n$ dimensions, we extend this idea: square the difference along each axis, sum them, and take the square root. The theorem $c^2 = a^2 + b^2$ becomes $d^2 = \sum_i (x_i - y_i)^2$ with arbitrarily many "legs."

---

### Key Properties

1. **Non-negativity**: $d(x, y) \geq 0$, and $d(x, y) = 0$ if and only if $x = y$. Two distinct points always have positive distance.

2. **Symmetry**: $d(x, y) = d(y, x)$ - distance does not depend on which point you start from.

3. **Triangle inequality**: $d(x, z) \leq d(x, y) + d(y, z)$ - the direct path is never longer than a detour through a third point.

These three properties make Euclidean distance a proper **metric**, which means it can be used in any algorithm that requires a valid distance function (metric trees, cover trees, ball trees, etc.).

---

### Connection to the Dot Product

Euclidean distance can be expressed via dot products:

$$d(x, y)^2 = (x - y) \cdot (x - y) = \|x\|^2 - 2\,x \cdot y + \|y\|^2$$

This identity is powerful in practice. When vectors are pre-normalized ($\|x\| = \|y\| = 1$), the squared distance simplifies to $2(1 - x \cdot y)$. This means computing distances reduces to computing dot products, which can be heavily optimized with BLAS libraries, GPU matrix multiplications, or approximate nearest-neighbor indices.

---

### Comparison with Other Distance Metrics

| Metric | Formula | Geometry |
|--------|---------|----------|
| Euclidean (L2) | $\sqrt{\sum (x_i - y_i)^2}$ | Straight line |
| Manhattan (L1) | $\sum \lvert x_i - y_i \rvert$ | Grid/city-block path |
| Chebyshev (L-inf) | $\max_i \lvert x_i - y_i \rvert$ | Maximum single-axis gap |
| Cosine distance | $1 - \cos\theta$ | Angular separation |

Euclidean distance is sensitive to magnitude, while cosine distance only cares about direction. Manhattan distance is more robust to outliers in individual dimensions. The right choice depends on your problem structure and data characteristics.

---

### Applications in Machine Learning

**k-Nearest Neighbors (kNN)**: Classifies a point by the majority class among its $k$ closest neighbors, measured by Euclidean distance. The algorithm assumes that nearby points in feature space share the same label.

**k-Means Clustering**: Assigns each point to the cluster whose centroid is nearest in Euclidean distance, then re-computes centroids iteratively. The objective function minimizes total within-cluster squared Euclidean distance.

**Embedding Similarity**: In representation learning, similar items (words, images, users) are mapped to nearby points in embedding space. Euclidean distance quantifies this "nearness" and is used for retrieval, recommendation, and anomaly detection.

**Loss Functions**: Mean Squared Error (MSE) is proportional to squared Euclidean distance between predicted and actual values. Minimizing MSE is equivalent to finding the closest point in Euclidean space.

---

### The Curse of Dimensionality

In high-dimensional spaces, Euclidean distance loses discriminative power. As dimensionality $n$ grows, the ratio of the farthest distance to the nearest distance among random points converges to 1:

$$\frac{d_{\max} - d_{\min}}{d_{\min}} \to 0 \quad \text{as } n \to \infty$$

This means all pairwise distances become nearly equal, making nearest-neighbor queries less meaningful. Techniques like dimensionality reduction (PCA, t-SNE, UMAP) or using alternative metrics (cosine similarity) can help restore discriminative power.

---

### Feature Scaling Matters

Euclidean distance treats all dimensions equally. If one feature ranges from 0 to 1000 while another ranges from 0 to 1, the large-scale feature dominates the distance calculation entirely. Always **standardize or normalize** features before computing Euclidean distances in ML pipelines. Common approaches include min-max scaling to $[0, 1]$ or z-score standardization to zero mean and unit variance.