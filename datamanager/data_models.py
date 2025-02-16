from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)

# Tabellen erstellen
def create_tables(app):
    with app.app_context():  # Flask benötigt den Anwendungs-Kontext
        db.create_all()  # Erstellt alle Tabellen, die in den Modellen definiert sind
