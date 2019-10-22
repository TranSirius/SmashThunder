from flask import Flask
from flask import Flask, session, g, render_template, send_file

from datetime import timedelta

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config = True)
    app.permanent_session_lifetime = timedelta(minutes = 10)
    app.config['SECRET_KEY'] = 'ZEOAOWEHFKLDSF'

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    

    @app.errorhandler(404)
    def not_found(error):
        return send_file('templates/index.html')

    @app.route('/')
    def index():
        return send_file('templates/index.html')

    from web import databases
    databases.registerInitDatabase(app)
    databases.registerDropDatabase(app)

    from web.views import auth
    app.register_blueprint(auth.mod)

    from web.views import parse
    app.register_blueprint(parse.mod)
    
    return app
