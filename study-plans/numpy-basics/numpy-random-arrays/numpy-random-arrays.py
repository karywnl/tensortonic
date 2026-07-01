import numpy as np

def generate_random_array(shape, kind, seed):
    """
    Returns: 2D ndarray of float64 random values
    """
    np.random.seed(seed)
    if kind == 'uniform':
        return np.random.random(shape)
    return np.random.standard_normal(shape)
