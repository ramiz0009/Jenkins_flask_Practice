import pytest
from app import app
from bson.objectid import ObjectId

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["MONGO_URI"] = "mongodb://localhost:27017/test_db"  # test DB
    test_client = app.test_client()
    return test_client


def test_homepage_loads(client):
    """Test if homepage loads successfully."""
    response = client.get("/")
    assert response.status_code == 200


def test_add_student(client, monkeypatch):
    """Test adding a student."""
    
    def mock_insert_one(data):
        return True

    monkeypatch.setattr("app.mongo.db.students.insert_one", mock_insert_one)

    response = client.post("/add", data={
        "name": "Test User",
        "email": "test@example.com",
        "course": "Math"
    })
    
    assert response.status_code == 302  # redirect after POST


def test_update_student(client, monkeypatch):
    """Test updating a student."""
    
    fake_id = ObjectId()

    def mock_find_one(query):
        return {
            "_id": fake_id,
            "name": "Old Name",
            "email": "old@example.com",
            "course": "Old Course"
        }

    def mock_update_one(query, update):
        return True

    monkeypatch.setattr("app.mongo.db.students.find_one", mock_find_one)
    monkeypatch.setattr("app.mongo.db.students.update_one", mock_update_one)

    response = client.post(f"/update/{fake_id}", data={
        "name": "New Name",
        "email": "new@example.com",
        "course": "New Course"
    })
    
    assert response.status_code == 302


def test_delete_student(client, monkeypatch):
    """Test deleting a student."""
    
    def mock_delete_one(query):
        return True

    monkeypatch.setattr("app.mongo.db.students.delete_one", mock_delete_one)

    fake_id = ObjectId()
    response = client.get(f"/delete/{fake_id}")

    assert response.status_code == 302
