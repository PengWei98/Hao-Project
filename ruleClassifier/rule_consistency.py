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
from utilities.item_token import Token


def get_vote_result(item, c_dict):
    count_d, count_m, count_e = 0, 0, 0

    for concept in item:
        if c_dict.get(concept) == 1: count_d += 1
        elif c_dict.get(concept) == 2: count_m += 1
        elif c_dict.get(concept) == 3: count_e += 1
        else: continue

    return (DATASET if count_d > count_m and count_d > count_e else
            MODEL if count_m > count_d and count_m > count_e else
            METRIC if count_e > count_d and count_e > count_m else None)


def add_consistency_words(l, item, c_dict):
    for concept in item.content:
        c_dict[concept] = l

    return c_dict


# ('kdd10-d0-p6.csv', 'M', 'Left1', 'Model', ['simSVM', '1vsR SVM', 'rankSVM', 'BPMLL', 'MLKNN'])
def get_rule_consistency(input_data, concept_dict):
    for i in input_data:
        item = Token(filename=i[0], label=i[1], position=i[2], indicator=i[3], content=i[4])

        vote_result = get_vote_result(item.content, concept_dict)
        if vote_result:
            add_consistency_words(vote_result, item, concept_dict)

    return concept_dict


