import pytest
from dotenv import find_dotenv, load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(find_dotenv())

from app.main.config.db_config import get_db_async

# Use SQLite as the testing database
DATABASE_URL = "sqlite+aiosqlite:///test-notes-app-db.sqlite3"


@pytest.fixture(scope="session")
def engine():
    return create_engine(DATABASE_URL)


@pytest.fixture(scope="session")
def SessionLocal():
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session(SessionLocal):
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def fastapi_app():
    from app.main import app  # Replace with your actual app module

    app.dependency_overrides[get_db_async] = db_session
    return app


@pytest.fixture
def test_client(fastapi_app, db_session):
    # from fastapi.testclient import TestClient
    print("Oh my God!!!!!!!!!!!!")
    client = TestClient(fastapi_app)
    yield client


def setup():
    print("Setting up....")


def teardown():
    print("Tearing down....")
