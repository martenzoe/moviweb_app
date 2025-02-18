from flask import Flask, request, jsonify, render_template, redirect
from datamanager import create_app
from datamanager.sqlite_data_manager import SQLiteDataManager
import os

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
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>', methods=['GET'])
def user_movies(user_id):
    """Zeigt die Lieblingsfilme eines bestimmten Benutzers an."""
    # Hole den Benutzer aus der Datenbank
    user = data_manager.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": f"User with ID {user_id} not found"}), 404

    # Hole die Lieblingsfilme des Benutzers
    movies = data_manager.get_favorite_movies_by_user(user_id)

    # Rendere das Template und übergebe die Daten
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Route: Fügt einen neuen Benutzer hinzu."""
    if request.method == 'POST':
        # Hole den Namen des Benutzers aus dem Formular
        name = request.form['name']
        if not name:
            return "Name is required", 400  # Fehler, wenn der Name fehlt

        # Füge den Benutzer über den DataManager hinzu
        data_manager.add_user(name)

        # Weiterleitung zur Benutzerliste
        return redirect('/users')

    # GET: Zeige das Formular an
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """Route: Fügt einen neuen Film zu den Lieblingsfilmen eines Benutzers hinzu."""
    # Überprüfen, ob der Benutzer existiert
    user = data_manager.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": f"User with ID {user_id} not found"}), 404

    if request.method == 'POST':
        # Hole die Filmdetails aus dem Formular
        name = request.form['name']
        director = request.form.get('director')
        year = request.form.get('year')
        rating = request.form.get('rating')

        # Füge den Film zur Datenbank hinzu
        new_movie = data_manager.add_movie(name=name, director=director, year=year, rating=rating)

        # Verknüpfe den Film mit dem Benutzer
        data_manager.add_favorite_movie(user_id=user_id, movie_id=new_movie.id)

        # Weiterleitung zur Seite des Benutzers
        return redirect(f'/users/{user_id}')

    # GET: Zeige das Formular an
    return render_template('add_movie.html', user=user)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """Route: Aktualisiert die Details eines bestimmten Films."""
    # Überprüfen, ob der Benutzer existiert
    user = data_manager.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": f"User with ID {user_id} not found"}), 404

    # Überprüfen, ob der Film existiert
    movie = data_manager.get_movie_by_id(movie_id)
    if not movie:
        return jsonify({"error": f"Movie with ID {movie_id} not found"}), 404

    if request.method == 'POST':
        # Hole die aktualisierten Filmdetails aus dem Formular
        name = request.form['name']
        director = request.form.get('director')
        year = request.form.get('year')
        rating = request.form.get('rating')

        # Aktualisiere den Film in der Datenbank
        updated_movie = data_manager.update_movie(
            movie_id=movie.id,
            name=name,
            director=director,
            year=year,
            rating=rating
        )

        # Weiterleitung zur Seite des Benutzers
        return redirect(f'/users/{user_id}')

    # GET: Zeige das Formular mit vorbefüllten Daten an
    return render_template('update_movie.html', user=user, movie=movie)

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Route: Entfernt einen Film aus den Lieblingsfilmen eines Benutzers."""
    # Überprüfen, ob der Benutzer existiert
    user = data_manager.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": f"User with ID {user_id} not found"}), 404

    # Überprüfen, ob der Film existiert
    movie = data_manager.get_movie_by_id(movie_id)
    if not movie:
        return jsonify({"error": f"Movie with ID {movie_id} not found"}), 404

    # Entferne den Film aus den Lieblingsfilmen des Benutzers
    data_manager.remove_favorite_movie(user_id=user_id, movie_id=movie_id)

    # Weiterleitung zur Seite des Benutzers
    return redirect(f'/users/{user_id}')


if __name__ == '__main__':
    # Startet den Flask-Entwicklungsserver
    app.run(debug=True)
