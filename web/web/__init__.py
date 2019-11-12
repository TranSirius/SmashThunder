from flask import Flask, session, g, render_template, send_file
from flask import current_app

from datetime import timedelta

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config = True)
    app.permanent_session_lifetime = timedelta(minutes = 10)

    if test_config == 'debug':
        app.config.from_pyfile('config_debug.py')
    elif test_config == 'release':
        app.config.from_pyfile('config_release.py')
    elif test_config == 'backend':
        app.config.from_pyfile('config_backend.py')
    else:
        app.config.from_pyfile('config_backend.py')

    ctx = app.app_context()
    ctx.push()

    from web.db import databases
    databases.registerInitDatabase(app)
    databases.registerDropDatabase(app)

    from web.views import auth
    app.register_blueprint(auth.mod)

    from web.views import submit
    app.register_blueprint(submit.mod)

    from web.views import get
    app.register_blueprint(get.mod)

    from web.views import parse
    app.register_blueprint(parse.mod)

    return app
