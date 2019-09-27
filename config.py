# -*- coding: utf-8 -*-
# @Time    : 2019-08-26 22:40
# @Author  : Wei Peng
# @FileName: config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'notre_dame'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@167.71.248.105:3306/tableuni'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = '/static/uploads'
