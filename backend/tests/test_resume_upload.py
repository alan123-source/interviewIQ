from fastapi.testclient import TestClient

from app.main import app

from app.core.security import get_current_user

client=TestClient(app)

def fake_current_user():
    class User:
        id=1
    return User()

app.dependency_overrides[get_current_user]=fake_current_user

def test_upload_rejects_non_pdf():
    response=client.post(
        "resumes/upload",
        files={
            "file":(
                "resume.txt",
                b"This is not a PDF",
                "text/plain",
            )
        },
    )

    assert response.status_code==400
    assert response.json()["detail"]=="Only PDF files are allowed"

def test_upload_rejects_empty_file():
    response = client.post(
        "/resumes/upload",
        files={
            "file": (
                "resume.pdf",
                b"",
                "application/pdf",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "File is empty"

def test_upload_rejects_large_file():
    large_file = b"%PDF-" + b"a" * (5 * 1024 * 1024)

    response = client.post(
        "/resumes/upload",
        files={
            "file": (
                "large_resume.pdf",
                large_file,
                "application/pdf",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "File size must be less than 5 MB"

def test_upload_rejects_invalid_pdf():
    response = client.post(
        "/resumes/upload",
        files={
            "file": (
                "fake_resume.pdf",
                b"This is not a real PDF file",
                "application/pdf",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid PDF file"