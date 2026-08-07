import numpy as np

def euclidean_distance(x, y):
    """
    Returns: float, the Euclidean distance between x and y.
    """
    x = np.array(x)
    y = np.array(y)
    
    return np.linalg.norm(x - y)