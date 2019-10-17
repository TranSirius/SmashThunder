from flask import Flask
from flask import Flask, session, g, render_template

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config = True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    @app.route('/')
    def index():
        return "index"

    from web import databases
    databases.registerInitDatabase(app)
    databases.registerDropDatabase(app)

    from web.views import auth
    app.register_blueprint(auth.mod)
    
    return app