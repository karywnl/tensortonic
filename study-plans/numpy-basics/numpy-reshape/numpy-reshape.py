import numpy as np

def reshape_array(data, operation):
    data = np.array(data, dtype='float64')
    if operation == "transpose":
        return data.T
    elif operation == "flatten":
        return data.reshape(-1)
    else:
        return np.expand_dims(data, axis=0)
