"""
Main Application package.
"""
from flask import Flask
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker
)
from flask_login import LoginManager
from sqlalchemy.ext.declarative import declarative_base
from .settings.database.config import init_connection_engine
import json
from from_root import from_root

# secrets will store all configurations and credentials from secret.json
secrets = {}

# reading secret.json
with open(from_root('secret.json'), 'r') as c:
    secrets = json.loads(c.read())


# Application Configuration
app = None
login_manager = LoginManager()
engine = init_connection_engine()
sessiondb = scoped_session(sessionmaker(bind=engine))()
Base = declarative_base()


def register_blueprints(app):
    """
    This function registers flask blueprints to flask application
    """
    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return None


def create_app():
    """
    this function create Flask Application
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secrets['secret_key']
    login_manager.init_app(app)
    register_blueprints(app)
    return app
