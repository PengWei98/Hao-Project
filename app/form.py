# -*- coding: utf-8 -*-
# @Time    : 2019-09-27 14:10
# @Author  : Wei Peng
# @FileName: form.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class RemarkForm(FlaskForm):
    # username = StringField('Username', validators=[DataRequired()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # remember_me = BooleanField('Remember Me')
    # submit = SubmitField('Sign In')
    textarea = StringField('textarea', validators=[DataRequired()])
    select = IntegerField('select', validators=[DataRequired()])
    filename = StringField('filename', validators=[DataRequired()])
