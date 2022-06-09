"""
Main Application package.
"""
import os
from flask import Flask
# from application.db_config import init_db


def register_blueprints(app):
    """
    This function registers flask blueprints to flask application
    """
    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return None


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRETKEY'
basedir = os.path.abspath(os.path.dirname(__file__))
register_blueprints(app)

def get_app():
    """
    this function returns Flask Application
    """
    return app
