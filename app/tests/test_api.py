import logging

import pytest
import pytest_asyncio

# Import your app's database base and dependency
from dotenv import find_dotenv, load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.main.config.db_config import Base, get_db_async

load_dotenv(find_dotenv())

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
# client = AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver")


async def override_get_db_async():
    print("Overriding get_db_async function Definition")
    db: AsyncSession = TestSessionLocal()
    try:
        yield db
    finally:
        await db.close()


app.dependency_overrides[get_db_async] = override_get_db_async
print(app.dependency_overrides)


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


@pytest.fixture(scope="session", autouse=True)
async def setup_and_teardown():
    print("Setting up for the data for session level...")
    await setup()
    yield
    await teardown()


def test_index():
    print("Testing the index route...")
    res = client.get("/")
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_get_all_notes(setup_and_teardown):
    print("Running test_get_all_notes test case")
    response = await client.get("/api/v1/notes/")
    print("Response: ", response.json())
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "List of notes"
    assert response.json()["ui_message"] == "List of notes from the database"
    assert len(response.json()["notes"]) >= 0
