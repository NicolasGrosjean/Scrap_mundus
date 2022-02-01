import os

def get_data_dir():
    if 'data' in os.listdir():
        return 'data'
    if 'data' in os.listdir('mundus'):
        return os.path.join('mundus', 'data')
    if 'data' in os.listdir('..'):
        return os.path.join('..', 'data')
    raise Exception("Data directory not found !")
