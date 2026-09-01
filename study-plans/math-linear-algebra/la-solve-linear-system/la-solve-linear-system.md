## <span style="font-size: 20px;">Solving Linear Systems</span>

A linear system $Ax = b$ is the central problem in computational linear algebra. Nearly every numerical method - from regression to neural network training - reduces to solving linear systems at some level.

---

## Problem Setup

Given an $m \times n$ matrix $A$ and a vector $b \in \mathbb{R}^m$, find $x \in \mathbb{R}^n$ such that:

$$
Ax = b
$$

This represents $m$ equations in $n$ unknowns. Each row of $A$ defines one linear equation, and the entries of $x$ are the unknowns. The solvability depends on the relationship between $m$, $n$, and the rank of $A$.

---

## Existence and Uniqueness

The **rank** of $A$ determines everything:

- **Consistent system**: $b$ is in the column space of $A$, i.e., $\text{rank}(A) = \text{rank}([A|b])$
- **Unique solution**: System is consistent AND $\text{rank}(A) = n$ (full column rank)
- **No solution**: $\text{rank}(A) < \text{rank}([A|b])$ - $b$ has a component outside the column space
- **Infinitely many solutions**: System is consistent but $\text{rank}(A) < n$ - the null space is nontrivial

The **Rouche-Capelli theorem** formalizes this: a system is consistent if and only if $\text{rank}(A) = \text{rank}([A|b])$.

---

## Cases by Shape

**Square system** ($m = n$): If $\det(A) \neq 0$ (equivalently, $A$ has full rank), there is exactly one solution $x = A^{-1}b$. Never explicitly compute $A^{-1}$ in practice - use factorization instead, as it is both faster and more numerically stable.

**Overdetermined** ($m > n$): More equations than unknowns. Generically no exact solution exists. The least-squares solution minimizes $\|Ax - b\|^2$:

$$
\hat{x} = (A^T A)^{-1} A^T b
$$

This is equivalent to projecting $b$ onto the column space of $A$.

**Underdetermined** ($m < n$): Fewer equations than unknowns. Infinitely many solutions exist (if any). The minimum-norm solution is $x = A^T(AA^T)^{-1}b$, which can also be found via the pseudoinverse $x = A^+b$.

---

## Solution Methods

**Gaussian Elimination**: Row-reduce $[A|b]$ to echelon form, then back-substitute. Equivalent to LU decomposition. Cost: $O(n^3)$ for the reduction.

**LU Decomposition**: Factor $A = LU$ (or $PA = LU$ with pivoting), then solve $Ly = Pb$ (forward substitution) and $Ux = y$ (backward substitution). Preferred when solving for multiple right-hand sides with the same $A$.

**QR Decomposition**: Factor $A = QR$, then $x = R^{-1}Q^Tb$. More numerically stable than LU for least-squares problems. This is what NumPy uses internally.

**Cholesky**: If $A$ is symmetric positive definite, factor $A = LL^T$. About twice as fast as general LU and guaranteed to exist without pivoting.

---

## Iterative Methods

For large sparse systems where direct methods are too expensive (both in time and memory), iterative approaches include:

- **Jacobi and Gauss-Seidel**: Simple splitting methods, easy to implement but slow convergence
- **Conjugate Gradient (CG)**: For symmetric positive definite systems, converges in at most $n$ steps (fewer with preconditioning)
- **GMRES**: For general non-singular systems, builds a Krylov subspace to find approximate solutions
- **BiCGSTAB**: For non-symmetric systems, often more stable than plain BiCG

These are essential for large-scale ML problems where $A$ may have millions of rows and direct factorization is impractical.

---

## Condition Number

The **condition number** $\kappa(A) = \|A\| \cdot \|A^{-1}\|$ measures sensitivity to perturbations in $b$ or $A$. A large condition number means small changes in $b$ cause large changes in $x$. Rule of thumb: you lose about $\log_{10}(\kappa)$ digits of accuracy. For example, if $\kappa = 10^8$ and you use double precision (about 16 digits), you can trust only about 8 digits of your solution.

---

## NumPy Functions

```python
# Square system (exact)
x = np.linalg.solve(A, b)

# General system (least-squares)
x, residuals, rank, sv = np.linalg.lstsq(A, b, rcond=None)

# Check condition number
kappa = np.linalg.cond(A)
```

---

## Applications

- **Linear regression**: $X\beta = y$ (overdetermined, solved via least squares)
- **Circuit analysis**: Kirchhoff's laws give linear systems for node voltages and branch currents
- **Polynomial interpolation**: Finding coefficients through data points yields a Vandermonde system
- **Finite differences**: Discretizing PDEs produces large sparse linear systems
- **Neural networks**: Each linear layer computes $Wx + b$; weight updates involve solving linear systems in second-order optimizers