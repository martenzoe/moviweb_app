"""
This module implements the SQLite data manager for the MovieWeb application.
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datamanager.data_models import db, User, Movie, UserMovie, Genre, Review
from sqlalchemy.orm.exc import NoResultFound


class SQLiteDataManager:
    """
    SQLite implementation of the data manager interface.
    """

    def __init__(self, db_file_name):
        """
        Initialize the SQLite data manager.

        Args:
            db_file_name (str): The name of the SQLite database file.
        """
        self.engine = create_engine(f'sqlite:///{db_file_name}')
        db.metadata.create_all(self.engine)  # Ensure tables are created
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    # CRUD operations for User
    def get_all_users(self):
        """
        Retrieve all users from the database.

        Returns:
            list: A list of all User objects.
        """
        return self.session.query(User).all()

    def add_user(self, name):
        """
        Add a new user to the database.

        Args:
            name (str): The name of the user.

        Returns:
            User: The newly created User object.
        """
        new_user = User(name=name)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def get_user_by_id(self, user_id):
        """
        Retrieve a user by their ID from the database.

        Args:
            user_id (int): The ID of the user.

        Returns:
            User: The User object if found, None otherwise.
        """
        return self.session.query(User).filter_by(id=user_id).first()

    # CRUD operations for Movie
    def get_all_movies(self):
        """
        Retrieve all movies from the database.

        Returns:
            list: A list of all Movie objects.
        """
        return self.session.query(Movie).all()

    def add_movie(self, name, director=None, year=None, rating=None, poster=None, genres=[]):
        """
        Add a new movie to the database.

        Args:
            name (str): The name of the movie.
            director (str, optional): The director of the movie.
            year (int, optional): The release year of the movie.
            rating (float, optional): The rating of the movie.
            poster (str, optional): The URL of the movie poster.
            genres (list, optional): A list of Genre objects for the movie.

        Returns:
            Movie: The newly created Movie object.
        """
        new_movie = Movie(name=name, director=director, year=year, rating=rating, poster=poster)
        for genre in genres:
            new_movie.genres.append(genre)
        self.session.add(new_movie)
        self.session.commit()
        return new_movie

    def get_movie_by_id(self, movie_id):
        """
        Retrieve a movie by its ID from the database.

        Args:
            movie_id (int): The ID of the movie.

        Returns:
            Movie: The Movie object if found, None otherwise.
        """
        return self.session.query(Movie).get(movie_id)

    def update_movie(self, movie_id, **kwargs):
        """
        Update a movie's details in the database.

        Args:
            movie_id (int): The ID of the movie to update.
            **kwargs: Arbitrary keyword arguments representing the movie attributes to update.

        Returns:
            Movie: The updated Movie object if found, None otherwise.
        """
        movie = self.session.query(Movie).get(movie_id)
        if not movie:
            return None
        for key, value in kwargs.items():
            if hasattr(movie, key):
                setattr(movie, key, value)
        self.session.commit()
        return movie

    # CRUD operations for UserMovie (relationship table)
    def add_favorite_movie(self, user_id, movie_id):
        """
        Add a movie to a user's favorites.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie to add as a favorite.

        Returns:
            UserMovie: The UserMovie object representing the favorite relationship.
        """
        existing_favorite = self.session.query(UserMovie).filter_by(user_id=user_id, movie_id=movie_id).first()
        if not existing_favorite:
            favorite = UserMovie(user_id=user_id, movie_id=movie_id)
            self.session.add(favorite)
            self.session.commit()
            return favorite
        return existing_favorite

    def get_favorite_movies_by_user(self, user_id):
        """
        Retrieve all favorite movies for a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of Movie objects that are favorites of the specified user.
        """
        return (
            self.session.query(Movie)
            .join(UserMovie)
            .filter(UserMovie.user_id == user_id)
            .all()
        )

    def get_users_by_favorite_movie(self, movie_id):
        """
        Retrieve all users who have favorited a specific movie.

        Args:
            movie_id (int): The ID of the movie.

        Returns:
            list: A list of User objects who have favorited the specified movie.
        """
        return (
            self.session.query(User)
            .join(UserMovie)
            .filter(UserMovie.movie_id == movie_id)
            .all()
        )

    def remove_favorite_movie(self, user_id, movie_id):
        """
        Remove a movie from a user's favorites.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie to remove from favorites.
        """
        favorite = self.session.query(UserMovie).filter_by(user_id=user_id, movie_id=movie_id).first()
        if favorite:
            self.session.delete(favorite)
            self.session.commit()

    # CRUD operations for Genre
    def get_all_genres(self):
        """
        Retrieve all genres from the database.

        Returns:
            list: A list of all Genre objects.
        """
        return self.session.query(Genre).all()

    def add_genre(self, name):
        """
        Add a new genre to the database.

        Args:
            name (str): The name of the genre.

        Returns:
            Genre: The newly created Genre object.
        """
        new_genre = Genre(name=name)
        self.session.add(new_genre)
        self.session.commit()
        return new_genre

    def get_genre_by_id(self, genre_id):
        """
        Retrieve a genre by its ID from the database.

        Args:
            genre_id (int): The ID of the genre.

        Returns:
            Genre: The Genre object if found, None otherwise.
        """
        return self.session.query(Genre).get(genre_id)

    def get_genre_by_name(self, genre_name):
        """
        Retrieve a genre by its name from the database.

        Args:
            genre_name (str): The name of the genre.

        Returns:
            Genre: The Genre object if found, None otherwise.
        """
        return self.session.query(Genre).filter_by(name=genre_name).first()

    def update_genre(self, genre_id, new_name):
        """
        Update a genre's name in the database.

        Args:
            genre_id (int): The ID of the genre to update.
            new_name (str): The new name for the genre.

        Returns:
            Genre: The updated Genre object if found, None otherwise.
        """
        genre = self.session.query(Genre).get(genre_id)
        if genre:
            genre.name = new_name
            self.session.commit()
            return genre
        return None

    def delete_genre(self, genre_id):
        """
        Delete a genre from the database.

        Args:
            genre_id (int): The ID of the genre to delete.
        """
        genre = self.session.query(Genre).get(genre_id)
        if genre:
            self.session.delete(genre)
            self.session.commit()

    # CRUD operations for Review
    def add_review(self, text, rating, user_id, movie_id):
        """
        Add a new review to the database.

        Args:
            text (str): The text content of the review.
            rating (float): The rating given in the review.
            user_id (int): The ID of the user who wrote the review.
            movie_id (int): The ID of the movie being reviewed.

        Returns:
            Review: The newly created Review object.
        """
        new_review = Review(text=text, rating=rating, user_id=user_id, movie_id=movie_id)
        self.session.add(new_review)
        self.session.commit()
        return new_review

    def get_reviews_by_movie(self, movie_id):
        """
        Retrieve all reviews for a specific movie.

        Args:
            movie_id (int): The ID of the movie.

        Returns:
            list: A list of Review objects for the specified movie.
        """
        return self.session.query(Review).filter_by(movie_id=movie_id).all()

    def get_reviews_by_user(self, user_id):
        """
        Retrieve all reviews by a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of Review objects by the specified user.
        """
        return self.session.query(Review).filter_by(user_id=user_id).all()

    def update_review(self, review_id, new_text=None, new_rating=None):
        """
        Update a review's content or rating in the database.

        Args:
            review_id (int): The ID of the review to update.
            new_text (str, optional): The new text content for the review.
            new_rating (float, optional): The new rating for the review.

        Returns:
            Review: The updated Review object if found, None otherwise.
        """
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
        """
        Delete a review from the database.

        Args:
            review_id (int): The ID of the review to delete.
        """
        review = self.session.query(Review).get(review_id)
        if review:
            self.session.delete(review)
            self.session.commit()

    def add_movie_to_genre(self, movie_id, genre_id):
        """
        Associate a movie with a genre.

        Args:
            movie_id (int): The ID of the movie.
            genre_id (int): The ID of the genre.
        """
        movie = self.get_movie_by_id(movie_id)
        genre = self.get_genre_by_id(genre_id)
        if movie and genre:
            movie.genres.append(genre)
            self.session.commit()

    def remove_movie_from_genre(self, movie_id, genre_id):
        """
        Remove the association between a movie and a genre.

        Args:
            movie_id (int): The ID of the movie.
            genre_id (int): The ID of the genre.
        """
        movie = self.get_movie_by_id(movie_id)
        genre = self.get_genre_by_id(genre_id)
        if movie and genre:
            movie.genres.remove(genre)
            self.session.commit()

    def delete_movie(self, movie_id):
        """
        Delete a movie and its associated data from the database.

        Args:
            movie_id (int): The ID of the movie to delete.

        Returns:
            bool: True if the movie was successfully deleted, False otherwise.
        """
        try:
            movie = self.session.query(Movie).get(movie_id)
            if movie:
                # Remove all relationships with users
                self.session.query(UserMovie).filter_by(movie_id=movie_id).delete()

                # Remove all reviews for this movie
                self.session.query(Review).filter_by(movie_id=movie_id).delete()

                # Remove the movie itself
                self.session.delete(movie)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            print(f"Error in delete_movie: {str(e)}")
            return False

    def search_movies(self, query):
        """
        Search for movies based on a query string.

        Args:
            query (str): The search query.

        Returns:
            list: A list of Movie objects that match the search query.
        """
        search = f"%{query}%"
        return self.session.query(Movie).filter(
            (Movie.name.ilike(search)) |
            (Movie.director.ilike(search))
        ).all()

    def get_recently_added_movies(self, limit=5):
        """
        Retrieve the most recently added movies.

        Args:
            limit (int, optional): The maximum number of movies to retrieve. Defaults to 5.

        Returns:
            list: A list of the most recently added Movie objects.
        """
        return self.session.query(Movie).order_by(Movie.id.desc()).limit(limit).all()

    def get_top_rated_movies(self, limit=5):
        """
        Retrieve the top-rated movies.

        Args:
            limit (int, optional): The maximum number of movies to retrieve. Defaults to 5.

        Returns:
            list: A list of the top-rated Movie objects.
        """
        return self.session.query(Movie).order_by(Movie.rating.desc()).limit(limit).all()