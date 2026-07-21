import numpy as np

def pairwise_diff(a):
    """Returns: np.ndarray of shape (n, n) where out[i,j] = a[i] - a[j]"""

    arr = np.array(a, dtype=np.float64)

    return arr[:, np.newaxis] - arr[np.newaxis, :]