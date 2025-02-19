from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datamanager.data_models import db, User, Movie, UserMovie, Genre, Review
from sqlalchemy.orm.exc import NoResultFound

class SQLiteDataManager:
    def __init__(self, db_file_name):
        self.engine = create_engine(f'sqlite:///{db_file_name}')
        db.metadata.create_all(self.engine)  # Stelle sicher, dass die Tabellen erstellt werden
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

    def get_user_by_id(self, user_id):
        """Holt einen Benutzer anhand seiner ID aus der Datenbank."""
        user = self.session.query(User).filter_by(id=user_id).first()
        return user

    # CRUD-Operationen für Filme
    def get_all_movies(self):
        return self.session.query(Movie).all()

    def add_movie(self, name, director=None, year=None, rating=None, poster=None, genres=[]):
        new_movie = Movie(name=name, director=director, year=year, rating=rating, poster=poster)
        for genre in genres:
            new_movie.genres.append(genre)
        self.session.add(new_movie)
        self.session.commit()
        return new_movie

    def get_movie_by_id(self, movie_id):
        """Holt einen Film anhand seiner ID aus der Datenbank."""
        return self.session.query(Movie).get(movie_id)

    def update_movie(self, movie_id, **kwargs):
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
        existing_favorite = self.session.query(UserMovie).filter_by(user_id=user_id, movie_id=movie_id).first()
        if not existing_favorite:
            favorite = UserMovie(user_id=user_id, movie_id=movie_id)
            self.session.add(favorite)
            self.session.commit()
            return favorite
        return existing_favorite

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
        favorite = self.session.query(UserMovie).filter_by(user_id=user_id, movie_id=movie_id).first()
        if favorite:
            self.session.delete(favorite)
            self.session.commit()

    # CRUD-Operationen für Genre
    def get_all_genres(self):
        return self.session.query(Genre).all()

    def add_genre(self, name):
        new_genre = Genre(name=name)
        self.session.add(new_genre)
        self.session.commit()
        return new_genre

    def get_genre_by_id(self, genre_id):
        return self.session.query(Genre).get(genre_id)

    def get_genre_by_name(self, genre_name):
        return self.session.query(Genre).filter_by(name=genre_name).first()

    def update_genre(self, genre_id, new_name):
        genre = self.session.query(Genre).get(genre_id)
        if genre:
            genre.name = new_name
            self.session.commit()
            return genre
        return None

    def delete_genre(self, genre_id):
        genre = self.session.query(Genre).get(genre_id)
        if genre:
            self.session.delete(genre)
            self.session.commit()

    # CRUD-Operationen für Review
    def add_review(self, text, rating, user_id, movie_id):
        new_review = Review(text=text, rating=rating, user_id=user_id, movie_id=movie_id)
        self.session.add(new_review)
        self.session.commit()
        return new_review

    def get_reviews_by_movie(self, movie_id):
         return self.session.query(Review).filter_by(movie_id=movie_id).all()

    def get_reviews_by_user(self, user_id):
        return self.session.query(Review).filter_by(user_id=user_id).all()

    def update_review(self, review_id, new_text=None, new_rating=None):
        review = self.session.query(Review).get(review_id)
        if review:
            if new_text:
                review.text = new_text
            if new_rating:
                review.rating = new_rating
            self.session.commit()
            return review
        return None

    def delete_review(self, review_id):
        review = self.session.query(Review).get(review_id)
        if review:
            self.session.delete(review)
            self.session.commit()

    def add_movie_to_genre(self, movie_id, genre_id):
        movie = self.get_movie_by_id(movie_id)
        genre = self.get_genre_by_id(genre_id)
        if movie and genre:
            movie.genres.append(genre)
            self.session.commit()

    def remove_movie_from_genre(self, movie_id, genre_id):
        movie = self.get_movie_by_id(movie_id)
        genre = self.get_genre_by_id(genre_id)
        if movie and genre:
            movie.genres.remove(genre)
            self.session.commit()

    def delete_movie(self, movie_id):
        try:
            movie = self.session.query(Movie).get(movie_id)
            if movie:
                # Entferne alle Beziehungen zu Benutzern
                self.session.query(UserMovie).filter_by(movie_id=movie_id).delete()

                # Entferne alle Reviews für diesen Film
                self.session.query(Review).filter_by(movie_id=movie_id).delete()

                # Entferne den Film selbst
                self.session.delete(movie)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            print(f"Error in delete_movie: {str(e)}")
            return False

    def search_movies(self, query):
        search = f"%{query}%"
        return self.session.query(Movie).filter(
            (Movie.name.ilike(search)) |
            (Movie.director.ilike(search))
        ).all()