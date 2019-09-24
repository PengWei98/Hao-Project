# Created by yuwenhao at 16/01/2019
"""
Feature: #Enter feature name here
# Enter feature description here
Scenario: #Enter scenario name here
# Enter steps here
Test File Location: # Enter]
"""

from utilities.item_token import Token
import os


def get_lower_text(input_data):
    output_data = []

    for i in input_data:
        item = Token(filename=i[0], label=i[1], position=i[2], indicator=i[3], content=i[4])

        item.label = item.label.lower()
        item.position = item.position.lower()
        item.indicator = item.indicator.lower()
        item.content = [item.content[index].lower() for index, concept in enumerate(item.content)]
        output_data.append((item.filename, item.label, item.position, item.indicator, item.content))

    return output_data


def get_statistic_total_concepts(input_data):
    concept_list = []
    for i in input_data:
        item = Token(filename=i[0], label=i[1], position=i[2], indicator=i[3], content=i[4])
        concept_list += [concept for concept in item.content]

    return len(list(set(concept_list)))


def get_title_list(i_data):
    i_title = []
    for i in i_data:
        if (i[0], i[5]) in i_title: continue
        i_title += [(i[0], i[5])]

    return i_title


def get_file_list(csv_folder):
    file_list = []
    for root, dirs, files in os.walk(csv_folder):
        for i_f in files:
            file_list.append(os.path.join(root, i_f))

    return file_list


def get_file_name(filename):
    return ''.join(os.path.splitext(filename)[:-1])
