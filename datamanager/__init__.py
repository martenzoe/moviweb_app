from flask import Flask
from datamanager.data_models import db


def create_app():
    """Application Factory: Erstellt und konfiguriert die Flask-App."""
    app = Flask(__name__)

    # Konfiguration der App
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviweb_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialisiere SQLAlchemy mit der App
    db.init_app(app)

    # Tabellen erstellen (optional, beim ersten Start)
    with app.app_context():
        db.create_all()

    return app

