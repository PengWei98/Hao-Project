# -*- coding: utf-8 -*-
# @Time    : 2019-08-26 22:50
# @Author  : Wei Peng
# @FileName: __init__.py

from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
# print(app.config["SECRET_KEY"])
db = SQLAlchemy(app)
db.create_all()
db.session.commit()
print("Begin!")

from app import models, views
