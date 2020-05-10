# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

# Python modules
import os

# Flask modules
from flask import render_template, request, url_for, redirect, send_from_directory
from flask_login import login_user, logout_user, current_user

# App modules
from app import app, lm, bc
from app.forms import LoginForm, RegisterForm, CreateUserForm
from app.models import User
from app.apis import get_all_users


# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Logout user
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('index'))


# Register a new user
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    # declare the Registration Form
    form = RegisterForm(request.form)

    msg = None

    if request.method == 'GET':
        return render_template('pages/register.html', form=form, msg=msg)

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str)
        email = request.form.get('email', '', type=str)
        name = request.form.get('name')
        mobile = request.form.get('mobile')
        gender = request.form.get('gender')
        age = request.form.get('age')

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'Error: User exists!'

        else:

            pw_hash = bc.generate_password_hash(password)

            user = User(name, username, mobile, gender, age, email, pw_hash)

            user.save()

            msg = 'User created, please <a href="' + url_for('login') + '">login</a>'

    else:
        msg = 'Input error'

    return render_template('pages/register.html', form=form, msg=msg)


# Register a new user
@app.route('/user', methods=['POST'])
def create_user():
    # declare the Registration Form
    form = CreateUserForm(request.form)
    # check if both http method is POST and form is valid on submit
    if form:
        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str)
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        mobile = request.form.get('mobile')
        address = request.form.get('address')
        roles = request.form.getlist('roles[]')

        # filter User out of database through username
        user = User.query.filter_by(username=username).first()

        if user:
            msg = 'Error: User exists!'

        else:

            pw_hash = bc.generate_password_hash(password)

            user = User(first_name, last_name, mobile, username, pw_hash, address, roles)

            user.save()

            msg = 'Success'

    else:
        msg = 'Input error'

    return {"msg": msg}


# Authenticate user
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    # Declare the login form
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str)

        # filter User out of database through username
        user = User.query.filter_by(username=username).first()

        if user:

            if bc.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unknown user"

    return render_template('pages/login.html', form=form, msg=msg)


@app.route('/users', methods=['GET'])
def get_users():
    user_query = request.args.get('q')
    return get_all_users(user_query)


@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()


# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    content = None

    try:

        # @WIP to fix this
        # Temporary solution to solve the dependencies
        if path.endswith(('.png', '.svg' '.ttf', '.xml', '.ico', '.woff', '.woff2')):
            return send_from_directory(os.path.join(app.root_path, 'static'), path)

            # try to match the pages defined in -> pages/<input file>
        return render_template('pages/' + path)

    except:

        return render_template('layouts/auth-default.html',
                               content=render_template('pages/404.html'))
