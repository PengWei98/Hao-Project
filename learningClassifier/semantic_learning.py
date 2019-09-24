# Created by yuwenhao at 16/01/2019
"""
Feature: #Enter feature name here
# Enter feature description here
Scenario: #Enter scenario name here
# Enter steps here
Test File Location: # Enter]
"""

from constants.hyper_parameter_manager import *
from numpy.random import RandomState

import tensorflow as tf
import numpy as np
import random


def get_label(i_int):
    return [1, 0, 0] if i_int == 1 else [0, 1, 0] if i_int == 2 else [0, 0, 1]


def get_data(model):
    X, Y, _X, _Y = [], [], [], []
    for index, concept in enumerate(CONCEPT_DICT):
        try:
            X.append(model[concept])
            Y.append(get_label(CONCEPT_DICT[concept]))
        except:
            continue

    for index, concept in enumerate(CONCEPT_TRUTH_DICT.keys() - CONCEPT_DICT.keys()):
        try:
            _X.append(model[concept])
            _Y.append(get_label(CONCEPT_TRUTH_DICT[concept]))
        except:
            continue

    return np.array(X), np.array(Y), np.array(_X), np.array(_Y), len(X), len(_X)


def semantic_learning(X, Y, _X, _Y, dataset_size, batch_size=50, steps=100):

    dataset_size = 10000

    w1 = tf.Variable(tf.random_normal([50, 10], stddev=1, seed=1))
    w2 = tf.Variable(tf.random_normal([10, 3], stddev=1, seed=1))

    x = tf.placeholder(tf.float32, shape=(None, 50))
    y_ = tf.placeholder(tf.float32, shape=(None, 3))

    a = tf.matmul(x, w1)
    y = tf.nn.softmax(tf.matmul(a, w2))

    cross_entropy = -tf.reduce_sum(y_*tf.log(y))
    train_step = tf.train.AdamOptimizer(0.01).minimize(cross_entropy)

    with tf.Session() as sess:
        init_op = tf.global_variables_initializer()
        sess.run(init_op)
        for i in range(steps):
            start = (i * batch_size) % dataset_size
            end = min(start+batch_size,dataset_size)

            sess.run(train_step,feed_dict={x: X[start:end], y_: Y[start:end]})

        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))

        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        print(sess.run(accuracy, feed_dict={x: _X, y_: _Y}))


if __name__ == '__main__':

    from learning_based_classifier.word_embedding import *

    input_folder = os.path.join(root, 'test_files', 'test_pdf')
    content_list = get_folder_pdf_clean_content(input_folder)
    content_list = get_training_sentences(content_list)
    model = get_word_vector(content_list)
    X, Y, _X, _Y, dataset_size, test_size = get_data(model)
    print(X, Y, _X, _Y, dataset_size)
