import sys
import os

CUR_DIR = os.path.dirname((os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(CUR_DIR)
sys.path.append(BASE_DIR)

from convert_csv_to_db import *
from convert_pdf_to_csv import *


# Input 1.1: pdf path should be set by user (download from user upload)
# Input 1.2: pdf table page should be set by user (download from user input)
pdf_path = os.path.join(CUR_DIR, 'toy_data', 'kdd18_paper_352.pdf')
page = 6

# Input 2: csv path should be set by ourselves (all should be kept in disk)
# Input 3: png path should be set by ourselves (could be deleted after operation)
# Input 4: db path should be set by ourselves (a complete db should be kept in disk)
csv_path = os.path.join(CUR_DIR, 'toy_data', 'kdd18_paper_352.csv')
png_path = os.path.join(CUR_DIR, 'toy_data', 'kdd18_paper_352.png')
db_path = os.path.join(CUR_DIR, 'toy_data', 'kdd18_paper_352_db.csv')

fileName = os.path.basename(pdf_path)

# Step 1: Input a pdf and page, output csv & png
df = with_table(pdf_path, csv_path, page, png_path)

# Evaluation 1: Quality of extracted table
print(df)

# Step 2: Input csv, output db(csv type)
df = with_db(csv_path, db_path)

# Evaluation 2: Quality of db
print(DataFrame(df))
