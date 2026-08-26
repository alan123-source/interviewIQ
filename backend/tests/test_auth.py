from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_register_user():
    response=client.post(
        "/auth/register",
        json={
            "name":"Test Userrrr",
            "email":"pytest_new_user_2026_0900000000@test.com",
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
    assert data["name"]=="Updated Test User"

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

def test_register_invalid_email():
    response=client.post(
        "/auth/register",
        json={
            "name":"Invalid Email User",
            "email":"not-an-email",
            "password":"123456"
        }
    )
    assert response.status_code==422

def test_register_short_password():
    response = client.post(
        "/auth/register",
        json={
            "name": "Short Password User",
            "email": "shortpassword@example.com",
            "password": "123"
        }
    )

    assert response.status_code == 422

def test_register_whitespace_name():
    response = client.post(
        "/auth/register",
        json={
            "name": "   ",
            "email": "whitespacename@example.com",
            "password": "123456"
        }
    )

    assert response.status_code == 422

def test_update_profile():
    login_response = client.post(
        "/auth/login",
        json={
            "email": "pytest_user2@test.com",
            "password": "123456"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.put(
        "/auth/profile",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "Updated Test User"
        }
    )

    assert response.status_code == 200

    data = response.json()
    print(data)

    assert data["user"]["name"] == "Updated Test User"
    assert data["user"]["email"] == "pytest_user2@test.com"

def test_profile_invalid_token():
    response = client.get(
        "/auth/profile",
        headers={
            "Authorization": "Bearer invalid-token"
        }
    )

    assert response.status_code == 401

def test_profile_inactive_user():
    login_response = client.post(
        "/auth/login",
        json={
            "email": "pytest_user2@test.com",
            "password": "123456"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Deactivate the user directly in the database
    from app.database.db import SessionLocal
    from app.models.user import User

    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.email == "pytest_user2@test.com"
        ).first()

        user.is_active = False
        db.commit()

        response = client.get(
            "/auth/profile",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        assert response.status_code == 403
        assert response.json()=={
            "detail":"User account is inactive"
        }

    finally:
        user.is_active = True
        db.commit()
        db.close()

def test_access_other_user():
    login_response = client.post(
        "/auth/login",
        json={
            "email": "pytest_user2@test.com",
            "password": "123456"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/users/23",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "You are not authorized to access this user"
    }