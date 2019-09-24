# Created by yuwenhao at 19/02/2019
"""
Feature: #Enter feature name here
# Enter feature description here
Scenario: #Enter scenario name here
# Enter steps here
Test File Location: # Enter]
"""

# import PyPDF2
#
# PDFfilename = ''
# pfr = PyPDF2.PdfFileReader(open(PDFfilename, "rb")) #PdfFileReader object
#
# pg6 = pfr.getPage(5)  # extract pg 6
#
# writer = PyPDF2.PdfFileWriter()  # create PdfFileWriter object
# # add pages
# writer.addPage(pg6)
# NewPDFfilename = ''  # filename of your PDF/directory where you want your new PDF to be
# with open(NewPDFfilename, "wb") as outputStream:  # create new PDF
#     writer.write(outputStream)  # write pages to new PDF

import sys
import os

CUR_DIR = os.path.dirname((os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(CUR_DIR)
sys.path.append(BASE_DIR)

# install tabula-py not tabula
# sudo pip install tabula-py
import tabula
import math

import pandas as pd
import numpy as np

from collections import Counter

from pandas import DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import six


def render_mpl_table(data, header, col_width=1.0, row_height=0.8, font_size=20, header_color='whitesmoke',
                     row_colors=['#f1f1f2', 'w'], edge_color='grey', bbox=[0, 0, 1, 1], ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, cellLoc='center')
    mpl_table.set_fontsize(font_size)

    for index, (k, cell) in enumerate(six.iteritems(mpl_table._cells)):
        cell.set_edgecolor(color=edge_color)
        if k[0] < header[0] and k[1] < header[1]:
            cell.set_text_props(style='normal', weight='bold', color='black')
            cell.set_facecolor(color=header_color)

        elif k[0] >= header[0] and k[1] < header[1] - 1:
            cell.set_text_props(color='black')
            cell.set_facecolor(color='sandybrown')
        elif k[0] >= header[0] and header[1] - 1 <= k[1] < header[1]:
            cell.set_text_props(color='black')
            cell.set_facecolor(color='gold')

        elif k[0] < header[0] - 1 and k[1] >= header[1]:
            cell.set_text_props(color='black')
            cell.set_facecolor(color='lightgreen')
        elif header[0] - 1 <= k[0] < header[0] and k[1] >= header[1]:
            cell.set_text_props(color='black')
            cell.set_facecolor(color='skyblue')
        else:
            cell.set_facecolor(color=header_color)
    return ax


def isnan(i):
    return True if str(i) != 'nan' else False


def cleanRows(df):
    dropIndex = []
    for row in range(df.shape[0]):
        nans = [str(df.iloc[row, col]) != 'nan' for col in range(df.shape[1])]
        if Counter(nans)[True] <= 2 : dropIndex.append(row)
    return dropIndex


def longColumns(df):
    dropIndex= []
    for col in range(df.shape[1]):
        lens = [len(str(df.iloc[row, col])) > 20 for row in range(df.shape[0])
                if str(df.iloc[row, col]) != 'nan']
        if Counter(lens)[True] > 2 * Counter(lens)[False]: dropIndex.append(col)
    return dropIndex


def longRows(df):
    dropIndex= []
    for row in range(df.shape[0]):
        lens = [len(str(df.iloc[row, col])) > 20 for col in range(df.shape[1])
                if str(df.iloc[row, col]) != 'nan']
        if Counter(lens)[True] > 2 * Counter(lens)[False]: dropIndex.append(row)
    return dropIndex


def is_number(tableCell):
    stringCell = str(tableCell)
    nums = any(i for i in stringCell if 48 <= ord(i) <= 57)
    letters = any(i for i in stringCell if 65 <= ord(i) <= 90 or 97 <= ord(i) <= 122)
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


def with_table(path, out, page, png_path):
    tabula.convert_into(path, out, output_format="csv", pages='6')
    # return tabula.read_pdf(pdf_path, header=-1, pages=page)
    df = pd.read_csv(out, encoding='utf-8', header=-1)
    df = df.drop(cleanRows(df), axis=0)
    df = df.drop(longColumns(df), axis=1)
    df = df.drop(longRows(df), axis=0)
    df = move_nans(df)
    df.to_csv(out, encoding='utf-8', header=0, index=False)

    row, column = firstCell(df)
    render_mpl_table(df, header=(row, column), col_width=1.8)
    plt.savefig(png_path)
    # plt.show()
    
    return df


def move_nans(df):
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            if str(df.iloc[i, j]) == 'nan':
                df.iloc[i, j] = ' '
    print(str(df.iloc[3, 0]))
    return df






