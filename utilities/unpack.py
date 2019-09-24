# Created by yuwenhao at 16/02/2019
"""
Feature: #Enter feature name here
# Enter feature description here
Scenario: #Enter scenario name here
# Enter steps here
Test File Location: # Enter]
"""

from zipfile import ZipFile

import os
import zipfile

ZIP, RAR, TGZ, GZ, TAR = '.zip', '.rar', '.tgz', '.gz', '.tar'
ZIP_FORMAT = (ZIP, )


def arg_first(iterables, pred):
    for index, element in enumerate(iterables):
        if pred(element): return index, element
    return None, None


def unpack_zip(filepath):

    zipfilename = filepath.split('/')[-1]

    index, ext = arg_first(ZIP_FORMAT, lambda n: n == zipfilename[-len(n):])
    # check if the file format is need unpack

    if index is None: return

    extract_path = filepath[:-len(ext)]

    if not os.path.exists(extract_path): os.makedirs(extract_path)

    function_mapper = {ZIP: lambda f: ZipFile(f)}

    parent_archive = function_mapper[ext](filepath)

    parent_archive.extractall(extract_path)
    namelist = parent_archive.namelist()
    parent_archive.close()

    for name in namelist:
        try:
            new_zip_filepath = os.path.join(extract_path, name)
            unpack_zip(new_zip_filepath)
        except zipfile.BadZipFile as e:
            print('failed on', name)
        except NotImplementedError as e:
            pass
        except OSError as e:
            pass

    # extract path is output folder path
    return extract_path
