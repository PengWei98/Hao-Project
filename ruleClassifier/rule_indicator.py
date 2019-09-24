# Created by yuwenhao at 14/01/2019

import sys
import os

CUR_DIR = os.path.dirname((os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(CUR_DIR)
sys.path.append(BASE_DIR)

from constants.hyperParameter import *
from utilities.item_token import Token

import pickle
import os


def add_indicator_words(l, item, c_dict):
    for concept in item.content:
        c_dict[concept] = l

    return c_dict


# ('kdd10-d0-p6.csv', 'M', 'Left1', 'Model', ['simSVM', '1vsR SVM', 'rankSVM', 'BPMLL', 'MLKNN'])
def get_rule_indicator(input_data, concept_dict):
    for i in input_data:
        item = Token(filename=i[0], label=i[1], position=i[2], indicator=i[3], content=i[4])

        if item.indicator == 'dataset': add_indicator_words(DATASET, item, concept_dict)
        elif item.indicator == 'model': add_indicator_words(MODEL, item, concept_dict)
        elif item.indicator == 'metric': add_indicator_words(METRIC, item, concept_dict)
        else: continue

    return concept_dict
        
        
