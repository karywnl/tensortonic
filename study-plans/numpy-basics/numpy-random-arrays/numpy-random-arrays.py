import numpy as np

def generate_random_array(shape, kind, seed):

    ## MODERN API
    
    # rng = np.random.default_rng(seed)
    # if kind == "uniform":
    #     return rng.random(shape)
    # else:
    #     return rng.standard_normal(shape)

    ## LEGACY API 

    np.random.seed(seed)
    if kind == 'uniform':
        return np.random.random(shape)
    return np.random.standard_normal(shape)
