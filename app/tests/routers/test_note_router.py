import pytest
from fastapi import status


# Test for creating a note
@pytest.mark.asyncio
async def test_create_note(client, setup_and_teardown_db):
    print("Test for creating a note")
    title = "Test Note"
    description = "This is a test note."
    target_date = "2024-01-20T00:00:00"
    user_id = 1

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
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["success"] is True
    assert response.json()["message"] == "New Note has been successfully created"
    assert response.json()["ui_message"] == "New Note has been successfully created"
    assert response.json()["created_note"]["title"] == title


# Test for getting all notes
@pytest.mark.asyncio
async def test_get_all_notes(client, setup_and_teardown_db):
    print("Test for getting all notes")
    response = await client.get("/api/v1/notes/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True
    assert response.json()["message"] == "List of notes"
    assert response.json()["ui_message"] == "List of notes from the database"
    assert len(response.json()["notes"]) >= 0
