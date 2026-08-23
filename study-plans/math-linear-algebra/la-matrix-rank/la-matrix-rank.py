import numpy as np

def matrix_rank(A):
    """
    Returns: int, the rank of matrix A.
    """
    A = np.array(A)

    return np.linalg.matrix_rank(A)