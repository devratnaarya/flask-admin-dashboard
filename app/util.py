# -*- encoding: utf-8 -*-
"""
Flask Boilerplate
Author: AppSeed.us - App Generator 
"""
import datetime

from flask import json

from app import app, db


# build a Json response
def response(data):
    return app.response_class(response=json.dumps(data),
                              status=200,
                              mimetype='application/json')


def g_db_commit():
    db.session.commit()


def g_db_add(obj):
    if obj:
        db.session.add(obj)


def g_db_del(obj):
    if obj:
        db.session.delete(obj)


def date_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
