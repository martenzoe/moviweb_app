from flask import Flask, request, jsonify, render_template, redirect
from datamanager import create_app
from datamanager.sqlite_data_manager import SQLiteDataManager
import requests  # Hinzugefügt für OMDb API
import os

# OMDb API Key
OMDB_API_KEY = "cafabb27"

# Erstellt die Flask-App durch Aufruf der Factory-Funktion
app = create_app()

# Initialisiere den Datenmanager
data_manager = SQLiteDataManager('instance/moviweb_app.db')

def fetch_movie_details(title):
    """Holt Filmdetails von der OMDb API anhand des Titels."""
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            return {
                "title": data.get("Title"),
                "year": data.get("Year"),
                "director": data.get("Director"),
                "rating": data.get("imdbRating"),
                "plot": data.get("Plot"),
                "poster": data.get("Poster"),
            }
        else:
            return {"error": data.get("Error")}
    else:
        return {"error": f"HTTP Error: {response.status_code}"}


@app.route('/')
def home():
    """Startseite der Anwendung."""
    return "Welcome to MovieWeb App!"


@app.route('/users', methods=['GET'])
def list_users():
    """Route: Gibt eine Liste aller Benutzer zurück."""
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>', methods=['GET'])
def user_movies(user_id):
    """Zeigt die Lieblingsfilme eines bestimmten Benutzers an."""
    user = data_manager.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": f"User with ID {user_id} not found"}), 404

    movies = data_manager.get_favorite_movies_by_user(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Route: Fügt einen neuen Benutzer hinzu."""
    if request.method == 'POST':
        name = request.form['name']
        if not name:
            return "Name is required", 400

        data_manager.add_user(name)
        return redirect('/users')

    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """Route: Fügt einen neuen Film zu den Lieblingsfilmen eines Benutzers hinzu."""
    user = data_manager.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": f"User with ID {user_id} not found"}), 404

    if request.method == 'POST':
        title = request.form['name']

        # Rufe Filmdetails von der OMDb API ab
        movie_details = fetch_movie_details(title)
        if "error" in movie_details:
            return jsonify({"error": movie_details["error"]}), 400

        # Füge den Film mit den abgerufenen Details hinzu
        new_movie = data_manager.add_movie(
            name=movie_details["title"],
            director=movie_details["director"],
            year=movie_details["year"],
            rating=movie_details["rating"]
        )

        # Verknüpfe den Film mit dem Benutzer
        data_manager.add_favorite_movie(user_id=user_id, movie_id=new_movie.id)

        return redirect(f'/users/{user_id}')

    return render_template('add_movie.html', user=user)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """Route: Aktualisiert die Details eines bestimmten Films."""
    user = data_manager.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": f"User with ID {user_id} not found"}), 404

    movie = data_manager.get_movie_by_id(movie_id)
    if not movie:
        return jsonify({"error": f"Movie with ID {movie_id} not found"}), 404

    if request.method == 'POST':
        name = request.form['name']
        director = request.form.get('director')
        year = request.form.get('year')
        rating = request.form.get('rating')

        updated_movie = data_manager.update_movie(
            movie_id=movie.id,
            name=name,
            director=director,
            year=year,
            rating=rating
        )

        return redirect(f'/users/{user_id}')

    return render_template('update_movie.html', user=user, movie=movie)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Route: Entfernt einen Film aus den Lieblingsfilmen eines Benutzers."""
    user = data_manager.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": f"User with ID {user_id} not found"}), 404

    movie = data_manager.get_movie_by_id(movie_id)
    if not movie:
        return jsonify({"error": f"Movie with ID {movie_id} not found"}), 404

    data_manager.remove_favorite_movie(user_id=user_id, movie_id=movie_id)
    return redirect(f'/users/{user_id}')


if __name__ == '__main__':
    app.run(debug=True)
