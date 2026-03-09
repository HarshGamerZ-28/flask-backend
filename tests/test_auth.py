import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        from extensions import db
        with app.app_context():
            db.drop_all()
            db.create_all()
        yield client

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200

def test_register(client):
    response = client.post("/register", json={
        "name": "Harsh",
        "email": "harsh@gmail.com",
        "password": "1234"
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "User registered successfully!"

def test_register_duplicate_email(client):
    client.post("/register", json={
        "name": "Harsh",
        "email": "harsh@gmail.com",
        "password": "1234"
    })
    response = client.post("/register", json={
        "name": "Harsh",
        "email": "harsh@gmail.com",
        "password": "1234"
    })
    assert response.status_code == 400
    assert response.get_json()["message"] == "Email already registered!"

def test_login_success(client):
    client.post("/register", json={
        "name": "Harsh",
        "email": "harsh@gmail.com",
        "password": "1234"
    })
    response = client.post("/login", json={
        "email": "harsh@gmail.com",
        "password": "1234"
    })
    assert response.status_code == 200
    assert "token" in response.get_json()

def test_login_wrong_password(client):
    client.post("/register", json={
        "name": "Harsh",
        "email": "harsh@gmail.com",
        "password": "1234"
    })
    response = client.post("/login", json={
        "email": "harsh@gmail.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401