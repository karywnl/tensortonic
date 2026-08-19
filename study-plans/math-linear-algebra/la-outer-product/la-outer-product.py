import numpy as np

def outer_product(u, v):
    """
    Returns: float64 matrix of shape (m, n), the outer product u v^T.
    """
    u = np.array(u, dtype='float64')
    v = np.array(v, dtype='float64')

    return np.outer(u, v)