import pytest
from app import app


@pytest.fixture
def client():
    """Fixture for the Flask test client."""
    with app.test_client() as client:
        yield client


def test_home(client):
    """Test the home page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to MovieWeb App!" in response.data


def test_list_users(client):
    """Test the user list page."""
    response = client.get('/users')
    assert response.status_code == 200
    assert b"Users" in response.data


def test_user_movies_not_found(client):
    """Test accessing a non-existent user's movies."""
    response = client.get('/users/9999')  # ID of a non-existent user
    assert response.status_code == 404
    assert b"Page Not Found" in response.data


def test_add_user(client):
    """Test adding a new user."""
    response = client.post('/add_user', data={'name': 'Test User'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test User" in response.data


def test_add_movie_invalid_user(client):
    """Test adding a movie for a non-existent user."""
    response = client.post('/users/9999/add_movie', data={'name': 'Inception'}, follow_redirects=True)
    assert response.status_code == 404