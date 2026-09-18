import torch

def tensor_op(x, y, op):
    """
    Returns: list (result tensor converted via .tolist())
    """
    x = torch.tensor(x, dtype=torch.float32)
    y = torch.tensor(y, dtype=torch.float32)
    if op == "add":
        res = torch.add(x, y)
    elif op == "power":
        res = torch.pow(x, y)
    elif op == "matmul":
        res = torch.matmul(x, y)
    elif op == "multiply":
        res = torch.multiply(x, y)
    elif op == "max":
        res = torch.max(x, y)

    return res.tolist()