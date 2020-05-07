# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, DataRequired


class LoginForm(FlaskForm):
    username = StringField(u'Username', validators=[DataRequired()])
    password = PasswordField(u'Password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    name = StringField(u'Name')
    mobile = StringField(u'Mobile')
    gender = StringField(u'Gender')
    age = StringField(u'Age')
    username = StringField(u'Username', validators=[DataRequired()])
    password = PasswordField(u'Password', validators=[DataRequired()])
    email = StringField(u'Email', validators=[DataRequired(), Email()])


class CreateUserForm(FlaskForm):

    username = StringField(u'username', validators=[DataRequired()])
    password = PasswordField(u'password', validators=[DataRequired()])
    first_name = StringField(u'first_name', validators=[DataRequired()])
    last_name = StringField(u'last_name')
    mobile = StringField(u'mobile', validators=[DataRequired()])
    address = StringField(u'address')
    roles = StringField(u'roles')
