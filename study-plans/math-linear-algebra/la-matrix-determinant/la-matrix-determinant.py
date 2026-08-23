import numpy as np

def matrix_determinant(A):
    """
    Returns: float, the determinant of square matrix A.
    """
    A = np.array(A)

    return np.linalg.det(A)