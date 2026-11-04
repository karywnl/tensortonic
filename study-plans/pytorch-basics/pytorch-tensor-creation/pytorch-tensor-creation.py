import torch

def create_tensor(method: str, shape: list, value: float = 0.0) -> torch.Tensor:
    """
    Returns a float32 tensor with the requested shape.
    """
    if method == "zeros":
        return torch.zeros(shape, dtype=torch.float32)
    elif method == "ones":
        return torch.ones(shape, dtype=torch.float32)
    else:
        return torch.full(shape, value, dtype=torch.float32)