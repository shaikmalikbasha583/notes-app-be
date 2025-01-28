# import logging

# import pytest
# import pytest_asyncio
# from httpx import ASGITransport, AsyncClient
# from sqlalchemy import StaticPool
# from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# from app.main import app
# from app.main.config.db_config import Base, get_db_async

# # SQLALCHEMY
# test_engine = create_async_engine(
#     "sqlite+aiosqlite:///tmp/notes-app-database.sqlite3",  # In-memory DB for tests
#     connect_args={"check_same_thread": False},
#     echo=True,
#     poolclass=StaticPool,
#     logging_name=logging.INFO,
# )

# TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


# # Override for get_db_async to use the test database session
# async def override_get_db_async():
#     async with TestSessionLocal() as db:
#         yield db


# # Setup database (create tables) and teardown (drop tables)
# @pytest_asyncio.fixture(scope="module")
# async def setup_and_teardown_db():
#     """Fixture to setup and teardown the database (create/drop tables)"""
#     # Create tables before any tests run
#     async with test_engine.begin() as conn:
#         print("Creating tables...")
#         await conn.run_sync(Base.metadata.create_all)

#     # Yield to the tests
#     yield

#     # Drop tables after all tests run
#     async with test_engine.begin() as conn:
#         print("Dropping tables...")
#         await conn.run_sync(Base.metadata.drop_all)


# # Override the FastAPI dependencies for the test lifecycle
# @pytest_asyncio.fixture(scope="module", autouse=True)
# async def override_dependencies():
#     app.dependency_overrides[get_db_async] = override_get_db_async
#     # app.dependency_overrides[initialize_db] = (
#     #     lambda: setup_and_teardown_db
#     # )  # No-op, we don't need to initialize DB in tests
#     yield
#     # No need to undo overrides since autouse=True will automatically clean up


# # Test case for creating a note
# @pytest.mark.asyncio
# async def test_create_note(setup_and_teardown_db):
#     title = "Test Note with Pytest Library"
#     description = "This is a test note created using Pytest Library"
#     target_date = "2024-01-20T00:00:00"
#     user_id = 1

#     async with AsyncClient(
#         transport=ASGITransport(app=app), base_url="http://test"
#     ) as ac:
#         print("Testing the create note endpoint...")
#         response = await ac.post(
#             "/api/v1/notes/",
#             json={
#                 "title": title,
#                 "description": description,
#                 "status": "PENDING",
#                 "target_date": target_date,
#                 "user_id": user_id,
#             },
#         )

#     print("Response:", response.json())
#     assert response.status_code == 200
#     assert response.json()["success"] is True
#     assert response.json()["message"] == "New Note has been successfully created"
#     assert response.json()["ui_message"] == "New Note has been successfully created"
#     assert response.json()["created_note"]["title"] == title
#     assert response.json()["created_note"]["description"] == description
#     assert response.json()["created_note"]["status"] == "PENDING"
#     assert response.json()["created_note"]["target_date"] == target_date


# # Test case for getting all notes
# @pytest.mark.asyncio
# async def test_get_all_notes(setup_and_teardown_db):
#     async with AsyncClient(
#         transport=ASGITransport(app=app), base_url="http://test"
#     ) as ac:
#         print("Testing the get all notes endpoint...")
#         response = await ac.get("/api/v1/notes/")

#     print("Response:", response.json())
#     assert response.status_code == 200
#     assert response.json()["success"] is True
#     assert response.json()["message"] == "List of notes"
#     assert response.json()["ui_message"] == "List of notes from the database"
#     assert len(response.json()["notes"]) >= 0
