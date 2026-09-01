import numpy as np

def solve_linear_system(A, b):
    """
    Returns: float64 array, the solution x to A @ x = b.
    """
    A = np.array(A)
    b = np.array(b)

    return np.linalg.solve(A, b)