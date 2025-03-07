import pytest
from fastapi import status


# Test for creating a note
@pytest.mark.asyncio
async def test_add_note(client, setup_and_teardown_db):
    print("Test for creating a note")
    title = "Test Note - <func name='test_add_note'>"
    description = "This is a test note - <func name='test_add_note'>."
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


# Test for getting a note by ID
@pytest.mark.asyncio
async def test_get_note_by_id(client, setup_and_teardown_db):
    print("Test for getting a note by ID")
    title = "Test Note - <func name='test_get_note_by_id'>"
    description = "This is a test note - <func name='test_get_note_by_id'>."
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
    _id = response.json()["created_note"]["id"]

    response = await client.get(f"/api/v1/notes/{_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True
    assert response.json()["message"] == "Note Details"
    assert response.json()["ui_message"] == "Note Details"
    assert response.json()["note"]["id"] == _id


# Test for Note not found
@pytest.mark.asyncio
async def test_get_note_by_id_not_found(client, setup_and_teardown_db):
    print("Test for Note not found")
    with pytest.raises(Exception):
        response = await client.get("/api/v1/notes/1000")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["success"] is True
        assert response.json()["message"] == "Bad Request"
        assert response.json()["description"] == "Note Not Found"
        assert response.json()["ui_message"] == "Note with id:'1000' doesn't exist"


# Test for updating a note
@pytest.mark.asyncio
async def test_update_note_by_id(client, setup_and_teardown_db):
    print("Test for updating a note")
    title = "Test Note - <func name='test_update_note_by_id'>"
    description = "This is a test note - <func name='test_update_note_by_id'>"
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
    _id = response.json()["created_note"]["id"]

    new_title = "Updated Test Note - <func name='test_update_note_by_id'>"
    new_description = (
        "This is an updated test note - <func name='test_update_note_by_id'>"
    )
    new_target_date = "2024-01-20T00:00:00"

    response = await client.put(
        f"/api/v1/notes/{_id}",
        json={
            "title": new_title,
            "description": new_description,
            "status": "PENDING",
            "target_date": new_target_date,
            "user_id": user_id,
        },
    )

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json()["success"] is True
    assert response.json()["message"] == "Note has been successfully updated"
    assert response.json()["ui_message"] == "Note has been successfully updated"
    assert response.json()["updated_note"]["title"] == new_title


# Test for deleting a note
@pytest.mark.asyncio
async def test_delete_note_by_id(client, setup_and_teardown_db):
    print("Test for deleting a note")
    title = "Test Note - <func name='test_delete_note_by_id'>"
    description = "This is a test note - <func name='test_delete_note_by_id'>"
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
    _id = response.json()["created_note"]["id"]

    response = await client.delete(f"/api/v1/notes/{_id}")

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json()["success"] is True
    assert response.json()["message"] == "Note has been successfully deleted!"
    assert response.json()["ui_message"] == "Note has been successfully deleted!"
    assert response.json()["is_deleted"] is True
