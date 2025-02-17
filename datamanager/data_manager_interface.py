from abc import ABC, abstractmethod

class DataManagerInterface(ABC):
    @abstractmethod
    def get_all_users(self):
        """Gibt eine Liste aller Benutzer zurück."""
        pass

    @abstractmethod
    def add_movie(self, name, director=None, year=None, rating=None):
        """Fügt einen neuen Film hinzu."""
        pass

    @abstractmethod
    def add_favorite_movie(self, user_id, movie_id):
        """Verknüpft einen Benutzer mit einem Lieblingsfilm."""
        pass

    @abstractmethod
    def get_user_favorite_movies(self, user_id):
        """Gibt alle Lieblingsfilme eines Benutzers zurück."""
        pass

    @abstractmethod
    def get_all_movies(self):
        """Gibt eine Liste aller Filme zurück."""
        pass

    @abstractmethod
    def update_movie(self, movie_id, **kwargs):
        """Aktualisiert die Details eines Films."""
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        """Löscht einen Film anhand seiner ID."""
        pass
