from datetime import datetime, timezone
import uuid

from src.db.main import get_session
from src import app
from unittest.mock import AsyncMock, Mock
import pytest
from fastapi.testclient import TestClient
from src.auth import dependencies as auth_dependencies
from src.auth import routes as auth_routes
from src.auth.dependencies import RoleChecker, AccessTokenBearer, RefreshTokenBearer
from src.db.models import User


class AsyncSessionStub:
    async def exec(self, *args, **kwargs):
        return Mock(one_or_none=lambda: None)

    async def commit(self):
        return None

    async def refresh(self, *args, **kwargs):
        return None

    def add(self, *args, **kwargs):
        return None


mock_session = AsyncSessionStub()
mock_user_service = Mock()
mock_book_service = Mock()

mock_user_service.user_exists = AsyncMock(return_value=False)
mock_user_service.create_user = AsyncMock(return_value=User(
    uid=uuid.uuid4(),
    username="testuser",
    email="testuser@example.com",
    first_name="Test",
    last_name="User",
    role="user",
    password_has="hashed",
    is_verified=False,
    created_at=datetime.now(timezone.utc),
    updated_at=datetime.now(timezone.utc),
))
mock_user_service.get_user_by_email = AsyncMock(return_value=None)
mock_user_service.get_user_by_uid = AsyncMock(return_value=None)

def get_mock_session():
    yield mock_session

access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()
role_checker = RoleChecker(['admin'])

auth_routes.user_service = mock_user_service
auth_dependencies.user_service = mock_user_service

app.dependency_overrides[get_session] = get_mock_session
app.dependency_overrides[role_checker] = Mock()
app.dependency_overrides[refresh_token_bearer] = Mock()

@pytest.fixture
def fake_session():
    return mock_session

@pytest.fixture
def fake_user_service():
    return mock_user_service

@pytest.fixture
def fake_book_service():
    return mock_book_service

@pytest.fixture
def test_client():
    return TestClient(app)