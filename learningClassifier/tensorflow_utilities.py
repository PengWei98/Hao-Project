# Created by yuwenhao at 18/02/2019
"""
Feature: #Enter feature name here
# Enter feature description here
Scenario: #Enter scenario name here
# Enter steps here
Test File Location: # Enter]
"""

import numpy as np
np.set_printoptions(threshold=200)


class Dataset:

    def __init__(self, input_data, input_label):
        self._index_in_epoch = 0
        self._epochs_completed = 0
        self.input_data = input_data
        self.input_label = input_label
        self._data = np.arange(len(input_data))
        self._num_examples = len(input_data)
        pass

    @property
    def data(self):
        return self._data

    def next_batch(self, batch_size, shuffle=True):
        start = self._index_in_epoch
        if start == 0 and self._epochs_completed == 0:
            idx = np.arange(0, self._num_examples)  # get all possible indexes
            np.random.shuffle(idx)  # shuffle index
            self._data = self.data[idx]  # get list of `num` random samples

        # go to the next batch
        if start + batch_size > self._num_examples:
            self._epochs_completed += 1
            rest_num_examples = self._num_examples - start
            data_rest_part = self.data[start:self._num_examples]
            idx0 = np.arange(0, self._num_examples)  # get all possible indexes
            np.random.shuffle(idx0)  # shuffle indexes
            self._data = self.data[idx0]  # get list of `num` random samples

            start = 0
            self._index_in_epoch = batch_size - rest_num_examples
            end = self._index_in_epoch
            data_new_part = self._data[start:end]
            return self.input_data[np.concatenate((data_rest_part, data_new_part), axis=0)], \
                   self.input_label[np.concatenate((data_rest_part, data_new_part), axis=0)]

        else:
            self._index_in_epoch += batch_size
            end = self._index_in_epoch
            return self.input_data[self._data[start:end]], self.input_label[self._data[start:end]]


def get_random_data():

    rand_x_train = np.random.rand(10000, 100)
    rand_y_train = np.random.rand(10000, 2)
    rand_x_test = np.random.rand(1000, 100)
    rand_y_test = np.random.rand(1000, 2)

    return rand_x_train, rand_y_train, rand_x_test, rand_y_test


if __name__ == '__main__':

    x_train, y_train, x_test, y_test = get_random_data()

    tr = Dataset(x_train, y_train)

    for i in range(100):
        data, label = tr.next_batch(100)
        print('The batch label number is:', label, '\n')
        print('The batch train data is:', data, '\n')
