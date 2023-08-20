def linear_map(value: int, min: int, max:int, tomin:int, tomax:int):
    m = (tomax-tomin)/(max-min)
    return m*(value-min)+tomin

def voltage_transform(value: int):
    return value/1.84