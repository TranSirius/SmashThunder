from flask import Blueprint
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import request
from flask import current_app as app

import sqlalchemy
import elasticsearch as es

from web.db import databases
from web.db import datamodels
from web.db.datamodels import User, Album, Photo

import os
import time
import datetime

mod = Blueprint('search', __name__, url_prefix = '/search')

@mod.route('/user')
def searchUser():
    pass

@mod.route('/img')
def searchImg():
    pass

@mod.route('post')
def searchPost():
    pass