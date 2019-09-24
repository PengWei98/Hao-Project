# Created by yuwenhao at 15/01/2019
"""
Feature: #Enter feature name here
# Enter feature description here
Scenario: #Enter scenario name here
# Enter steps here
Test File Location: # Enter]
"""
import sys
import os

CUR_DIR = os.path.dirname((os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(CUR_DIR)
sys.path.append(BASE_DIR)

from constants.hyperParameter import *
from ruleClassifier.rule_consistency import get_vote_result
from utilities.item_token import Token
from collections import Counter
from ruleClassifier.rule_indicator import add_indicator_words


def get_2d_filename(i_data):
    filename_list = [i[0] for i in i_data]
    filename_counts = Counter(filename_list)

    return [j for j in filename_counts if filename_counts[j] == 2]


def add_r3_words(content, _type, c_dict):
    for c in content:
        c_dict[c] = _type

    return c_dict


def get_title_category(i_title, c_dict):

    file_name, title_name = 0, 1

    t_dict, t_flag = {}, 0
    for item in i_title:
        for concept in c_dict:

            if concept in item[title_name].lower():
                t_flag += 1
                t_dict[item[file_name]] = c_dict[concept]

    return t_dict if t_flag == 1 else {}


def is_one_none(i_list):
    r, n_r = 0, 0

    for item in i_list:
        if item[1]: r += 1
        else: n_r += 1

    return True if (r == 2 and n_r == 1) else False


def get_unlabel(i_l):
    return [i for i in [1, 2, 3] if i not in i_l][0]


def get_which_list(i_list):
    n_index = [index for index, i in enumerate(i_list) if not i[1]][0]
    n_label = get_unlabel([i[1] for i in i_list])
    return i_list[n_index][0], n_label


# ('kdd10-d0-p6.csv', 'M', 'Left1', 'Model', ['simSVM', '1vsR SVM', 'rankSVM', 'BPMLL', 'MLKNN'])
def get_rule_completeness(input_data, input_title, concept_dict):
    # get [file1, file2, ...]
    filename_2d = get_2d_filename(input_data)
    # get [file1: 3, file2: 1, ...]
    title_dict = get_title_category(input_title, concept_dict)
    # get filename in title_dict
    filename_2d = [file for file in filename_2d if title_dict.get(file)]

    for file in filename_2d:

        sub_list = []
        sub_list += [(file, title_dict[file])]

        for i in input_data:

            item = Token(filename=i[0], label=i[1], position=i[2], indicator=i[3], content=i[4])
            if file == item.filename:
                sub_list += [(item.content, get_vote_result(item.content, concept_dict))]

        if not is_one_none(sub_list): continue

        content, _type = get_which_list(sub_list)

        if not content: continue

        concept_dict = add_r3_words(content, _type, concept_dict)

    return concept_dict



