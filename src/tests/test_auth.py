from src.auth.schemas import UserCreateModel
from src.db.models import User

auth_prefix = f"/api/v1/auth"


def test_openapi_schema_available_at_versioned_prefix(test_client):
    response = test_client.get("/api/v1/openapi.json")

    assert response.status_code == 200
    assert response.json()["openapi"]


def test_user_creation(fake_session, fake_user_service, test_client):
    signup_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass",
        "first_name": "Test",
        "last_name": "User"
    }
    response = test_client.post(
        url=f"{auth_prefix}/signup",
        json=signup_data
    )

    assert response.status_code == 201

    # correct way — assert_called_once() on the specific method, not on the service
    fake_user_service.user_exists.assert_called_once()
    fake_user_service.create_user.assert_called_once()


def test_signup_with_invalid_unicode_returns_bad_request(test_client):
    response = test_client.post(
        url=f"{auth_prefix}/signup",
        content=b'{"username":"testuser","email":"testuser@example.com","password":"\\ud800","first_name":"Test","last_name":"User"}',
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid request body"


def test_openapi_documents_authentication_and_conflict_responses(test_client):
    schema = test_client.get("/api/v1/openapi.json").json()
    paths = schema["paths"]

    assert "401" in paths["/api/v1/auth/logout"]["get"]["responses"]
    assert "403" in paths["/api/v1/auth/login"]["post"]["responses"]
    assert "409" in paths["/api/v1/auth/signup"]["post"]["responses"]


def test_openapi_documents_403_for_invalid_authentication(test_client):
    schema = test_client.get("/api/v1/openapi.json").json()
    paths = schema["paths"]

    # fixed: use single `paths` variable instead of two pointing at the same object
    assert "403" in paths["/api/v1/auth/logout"]["get"]["responses"]
    assert "400" in paths["/api/v1/auth/login"]["post"]["responses"]


def test_openapi_documents_403_for_protected_books_and_authors(test_client):
    schema = test_client.get("/api/v1/openapi.json").json()
    paths = schema["paths"]

    # fixed: use single `paths` variable instead of books_paths/authors_paths both pointing at same object
    assert "403" in paths["/api/v1/books/"]["get"]["responses"]
    assert "403" in paths["/api/v1/books/{book_uid}"]["get"]["responses"]
    assert "403" in paths["/api/v1/authors/"]["get"]["responses"]
    assert "403" in paths["/api/v1/authors/{author_uid}"]["get"]["responses"]


def test_user_timestamps_are_timezone_aware():
    user = User(
        username="u",
        email="u@example.com",
        first_name="First",
        last_name="Last",
        password_has="hashed",
    )

    assert user.created_at is not None
    assert user.updated_at is not None
    assert user.created_at.tzinfo is not None
    assert user.updated_at.tzinfo is not None