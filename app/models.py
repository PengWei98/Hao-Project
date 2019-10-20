from flask_sqlalchemy import SQLAlchemy
from app import db
import datetime


class Tableuni(db.Model):
    __tablename__ = "Tableuni"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dataset = db.Column(db.String(64))
    method = db.Column(db.String(64))
    metric = db.Column(db.String(64))
    score = db.Column(db.String(64))
    filename = db.Column(db.String(64))

    def __init__(self, dataset, method, metric, score, filename):
        self.dataset = dataset
        self.method = method
        self.metric = metric
        self.score = score
        self.filename = filename


class Evaluation(db.Model):
    __tablename__ = "Evaluation"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(128))
    remark = db.Column(db.INT)
    time = db.Column(db.DateTime, default=datetime.datetime.now())
    time = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, comment, remark):
        self.comment = comment
        self.remark = remark


class Feedback(db.Model):
    __tablename__ = "Feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(64))
    path = db.Column(db.String(128))
    correctness = db.Column(db.Boolean)
    reason = db.Column(db.String(64))
    comment = db.Column(db.String(128))
    remark = db.Column(db.INT)

    def __init__(self, filename, path, correctness, reason, comment, remark):
        self.path = path
        self.correctness = correctness
        self.reason = reason
        self.comment = comment
        self.remark = remark
        self.filename = filename
