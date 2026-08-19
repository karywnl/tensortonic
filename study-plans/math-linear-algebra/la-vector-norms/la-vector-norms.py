import numpy as np

def vector_norms(v):
    """
    Returns: float64 array of shape (3,) containing [L1, L2, L-inf] norms.
    """
    v = np.array(v, dtype='float64')

    return [
        np.linalg.norm(v, ord=1),
        np.linalg.norm(v),
        np.linalg.norm(v, ord=np.inf)
    ]