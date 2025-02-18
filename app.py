from flask import Flask, request, jsonify, render_template, redirect
from datamanager import create_app
from datamanager.sqlite_data_manager import SQLiteDataManager
import requests  # Für OMDb API
import logging  # Für Logging

# OMDb API Key
OMDB_API_KEY = "cafabb27"

# Erstellt die Flask-App durch Aufruf der Factory-Funktion
app = create_app()

# Initialisiere den Datenmanager
data_manager = SQLiteDataManager('instance/moviweb_app.db')

# Logging konfigurieren
logging.basicConfig(level=logging.ERROR)
app.logger.setLevel(logging.ERROR)

def fetch_movie_details(title):
    """Holt Filmdetails von der OMDb API anhand des Titels."""
    try:
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
                raise ValueError(f"OMDb API error: {data.get('Error')}")
        else:
            raise ConnectionError(f"HTTP Error: {response.status_code}")
    except Exception as e:
        app.logger.error(f"Error fetching movie details for {title}: {e}")
        return None

@app.errorhandler(404)
def page_not_found(e):
    """Handler für 404-Fehler."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handler für 500-Fehler."""
    return render_template('500.html'), 500

@app.route('/')
def home():
    """Startseite der Anwendung."""
    return "Welcome to MovieWeb App!"

@app.route('/users', methods=['GET'])
def list_users():
    """Route: Gibt eine Liste aller Benutzer zurück."""
    try:
        users = data_manager.get_all_users()
        return render_template('users.html', users=users)
    except Exception as e:
        app.logger.error(f"Error fetching users: {e}")
        return render_template('500.html'), 500

@app.route('/users/<int:user_id>', methods=['GET'])
def user_movies(user_id):
    """Zeigt die Lieblingsfilme eines bestimmten Benutzers an."""
    try:
        user = data_manager.get_user_by_id(user_id)
        if not user:
            return render_template('404.html'), 404

        movies = data_manager.get_favorite_movies_by_user(user_id)
        return render_template('user_movies.html', user=user, movies=movies)
    except Exception as e:
        app.logger.error(f"Error fetching user {user_id}: {e}")
        return render_template('500.html'), 500

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Route: Fügt einen neuen Benutzer hinzu."""
    if request.method == 'POST':
        try:
            name = request.form['name']
            if not name:
                raise ValueError("Name is required")

            data_manager.add_user(name)
            return redirect('/users')
        except Exception as e:
            app.logger.error(f"Error adding user: {e}")
            return render_template('500.html'), 500

    return render_template('add_user.html')

@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """Route: Fügt einen neuen Film zu den Lieblingsfilmen eines Benutzers hinzu."""
    try:
        user = data_manager.get_user_by_id(user_id)
        if not user:
            return render_template('404.html'), 404

        if request.method == 'POST':
            title = request.form['name']
            movie_details = fetch_movie_details(title)

            if not movie_details or "error" in movie_details:
                raise ValueError(f"OMDb API error: {movie_details.get('error', 'Unknown error')}")

            new_movie = data_manager.add_movie(
                name=movie_details["title"],
                director=movie_details["director"],
                year=movie_details["year"],
                rating=movie_details["rating"]
            )
            data_manager.add_favorite_movie(user_id=user.id, movie_id=new_movie.id)
            return redirect(f'/users/{user_id}')

        return render_template('add_movie.html', user=user)
    except Exception as e:
        app.logger.error(f"Error adding movie for user {user_id}: {e}")
        return render_template('500.html'), 500

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """Route: Aktualisiert die Details eines bestimmten Films."""
    try:
        user = data_manager.get_user_by_id(user_id)
        if not user:
            return render_template('404.html'), 404

        movie = data_manager.get_movie_by_id(movie_id)
        if not movie:
            return render_template('404.html'), 404

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
    except Exception as e:
        app.logger.error(f"Error updating movie {movie_id} for user {user_id}: {e}")
        return render_template('500.html'), 500

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Route: Entfernt einen Film aus den Lieblingsfilmen eines Benutzers."""
    try:
        user = data_manager.get_user_by_id(user_id)
        if not user:
            return render_template('404.html'), 404

        movie = data_manager.get_movie_by_id(movie_id)
        if not movie:
            return render_template('404.html'), 404

        data_manager.remove_favorite_movie(user_id=user.id, movie_id=movie.id)
        return redirect(f'/users/{user_id}')
    except Exception as e:
        app.logger.error(f"Error deleting movie {movie_id} for user {user_id}: {e}")
        return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)