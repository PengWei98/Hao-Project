# Demo of WWW 2020 TableUni Paper
# Created by Wenhao at Sep 12th, 2019

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from pandas import DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import six

row, column = 2, 1


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
        elif k[0] >= header[0] and k[1] < header[1]:
            cell.set_text_props(color='black')
            cell.set_facecolor(color='sandybrown')
        elif k[0] < header[0] - 1 and k[1] >= header[1]:
            cell.set_text_props(color='black')
            cell.set_facecolor(color='lightgreen')
        elif header[0] - 1 <= k[0] < header[0] and k[1] >= header[1]:
            cell.set_text_props(color='black')
            cell.set_facecolor(color='skyblue')
        else:
            cell.set_facecolor(color=header_color)
    return ax


def with_pdf(pdf_doc, pdf_pwd='', *args):
    fp = open(pdf_doc, 'rb')
    parser = PDFParser(fp)

    document = PDFDocument(parser, pdf_pwd)
    parser.set_document(document)

    if not document.is_extractable:
        print('The document does not allow text extraction.')

    print('Parsing PDF function is good!')


def with_table(pdf_doc, csv_path, png_path, pdf_pwd=''):
    # test whether pdf file could be dealt with
    with_pdf(pdf_doc, pdf_pwd)
    table = pd.read_csv(csv_path, encoding='utf-8', header=-1)
    render_mpl_table(table, header=(row, column), col_width=1.8)
    plt.savefig(png_path)
    # plt.show()
    return table


def with_db(table, db_path):
    filename = 'KDD2018-279.pdf'
    db = open(db_path, 'w')
    db.write('Dataset\tMethod\tMetric\tScore\tFileName\n'.format())
    df = []
    for i in range(row, table.shape[0]):
        for j in range(column, table.shape[1]):
            db.write(
                '{}\t{}\t{}\t{}\t{}\n'.format(table.iloc[0, j], table.iloc[1, j], table.iloc[i, 0], table.iloc[i, j],
                                              filename))
            df.append((table.iloc[0, j], table.iloc[1, j], table.iloc[i, 0], table.iloc[i, j], filename))
    return DataFrame(df)

# if __name__ == "__main__":
#
#     # 4 Paths are needed
#     # PDF path refers you should input a pdf to the 'TableUni'
#     pdf_path = '../test/test.pdf'
#     # First human-evaluation returns a png(need to give reply) and a csv(use for next step to build DB)
#     csv_path = '../test/test.csv'
#     png_path = '../test/table.png'
#     # If user thinks png is good, then input csv to build DB
#     db_path = '../test/database.txt'
#
#     # Input PDF and return png and csv
#     table = with_table(pdf_path, csv_path, png_path)
#
#     # Input csv an return DB
#     db = with_db(table, db_path)
#     print(db)
