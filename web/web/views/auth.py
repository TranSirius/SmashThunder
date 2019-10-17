from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import session
from flask import g
from flask import redirect
from flask import url_for

mod = Blueprint('auth', __name__, url_prefix = '/auth')

mod.add_url_rule("/", endpoint = "login")

@mod.before_app_request
def loadLoggedUser():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = user_id

@mod.route('/register')
def register():
    return 'register'

@mod.route('/login')
def login():
    if g.user is not None:
        return redirect(url_for("index"))
    return 'login'
