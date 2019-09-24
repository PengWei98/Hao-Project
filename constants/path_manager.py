# Created by yuwenhao at 14/01/2018

import pathlib
import os

root = pathlib.Path(os.path.abspath(__file__)).parent.parent
root = str(root)


def get_all_files(path, verbose=False):
    """"Gets all files in a directory"""
    if verbose: print(path)

    if not os.path.exists(path): return []
    if os.path.isfile(path): return [path]

    return [f for d in os.listdir(path) for f in get_all_files(os.path.join(path, d), verbose)]


def get_file_absolute_path(filename):
    assert os.path.exists(filename), 'file: {} , not exist'.format(filename)
    return os.path.abspath(filename)


