import pytest
from pydantic import ValidationError
from datetime import datetime
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, UserListResponse, LoginRequest

# Fixtures for common test data
@pytest.fixture
def user_base_data():
    return {
        "username": "john_doe_123",
        "email": "john.doe@example.com",
        "full_name": "John Doe",
        "bio": "I am a software engineer with over 5 years of experience.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe.jpg"
    }

@pytest.fixture
def user_create_data(user_base_data):
    return {**user_base_data, "password": "SecurePassword123!"}

@pytest.fixture
def user_update_data():
    return {
        "email": "john.doe.new@example.com",
        "full_name": "John H. Doe",
        "bio": "I specialize in backend development with Python and Node.js.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe_updated.jpg"
    }

@pytest.fixture
def user_response_data():
    return {
        "id": "UUID",
        "username": "testuser",
        "email": "test@example.com",
        "last_login_at": datetime.now(),
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "links": []
    }

@pytest.fixture(scope="module")
def db():
    # Setup database connection or ORM session
    yield None  # Return connection/session if needed
    # Teardown database connection or ORM session

def test_unique_username(db):
    # Create a user with a unique username
    user_data = {
        "username": "test_user_123",
        "email": "test@example.com",
        "password": "TestPassword123!",
        "full_name": "Test User",
        "bio": "Testing user creation",
        "profile_picture_url": "https://example.com/test_user.jpg"
    }
    user_create_schema = UserCreate(**user_data)
    assert user_create_schema.username == "test_user_123"

    # Attempt to create another user with the same username
    with pytest.raises(ValueError) as excinfo:
        UserCreate(**user_data)
    assert "Username already exists." in str(excinfo.value)
    
@pytest.fixture
def login_request_data():
    return {"username": "john_doe_123", "password": "SecurePassword123!"}

# Tests for UserBase
def test_user_base_valid(user_base_data):
    user = UserBase(**user_base_data)
    assert user.username == user_base_data["username"]
    assert user.email == user_base_data["email"]

# Tests for UserCreate
def test_user_create_valid(user_create_data):
    user = UserCreate(**user_create_data)
    assert user.username == user_create_data["username"]
    assert user.password == user_create_data["password"]

# Tests for UserUpdate
def test_user_update_partial(user_update_data):
    partial_data = {"email": user_update_data["email"]}
    user_update = UserUpdate(**partial_data)
    assert user_update.email == partial_data["email"]

# Tests for UserResponse
def test_user_response_datetime(user_response_data):
    user = UserResponse(**user_response_data)
    assert user.last_login_at == user_response_data["last_login_at"]
    assert user.created_at == user_response_data["created_at"]
    assert user.updated_at == user_response_data["updated_at"]

# Tests for LoginRequest
def test_login_request_valid(login_request_data):
    login = LoginRequest(**login_request_data)
    assert login.username == login_request_data["username"]
    assert login.password == login_request_data["password"]

# Parametrized tests for username and email validation
@pytest.mark.parametrize("username", ["test_user", "test-user", "testuser123", "123test"])
def test_user_base_username_valid(username, user_base_data):
    user_base_data["username"] = username
    user = UserBase(**user_base_data)
    assert user.username == username

@pytest.mark.parametrize("username", ["test user", "test?user", "", "us"])
def test_user_base_username_invalid(username, user_base_data):
    user_base_data["username"] = username
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Test for username length validator
def test_username_length_validator():
    # Valid username length
    valid_username = "valid_username_123"
    try:
        UserBase(username=valid_username, email="test@example.com")
    except ValidationError as e:
        pytest.fail(f"Validation failed for valid username length: {valid_username}. Exception: {e}")

def test_password_length_validator():
    # Valid password length
    valid_password = "ValidPwd123!"
    try:
        UserCreate(username="testuser", email="test@example.com", password=valid_password)
    except ValidationError as e:
        pytest.fail(f"Validation failed for valid password length: {valid_password}. Exception: {e}")

    # Invalid password length
    invalid_password = "ShortPwd"
    with pytest.raises(ValidationError):
        UserCreate(username="testuser", email="test@example.com", password=invalid_password)