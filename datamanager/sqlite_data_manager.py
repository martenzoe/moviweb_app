from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datamanager.data_models import db, User, Movie, UserMovie

class SQLiteDataManager:
    def __init__(self, db_file_name):
        self.engine = create_engine(f'sqlite:///{db_file_name}')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    # CRUD-Operationen für Benutzer
    def get_all_users(self):
        return self.session.query(User).all()

    def add_user(self, name):
        new_user = User(name=name)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    # CRUD-Operationen für Filme
    def get_all_movies(self):
        return self.session.query(Movie).all()

    def add_movie(self, name, director=None, year=None, rating=None):
        new_movie = Movie(name=name, director=director, year=year, rating=rating)
        self.session.add(new_movie)
        self.session.commit()
        return new_movie

    def update_movie(self, movie_id, **kwargs):
        """Aktualisiert die Details eines Films."""
        movie = self.session.query(Movie).get(movie_id)
        if not movie:
            return None
        for key, value in kwargs.items():
            if hasattr(movie, key):
                setattr(movie, key, value)
        self.session.commit()
        return movie

    # CRUD-Operationen für UserMovie (Beziehungstabelle)
    def add_favorite_movie(self, user_id, movie_id):
        favorite = UserMovie(user_id=user_id, movie_id=movie_id)
        self.session.add(favorite)
        self.session.commit()
        return favorite

    def get_favorite_movies_by_user(self, user_id):
        favorites = (
            self.session.query(Movie)
            .join(UserMovie)
            .filter(UserMovie.user_id == user_id)
            .all()
        )
        return favorites

    def get_users_by_favorite_movie(self, movie_id):
        users = (
            self.session.query(User)
            .join(UserMovie)
            .filter(UserMovie.movie_id == movie_id)
            .all()
        )
        return users

    def remove_favorite_movie(self, user_id, movie_id):
        favorite = (
            self.session.query(UserMovie)
            .filter_by(user_id=user_id, movie_id=movie_id)
            .first()
        )
        if favorite:
            self.session.delete(favorite)
            self.session.commit()
