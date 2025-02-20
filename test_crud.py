"""
This script tests the basic CRUD operations of the SQLiteDataManager.
It demonstrates adding users and movies, marking favorites, and retrieving data.
"""

from datamanager.sqlite_data_manager import SQLiteDataManager


def test_user_operations(data_manager):
    """Test user-related operations."""
    print("=== Test: Adding a user ===")
    new_user = data_manager.add_user("John Doe")
    print(f"User added: {new_user.name} (ID: {new_user.id})")
    return new_user


def test_movie_operations(data_manager):
    """Test movie-related operations."""
    print("\n=== Test: Adding a movie ===")
    new_movie = data_manager.add_movie(
        name="Inception",
        director="Christopher Nolan",
        year=2010,
        rating=9.0
    )
    print(f"Movie added: {new_movie.name} (ID: {new_movie.id})")
    return new_movie


def test_favorite_movie_operations(data_manager, user, movie):
    """Test operations related to favorite movies."""
    print("\n=== Test: Adding a favorite movie ===")
    favorite = data_manager.add_favorite_movie(user_id=user.id, movie_id=movie.id)
    print(f"Favorite movie added: User ID {favorite.user_id}, Movie ID {favorite.movie_id}")

    print("\n=== Test: Retrieving favorite movies of a user ===")
    favorite_movies = data_manager.get_favorite_movies_by_user(user_id=user.id)
    for fav_movie in favorite_movies:
        print(f"- {fav_movie.name} (Director: {fav_movie.director})")

    print("\n=== Test: Retrieving users who favorited a movie ===")
    users = data_manager.get_users_by_favorite_movie(movie_id=movie.id)
    for fav_user in users:
        print(f"- {fav_user.name}")


def main():
    """Main function to run all tests."""
    # Initialize the data manager with the database
    data_manager = SQLiteDataManager('instance/moviweb_app.db')

    # Run tests
    new_user = test_user_operations(data_manager)
    new_movie = test_movie_operations(data_manager)
    test_favorite_movie_operations(data_manager, new_user, new_movie)


if __name__ == "__main__":
    main()