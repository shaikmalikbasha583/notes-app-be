"""
This is used to create common fixtures for the tests
"""

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.main import app
from app.main.config.db_config import Base, get_db_async

# SQLALCHEMY CONFIG
test_engine = create_async_engine(
    "sqlite+aiosqlite:///tmp/notes-app-db.sqlite3",  # In-memory DB for tests, use (:memory:)
    connect_args={"check_same_thread": False},
    echo=False,
    poolclass=StaticPool,
)

TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


# Override get_db_async to use the test DB session
async def override_get_db_async():
    async with TestSessionLocal() as db:
        yield db


# DB Setup and Teardown
@pytest_asyncio.fixture(scope="module")
async def setup_and_teardown_db():
    """Create/drop tables before/after tests."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Dependency overrides for FastAPI for testing
@pytest_asyncio.fixture(scope="module", autouse=True)
async def override_dependencies():
    app.dependency_overrides[get_db_async] = override_get_db_async
    yield
    # No need to undo overrides since autouse=True will handle cleanup


# HTTP Client Fixture
@pytest_asyncio.fixture()
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
