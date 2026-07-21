import numpy as np

def scale_rows(data, weights):
    """Returns: np.ndarray of shape (m, n), each row scaled by corresponding weight"""
    arr = np.array(data, dtype='float64')
    scalars = np.array(weights, dtype='float64')

    return arr * scalars[:, np.newaxis]