from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import session as flask_session
from flask import g
from flask import redirect
from flask import url_for
from flask import request
from flask import current_app as app

from web.db import datamodels
from web.db import databases
from web.logic import utils

import sqlalchemy

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

import os
import shutil
import time
import datetime
import functools

mod = Blueprint('auth', __name__, url_prefix = '/auth')

@mod.before_app_request
def loadLoggedUser():
    user_id = flask_session.get("ID")
    g.user_id = user_id

def loginRequest(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user_id is None:
            ret = dict()
            ret['status'] = 'please login first'
            return ret
        return view(**kwargs)
    return wrapped_view

def notBanRequest(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        db_session_instance = databases.db_session()
        user = db_session_instance\
            .query(datamodels.User)\
            .filter(User.ID == g.user_id)\
            .first()
        if user.ban:
            ret = dict()
            ret['status'] = 'You are temporarily not allowed to use this function'
            return ret
        return view(**kwargs)
    return wrapped_view

def adminRequest(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        db_session_instance = databases.db_session()
        user = db_session_instance\
            .query(datamodels.User)\
            .filter(datamodels.User.ID == g.user_id)\
            .first()
        if not (user.user_type == 'admin' or user.user_type == 'super_admin'):
            ret = dict()
            ret['status'] = 'This function was reserved for system administrator'
            return ret
        return view(**kwargs)
    return wrapped_view

@mod.route('/register', methods = ['POST'])
def register():
    ret = dict()
    try:
        username = request.json['username']
        password = request.json['password']
    except KeyError:
        ret['status'] = 'Request Error!'
        return ret
    db_session = databases.db_session()

    query_res = db_session.query(datamodels.User).filter_by(user_name = username).first()
    if query_res is None:
        try:
            datamodels.User.generateUser(username = username, password = password)
        except sqlalchemy.exc.DataError:
            ret['status'] = 'Data Format Error'
            return ret
        flask_session.clear()

        flask_session['ID'] = g.user_id
        flask_session.permanent = True

        ret['status'] = 'ok'
        return ret
    else:
        ret['status'] = "User already exists"
        return ret
    

@mod.route('/login', methods = ['POST'])
def login():
    ret = dict()
    flask_session.clear()

    try:
        username = request.json['username']
        password = request.json['password']
    except KeyError:
        ret['status'] = 'Login Request Error!'
        return ret
    
    db_session_instance = databases.db_session()
    user = db_session_instance.query(databases.User).filter_by(user_name = username).first()

    if user is None:
        ret['status'] = 'User not exists!'
        return ret
    elif not check_password_hash(user.pass_word, password):
        ret['status'] = 'Password error!'
        return ret

    flask_session['ID'] = user.ID
    flask_session.permanent = True

    login_record = datamodels.LoginActivity(user_id = user.ID, login_time = utils.CurrentTime()())
    db_session_instance.add(login_record)
    db_session_instance.commit()

    ret['status'] = 'ok'
    return ret

@mod.route('/autoLogin', methods = ['POST'])
def autoLogin():
    ret = dict()
    user_id = flask_session.get('ID')
    if user_id is None:
        ret['status'] = 'error'
        return ret
    
    db_session_instance = databases.db_session()
    user = db_session_instance.query(databases.User).filter_by(ID = user_id).first()

    if user is None:
        ret['status'] = 'error'
        return ret
    
    login_record = datamodels.LoginActivity(user_id = user.ID, login_time = utils.CurrentTime()())
    db_session_instance.add(login_record)
    db_session_instance.commit()

    ret['status'] = 'ok'
    ret['username'] = user.user_name
    return ret

@mod.route('/logout', methods = ['POST'])
def logout():
    ret = dict()
    try:
        flask_session.clear()
    except:
        ret['status'] = 'You have logged out already'
        return ret

    ret['status'] = 'ok'
    return ret
    