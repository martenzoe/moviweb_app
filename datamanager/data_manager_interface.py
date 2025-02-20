from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """
    Abstract base class defining the interface for data management operations.
    """

    @abstractmethod
    def get_all_users(self):
        """
        Retrieves a list of all users.

        Returns:
            list: A list of all user objects.
        """
        pass

    @abstractmethod
    def add_movie(self, name, director=None, year=None, rating=None):
        """
        Adds a new movie to the database.

        Args:
            name (str): The name of the movie.
            director (str, optional): The director of the movie. Defaults to None.
            year (int, optional): The release year of the movie. Defaults to None.
            rating (float, optional): The rating of the movie. Defaults to None.

        Returns:
            Movie: The newly created movie object.
        """
        pass

    @abstractmethod
    def add_favorite_movie(self, user_id, movie_id):
        """
        Associates a user with a favorite movie.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie to be added as a favorite.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        pass

    @abstractmethod
    def get_user_favorite_movies(self, user_id):
        """
        Retrieves all favorite movies for a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of movie objects that are favorites of the specified user.
        """
        pass

    @abstractmethod
    def get_all_movies(self):
        """
        Retrieves a list of all movies.

        Returns:
            list: A list of all movie objects.
        """
        pass

    @abstractmethod
    def update_movie(self, movie_id, **kwargs):
        """
        Updates the details of a specific movie.

        Args:
            movie_id (int): The ID of the movie to update.
            **kwargs: Arbitrary keyword arguments representing the movie attributes to update.

        Returns:
            Movie: The updated movie object.
        """
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        """
        Deletes a movie from the database.

        Args:
            movie_id (int): The ID of the movie to delete.

        Returns:
            bool: True if the movie was successfully deleted, False otherwise.
        """
        pass