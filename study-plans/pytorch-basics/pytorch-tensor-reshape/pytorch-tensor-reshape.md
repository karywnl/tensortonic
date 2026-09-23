## Why Reshaping Matters in Deep Learning

Tensor reshaping is one of the most frequently used operations in deep learning pipelines. Data arrives in one shape, but layers expect another. Images from a data loader might be $(B, H, W, C)$ (batch, height, width, channels), but a convolutional layer expects $(B, C, H, W)$. An attention layer first splits $(B, L, D)$ into $(B, L, H, D/H)$, then reorders the axes to $(B, H, L, D/H)$. Fully connected layers require flattening spatial dimensions. Getting reshaping wrong produces silent shape mismatches that either crash with cryptic error messages or, worse, produce incorrect results without any error.

There are three core reshaping operations in PyTorch, each with distinct semantics:

## view: Zero-Copy Reshape

tensor.view(new_shape) reinterprets the same underlying memory as a different shape:

- The total number of elements must be preserved: $\prod_{i} n_i = \prod_{j} d_j$
- One dimension can be $-1$, meaning "infer this from the others." For example, t.view(3, -1) on a tensor with 12 elements gives shape $(3, 4)$
- **Requires strides compatible with the requested shape.** Contiguous tensors support the usual reshapes; some non-contiguous tensors also support a view
- Returns a view (shares memory): modifying the result modifies the original, and no data is copied

$$
\text{view}: \mathbb{R}^{n_1 \times n_2 \times \cdots \times n_k} \to \mathbb{R}^{d_1 \times d_2 \times \cdots \times d_m}, \quad \prod_{i=1}^{k} n_i = \prod_{j=1}^{m} d_j
$$

**Worked example:** A tensor of shape $(2, 3, 4)$ has $2 \times 3 \times 4 = 24$ elements. Calling .view(6, 4) gives shape $(6, 4)$, .view(2, 12) gives $(2, 12)$, and .view(-1) gives $(24{,})$ (flatten). The memory layout is identical in every case; only the shape metadata changes.

## reshape: Flexible Alternative

tensor.reshape(new_shape) returns a view when the shape and strides permit it, and copies data otherwise:

- Same interface as view: same element-count constraint, same $-1$ inference
- Advantage: never raises a contiguity error
- Disadvantage: you lose the guarantee that the result shares memory with the original. If you rely on shared-memory semantics (e.g., modifying the reshaped tensor should update the original), use view explicitly so you get an error when the assumption breaks

**Practical guideline:** Use view when memory sharing is required; it raises if the requested shape cannot share the existing storage. Use reshape when either a view or a copy is acceptable.

## permute: Dimension Reordering

tensor.permute(dims) reorders the axes of a tensor without changing the data layout:

- Takes a tuple of dimension indices specifying the new order. For a 3D tensor, .permute(2, 0, 1) makes the old axis 2 the new axis 0, old axis 0 the new axis 1, and old axis 1 the new axis 2
- Given original shape $(a, b, c)$, permuting with $(2, 0, 1)$ gives shape $(c, a, b)$
- Always returns a **view** (no data copy), but the result is typically **non-contiguous**
- This is the primary tool for converting between channel orderings: $(B, H, W, C) \to (B, C, H, W)$ uses .permute(0, 3, 1, 2)

$$
\text{permute}(T, \pi) : \mathbb{R}^{n_0 \times n_1 \times \cdots \times n_{k-1}} \to \mathbb{R}^{n_{\pi(0)} \times n_{\pi(1)} \times \cdots \times n_{\pi(k-1)}}
$$

**Worked example:** A tensor $T$ of shape $(2, 3, 4)$ permuted with $(1, 2, 0)$ becomes shape $(3, 4, 2)$. Element $T[i, j, k]$ in the original maps to $T'[j, k, i]$ in the permuted tensor.

## Contiguity: The Key Constraint

A tensor is **contiguous** when its elements are stored in memory in the order that row-major (C-order) traversal would visit them. More precisely, a contiguous tensor's strides satisfy $\text{stride}[i] = \prod_{j=i+1}^{n-1} \text{shape}[j]$.

Operations that break contiguity:
- transpose and permute: they swap stride values but do not move data
- narrow and slicing with non-trivial steps: they change the offset or stride

After a non-contiguous operation:
- view fails when the requested shape is incompatible with the existing strides
- .contiguous() copies data into a fresh contiguous block, after which view works
- .reshape makes a copy only when the requested shape cannot be represented as a view

**Practical pattern:** After permute, if you need to call view, chain .contiguous().view(...). Better yet, use .reshape if you do not need shared-memory semantics.

## transpose vs permute

tensor.transpose(dim0, dim1) swaps exactly two dimensions. It is a special case of permute:

- t.transpose(0, 2) on shape $(2, 3, 4)$ gives $(4, 3, 2)$
- Equivalent to t.permute(2, 1, 0) only because the middle dimension stays in place
- For swapping exactly two axes, transpose is more readable; for arbitrary reorderings, use permute

tensor.T is shorthand for reversing all dimensions (full transpose). For 2D tensors this is the familiar matrix transpose. For higher dimensions, .T reverses all axes, which may not be what you want.

## Common Reshaping Patterns in Practice

- **Flatten for linear layer:** x.view(batch_size, -1) collapses all spatial dimensions. Equivalently, torch.flatten(x, start_dim=1)
- **Split heads in attention:** x.view(B, L, H, D//H).permute(0, 2, 1, 3) goes from $(B, L, D)$ to $(B, H, L, D/H)$
- **Image channel reorder:** img.permute(0, 3, 1, 2) converts NHWC to NCHW
- **Add batch dimension:** x.unsqueeze(0) adds a dimension of size 1 at position 0. Useful for passing a single sample through a model that expects a batch
- **Remove batch dimension:** x.squeeze(0) removes a size-1 dimension at position 0

## Debugging Tip

When shapes go wrong, insert print(tensor.shape) (or use a debugger) at each transformation step. Many bugs come from confusing the order of dimensions or forgetting that permute returns a non-contiguous tensor. Building the habit of checking .shape after every reshaping operation will save significant debugging time.