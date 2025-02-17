from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datamanager.data_models import db, User, Movie, UserMovie  # Importiere die Modelle und SQLAlchemy-Instanz

class SQLiteDataManager:
    def __init__(self, db_file_name):
        """Initialisiert den SQLiteDataManager mit einer SQLite-Datenbank."""
        self.engine = create_engine(f'sqlite:///{db_file_name}')  # Verbindung zur SQLite-Datenbank
        Session = sessionmaker(bind=self.engine)  # Erstellt eine Sitzung
        self.session = Session()  # Initialisiert die Sitzung

    # CRUD-Operationen für Benutzer
    def get_all_users(self):
        """Gibt eine Liste aller Benutzer zurück."""
        return self.session.query(User).all()

    def add_user(self, name):
        """Fügt einen neuen Benutzer hinzu."""
        new_user = User(name=name)
        self.session.add(new_user)  # Fügt den Benutzer zur Sitzung hinzu
        self.session.commit()  # Speichert die Änderungen in der Datenbank
        return new_user

    # CRUD-Operationen für Filme
    def get_all_movies(self):
        """Gibt eine Liste aller Filme zurück."""
        return self.session.query(Movie).all()

    def add_movie(self, name, director=None, year=None, rating=None):
        """Fügt einen neuen Film hinzu."""
        new_movie = Movie(
            name=name,
            director=director,
            year=year,
            rating=rating
        )
        self.session.add(new_movie)  # Fügt den Film zur Sitzung hinzu
        self.session.commit()  # Speichert die Änderungen in der Datenbank
        return new_movie

    # CRUD-Operationen für UserMovie (Beziehungstabelle)
    def add_favorite_movie(self, user_id, movie_id):
        """Verknüpft einen Benutzer mit einem Lieblingsfilm."""
        favorite = UserMovie(user_id=user_id, movie_id=movie_id)
        self.session.add(favorite)  # Fügt die Beziehung zur Sitzung hinzu
        self.session.commit()  # Speichert die Änderungen in der Datenbank
        return favorite

    def get_favorite_movies_by_user(self, user_id):
        """Gibt alle Lieblingsfilme eines Benutzers zurück."""
        favorites = (
            self.session.query(Movie)
            .join(UserMovie)
            .filter(UserMovie.user_id == user_id)
            .all()
        )
        return favorites

    def get_users_by_favorite_movie(self, movie_id):
        """Gibt alle Benutzer zurück, die einen bestimmten Film als Favoriten markiert haben."""
        users = (
            self.session.query(User)
            .join(UserMovie)
            .filter(UserMovie.movie_id == movie_id)
            .all()
        )
        return users

    def remove_favorite_movie(self, user_id, movie_id):
        """Entfernt einen Lieblingsfilm für einen Benutzer."""
        favorite = (
            self.session.query(UserMovie)
            .filter_by(user_id=user_id, movie_id=movie_id)
            .first()
        )
        if favorite:
            self.session.delete(favorite)  # Entfernt die Beziehung aus der Sitzung
            self.session.commit()  # Speichert die Änderungen in der Datenbank
