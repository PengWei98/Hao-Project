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

import codecs
import random
import re

from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

from constants.hyperParameter import *
from utilities.item_token import Token


def get_clean_content(content):
    def clean_space(con):
        while con != re.sub('  ', ' ', con):
            con = re.sub('  ', ' ', con)
        return con.strip()

    def clean_content(con):
        con = clean_space(con)
        con = re.sub('[(](.*)[)]|\n|\t|:|,|!|#|=(.*)|[[](.*)[]]', '', con)
        return con.lower()

    return clean_content(content)


def add_ground_truth(l, item, concept_dict):
    for concept in item.content:
        concept_dict[concept] = l

    return concept_dict


def get_ground_truth(input_data):
    for i in input_data:
        item = Token(filename=i[0], label=i[1], position=i[2], indicator=i[3], content=i[4])

        if item.label == 'd':
            add_ground_truth(DATASET, item, CONCEPT_TRUTH_DICT)
        elif item.label == 'm':
            add_ground_truth(MODEL, item, CONCEPT_TRUTH_DICT)
        elif item.label == 'e':
            add_ground_truth(METRIC, item, CONCEPT_TRUTH_DICT)
        else:
            continue

    return CONCEPT_TRUTH_DICT


def get_random_label():
    s = lambda x: [x] if x else None
    for concept in CONCEPT_TRUTH_DICT:
        if not s(CONCEPT_DICT.get(concept)):
            CONCEPT_DICT[concept] = random.choice([1, 2, 3])

    return CONCEPT_DICT


def get_evaluation_results():
    y_true, y_pred = [], []
    s = lambda x: [x] if x else None

    for index, concept in enumerate(CONCEPT_TRUTH_DICT):
        y_true += [CONCEPT_TRUTH_DICT[concept]]
        y_pred += s(CONCEPT_DICT.get(concept)) or [random.choice([1, 2, 3])]

    micro_precision = round(precision_score(y_true, y_pred, average='micro'), 4)
    macro_precision = round(precision_score(y_true, y_pred, average='macro'), 4)
    micro_recall = round(recall_score(y_true, y_pred, average='micro'), 4)
    macro_recall = round(recall_score(y_true, y_pred, average='macro'), 4)
    micro_f1 = round(f1_score(y_true, y_pred, average='micro'), 4)
    macro_f1 = round(f1_score(y_true, y_pred, average='macro'), 4)

    print('micro_precision:', micro_precision)
    print('macro_precision:', macro_precision)
    print('micro_recall:', micro_recall)
    print('macro_recall:', macro_recall)
    print('micro_f1:', micro_f1)
    print('macro_f1:', macro_f1)

    f = codecs.open("result.txt", 'w', 'utf-8')
    f.write('Evaluative Metric: </br>macro-precision: ' + str(macro_precision) +
            '</br>micro-precision: ' + str(micro_precision) +
            '</br>macro-recall: ' + str(macro_recall) +
            '</br>micro-recall:' + str(micro_recall) +
            '</br>macro-f1:' + str(macro_f1) +
            '</br>micro-f1:' + str(micro_f1) + '\r\n')
    f.close()
