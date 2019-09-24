# Created by yuwenhao at 14/01/2019
"""
Feature: #Enter feature name here
# Enter feature description here
Scenario: #Enter scenario name here
# Enter steps here
Test File Location: # Enter]
"""

# content types
typeDict = {1: 'dataset', 2: 'model', 3: 'metric'}

DATASET = 1
MODEL = 2
METRIC = 3

# label dictionary
CONCEPT_DICT = {}
CONCEPT_TRUTH_DICT = {}

indicator_dataset = ['data', 'dataset', 'category', 'aspect']
indicator_model = ['model', 'method', 'algorithm', 'system']
indicator_metric = ['metric', 'measure']

initial_dataset = ['amazon', 'wiki', 'dblp', 'iris', 'google', 'facebook']
initial_model = ['svm', 'lr', 'line', 'rf', 'forest', 'dt', 'deepwalk', 'line']
initial_metric = ['prec', 'p@', 'acc', 'f1', 'recall', 'map', 'mae']

frequent_dataset = ['amazon', 'wiki', 'dblp', 'iris', 'google', 'apple', 'fedex', 'starbucks',
                    'frwiki', 'wikipedia memory', 'dblp memory', 'wikipedia', 'amazon0601',
                    'frwiki', 'british airways', 'american express', 'microsoft', '']
frequent_model = ['svm', 'linear regression', 'line', 'random forest', 'decision tree',
                  'ridge regression', 'crossrank', 'rbf', 'pagerank', 'lda', 'svm-linear',
                  'imsf-average', 'svd', 'k-given model', 'polynomial regression']
frequent_metric = ['precision', 'p@1', 'accuracy', 'f1-score', 'recall', 'map', 'mae', 'top-4 acc',
                   'jaccard similarity', 'probability measure', 'mean probability', 'training time',
                   'test loss', 'runtime', 'r@10', 's@5', 'clustering coefficient', 'ndcg',
                   'hammingloss rankingloss', 'top-10 acc', 'top-k']
