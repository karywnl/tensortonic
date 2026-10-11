## The Role of Activation Functions

Activation functions are the nonlinear components that give neural networks their expressive power. Without them, a network of any depth would collapse into a single linear transformation: composing $f_1(x) = W_1 x + b_1$ and $f_2(x) = W_2 x + b_2$ yields $f_2(f_1(x)) = W_2 W_1 x + W_2 b_1 + b_2$, which is still a linear function. The activation function, applied element-wise after each linear transformation, introduces the nonlinearity that allows the network to approximate arbitrary continuous functions (by the universal approximation theorem).

Formally, a layer in a neural network computes:

$$
\mathbf{h} = \sigma(W\mathbf{x} + \mathbf{b})
$$

where $W$ is the weight matrix, $\mathbf{b}$ is the bias vector, and $\sigma$ is the activation function applied element-wise. The choice of $\sigma$ affects training dynamics, gradient flow, output range, and computational cost.

## ReLU: The Default Choice

The Rectified Linear Unit is the most widely used activation in modern deep learning:

$$
\text{ReLU}(x) = \max(0, x) = \begin{cases} x & \text{if } x > 0 \\ 0 & \text{if } x \le 0 \end{cases}
$$

**Advantages:**
- Computationally cheap: a single comparison and a conditional assignment
- Sparse activation: neurons with negative pre-activation output exactly 0, which provides a form of implicit regularization and computational efficiency
- Non-saturating for positive values: the gradient is exactly 1 for $x > 0$, so gradients do not diminish as they propagate backward through many layers (unlike sigmoid/tanh)

**The dying ReLU problem:** For $x \le 0$, the gradient is exactly 0. If a neuron's weights drift such that it always receives negative inputs (e.g., after a large negative gradient update), it will never activate again and its weights will never receive gradient updates. This neuron is "dead." This can happen to a significant fraction of neurons in deep networks, especially with large learning rates or poor initialization.

## LeakyReLU: Fixing the Dying Neuron Problem

LeakyReLU addresses the zero-gradient problem by using a small positive slope $\alpha$ for negative inputs:

$$
\text{LeakyReLU}(x) = \begin{cases} x & \text{if } x > 0 \\ \alpha x & \text{if } x \le 0 \end{cases}
$$

where $\alpha$ is typically 0.01 (the default in PyTorch). This ensures that the gradient is never zero:

$$
\frac{d}{dx}\text{LeakyReLU}(x) = \begin{cases} 1 & \text{if } x > 0 \\ \alpha & \text{if } x \le 0 \end{cases}
$$

**Worked example:** With $\alpha = 0.01$ and input values $[3.0, -2.0, 0.0, 1.5, -0.5]$:
- $3.0 > 0 \to 3.0$
- $-2.0 \le 0 \to 0.01 \times (-2.0) = -0.02$
- $0.0 \le 0 \to 0.01 \times 0.0 = 0.0$
- $1.5 > 0 \to 1.5$
- $-0.5 \le 0 \to 0.01 \times (-0.5) = -0.005$

Result: $[3.0, -0.02, 0.0, 1.5, -0.005]$

## Implementing with Tensor Operations

The key insight for implementing LeakyReLU from scratch is that it is a piecewise function: it selects between two expressions based on a condition. PyTorch provides several ways to implement this element-wise:

**Approach 1: torch.where**

torch.where(condition, x, y) returns a tensor where each element is taken from $x$ if the condition is True, and from $y$ otherwise. This is the most readable approach:

```
result = torch.where(x > 0, x, alpha * x)
```

This computes the condition $x > 0$ as a boolean tensor, then selects $x$ where True and $\alpha x$ where False.

**Approach 2: Boolean masking**

Create a mask and use it to blend the two branches:

```
mask = (x > 0).float()
result = mask * x + (1 - mask) * alpha * x
```

This approach is mathematically equivalent but involves more computation (two multiplications and an addition vs one conditional selection).

**Approach 3: Clamp-based**

Using the identity $\text{LeakyReLU}(x) = \max(0, x) + \alpha \min(0, x)$:

```
result = torch.clamp(x, min=0) + alpha * torch.clamp(x, max=0)
```

All three approaches are correct and produce identical results. torch.where is generally preferred for clarity and efficiency.

## Other Common Activation Functions

For broader context, here are the activations you will encounter most often:

**Sigmoid:**

$$
\sigma(x) = \frac{1}{1 + e^{-x}}
$$

Output range $(0, 1)$. Used in binary classification outputs and gating mechanisms (LSTM, GRU). Suffers from vanishing gradients: for large $|x|$, the gradient approaches 0, making training slow for deep networks.

**Tanh:**

$$
\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}
$$

Output range $(-1, 1)$. Zero-centered (unlike sigmoid), which improves optimization dynamics. Still suffers from vanishing gradients at extreme values. Commonly used in RNNs and as the output activation in some generative models.

**GELU (Gaussian Error Linear Unit):**

$$
\text{GELU}(x) = x \cdot \Phi(x)
$$

where $\Phi(x)$ is the CDF of the standard normal distribution. This is the default activation in transformers (BERT, GPT). It is smooth, non-monotonic near zero, and provides a stochastic interpretation: each neuron's output is weighted by the probability that it would "survive" a Gaussian dropout mask.

**Swish / SiLU:**

$$
\text{Swish}(x) = x \cdot \sigma(x) = \frac{x}{1 + e^{-x}}
$$

A smooth approximation to ReLU discovered by neural architecture search. It is self-gated (the sigmoid controls how much of $x$ passes through) and non-monotonic near the origin. Used in EfficientNet and other modern architectures.

## Gradients and Backpropagation

When implementing activations from scratch, the gradient computation is handled automatically by PyTorch's autograd as long as you use differentiable tensor operations. torch.where, element-wise multiplication, and torch.clamp are all tracked by the autograd graph, so backpropagation through the intermediate tensor works without additional derivative code. Returning the tensor preserves its connection to the computation graph when gradient tracking is enabled.

If you need to verify the gradient, you can check with:

```
x = torch.tensor([-1.0, 2.0], requires_grad=True)
y = leaky_relu(x, 0.01)
y.sum().backward()
print(x.grad)  # should be [0.01, 1.0]
```

## Choosing an Activation Function

- **Hidden layers in CNNs:** ReLU or LeakyReLU. Simple, fast, effective. Use LeakyReLU if you observe many dead neurons
- **Hidden layers in transformers:** GELU. It is the standard choice and empirically performs best with attention mechanisms
- **Hidden layers in RNNs:** Tanh. The bounded output prevents exploding activations in the recurrent loop
- **Output layer for binary classification:** Sigmoid (squashes to probability)
- **Output layer for multi-class classification:** No activation (raw logits); apply softmax inside the loss function (CrossEntropyLoss does this automatically)
- **Output layer for regression:** No activation (identity)