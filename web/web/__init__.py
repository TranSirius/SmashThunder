from flask import Flask, session, g, render_template, send_file
from flask import current_app
from flask_cors import CORS

from datetime import timedelta

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config = True)
    cors = CORS(app, origins = r'/*', support_credentials=True)
    app.permanent_session_lifetime = timedelta(hours = 24)

    if test_config == 'debug':
        app.config.from_pyfile('config_debug.py')
    elif test_config == 'release':
        app.config.from_pyfile('config_release.py')
    else:
        app.config.from_pyfile('config_debug.py')

    ctx = app.app_context()
    ctx.push()

    from web.db import databases
    databases.registerInitDatabase(app)
    databases.registerDropDatabase(app)

    from web.index import esclient
    esclient.registerDropIndex(app)
    esclient.registerInitIndex(app)

    from web.views import auth
    app.register_blueprint(auth.mod)

    from web.views import submit
    app.register_blueprint(submit.mod)

    from web.views import get
    app.register_blueprint(get.mod)

    from web.views import edit
    app.register_blueprint(edit.mod)

    from web.views import render
    app.register_blueprint(render.mod)

    from web.views import follow
    app.register_blueprint(follow.mod)

    from web.views import star
    app.register_blueprint(star.mod)

    return app
