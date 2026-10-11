import torch

def activate(x: torch.Tensor, method: str = "relu") -> torch.Tensor:
    """
    Returns a float32 tensor with the same shape as x.
    """
    if method == "relu":
        return torch.relu(x)
    elif method == "sigmoid":
        return torch.sigmoid(x)
    elif method == "tanh":
        return torch.tanh(x)
    else:
        return torch.where(x > 0, x, 0.01 * x)
                                        
                                                     
                                                     
                                                     
                                                     
                                                

                                                