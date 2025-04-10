def process_data(data):
    if not isinstance(data, list):
        raise TypeError("Data must be a list")
    return [x * 2 for x in data]

def filter_data(data, threshold):
    if not isinstance(data, list):
        raise TypeError("Data must be a list")
    return [x for x in data if x > threshold]