import logging
from contextlib import asynccontextmanager

import pytest
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv(find_dotenv())


from app.main import app
from app.main.config.db_config import Base, get_db_async, initialize_db

# app_client = TestClient(app)
import httpx
from httpx import ASGITransport, AsyncClient


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

# @pytest.fixture
# def setup():
#     # Setup logic
#     print("Setting up for the database for testing...")
#     yield  # Test runs here
#     # Teardown logic
#     print("Tearing down after the test...")


# def test_example(setup_and_teardown):
#     print("Running the test...")
#     assert True


async def override_get_db_async():
    db: AsyncSession = TestSessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def override_initialize_db():
    async with test_engine.begin() as conn:
        print("Initializing database...")
        await conn.run_sync(Base.metadata.create_all)
        print("Database has been successfully initialized!")


@pytest.fixture
async def setup_and_teardown():
    # Setup logic
    print("Setting up for the test...")

    yield override_initialize_db
    # Teardown logic
    print("Tearing down after the test...")


async def setup(setup_and_teardown):
    print("Setting up for the test...")

    yield
    print("Tearing down after the test...")


print("Overriding the dependencies...")
app.dependency_overrides[get_db_async] = override_get_db_async
app.dependency_overrides[initialize_db] = override_initialize_db


@pytest.mark.asyncio
async def test_root_working():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        print("Testing the root endpoint... using with context manager")
        response = await ac.get("/")
    print("Response: ", response.json())
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "docs": "/docs",
        "redoc": "/redocs",
    }


@pytest.fixture
async def teardown():
    print("I am shutting down the database...")


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
