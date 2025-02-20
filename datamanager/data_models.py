"""
This module defines the database models for the MovieWeb application.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, UTC

db = SQLAlchemy()

movie_genre = db.Table('movie_genre',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

class User(db.Model):
    """
    Represents a user in the system.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    favorite_movies = db.relationship('Movie', secondary='user_movie', backref=db.backref('users', lazy=True))
    reviews = db.relationship('Review', backref='user', lazy=True)

class Movie(db.Model):
    """
    Represents a movie in the system.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(50), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    poster = db.Column(db.String(255), nullable=True)
    genres = db.relationship('Genre', secondary=movie_genre, backref=db.backref('movies', lazy=True))
    reviews = db.relationship('Review', backref='movie', lazy=True)

class UserMovie(db.Model):
    """
    Represents the association between a user and their favorite movies.
    """
    __tablename__ = 'user_movie'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    date_added = db.Column(db.DateTime, default=lambda: datetime.now(UTC))

class Genre(db.Model):
    """
    Represents a movie genre.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

class Review(db.Model):
    """
    Represents a user's review of a movie.
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    date_posted = db.Column(db.DateTime, default=lambda: datetime.now(UTC))