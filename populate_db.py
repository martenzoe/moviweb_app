from datamanager.sqlite_data_manager import SQLiteDataManager

# Initialisiere den Datenmanager
data_manager = SQLiteDataManager('instance/moviweb_app.db')

# Beispielbenutzer hinzufügen
user1 = data_manager.add_user('John Doe')
user2 = data_manager.add_user('Jane Smith')

# Beispiel-Filme hinzufügen
movie1 = data_manager.add_movie(name='Inception', director='Christopher Nolan', year=2010, rating=9.0)
movie2 = data_manager.add_movie(name='The Matrix', director='Lana Wachowski', year=1999, rating=8.7)

# Lieblingsfilme zu Benutzern hinzufügen
data_manager.add_favorite_movie(user_id=user1.id, movie_id=movie1.id)
data_manager.add_favorite_movie(user_id=user1.id, movie_id=movie2.id)
data_manager.add_favorite_movie(user_id=user2.id, movie_id=movie2.id)

print("Beispieldaten erfolgreich hinzugefügt!")
