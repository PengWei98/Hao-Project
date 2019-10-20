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
import pandas


@app.route('/upload', methods=['POST'])
def upload_file():
    fileform = FileForm()
    table_json = {}
    if fileform.validate_on_submit():
        f = fileform.file.data
        page = fileform.page.data
        print("page:")
        page = int(page)
        if page == 0:
            page = "all"
        print(page)
        # f = request.files["file"]
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
                                              png_path, page)
        print("table:")
        print(type(table))
        print(type(type(table)))
        if isinstance(table, pandas.core.frame.DataFrame):
            print(table.index.values[0])
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
    table_json["table"] = []
    table_json["id"] = "error"
    return jsonify(table_json)


@app.route('/remark', methods=['POST'])
def remark():
    form = RemarkForm()
    result = {}
    if form.validate_on_submit():
        print("begin your remark!")
        comment = form.textarea.data
        remark = form.select.data
        # filename = form.filename.data
        # txt_path = filename + ".txt"
        # print(txt_path)
        # filename = filename.split("/")[-1][:-37]
        # print(filename)
        # with open(txt_path, "r") as fr:
        #     for line in fr:
        #         row = line.split(",")
        #         print(row)
        #         if remark >= 3:
        #             db.session.add(Tableuni(row[0].replace(" ", ""), row[1].replace(" ", ""), row[2].replace(" ", ""),
        #                                     row[3].replace(" ", ""), filename))
        #             db.session.commit()
        # basepath = os.path.dirname(__file__)
        # upload_path = basepath + app.config["UPLOAD_FOLDER"]

        # upload_path = os.path.join(upload_path, filename)
        # print(upload_path)
        # db.session.add(Feedback(filename, upload_path + ".pdf", True, "", comment, remark))
        db.session.add(Evaluation(comment, remark))
        db.session.commit()
        result["result"] = "1"
        return jsonify(result)
    else:
        print("oh sorry!")
        result["result"] = "0"
        return jsonify(result)


@app.route('/db_table', methods=['GET'])
def get_db_table():
    remarkform = RemarkForm()
    fileform = FileForm()
    id = request.args.get("id")

    good_remarks = Feedback.query.filter(Feedback.remark >= 3).all()
    remark_num = len(good_remarks)
    if id is None or id == "":
        return render_template('index.html', state=0, db_table=None, remarkform=remarkform, fileform=fileform, good_remarks=good_remarks,
                               remark_num=remark_num)

    csv_path = id + ".csv"
    table = pd.read_csv(csv_path, encoding='utf-8',
                        header=-1)
    txt_path = id + ".txt"
    open(txt_path, "w")
    db_table = convert_csv_to_db.with_db(csv_path, txt_path)
    for row_id in db_table.index:
        row = db_table.loc[row_id].values
        row[4] = row[4][:-41]  # remove uuid code

        db.session.add(Tableuni(row[0].replace(" ", ""), row[1].replace(" ", ""), row[2].replace(" ", ""), row[3].replace(" ", ""), row[4].replace(" ", "")))
        db.session.commit()
        # print(row)
        # test
        # break
        #
    # print(db_table)

    return render_template('index.html', state=2, db_table=db_table, remarkform=remarkform, id=id, fileform=fileform,
                           good_remarks=good_remarks,
                           remark_num=remark_num)


@app.route('/wrong_table', methods=['GET'])
def get_feedback():
    id = request.args.get("id")
    fileform = FileForm()
    remarkform = RemarkForm()
    good_remarks = Feedback.query.filter(Feedback.remark >= 3).all()
    remark_num = len(good_remarks)
    return render_template('index.html', state=1, db_table=None, remarkform=remarkform, fileform=fileform, id=id, good_remarks=good_remarks,
                           remark_num=remark_num)


@app.route('/feedback', methods=['POST'])
def feedback():
    # id = request.args.get("id")
    fileform = FileForm()
    remarkform = RemarkForm()
    if request.method == "POST":
        reason = request.values.get("customRadio")
        print(reason)
        id = request.values.get("filepath")
        print(id)
        filename = id.split("/")[-1][:-37]
        print(filename)
        path = id + ".pdf"
        # db.drop_all()
        # db.create_all()
        # db.session.commit()
        db.session.add(Feedback(filename, path, False, reason, "", -1))
        db.session.commit()
        good_remarks = Feedback.query.filter(Feedback.remark >= 3).all()
        remark_num = len(good_remarks)
    return render_template('index.html', state=0, db_table=None, remarkform=remarkform, fileform=fileform, good_remarks=good_remarks,
                           remark_num=remark_num)


