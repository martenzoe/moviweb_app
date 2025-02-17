from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Eindeutige Benutzer-ID
    name = db.Column(db.String(100), nullable=False)  # Name des Benutzers (Pflichtfeld)
    movies = db.relationship('Movie', backref='user', lazy=True)  # Beziehung zu Movie

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Eindeutige Film-ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Fremdschlüssel zu User
    name = db.Column(db.String(200), nullable=False)  # Name des Films (Pflichtfeld)
    director = db.Column(db.String(100), nullable=True)  # Regisseur des Films (Pflichtfeld)
    year = db.Column(db.Integer, nullable=True)  # Erscheinungsjahr des Films (Pflichtfeld)
    rating = db.Column(db.Float, nullable=True)  # Bewertung des Films (z. B. 8.5)

class UserMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Eindeutige ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Fremdschlüssel zu User
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)  # Fremdschlüssel zu Movie
