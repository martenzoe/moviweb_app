from sqlalchemy import create_engine  # Zum Erstellen einer Datenbankverbindung
from sqlalchemy.orm import sessionmaker  # Zum Erstellen von Sitzungen (Sessions)
from datamanager.data_manager_interface import DataManagerInterface  # Importiert das Interface
from data_models import Movie, User

class SQLiteDataManager(DataManagerInterface):  # Implementiert das Interface
    def __init__(self, db_file_name): #Dateiname muss noch ergänzt werden
        self.engine = create_engine(f'sqlite:///{db_file_name}')  # Erstellt eine Verbindung zur SQLite-Datenbank
        Session = sessionmaker(bind=self.engine)  # Erstellt einen Sessionmaker
        self.session = Session()  # Erstellt eine Sitzung


