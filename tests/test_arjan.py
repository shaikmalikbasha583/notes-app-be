import logging

import pytest
import pytest_asyncio

# Import your app's database base and dependency
from dotenv import find_dotenv, load_dotenv
from fastapi.testclient import TestClient
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

client = TestClient(app)


async def override_get_db_async():
    print("Overriding get_db_async function Definition")
    db: AsyncSession = TestSessionLocal()
    try:
        yield db
    finally:
        await db.close()


app.dependency_overrides[get_db_async] = override_get_db_async


async def setup():
    print("Creating tables...")
    async with test_engine.begin() as conn:
        print("Initializing database...")
        await conn.run_sync(Base.metadata.create_all)
        print("Database has been successfully initialized!")


async def teardown():
    print("Dropping tables...")
    async with test_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)

        print("Dropping tables...")


# async def override_initialize_db():
#     print("Overriding initialize_db function Definition")
#     async with test_engine.begin() as conn:
#         print("Initializing database...")
#         await conn.run_sync(Base.metadata.create_all)
#         print("Database has been successfully initialized!")


def test_index():
    res = client.get("/")
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_create_note():
    title = "Test Note with Pytest Library"
    description = "This is a test note created using Pytest Library"
    target_date = "2024-01-20T00:00:00"
    user_id = 1

    print("Testing the create note endpoint... using with context manager")
    response = await client.post(
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
