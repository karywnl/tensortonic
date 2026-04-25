import numpy as np

def create_sequence(start, stop, param, kind):
    if kind == "arange":
        return np.arange(start=start, stop=stop, step=param, dtype='float64')
    else : 
        return np.linspace(start, stop, param, dtype='float64')