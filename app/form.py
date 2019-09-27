# -*- coding: utf-8 -*-
# @Time    : 2019-09-27 14:10
# @Author  : Wei Peng
# @FileName: form.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed


class FileForm(FlaskForm):
    page = StringField('page', validators=[DataRequired()])
    file = FileField('file', validators=[FileRequired(), FileAllowed(['pdf'])])


class RemarkForm(FlaskForm):
    textarea = StringField('textarea', validators=[DataRequired()])
    select = IntegerField('select', validators=[DataRequired()])
    filename = StringField('filename', validators=[DataRequired()])
