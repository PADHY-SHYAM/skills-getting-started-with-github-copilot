import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert (AAA) pattern is used in all tests

def test_get_activities():
    # Arrange: (No special setup needed, uses default in-memory data)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    assert "Chess Club" in data

def test_signup_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser@example.com"
    
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"

def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "duplicate@example.com"
    client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_nonexistent_activity():
    # Arrange
    activity = "Nonexistent Club"
    email = "ghost@example.com"
    
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_unregister_success():
    # Arrange
    activity = "Chess Club"
    email = "removeuser@example.com"
    client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"

def test_unregister_nonexistent_activity():
    # Arrange
    activity = "Nonexistent Club"
    email = "ghost@example.com"
    
    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_unregister_not_registered():
    # Arrange
    activity = "Chess Club"
    email = "notregistered@example.com"
    
    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]
