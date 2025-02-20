from flask import Flask
from datamanager.data_models import db
import os

def create_app():
    """Application Factory: Erstellt und konfiguriert die Flask-App."""
    template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
    app = Flask(__name__, template_folder=template_folder, static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static'))

    # Konfiguration der App
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviweb_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialisiere SQLAlchemy mit der App
    db.init_app(app)

    # Tabellen erstellen (optional, beim ersten Start)
    with app.app_context():
        db.create_all()

    return app
