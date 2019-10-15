from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import session
from flask import g

mod = Blueprint('authentication', __name__, url_prefix = '/auth')

@mod.route('/index')
def index():
    return 'hello_world'

@mod.before_app_request
def loadLoggedUser():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = user_id