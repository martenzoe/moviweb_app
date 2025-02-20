"""
This module initializes the Flask application and sets up the database.
"""

import os
from flask import Flask
from datamanager.data_models import db


def create_app():
    """
    Application Factory: Creates and configures the Flask app.

    Returns:
        Flask: The configured Flask application instance.
    """
    template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
    static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static')

    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

    # App configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviweb_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Create tables (optional, on first start)
    with app.app_context():
        db.create_all()

    return app