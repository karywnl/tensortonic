import numpy as np

def create_filled_array(shape, kind):

    if kind.lower() == "ones":
        return np.ones(tuple(shape))
    else:
        return np.zeros(tuple(shape))