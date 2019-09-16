# -*- coding: utf-8 -*-
# @Time    : 2019-08-26 22:56
# @Author  : Wei Peng
# @FileName: views.py

from flask import request, render_template, flash, jsonify
from werkzeug.utils import secure_filename
import os
from app import app
import tableuni
import uuid
import pandas as pd
from app import db
from app.models import *


@app.route('/upload', methods=['POST'])
def upload_file():
    f = request.files["file"]
    basepath = os.path.dirname(__file__)
    upload_path = basepath + app.config["UPLOAD_FOLDER"]
    print(upload_path)
    upload_path = os.path.join(upload_path, secure_filename(f.filename))
    id = str(uuid.uuid1())
    pdf_path = upload_path.split(".")[0] + "-" + id + ".pdf"  # the unique name of the file
    f.save(pdf_path)
    csv_path = upload_path.split(".")[0] + "-" + id + ".csv"
    # open(csv_path, "w")
    png_path = upload_path.split(".")[0] + "-" + id + ".png"
    # open(png_path, "w")
    table = tableuni.with_table(pdf_path, "/Users/pengwei/PycharmProjects/Hao-Project/app/static/uploads/test.csv",
                                "/Users/pengwei/PycharmProjects/Hao-Project/app/static/uploads/table.png")
    # print(type(table))
    # print(table)
    print(table)
    print(table.index.values[0])
    table_json = {}
    table_json["table"] = []
    table_json["id"] = upload_path.split(".")[0] + "-" + id
    for row_id in table.index:
        row = []
        for item in table.loc[row_id].values:
            row.append(item)

        print(row)
        table_json["table"].append(row)
    # return render_template('index.html', show=True, table=table)
    print(table_json)

    return jsonify(table_json)


@app.route('/db_table', methods=['GET'])
def get_db_table():
    id = request.args.get("id")
    csv_path = id + ".csv"
    table = pd.read_csv("/Users/pengwei/PycharmProjects/Hao-Project/app/static/uploads/test.csv", encoding='utf-8',
                        header=-1)
    db_table = tableuni.with_db(table, "/Users/pengwei/PycharmProjects/Hao-Project/app/static/uploads/db.txt")
    for row_id in db_table.index:
        row = db_table.loc[row_id].values
        db.session.add(Tableuni(row[0], row[1], row[2], row[3], row[4]))
        db.session.commit()
        print(row)
    print(db_table)
    return render_template('index.html', show=True, db_table=db_table)


@app.route('/', methods=['GET', "POST"])
def index():
    return render_template('index.html', show=False, db_table=None)
