# -*- coding: utf-8 -*-
# @Time    : 2019-08-26 22:56
# @Author  : Wei Peng
# @FileName: views.py

from flask import request, render_template, flash
from werkzeug.utils import secure_filename
import os
from app import app
import tableuni
import uuid


@app.route('/upload', methods=['POST'])
def upload_file():
    f = request.files["file"]
    basepath = os.path.dirname(__file__)
    upload_path = basepath + app.config["UPLOAD_FOLDER"]
    print(upload_path)
    upload_path = os.path.join(upload_path, secure_filename(f.filename))
    id = str(uuid.uuid1())
    pdf_path = upload_path.split(".")[0] + "-" + id + ".pdf" # the unique name of the file
    f.save(pdf_path)
    csv_path = upload_path.split(".")[0] + "-" + id + ".csv"
    # open(csv_path, "w")
    png_path = upload_path.split(".")[0] + "-" + id + ".png"
    # open(png_path, "w")
    table = tableuni.with_table(pdf_path, "/Users/pengwei/PycharmProjects/Hao-Project/app/static/uploads/test.csv", "/Users/pengwei/PycharmProjects/Hao-Project/app/static/uploads/table.png")
    # print(type(table))
    # print(table)
    # print(table.index.values[0])
    flash('Your file has been uploaded!', 'success')
    return render_template('index.html', show=True, table=table)


@app.route('/', methods=['GET', "POST"])
def index():
    print("hello")
    flash('Hello, test flash', 'success')
    return render_template('index.html', show=False, table=None)
