from flask import Flask, request, jsonify
from datamanager import create_app
from datamanager.sqlite_data_manager import SQLiteDataManager

# Erstellt die Flask-App durch Aufruf der Factory-Funktion
app = create_app()

# Initialisiere den Datenmanager
data_manager = SQLiteDataManager('instance/moviweb_app.db')

@app.route('/')
def home():
    """Startseite der Anwendung."""
    return "Welcome to MovieWeb App!"

@app.route('/users', methods=['GET'])
def list_users():
    """Route: Gibt eine Liste aller Benutzer zurück."""
    users = data_manager.get_all_users()
    return jsonify([{"id": user.id, "name": user.name} for user in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def user_movies(user_id):
    """Route: Gibt die Lieblingsfilme eines bestimmten Benutzers zurück."""
    movies = data_manager.get_favorite_movies_by_user(user_id)  # Angepasster Methodenname
    return jsonify([{"id": movie.id, "name": movie.name} for movie in movies])

@app.route('/add_user', methods=['POST'])
def add_user():
    """Route: Fügt einen neuen Benutzer hinzu."""
    data = request.json  # Erwartet JSON-Daten im Format {"name": "John Doe"}
    new_user = data_manager.add_user(data['name'])
    return jsonify({"id": new_user.id, "name": new_user.name}), 201

@app.route('/users/<int:user_id>/add_movie', methods=['POST'])
def add_movie(user_id):
    """Route: Fügt einen neuen Film zu den Lieblingsfilmen eines Benutzers hinzu."""
    data = request.json  # Erwartet JSON-Daten im Format {"name": "Inception", ...}
    new_movie = data_manager.add_movie(
        name=data['name'],
        director=data.get('director'),
        year=data.get('year'),
        rating=data.get('rating')
    )
    data_manager.add_favorite_movie(user_id=user_id, movie_id=new_movie.id)
    return jsonify({"id": new_movie.id, "name": new_movie.name}), 201

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    """Route: Aktualisiert die Details eines bestimmten Films."""
    data = request.json  # Erwartet JSON-Daten mit den zu aktualisierenden Feldern
    updated_movie = data_manager.update_movie(movie_id, **data)  # Sicherstellen, dass diese Methode existiert
    if updated_movie:
        return jsonify({"id": updated_movie.id, "name": updated_movie.name}), 200
    else:
        return jsonify({"error": f"Movie with ID {movie_id} not found"}), 404

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['DELETE'])
def delete_movie(user_id, movie_id):
    """Route: Entfernt einen Film aus den Lieblingsfilmen eines Benutzers."""
    success = data_manager.remove_favorite_movie(user_id=user_id, movie_id=movie_id)
    if success:
        return jsonify({"message": f"Movie {movie_id} removed from user {user_id}'s favorites"}), 200
    else:
        return jsonify({"error": f"Movie with ID {movie_id} not found for user {user_id}"}), 404

if __name__ == '__main__':
    # Startet den Flask-Entwicklungsserver
    app.run(debug=True)
