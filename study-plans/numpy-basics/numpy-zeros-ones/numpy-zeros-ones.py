import numpy as np

def create_filled_array(shape, kind):
    """
    Returns: 2D numpy array of given shape with dtype float64
    """
    if kind == 'zeros':
        return np.zeros(shape)
    else:
        return np.ones(shape)