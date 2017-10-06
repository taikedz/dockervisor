import os

def ensure_dir(path_array):
    s_path = as_path(path_array)
    if not os.path.isdir(s_path):
        os.makedirs(s_path)

def read_file(path_array):
    filepath = as_path(path_array)

    if not os.path.is_file(filepath):
        return None

    fh = open(filepath, "r")
    lines = fh.readlines()
    fh.close()

    return ''.join(lines).strip()

def write_file(path_array, filedata):
    filepath = as_path(path_array)
    fh = open(filepath, "w")
    fh.write(filedata)
    fh.close()

def as_path(path_array):
    return path.os.sep.join(path_array)
