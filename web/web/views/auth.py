from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import request
from flask import current_app as app

from web.db import datamodels
from web.db import databases

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

import os
import time
import datetime
import functools

mod = Blueprint('auth', __name__, url_prefix = '/auth')

@mod.before_app_request
def loadLoggedUser():
    user_id = session.get("ID")
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
        datamodels.User.generateUser(username = username, password = password)
        try:
            session.clear()
        except:
            pass

        session['ID'] = g.user_id
        session.permanent = True

        ret['status'] = 'ok'
        db_session.commit()
        return ret
    else:
        ret['status'] = "User already exists"
        return ret
    

@mod.route('/login', methods = ['POST'])
def login():
    ret = dict()
    session.clear()

    try:
        username = request.json['username']
        password = request.json['password']
    except KeyError:
        ret['status'] = 'Login Request Error!'
        return ret
    
    db_session = databases.db_session()
    user = db_session.query(databases.User).filter_by(user_name = username).first()

    if user is None:
        ret['status'] = 'User not exists!'
        return ret
    elif not check_password_hash(user.pass_word, password):
        ret['status'] = 'Password error!'
        return ret

    session['ID'] = user.ID
    session.permanent = True
    
    ret['status'] = 'ok'
    return ret

@mod.route('/autoLogin', methods = ['POST'])
def autoLogin():
    ret = dict()
    user_id = session.get('ID')
    if user_id is None:
        ret['status'] = 'error'
        return ret
    
    db_session = databases.db_session()
    user = db_session.query(databases.User).filter_by(ID = user_id).first()

    if user is None:
        ret['status'] = 'error'
        return ret
    
    ret['status'] = 'ok'
    ret['username'] = user.user_name
    return ret

@mod.route('/logout', methods = ['POST'])
def logout():
    ret = dict()
    try:
        session.clear()
    except:
        ret['status'] = 'You have logged out already'
        return ret

    ret['status'] = 'ok'
    return ret
    