import pytest
from fastapi import status


# Test for creating a note
@pytest.mark.asyncio
async def test_create_note(client, setup_and_teardown_db):
    name: str = "Shaik Malik Basha"

    response = await client.post(
        "/api/v1/users/",
        json={"name": name},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["success"] is True
    assert response.json()["message"] == "New user has been successfully created"
    assert response.json()["ui_message"] == "New user has been successfully created"
    assert response.json()["created_user"]["name"] == name
