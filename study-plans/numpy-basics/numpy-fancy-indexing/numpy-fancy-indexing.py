import numpy as np

def select_by_index(arr, indices, axis):
    """
    Returns: 2D ndarray of float64
    """
    arr = np.array(arr, dtype='float64')
    if axis == 0:
        return arr[indices, :]
    return arr[:, indices]