from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_register_user():
    response=client.post(
        "/auth/register",
        json={
            "name":"Test User",
            "email":"pytest_unique_2026_08_254@test.com",
            "password":"123456"
        }
    )

    assert response.status_code==200
    assert response.json()=={
        "message":"User registered successfully"
    }

def test_register_duplicate_email():
    response=client.post(
        "/auth/register",
        json={
            "name":"Another user",
            "email":"pytest_user@test.com",
            "password":"123456"
        }
    )

    assert response.status_code==400
    assert response.json()=={
        "detail":"Email already exists"
    }
def test_login_user():
    response=client.post(
        "/auth/login",
        json={
            "email":"pytest_user2@test.com",
            "password":"123456"
        }
    )

    assert response.status_code==200
    data=response.json()
    assert data["message"]=="Login successfull"
    assert "access_token" in data
    assert data["token_type"]=="bearer"

def test_profile():
    login_response=client.post(
        "/auth/login",
        json={
            "email":"pytest_user2@test.com",
            "password":"123456"
        }
    )

    assert login_response.status_code==200

    token=login_response.json()["access_token"]
    profile_response=client.get(
        "/auth/profile",
        headers={
            "Authorization":f"Bearer {token}"
        }
    )

    assert profile_response.status_code==200

    data=profile_response.json()

    assert data["email"]=="pytest_user2@test.com"
    assert data["name"]=="Test User"

def test_profile_without_token():
    response=client.get(
        "/auth/profile"
    )
    assert response.status_code==401

def test_login_invalid_credentials():
    response=client.post(
        "/auth/login",
        json={
            "email":"pytest_user2@test.com",
            "password":"wrong password"
        }
    )

    assert response.status_code==401
    assert response.json()=={
        "detail":"Invalid email or password"
    }