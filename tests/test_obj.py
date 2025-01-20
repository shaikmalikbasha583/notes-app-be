import logging

import pytest_asyncio
import pytest

# Import your app's database base and dependency
from dotenv import find_dotenv, load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv(find_dotenv())


from app.main import app
from app.main.config.db_config import Base, get_db_async, initialize_db

# SQLALCHEMY
test_engine = create_async_engine(
    # "sqlite+aiosqlite:///:memory:",
    "sqlite+aiosqlite:///test-notes-app-db.sqlite3",
    connect_args={"check_same_thread": False},
    echo=True,
    poolclass=StaticPool,
    logging_name=logging.INFO,
)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


async def override_get_db_async():
    print("Overriding get_db_async function Definition")
    db: AsyncSession = TestSessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def override_initialize_db():
    print("Overriding initialize_db function Definition")
    async with test_engine.begin() as conn:
        print("Initializing database...")
        await conn.run_sync(Base.metadata.create_all)
        print("Database has been successfully initialized!")


@pytest_asyncio.fixture
async def setup_and_teardown_db():
    """
    Fixture to set up and tear down a test database.
    """
    async with test_engine.begin() as conn:
        # Create all tables
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
    async with TestSessionLocal() as session:
        yield session
    async with test_engine.begin() as conn:
        # Drop all tables
        print("Dropping tables...")
        await conn.run_sync(Base.metadata.drop_all)


app.dependency_overrides[get_db_async] = override_get_db_async
app.dependency_overrides[initialize_db] = override_initialize_db


@pytest.mark.asyncio
async def test_create_note():
    title = "Test Note with Pytest Library"
    description = "This is a test note created using Pytest Library"
    target_date = "2024-01-20T00:00:00"
    user_id = 1

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        print("Testing the create note endpoint... using with context manager")
        response = await ac.post(
            "/api/v1/notes/",
            json={
                "title": title,
                "description": description,
                "status": "PENDING",
                "target_date": target_date,
                "user_id": user_id,
            },
        )
    print("Response: ", response.json())
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "New Note has been successfully created"
    assert response.json()["ui_message"] == "New Note has been successfully created"
    assert response.json()["created_note"]["title"] == title
    assert response.json()["created_note"]["description"] == description
    assert response.json()["created_note"]["status"] == "PENDING"
    assert response.json()["created_note"]["target_date"] == target_date


@pytest.mark.asyncio
async def test_get_all_notes(setup_and_teardown_db):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        print("Testing the get all notes endpoint... using with context manager")
        app.dependency_overrides[get_db_async] = override_get_db_async
        app.dependency_overrides[initialize_db] = override_initialize_db
        response = await ac.get("/api/v1/notes/")
    print("Response: ", response.json())
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "List of notes"
    assert response.json()["ui_message"] == "List of notes from the database"
    assert len(response.json()["notes"]) >= 0
