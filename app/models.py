from flask_sqlalchemy import SQLAlchemy
from app import db


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

