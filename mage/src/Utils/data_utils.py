import numpy as np

def key_value_pairs_for_epoch(data, epoch):
    values = {}
    for key in data:
        if isinstance(data[key], dict):
            for k in data[key]:
                values[ key + '.' + k ] = data[key][k][epoch]
        else:
            values[key] = data[key][epoch]
    return values

def extract_values(data, key):
    if '.' in key:
        keys = key.split(".")
        return data[keys[0]][keys[1]]
    else:
        return data[key]
    
def empty_data_from_keys(data):
    new_data = {}
    for key in data:
        if key not in new_data:
            if isinstance(data[key], dict):
                new_data[key] = {}
                for k in data[key]:
                    new_data[key][k] = np.array([])
            else:
                new_data[key] = np.array([])
    return new_data