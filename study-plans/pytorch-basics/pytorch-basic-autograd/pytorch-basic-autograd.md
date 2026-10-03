Autograd records operations on tensors with requires_grad=True and computes gradients via the chain rule. Here we use the same computation as in the problem: $y = \sum_i (x_i^3 + 2x_i)$.

## Partial derivatives for $y = \sum_i (x_i^3 + 2x_i)$

Each term in the sum depends on only one $x_i$, so the gradient is element-wise. For the $i$-th component:

$$
\frac{\partial y}{\partial x_i} = \frac{\partial}{\partial x_i}\bigl( x_i^3 + 2x_i \bigr) = 3x_i^2 + 2.
$$

So $\frac{\partial y}{\partial x}$ is a tensor of the same shape as $x$, with $i$-th entry $3x_i^2 + 2$. PyTorch autograd will compute exactly these values and store them in x.grad.

## How autograd does it: computational graph and chain rule

The forward pass builds a graph:

* From $x$, compute element-wise $u = x^3$ and $v = 2x$, then $z = u + v = x^3 + 2x$, then $y = \sum_i z_i$ (a scalar).

When you call y.backward(), PyTorch walks backward through this graph. At each node it applies the chain rule:

* At the sum: $y = \sum_i z_i$ gives $\frac{\partial y}{\partial z_i} = 1$ for each $i$.
* At the addition $z = u + v$: $\frac{\partial y}{\partial u_i} = \frac{\partial y}{\partial z_i} \cdot 1 = 1$ and similarly $\frac{\partial y}{\partial v_i} = 1$.
* At $u_i = x_i^3$: the chain rule adds $\frac{\partial y}{\partial u_i} \cdot \frac{\partial u_i}{\partial x_i} = 1 \cdot 3x_i^2 = 3x_i^2$ to $\frac{\partial y}{\partial x_i}$.
* At $v_i = 2x_i$: it adds $\frac{\partial y}{\partial v_i} \cdot \frac{\partial v_i}{\partial x_i} = 1 \cdot 2 = 2$ to $\frac{\partial y}{\partial x_i}$.

So the gradient at $x$ is $\frac{\partial y}{\partial x_i} = 3x_i^2 + 2$, which is written into x.grad. That is exactly the analytical partial derivative we derived above.

## What you do in code

* Enable gradient tracking on the supplied tensor so the graph is recorded
* Compute $y = (x^3 + 2x).\texttt{sum()}$ (a scalar)
* Call y.backward() to backpropagate; then x.grad holds $\frac{\partial y}{\partial x}$, a tensor of $3x_i^2 + 2$ values
