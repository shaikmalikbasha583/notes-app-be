import pytest


# Session-scoped fixture (e.g., database connection)
@pytest.fixture(scope="session")
def db_connection():
    print("\n[SETUP] Create a database connection")
    connection = "Session-Scoped Database Connection"  # Simulate a DB connection
    yield connection
    print("\n[TEARDOWN] Close the database connection")


# Function-scoped fixture (e.g., user setup for each test)
@pytest.fixture(scope="function")
def user_data():
    print("[SETUP] Create user data")
    user = {"username": "test_user", "email": "test@example.com"}
    yield user
    print("[TEARDOWN] Clean up user data")


# Test using both session-scoped and function-scoped fixtures
def test_example_1(db_connection, user_data):
    print(f"Running test_example_1 with {db_connection} and {user_data}")
    assert db_connection == "Session-Scoped Database Connection"
    assert user_data["username"] == "test_user"


def test_example_2(db_connection, user_data):
    print(f"Running test_example_2 with {db_connection} and {user_data}")
    assert db_connection == "Session-Scoped Database Connection"
    assert user_data["email"] == "test@example.com"
