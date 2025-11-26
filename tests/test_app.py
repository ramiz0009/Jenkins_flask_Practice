import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app

@pytest.fixture
def app():
    """Create application fixture"""
    flask_app.config.update({
        "TESTING": True,
        "MONGO_URI": "mongodb://localhost:27017/test_db"  # Test database
    })
    yield flask_app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

def test_home_page(client):
    """Test home page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200

def test_add_student_page(client):
    """Test add student page loads"""
    response = client.get('/add')
    assert response.status_code == 200

def test_app_configuration(app):
    """Test app is in testing mode"""
    assert app.config['TESTING'] == True

def test_404_error(client):
    """Test 404 page"""
    response = client.get('/nonexistent')
    assert response.status_code == 404
