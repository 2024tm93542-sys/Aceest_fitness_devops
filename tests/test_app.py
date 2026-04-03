import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["message"] == "ACEest Fitness API running"


def test_login_success(client):
    response = client.post(
        "/login",
        json={
            "username": "admin",
            "password": "admin"
        }
    )

    assert response.status_code == 200
    assert response.get_json()["status"] == "success"
    assert response.get_json()["role"] == "Admin"


def test_login_failure(client):
    response = client.post(
        "/login",
        json={
            "username": "wrong",
            "password": "wrong"
        }
    )

    assert response.status_code == 401
    assert response.get_json()["status"] == "failed"


def test_add_client(client):
    response = client.post(
        "/clients",
        json={
            "name": "John"
        }
    )

    assert response.status_code == 200
    assert response.get_json()["status"] == "client added"


def test_list_clients(client):
    client.post(
        "/clients",
        json={
            "name": "John"
        }
    )

    response = client.get("/clients")

    assert response.status_code == 200
    assert "John" in response.get_json()


def test_add_workout(client):
    client.post(
        "/clients",
        json={
            "name": "John"
        }
    )

    response = client.post(
        "/workouts",
        json={
            "client": "John",
            "type": "Strength",
            "duration": 60,
            "notes": "Leg day"
        }
    )

    assert response.status_code == 200
    assert response.get_json()["status"] == "workout saved"


def test_get_workouts(client):
    client.post(
        "/clients",
        json={
            "name": "John"
        }
    )

    client.post(
        "/workouts",
        json={
            "client": "John",
            "type": "Strength",
            "duration": 60,
            "notes": "Leg day"
        }
    )

    response = client.get("/workouts/John")

    assert response.status_code == 200
    data = response.get_json()

    assert len(data) >= 1
    assert data[0]["type"] == "Strength"


def test_membership(client):
    client.post(
        "/clients",
        json={
            "name": "John"
        }
    )

    response = client.get("/membership/John")

    assert response.status_code == 200
    assert response.get_json()["membership_status"] == "Active"