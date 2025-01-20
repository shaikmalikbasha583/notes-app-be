import asyncio

import pytest
import pytest_asyncio
from dotenv import find_dotenv, load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv(find_dotenv())

from app.main import app  # Import your FastAPI app
from app.main.config.db_config import Base, get_db_async, initialize_db

# SQLALCHEMY
test_engine = create_async_engine(
    # "sqlite+aiosqlite:///:memory:",
    "sqlite+aiosqlite:///test-notes-app-db.sqlite3",
    connect_args={"check_same_thread": False},
    echo=True,
    # poolclass=StaticPool
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


@pytest.mark.asyncio
async def test_runs_in_a_loop():
    assert asyncio.get_running_loop()


@pytest_asyncio.fixture()
async def setup_database():
    """
    Setup and teardown fixture for the test database.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Test database setup complete.")

    yield  # Run all tests here

    async with test_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        print("Dropping tables...")
    print("Test database teardown complete.")


@pytest_asyncio.fixture()
async def override_get_db():
    """
    Fixture to provide the test database session for dependency overrides.
    """
    async with TestSessionLocal() as session:
        yield session


# Override the app dependency to use the test database
@pytest_asyncio.fixture(scope="function", autouse=True)
def apply_dependency_override(override_get_db):
    app.dependency_overrides[get_db_async] = override_get_db
    app.dependency_overrides[initialize_db] = override_initialize_db


@pytest.mark.asyncio
async def test_get_all_notes():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        print(app.dependency_overrides)
        response = await ac.get("/api/v1/notes/")

    print("Response: ", response.json())
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "List of notes"
    assert response.json()["ui_message"] == "List of notes from the database"
    assert len(response.json()["notes"]) >= 0
