## <span style="font-size: 20px;">What Is a Tensor?</span>

A tensor is PyTorch's core data structure: a multi-dimensional array that lives on CPU or GPU and supports automatic differentiation. Conceptually, a scalar is a 0-dimensional tensor, a vector is 1D, a matrix is 2D, and anything beyond is an $n$-dimensional tensor. The word "tensor" in deep learning is borrowed from physics and mathematics, where it denotes an object that transforms in specific ways under coordinate changes, but in PyTorch it simply means "a typed, strided, $n$-dimensional array with optional gradient tracking."

Every tensor has three fundamental attributes:

- **Shape** (or size): a tuple of integers describing the extent along each axis. A shape of $(3, 4)$ means 3 rows and 4 columns; $(2, 3, 4)$ means 2 "slices" of $3 \times 4$ matrices. Shape is the single most common source of bugs in deep learning code, so developing strong intuition about shapes is essential.
- **Dtype** (data type): the numeric type of every element. Common dtypes include `torch.float32` (default for floats), `torch.int64` (default for integers), `torch.float16`, `torch.bfloat16`, and `torch.bool`. Mixed-precision training uses float16 or bfloat16 for speed while keeping a float32 "master copy" of weights.
- **Device**: either `cpu` or a CUDA device like `cuda:0`. Tensors on different devices cannot interact directly; you must explicitly move one to match the other.

## Creating Tensors from Python Data

The primary function for converting Python data into a tensor is `torch.tensor(data)`:

- It accepts Python lists, tuples, nested lists, NumPy arrays, and scalars
- Shape is inferred from the nesting structure: a flat list $[1, 2, 3]$ becomes shape $(3{,})$, a list of two 3-element lists $[[1,2,3],[4,5,6]]$ becomes shape $(2, 3)$
- Dtype is inferred from the input values: all-integer input yields `torch.int64`, any float yields `torch.float32`. You can override with the `dtype` keyword argument
- The function **always copies** the data. If you want to share memory with a NumPy array (zero-copy), use `torch.from_numpy(arr)` instead, which creates a tensor that shares the same underlying storage

**Important distinction**: `torch.tensor` is a function that always copies data. `torch.Tensor` (capital T) is the class itself; calling `torch.Tensor([1,2,3])` also creates a tensor, but it always produces `float32` regardless of input type. Prefer the lowercase `torch.tensor` for clarity and explicit dtype control.

**Worked example:** Given the input $[[1, 2], [3, 4], [5, 6]]$, calling `torch.tensor` produces a 2D tensor of shape $(3, 2)$ with dtype `int64`. If the input were $[[1.0, 2], [3, 4], [5, 6]]$, the single float value $1.0$ promotes the entire tensor to `float32`.

## Other Creation Functions

PyTorch provides a family of convenience functions for creating tensors with specific values or patterns:

- `torch.zeros(shape)` and `torch.ones(shape)`: tensors filled with 0s or 1s. Commonly used to initialize accumulators, masks, or bias vectors
- `torch.zeros_like(t)` and `torch.ones_like(t)`: create tensors with the same shape, dtype, and device as an existing tensor $t$. This avoids hardcoding shapes and device placement
- `torch.randn(shape)`: draws each element independently from $\mathcal{N}(0, 1)$. Used for weight initialization (usually scaled by a factor like $\frac{1}{\sqrt{n}}$), noise injection, and random projections
- `torch.rand(shape)`: uniform samples from $[0, 1)$
- `torch.arange(start, end, step)`: evenly spaced integer or float values, similar to Python's `range` but returning a tensor. Useful for creating positional indices
- `torch.linspace(start, end, steps)`: exactly `steps` evenly spaced values between start and end (inclusive). Useful for creating coordinate grids
- `torch.eye(n)`: the $n \times n$ identity matrix. Often used to create one-hot encodings or initialize weight matrices

Each of these accepts optional `dtype` and `device` arguments so you can create tensors directly on GPU without a subsequent `.to(device)` call.

## Memory Layout and Strides

Understanding how tensors are stored in memory helps explain many PyTorch behaviors:

- Tensor data is stored in a flat, contiguous block of memory
- The **stride** tuple tells PyTorch how many elements to skip in memory to advance one position along each dimension. For a row-major $(3, 4)$ tensor, strides are $(4, 1)$: moving one row means jumping 4 elements, moving one column means jumping 1 element
- Many operations (transpose, narrow, slice) create a **view** that shares the same underlying storage but has different shape and stride metadata. No data is copied
- When a tensor is non-contiguous (strides don't correspond to a simple row-major layout), certain operations like `view` will fail and you need to call `.contiguous()` first to copy the data into a fresh contiguous block

## Dtype Conversion and Casting

Type mismatches are a frequent source of runtime errors:

- Use `tensor.float()` as shorthand for `tensor.to(torch.float32)`, `tensor.long()` for `torch.int64`, `tensor.half()` for `torch.float16`
- Casting creates a new tensor (copy); it does not modify in place
- Binary operations between tensors of different dtypes trigger automatic promotion: int + float yields float, float32 + float64 yields float64
- Neural network parameters are `float32` by default, so input data must be cast to `float32` before passing through a model (a very common mistake with integer-valued features)

## Gradients and Tensor Creation

By default, tensors created from Python data have `requires_grad=False`. To track gradients for optimization:

- Pass `requires_grad=True` to `torch.tensor` or call `tensor.requires_grad_(True)` (in-place)
- Parameters created via `nn.Parameter` automatically have `requires_grad=True`
- Gradient tracking adds overhead, so only enable it for tensors that need to be optimized (weights). Input data and labels should not require gradients

**Common pitfall:** `torch.tensor([1, 2, 3], requires_grad=True)` will fail because integer tensors cannot track gradients (gradients are real-valued). You must create a float tensor: `torch.tensor([1.0, 2.0, 3.0], requires_grad=True)`.