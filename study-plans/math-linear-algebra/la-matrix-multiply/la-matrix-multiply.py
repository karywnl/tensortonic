import numpy as np

def matrix_multiply(A, B):
    """
    Returns: 2-D float64 array, the matrix product A @ B.
    """
    A = np.array(A)
    B = np.array(B)

    return A @ B