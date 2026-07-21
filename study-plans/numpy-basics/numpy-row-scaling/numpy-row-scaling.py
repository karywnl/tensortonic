import numpy as np

def scale_rows(data, weights):
    """Returns: np.ndarray of shape (m, n), each row scaled by corresponding weight"""
    arr = np.array(data, dtype='float64')

    for i in range(len(weights)):
        arr[i] = weights[i] * arr[i]

    return arr