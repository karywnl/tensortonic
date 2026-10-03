import torch

def compute_gradient(values: torch.Tensor) -> torch.Tensor:
    """
    Returns a float32 gradient tensor with the same shape as values.
    """
    
    x = torch.tensor(values, dtype=torch.float32, requires_grad=True)
    y = ((x**3) + 2*x)
    y = y.sum()
    y.backward()

    return x.grad