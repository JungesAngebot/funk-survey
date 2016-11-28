from importlib import import_module

from flask import Flask
from flask.ext.cors import CORS
from flask.ext.reggie import Reggie

from survey import APP_ROOT, login_manager
from survey.blueprints import all_blueprints


def create_app():
    """ Creates an instance of the flask micro framework.

    The Flask instance will be configured here. All blueprints of the application will be added here, and
    also the common header information will be set here.
    To measure performance of each function the app will also get a middleware profiler. This enables
    the python env, to measure each function call. This is used to detect bottle necks in the app.
    """
    app = Flask(__name__, static_folder=APP_ROOT + '/static', static_url_path='/static', template_folder=APP_ROOT + '/templates')
    app.secret_key = 'bit_lake_survey_key'
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    Reggie(app)
    register_blueprints(app)
    login_manager.init_app(app)
    return app


def register_blueprints(app):
    """ Registers all blueprints in the application to the flask instance.

    Blueprints are stored in the blueprints module as tuple. Every blueprint will be registered here, and
    the view module for each blueprint will be imported.
    """
    for bp in all_blueprints:
        import_module(bp.import_name)
        app.register_blueprint(bp)
