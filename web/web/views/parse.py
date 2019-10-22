import pypandoc as pdc

from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import request

from web import databases

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

mod = Blueprint('parse', __name__, url_prefix = '/parse')

mod.route('/', methods = ['POST'])