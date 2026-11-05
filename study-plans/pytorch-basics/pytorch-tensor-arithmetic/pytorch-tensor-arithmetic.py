import torch

def tensor_op(x: torch.Tensor, y: torch.Tensor, op: str) -> torch.Tensor:
    """
    Returns the operation result as a float32 tensor.
    """
    if op == "add":
        return torch.add(x, y)
    elif op == "multiply":
        return torch.multiply(x, y)
    elif op == "matmul":
        return x @ y
    elif op == "power":
        return x ** y
    else:
        return torch.maximum(x, y)
    