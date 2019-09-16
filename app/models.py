from flask_sqlalchemy import SQLAlchemy
from app import db


class Tableuni(db.Model):
    __tablename__ = "Tableuni"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dataset = db.Column(db.String(32))
    method = db.Column(db.String(32))
    metric = db.Column(db.String(32))
    score = db.Column(db.Float)
    filename = db.Column(db.String(32))

    def __init__(self, dataset, method, metric, score, filename):
        self.dataset = dataset
        self.method = method
        self.metric = metric
        self.score = score
        self.filename = filename

