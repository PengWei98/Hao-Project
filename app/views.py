# -*- coding: utf-8 -*-
# @Time    : 2019-08-26 22:56
# @Author  : Wei Peng
# @FileName: views.py

from flask import request, render_template, flash, jsonify
from werkzeug.utils import secure_filename
import os
from app import app
import uuid
import pandas as pd
from app import db
from app.models import *
from app.form import *
from tablepedia import convert_csv_to_db
from tablepedia import convert_pdf_to_csv


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
    open(csv_path, "w")
    png_path = upload_path.split(".")[0] + "-" + id + ".png"
    open(png_path, "w")
    table = convert_pdf_to_csv.with_table(pdf_path, csv_path,
                                          png_path, 6)
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
    print(table_json)

    return jsonify(table_json)


@app.route('/remark', methods=['POST'])
def remark():
    print("remark")
    form = RemarkForm()
    result = {}
    if form.validate_on_submit():
        comment = form.textarea.data
        remark = form.select.data
        filename = form.filename.data
        filename = filename.split("/")[-1]
        print(filename)
        db.session.add(Evaluation(comment, remark, filename))
        db.session.commit()
        result["result"] = "1"
        return jsonify(result)
    else:
        result["result"] = "0"
        return jsonify(result)


@app.route('/db_table', methods=['GET'])
def get_db_table():
    form = RemarkForm()
    id = request.args.get("id")
    csv_path = id + ".csv"
    table = pd.read_csv(csv_path, encoding='utf-8',
                        header=-1)
    db_table = convert_csv_to_db.with_db(csv_path, "db.txt")
    for row_id in db_table.index:
        row = db_table.loc[row_id].values
        db.drop_all()
        db.create_all()
        db.session.commit()
        db.session.add(Tableuni(row[0], row[1], row[2], row[3], row[4]))
        db.session.commit()
        print(row)
        # test
        break
        #
    print(db_table)
    return render_template('index.html', state=2, db_table=db_table, form=form, id=id)


@app.route('/', methods=['GET', "POST"])
@app.route('/index', methods=['GET', "POST"])
def index():
    state = request.args.get("state")
    if state is not None:
        return render_template('index.html', state=1, db_table=None)
    return render_template('index.html', state=0, db_table=None)
