from sqlalchemy import create_engine  # Zum Erstellen einer Datenbankverbindung
from sqlalchemy.orm import sessionmaker  # Zum Erstellen von Sitzungen (Sessions)
from datamanager.data_manager_interface import DataManagerInterface  # Importiert das Interface
from data_models import Movie, User

class SQLiteDataManager(DataManagerInterface):  # Implementiert das Interface
    def __init__(self, db_file_name): #Dateiname muss noch ergänzt werden
        self.engine = create_engine(f'sqlite:///{db_file_name}')  # Erstellt eine Verbindung zur SQLite-Datenbank
        Session = sessionmaker(bind=self.engine)  # Erstellt einen Sessionmaker
        self.session = Session()  # Erstellt eine Sitzung

    def get_all_users(self):
        return self.session.query(User).all()  # Gibt alle Benutzer zurück

    def get_user_movies(self, user_id):
        return self.session.query(Movie).filter_by(user_id=user_id).all()  # Gibt alle Filme eines Benutzers zurück

    def add_user(self, name):
        new_user = User(name=name)  # Erstellt einen neuen Benutzer
        self.session.add(new_user)  # Fügt den Benutzer zur Sitzung hinzu
        self.session.commit()  # Speichert die Änderungen in der Datenbank
        return new_user

    def add_movie(self, user_id, name, director, year, rating):
        new_movie = Movie(user_id=user_id, name=name,
                          director=director, year=year,
                          rating=rating)
        self.session.add(new_movie)
        self.session.commit()
        return new_movie

    def update_movie(self, movie_id, **kwargs):
        movie = self.session.query(Movie).get(movie_id)  # Holt den Film aus der DB
        if not movie:
            return None
        for key, value in kwargs.items():
            setattr(movie, key, value)  # Aktualisiert Attribute des Films
        self.session.commit()
        return movie

    def delete_movie(self, movie_id):
        movie = self.session.query(Movie).get(movie_id)
        if not movie:
            return None
        self.session.delete(movie)
        self.session.commit()
