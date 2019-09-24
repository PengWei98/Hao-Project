# Created by yuwenhao at 16/02/2019
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
from gensim.models import FastText
from learningClassifier.pre_embedding import get_folder_pdf_clean_content

import os
import io

wiki_vector_path = os.path.join(BASE_DIR, 'constants', 'wiki-news-300d-1M.vec')


def get_training_sentences(i_list):
    return [item.split() for item in i_list]


def load_wiki_vectors():
    fin = io.open(wiki_vector_path, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())

    data = {}
    for line in fin:
        tokens = line.rstrip().split()
        data[tokens[0]] = map(float, tokens[1:])

    return data


def get_word_vector(sentences):
    return FastText(sentences, size=100, window=3, min_count=1, iter=10, min_n=3, max_n=6, word_ngrams=0)


if __name__ == '__main__':

    input_folder = os.path.join(BASE_DIR, 'test_files', 'test_pdf')
    content_list = get_folder_pdf_clean_content(input_folder)
    content_list = get_training_sentences(content_list)
    model = get_word_vector(content_list)

    print(model['and'])
    print(model.wv['and'])
    print(model.wv.similarity('and', 'svm'))
    print(model.wv.similar_by_word('svm', topn = 3))

    # print(load_wiki_vectors())
