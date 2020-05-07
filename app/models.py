# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from app import db
from flask_login import UserMixin
from sqlalchemy.inspection import inspect

ROLE_ID_MAP = {
    "Admin": 1,
    "Account": 2,
    "Operation": 3
}

ID_ROLE_MAP = {
    1: "Admin",
    2: "Account",
    3: "Operation"
}


class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class User(UserMixin, db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    mobile = db.Column(db.String(13))
    password = db.Column(db.String(500))
    address = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    created_by = db.Column(db.String(45))
    updated_by = db.Column(db.String(45))
    roles = []

    # # Relationships
    # roles = db.relationship('Role', secondary='user_roles',
    #                         backref=db.backref('user', lazy='dynamic'))

    def __init__(self, first_name, last_name, mobile, username, password, address, roles):
        self.first_name = first_name
        self.last_name = last_name
        self.mobile = mobile
        self.username = username
        self.password = password
        self.address = address
        self.roles = roles

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.username)

    def save(self):
        # inject self into db session
        db.session.add(self)
        user = User.query.filter(User.username == self.username).first()
        for role in self.roles:
            u_r = UserRoles(user_id=user.id, role_id=ROLE_ID_MAP.get(role))
            db.session.add(u_r)
        # commit change and save the object
        db.session.commit()
        return self

    def serialize(self):
        d = Serializer.serialize(self)
        del d['password']
        return d


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
