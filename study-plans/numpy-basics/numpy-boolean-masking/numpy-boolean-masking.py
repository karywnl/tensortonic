import numpy as np

def row_summary(data, threshold):
    """Returns: np.ndarray of shape (3, m, n), stacked element mask, any-filtered, all-filtered"""

    arr = np.array(data, dtype='float64')
    mask1 = arr <= threshold
    mask2 = np.all(arr <= threshold, axis=1)
    mask2 = mask2[:, np.newaxis]
    mask3 = np.any(arr <= threshold, axis=1)
    mask3 = mask3[:, np.newaxis]
    arr1 = np.where(mask1, 0.0, 1.0)
    arr2 = np.where(mask2, 0.0, arr)
    arr3 = np.where(mask3, 0.0, arr)
    return [arr1, arr2, arr3]