import pytest
from app import app

@pytest.fixture
def client():
    """Fixture für den Flask-Testclient."""
    with app.test_client() as client:
        yield client

def test_home(client):
    """Testet die Startseite."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to MovieWeb App!" in response.data

def test_list_users(client):
    """Testet die Benutzerliste."""
    response = client.get('/users')
    assert response.status_code == 200
    assert b"Users" in response.data

def test_user_movies_not_found(client):
    """Testet den Zugriff auf einen nicht existierenden Benutzer."""
    response = client.get('/users/9999')  # ID eines nicht existierenden Benutzers
    assert response.status_code == 404
    assert b"Page Not Found" in response.data

def test_add_user(client):
    """Testet das Hinzufügen eines neuen Benutzers."""
    response = client.post('/add_user', data={'name': 'Test User'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test User" in response.data

def test_add_movie_invalid_user(client):
    """Testet das Hinzufügen eines Films für einen nicht existierenden Benutzer."""
    response = client.post('/users/9999/add_movie', data={'name': 'Inception'}, follow_redirects=True)
    assert response.status_code == 404
