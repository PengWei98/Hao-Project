# Created by yuwenhao at 16/02/2019
"""
Feature: #Enter feature name here
# Enter feature description here
Scenario: #Enter scenario name here
# Enter steps here
Test File Location: # Enter]
"""

from utilities.pdf2txt import get_texts_from_pdf
from constants.path_manager import root
import os
import re


def get_folder_pdf_content(i_folder):

    file_list= []
    for root, dirs, files in os.walk(i_folder):
        for i_folder in files:
            file_list.append(os.path.join(root, i_folder))

    content_list = []
    for file in file_list:
        if file.split('.')[-1] != 'pdf': continue
        content_list += get_texts_from_pdf(file)

    return content_list


def get_content_clean(i_string):

    i_string = i_string.lower()
    i_string = re.sub(r"i\.e\.", " ", i_string)
    i_string = re.sub(r"\n", " ", i_string)
    i_string = re.sub(r"\(cid:128\)", "fi", i_string)
    i_string = re.sub(r"\(cid:140\)", "th", i_string)
    i_string = re.sub(r"\(cid:\S+\)", " ", i_string)
    i_string = re.sub(r"\.", " .", i_string)
    i_string = re.sub(r",", " ,", i_string)

    while i_string != re.sub(r"  ", " ", i_string):
        i_string = re.sub(r"  ", " ", i_string)

    return i_string


def get_content_list_clean(i_list):
    output_list = []
    for item in i_list:
        if ' ' not in item: continue
        output_list.append(get_content_clean(item))

    return output_list


def get_folder_pdf_clean_content(i_folder):
    content = get_folder_pdf_content(i_folder)

    return get_content_list_clean(content)


if __name__ == '__main__':

    input_folder = os.path.join(root, 'test_files', 'test_pdf')

    print(get_content_list_clean(get_folder_pdf_content(input_folder)))

