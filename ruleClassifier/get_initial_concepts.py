# Created by yuwenhao at 16/01/2019
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

import re


def is_initial_concepts(concept):
    return (DATASET if any(re.findall(p, concept) for p in initial_dataset) else
            MODEL if any(re.findall(p, concept) for p in initial_model) else
            METRIC if any(re.findall(p, concept) for p in initial_metric) else None)


# ('kdd10-d0-p6.csv', 'M', 'Left1', 'Model', ['simSVM', '1vsR SVM', 'rankSVM', 'BPMLL', 'MLKNN'])
def get_initial_concepts(input_data, concept_dict):
    for i in input_data:
        item = Token(filename=i[0], label=i[1], position=i[2], indicator=i[3], content=i[4])

        for concept in item.content:
            if is_initial_concepts(concept) == DATASET: concept_dict[concept] = DATASET
            if is_initial_concepts(concept) == MODEL: concept_dict[concept] = MODEL
            if is_initial_concepts(concept) == METRIC: concept_dict[concept] = METRIC

    return concept_dict

