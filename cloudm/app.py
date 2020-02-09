from flask import Flask

from cloudm.api.api_docs import init_docs
from cloudm.api.api_response import ApiResponse
from cloudm.exception import APIException, exception_handler
from cloudm.extensions import db, jwt, apispec
from cloudm.api.urls import blueprint as cloudm_bp
from flask_cors import CORS


def create_app(testing=False, cli=False):
    """Application factory, used to create application
    """
    app = Flask("cloudm")
    app.config.from_object("cloudm.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app, cli)
    register_blueprints(app)
    configure_apispec(app)
    CORS(app, resources={r"*": {"origins": "*"}})
    register_errorhandlers(app)

    return app


def configure_extensions(app, cli):
    """configure flask extensions
    """
    db.init_app(app)
    jwt.init_app(app)


def configure_apispec(app):
    """Configure APISpec for swagger support
    """
    init_docs(app)


def register_blueprints(app):
    """register all blueprints for application
    """
    # app.register_blueprint(auth.views.blueprint)
    # app.register_blueprint(api.views.blueprint)
    app.register_blueprint(cloudm_bp)


def register_errorhandlers(app):
    """Register error handlers."""

    app.register_error_handler(APIException, exception_handler)
