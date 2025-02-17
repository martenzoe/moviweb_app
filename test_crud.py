from datamanager.sqlite_data_manager import SQLiteDataManager

# Initialisiere den Datenmanager mit der Datenbank
data_manager = SQLiteDataManager('instance/moviweb_app.db')

# Test: Benutzer hinzufügen
print("=== Test: Benutzer hinzufügen ===")
new_user = data_manager.add_user("John Doe")
print(f"Benutzer hinzugefügt: {new_user.name} (ID: {new_user.id})")

# Test: Film hinzufügen
print("\n=== Test: Film hinzufügen ===")
new_movie = data_manager.add_movie(
    name="Inception",
    director="Christopher Nolan",
    year=2010,
    rating=9.0
)
print(f"Film hinzugefügt: {new_movie.name} (ID: {new_movie.id})")

# Test: Lieblingsfilm hinzufügen
print("\n=== Test: Lieblingsfilm hinzufügen ===")
favorite = data_manager.add_favorite_movie(user_id=new_user.id, movie_id=new_movie.id)
print(f"Liebingsfilm hinzugefügt: User ID {favorite.user_id}, Movie ID {favorite.movie_id}")

# Test: Lieblingsfilme eines Benutzers abrufen
print("\n=== Test: Lieblingsfilme eines Benutzers abrufen ===")
favorite_movies = data_manager.get_favorite_movies_by_user(user_id=new_user.id)
for movie in favorite_movies:
    print(f"- {movie.name} (Regisseur: {movie.director})")

# Test: Benutzer eines Lieblingsfilms abrufen
print("\n=== Test: Benutzer eines Lieblingsfilms abrufen ===")
users = data_manager.get_users_by_favorite_movie(movie_id=new_movie.id)
for user in users:
    print(f"- {user.name}")
