from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Eindeutige Benutzer-ID
    name = db.Column(db.String(100), nullable=False)  # Name des Benutzers (Pflichtfeld)
    # Many-to-Many-Beziehung zu Movie über UserMovie
    favorite_movies = db.relationship(
        'Movie',
        secondary='user_movie',  # Verknüpfung über die Zwischentabelle user_movie
        backref=db.backref('users', lazy=True),
        lazy=True
    )

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Eindeutige Film-ID
    name = db.Column(db.String(200), nullable=False)  # Name des Films (Pflichtfeld)
    director = db.Column(db.String(100), nullable=True)  # Regisseur des Films (optional)
    year = db.Column(db.Integer, nullable=True)  # Erscheinungsjahr des Films (optional)
    rating = db.Column(db.Float, nullable=True)  # Bewertung des Films (optional)

class UserMovie(db.Model):
    __tablename__ = 'user_movie'  # Name der Zwischentabelle
    id = db.Column(db.Integer, primary_key=True)  # Eindeutige ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Fremdschlüssel zu User
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)  # Fremdschlüssel zu Movie
