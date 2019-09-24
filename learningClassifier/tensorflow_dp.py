# Created by yuwenhao at 18/02/2019
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
from learningClassifier.tensorflow_utilities import Dataset, get_random_data

import tensorflow as tf
import numpy as np


def get_label(i_int):
    return [1, 0, 0] if i_int == 1 else [0, 1, 0] if i_int == 2 else [0, 0, 1]


def get_data(model):

    X, Y, _X, _Y = [], [], [], []
    X_name, _X_name = [], []

    for index, concept in enumerate(CONCEPT_DICT):
        try:
            X.append(model[concept])
            Y.append(get_label(CONCEPT_DICT[concept]))
            X_name.append(concept)
        except:
            continue

    for index, concept in enumerate(CONCEPT_TRUTH_DICT.keys() - CONCEPT_DICT.keys()):
        try:
            _X.append(model[concept])
            _Y.append(get_label(CONCEPT_TRUTH_DICT[concept]))
            _X_name.append(concept)
        except:
            continue

    return np.array(X), np.array(Y), np.array(_X), np.array(_Y), X_name, _X_name, len(X), len(_X)


def semantic_learning(x_train, y_train, x_test, y_test=None, batch_size=50, learning_rate=0.5, epochs=10):

    train, test = Dataset(x_train, y_train), Dataset(x_test, y_test)

    # placeholder
    x = tf.placeholder(tf.float32, [None, 100])
    y = tf.placeholder(tf.float32, [None, 3])

    # hidden layer => w, b
    W1 = tf.Variable(tf.random_normal([100, 10], stddev=0.03), name='W1')
    b1 = tf.Variable(tf.random_normal([10]), name='b1')
    # output layer => w, b
    W2 = tf.Variable(tf.random_normal([10, 3], stddev=0.03), name='W2')
    b2 = tf.Variable(tf.random_normal([3]), name='b2')

    # hidden layer
    hidden_out = tf.add(tf.matmul(x, W1), b1)
    hidden_out = tf.nn.relu(hidden_out)

    # calculate using softmax
    y_ = tf.nn.softmax(tf.add(tf.matmul(hidden_out, W2), b2))

    y_clipped = tf.clip_by_value(y_, 1e-10, 0.9999999)
    cross_entropy = -tf.reduce_mean(tf.reduce_sum(y * tf.log(y_clipped) + (1 - y) * tf.log(1 - y_clipped), axis=1))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cross_entropy)

    # init operator
    init = tf.global_variables_initializer()

    # argmax to get accuracy
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # set session
    with tf.Session() as sess:
        sess.run(init)
        total_batch = int(len(train.input_label) / batch_size)
        for epoch in range(epochs):
            avg_cost = 0
            for i in range(total_batch):
                batch_x, batch_y = train.next_batch(batch_size=batch_size)
                _, c = sess.run([optimizer, cross_entropy], feed_dict={x: batch_x, y: batch_y})
                avg_cost += c / total_batch
            # print("Epoch:", (epoch + 1), "cost = ", "{:.3f}".format(avg_cost))
        # print('Accuracy:', sess.run(accuracy, feed_dict={x: test.input_data, y: test.input_label}))

        return sess.run(tf.argmax(y_, 1), feed_dict={x: test.input_data})


def get_semantic_learning(model):
    x_train, y_train, x_test, y_test, x_name, _x_name, len_train, len_test = get_data(model)
    # print(x_train, y_train, x_test, y_test)

    for index, label in enumerate(semantic_learning(x_train, y_train, x_test, y_test)):

        if label == 0: CONCEPT_DICT[_x_name[index]] = DATASET
        elif label == 1: CONCEPT_DICT[_x_name[index]] = MODEL
        elif label == 2: CONCEPT_DICT[_x_name[index]] = METRIC
        else: continue

        if index > 20: break

    return CONCEPT_DICT


if __name__ == '__main__':

    from learning_based_classifier.word_embedding import *

    inputfolder = os.path.join(root, 'test_files', 'test_pdf')
    content_list = get_folder_pdf_clean_content(inputfolder)
    content_list = get_training_sentences(content_list)
    model = get_word_vector(content_list)
    concept_dict = get_semantic_learning(model)







