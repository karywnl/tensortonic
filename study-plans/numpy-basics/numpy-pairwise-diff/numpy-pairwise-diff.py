import numpy as np

def pairwise_diff(a):
    """Returns: np.ndarray of shape (n, n) where out[i,j] = a[i] - a[j]"""

    arr = np.array(a, dtype=np.float64)
    n = len(arr)
    res = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            res[i, j] = arr[i] - arr[j]

    return res