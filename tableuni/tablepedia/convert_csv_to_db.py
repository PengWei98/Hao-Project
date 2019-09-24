import sys
import os

CUR_DIR = os.path.dirname((os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(CUR_DIR)
sys.path.append(BASE_DIR)

import pandas as pd 
import pickle
from pandas import DataFrame
from collections import Counter
from collections import defaultdict
from constants.hyperParameter import *

g = open(os.path.join(CUR_DIR, 'groundtruth.pkl'), 'rb')
CONCEPT_TRUTH_DICT = pickle.load(g)

def is_number(tableCell):
    stringCell = str(tableCell)
    nums = any(i for i in stringCell if 48 <= ord(i) <= 57)
    letters = any(i for i in stringCell
    # print(nums, letters)
    return nums and (not letters)


def firstCell(df):
    nums = [(i, j) for i in range(df.shape[0]) for j in range(df.shape[1]) if is_number(df.iloc[i, j])]
    sortedNums = sorted(nums, key=lambda x: x[0] + x[1])
    firstRow, firstCol = -1, -1
    for item in sortedNums:
        if item[0] <= 2 and item[1] <= 2:
            firstRow, firstCol = item
            break
    
    return firstRow, firstCol


def get_set_type(iterable):
    
    return [CONCEPT_TRUTH_DICT.get(i.lower()) for i in iterable]
    

def lowercase_df(df):
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            df.iloc[i, j] = df.iloc[i, j].lower()
    
    return df


def get_cell_list(df, firstRow, firstCol, i, j):
    cellDict = defaultdict(str)
    for m in range(firstRow):
        cellDict[singleDict[df.iloc[m, j]]] += df.iloc[m, j]

    for n in range(firstCol):
        cellDict[singleDict[df.iloc[i, n]]] += df.iloc[i, n]
    
    return cellDict


def get_single_dict(df, firstRow, firstCol):
    singleDict = defaultdict(int)

    if firstRow == firstCol == 1:
        setA = set([df.iloc[i, 0] for i in range(firstRow, df.shape[0])])
        setB = set([df.iloc[0, j] for j in range(firstCol, df.shape[1])])
        typeA = Counter([i for i in get_set_type(setA) if i]).most_common(1)
        typeB = Counter([i for i in get_set_type(setB) if i]).most_common(1)
        typeA, typeB = typeA[0][0], typeB[0][0]
        
        for i in setA: singleDict[i] = typeA 
        for j in setB: singleDict[j] = typeB

    if firstRow == 1 and firstCol == 2:
        setA = set([df.iloc[i, 0] for i in range(firstRow, df.shape[0])])
        setB = set([df.iloc[0, j] for j in range(firstCol, df.shape[1])])
        setC = set([df.iloc[k, 1] for k in range(firstCol, df.shape[0])])
        typeA = Counter([i for i in get_set_type(setA) if i]).most_common(1)
        typeB = Counter([i for i in get_set_type(setB) if i]).most_common(1)
        typeC = Counter([i for i in get_set_type(setC) if i]).most_common(1)

        typeA, typeB, typeC = typeA[0][0], typeB[0][0], typeC[0][0]
        
        for i in setA: singleDict[i] = typeA 
        for j in setB: singleDict[j] = typeB
        for k in setC: singleDict[k] = typeC

    if firstRow == 2 and firstCol == 1:
        setA = set([df.iloc[i, 0] for i in range(firstRow, df.shape[0])])
        setB = set([df.iloc[0, j] for j in range(firstCol, df.shape[1])])
        setC = set([df.iloc[1, k] for k in range(firstCol, df.shape[1])])
        typeA = Counter([i for i in get_set_type(setA) if i]).most_common(1)
        typeB = Counter([i for i in get_set_type(setB) if i]).most_common(1)
        typeC = Counter([i for i in get_set_type(setC) if i]).most_common(1)

        typeA, typeB, typeC = typeA[0][0], typeB[0][0], typeC[0][0]
        
        for i in setA: singleDict[i] = typeA 
        for j in setB: singleDict[j] = typeB
        for k in setC: singleDict[k] = typeC

    if firstRow == 2 and firstCol == 2:
        setA = set([df.iloc[i, 0] for i in range(firstRow, df.shape[0])])
        setB = set([df.iloc[0, j] for j in range(firstCol, df.shape[1])])
        setC = set([df.iloc[1, k] for k in range(firstCol, df.shape[1])])
        setD = set([df.iloc[l, 1] for l in range(firstCol, df.shape[0])])
        typeA = Counter([i for i in get_set_type(setA) if i]).most_common(1)
        typeB = Counter([i for i in get_set_type(setB) if i]).most_common(1)
        typeC = Counter([i for i in get_set_type(setC) if i]).most_common(1)
        typeD = Counter([i for i in get_set_type(setD) if i]).most_common(1)

        typeA, typeB, typeC, typeD = typeA[0][0], typeB[0][0], typeC[0][0], typeD[0][0]
        
        for i in setA: singleDict[i] = typeA 
        for j in setB: singleDict[j] = typeB
        for k in setC: singleDict[k] = typeC
        for l in setD: singleDict[l] = typeD

    return singleDict


def get_db_list(df, firstRow, firstCol):
    db_list = []
    for i in range(firstRow, df.shape[0]):
        for j in range(firstCol, df.shape[1]):
            cellDict = get_cell_list(df, firstRow, firstCol, i, j)
            db_list.append([fileName, cellDict[1], cellDict[2], cellDict[3], df.iloc[i, j]])
            # print(cellDict)
    return db_list