@app.route('/search1', methods=['GET'])
def search1():
    text = request.args.get("text")
    print("text:")
    print(text)
    methods = set()
    results = Tableuni.query.filter_by(dataset=text).all()
    for result in results:
        if result.method.replace(" ", "") != "":
            methods.add(result.method)
    for method in methods:
        print(method)
    json = {}
    json["methods"] = list(methods)
    print(json)
    return jsonify(json)


@app.route('/search2', methods=['GET'])
def search2():
    text = request.args.get("text")
    print("text:")
    print(text)
    metrics = set()
    results = Tableuni.query.filter_by(dataset=text).all()
    for result in results:
        if result.metric.replace(" ", "") != "":
            metrics.add(result.metric)
    print(metrics)
    json = {}
    json["metrics"] = list(metrics)
    print(json)
    return jsonify(json)


@app.route('/search3', methods=['GET'])
def search3():
    text = request.args.get("text")
    print("text:")
    print(text)
    sources = set()
    results = Tableuni.query.filter_by(dataset=text).all()
    print("len:" + str(len(results)))
    for result in results:
        if result.filename.replace(" ", "") != "":
            # print("replace" + result.filename.replace(" ", ""))
            print("filename:")
            print(result.filename)
            sources.add(result.filename)
    print(sources)
    datasets = set()
    for filename in sources:
        results = Tableuni.query.filter_by(filename=filename)
        for result in results:
            if result.dataset.replace(" ", "") != "":
                datasets.add(result.dataset)
    json = {}
    json["datasets"] = list(datasets)
    print(json)
    return jsonify(json)


@app.route('/search4', methods=['GET'])
def search4():
    text1 = request.args.get("text1")
    text2 = request.args.get("text2")
    text3 = request.args.get("text3")
    method_score = []
    results = Tableuni.query.filter_by(dataset=text2).filter_by(metric=text3).order_by(
        db.desc(Tableuni.score)).all()
    for result in results:
        if result.method.replace(" ", "") != "":
            method_score.append((result.method, result.score))
            if len(method_score) == int(text1):
                break
    json = {}
    json["method_score"] = method_score
    print(json)
    return jsonify(json)


# dump
@app.route('/dump', methods=['GET'])
def dump():
    basepath = os.path.dirname(__file__)
    fileform = FileForm()
    remarkform = RemarkForm()
    # upload_path = basepath + app.config["UPLOAD_FOLDER"]
    f = open(basepath + '/tablepedia_db.txt', 'r')
    lines = [line.strip('\n').split('\t') for line in f]
    for row in lines:
        filename = row[0][:-4]
        print(filename)
        db.session.add(Tableuni(row[1].replace(" ", ""), row[2].replace(" ", ""), row[3].replace(" ", ""),
                                row[4].replace(" ", ""), filename))
        db.session.commit()
    # print(lines)
    good_remarks = Feedback.query.filter(Feedback.remark >= 3).all()
    remark_num = len(good_remarks)
    return render_template('index.html', state=0, db_table=None, remarkform=remarkform, fileform=fileform, good_remarks=good_remarks,
                           remark_num=remark_num)


@app.route('/', methods=['GET', "POST"])
@app.route('/index', methods=['GET', "POST"])
def index():
    # db.drop_all()
    # db.create_all()
    # db.session.commit()
    fileform = FileForm()
    remarkform = RemarkForm()
    state = request.args.get("state")

    good_remarks = Evaluation.query.filter(Evaluation.remark >= 3).all()
    remark_num = len(good_remarks)

    good_remarks.sort(key=lambda x:x.time, reverse=True)
    print(good_remarks)

    if state is not None:
        return render_template('index.html', state=1, db_table=None, remarkform=remarkform, fileform=fileform, good_remarks=good_remarks,
                               remark_num=remark_num)
    return render_template('index.html', state=0, db_table=None, remarkform=remarkform, fileform=fileform, good_remarks=good_remarks,
                           remark_num=remark_num)
