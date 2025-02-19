from flask import Flask, request, render_template, redirect, url_for
from datamanager import create_app
from datamanager.sqlite_data_manager import SQLiteDataManager
import requests
import logging
import traceback

OMDB_API_KEY = "cafabb27"

app = create_app()
data_manager = SQLiteDataManager('instance/moviweb_app.db')

logging.basicConfig(level=logging.ERROR)
app.logger.setLevel(logging.ERROR)

def fetch_movie_details(title):
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
                    "genre": data.get("Genre", "").split(", ")
                }
            else:
                raise ValueError(f"OMDb API error: {data.get('Error')}")
        else:
            raise ConnectionError(f"HTTP Error: {response.status_code}")
    except Exception as e:
        app.logger.error(f"Error fetching movie details for {title}: {e}")
        return None

@app.errorhandler(404)
def page_not_found(_e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(movie_id):
    try:
        movie = data_manager.get_movie_by_id(movie_id)
        if not movie:
            return render_template('404.html'), 404

        # Delete the movie from the database
        data_manager.delete_movie(movie_id)

        # Redirect back to the movies page
        return redirect(url_for('list_movies'))
    except Exception as e:
        app.logger.error(f"Error deleting movie {movie_id}: {str(e)}")
        return render_template('500.html'), 500

@app.route('/')
def home():
    try:
        return render_template('home.html')
    except Exception as e:
        app.logger.error(f"Ein Fehler ist auf der Startseite aufgetreten: {str(e)}")
        return render_template('500.html'), 500

@app.route('/users', methods=['GET'])
def list_users():
    try:
        users = data_manager.get_all_users()
        return render_template('users.html', users=users)
    except Exception as e:
        app.logger.error(f"Error fetching users: {e}")
        return render_template('500.html'), 500

@app.route('/users/<int:user_id>', methods=['GET'])
def user_movies(user_id):
    try:
        user = data_manager.get_user_by_id(user_id)
        if not user:
            return render_template('404.html'), 404

        movies = data_manager.get_favorite_movies_by_user(user_id)
        return render_template('user_movies.html', user=user, movies=movies)
    except Exception as e:
        app.logger.error(f"Error fetching user {user_id}: {e}")
        return render_template('500.html'), 500

@app.route('/movies', methods=['GET'])
def list_movies():
    try:
        movies = data_manager.get_all_movies()
        return render_template('movies.html', movies=movies)
    except Exception as e:
        app.logger.error(f"Error fetching movies: {e}")
        return render_template('500.html'), 500

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        try:
            name = request.form['name']
            if not name:
                raise ValueError("Name is required")

            data_manager.add_user(name)
            return redirect(url_for('list_users'))
        except Exception as e:
            app.logger.error(f"Error adding user: {e}")
            return render_template('500.html'), 500

    return render_template('add_user.html')

@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    try:
        user = data_manager.get_user_by_id(user_id)
        if not user:
            return render_template('404.html'), 404

        if request.method == 'POST':
            title = request.form['name']
            director = request.form['director']
            year = request.form['year']
            rating = request.form['rating']
            genre_names = request.form.getlist('genres')  # Get list of selected genres

            # Fetch movie details from OMDb API if title is provided
            if not title:
                raise ValueError("Title is required")

            movie_details = fetch_movie_details(title)

            if not movie_details:
                raise ValueError(f"OMDb API error: Unable to fetch movie details")

            genres = []
            for genre_name in genre_names:
                genre = data_manager.get_genre_by_name(genre_name)
                if not genre:
                    genre = data_manager.add_genre(genre_name)
                genres.append(genre)

            new_movie = data_manager.add_movie(
                name=movie_details["title"],
                director=movie_details["director"],
                year=movie_details["year"],
                rating=movie_details["rating"],
                poster=movie_details["poster"],
                genres=genres
            )
            data_manager.add_favorite_movie(user_id=user.id, movie_id=new_movie.id)
            return redirect(url_for('user_movies', user_id=user_id))

        return render_template('add_movie.html', user=user)
    except Exception as e:
        app.logger.error(f"Error adding movie for user {user_id}: {e}")
        app.logger.error(traceback.format_exc())
        return render_template('500.html'), 500

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
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

            data_manager.update_movie(
                movie_id=movie.id,
                name=name,
                director=director,
                year=year,
                rating=rating
            )

            return redirect(url_for('user_movies', user_id=user_id))

        return render_template('update_movie.html', user=user, movie=movie)
    except Exception as e:
        app.logger.error(f"Error updating movie {movie_id} for user {user_id}: {e}")
        app.logger.error(traceback.format_exc())
        return render_template('500.html'), 500

@app.route('/genres', methods=['GET'])
def list_genres():
    try:
        genres = data_manager.get_all_genres()
        return render_template('genres.html', genres=genres)
    except Exception as e:
        app.logger.error(f"Error fetching genres: {e}")
        app.logger.error(traceback.format_exc())
        return render_template('500.html'), 500

@app.route('/genres/<int:genre_id>', methods=['GET'])
def genre_movies(genre_id):
    try:
        genre = data_manager.get_genre_by_id(genre_id)
        if not genre:
            return render_template('404.html'), 404
        return render_template('genre_movies.html', genre=genre)
    except Exception as e:
        app.logger.error(f"Error fetching movies for genre {genre_id}: {e}")
        app.logger.error(traceback.format_exc())
        return render_template('500.html'), 500

@app.route('/genres/add', methods=['GET', 'POST'])
def add_genre():
    if request.method == 'POST':
        try:
            name = request.form['name']
            if not name:
                raise ValueError("Name is required")

            data_manager.add_genre(name)
            return redirect(url_for('list_genres'))
        except Exception as e:
            app.logger.error(f"Error adding genre: {e}")
            app.logger.error(traceback.format_exc())
            return render_template('500.html'), 500

    return render_template('add_genre.html')

@app.route('/genres/update/<int:genre_id>', methods=['GET', 'POST'])
def update_genre(genre_id):
    try:
        genre = data_manager.get_genre_by_id(genre_id)
        if not genre:
            return render_template('404.html'), 404

        if request.method == 'POST':
            new_name = request.form['name']
            if not new_name:
                raise ValueError("Name is required")

            data_manager.update_genre(genre_id, new_name)
            return redirect(url_for('list_genres'))

        return render_template('update_genre.html', genre=genre)
    except Exception as e:
        app.logger.error(f"Error updating genre {genre_id}: {e}")
        app.logger.error(traceback.format_exc())
        return render_template('500.html'), 500

@app.route('/genres/delete/<int:genre_id>', methods=['POST'])
def delete_genre(genre_id):
    try:
        data_manager.delete_genre(genre_id)
        return redirect(url_for('list_genres'))
    except Exception as e:
        app.logger.error(f"Error deleting genre {genre_id}: {e}")
        app.logger.error(traceback.format_exc())
        return render_template('500.html'), 500

@app.route('/movies/<int:movie_id>/add_review', methods=['GET', 'POST'])
def add_review(movie_id):
    try:
        movie = data_manager.get_movie_by_id(movie_id)
        if not movie:
            return render_template('404.html'), 404

        if request.method == 'POST':
            text = request.form['text']
            rating = float(request.form['rating'])
            user_id = int(request.form['user_id'])
            data_manager.add_review(text, rating, user_id, movie_id)
            return redirect(url_for('movie_details', movie_id=movie_id))

        users = data_manager.get_all_users()
        return render_template('add_review.html', movie=movie, users=users)
    except Exception as e:
        app.logger.error(f"Error adding review for movie {movie_id}: {e}")
        app.logger.error(traceback.format_exc())
        return render_template('500.html'), 500

@app.route('/movies/<int:movie_id>', methods=['GET'])
def movie_details(movie_id):
    try:
        movie = data_manager.get_movie_by_id(movie_id)
        if not movie:
            return render_template('404.html'), 404
        reviews = data_manager.get_reviews_by_movie(movie_id)
        return render_template('movie_details.html', movie=movie, reviews=reviews)
    except Exception as e:
        app.logger.error(f"Error fetching details for movie {movie_id}: {e}")
        app.logger.error(traceback.format_exc())
        return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)

