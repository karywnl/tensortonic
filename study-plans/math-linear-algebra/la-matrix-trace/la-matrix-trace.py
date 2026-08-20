import numpy as np

def matrix_trace(A):
    """
    Returns: float, the trace (sum of diagonal elements) of A.
    """
    A = np.array(A)

    return np.linalg.trace(A)