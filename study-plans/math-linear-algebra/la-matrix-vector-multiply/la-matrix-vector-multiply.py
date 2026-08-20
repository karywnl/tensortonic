import numpy as np

def matrix_vector_multiply(A, x):
    """
    Returns: 1-D float64 array, the product A @ x.
    """
    A = np.array(A)
    x = np.array(x)

    return A @ x