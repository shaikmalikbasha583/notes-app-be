import pytest
from fastapi import status


# Test for creating a user
@pytest.mark.asyncio
async def test_create_user(client, setup_and_teardown_db):
    name: str = "Shaik Malik Basha create_user"

    response = await client.post(
        "/api/v1/users/",
        json={"name": name},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["success"] is True
    assert response.json()["message"] == "New user has been successfully created"
    assert response.json()["ui_message"] == "New user has been successfully created"
    assert response.json()["created_user"]["name"] == name


# Test for get_all_users
@pytest.mark.asyncio
async def test_get_all_users(client, setup_and_teardown_db):
    response = await client.get("/api/v1/users/")
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True
    assert response.json()["message"] == "List of users"
    assert response.json()["ui_message"] == "List of users from the database"
    assert len(response.json()["users"]) >= 0


# Test to get user by id
@pytest.mark.asyncio
async def test_get_user_by_id(client, setup_and_teardown_db):
    name: str = "Shaik Malik Basha get_user_by_id"

    response = await client.post(
        "/api/v1/users/",
        json={"name": name},
    )

    user_id = response.json()["created_user"]["id"]

    response = await client.get(f"/api/v1/users/{user_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True
    assert response.json()["message"] == "User details"
    assert response.json()["ui_message"] == "User details"
    assert response.json()["user"]["name"] == name


# Test for updating a user
@pytest.mark.asyncio
async def test_update_user(client, setup_and_teardown_db):
    name: str = "Shaik Malik Basha update_user"

    response = await client.post(
        "/api/v1/users/",
        json={"name": name},
    )

    user_id = response.json()["created_user"]["id"]
    new_name = "Shaik Malik Basha"

    response = await client.put(
        f"/api/v1/users/{user_id}",
        json={"name": new_name},
    )

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json()["success"] is True
    assert response.json()["message"] == "User has been successfully updated"
    assert response.json()["ui_message"] == "User has been successfully updated"
    assert response.json()["updated_user"]["name"] == new_name


# Test for deleting a user
@pytest.mark.asyncio
async def test_delete_user(client, setup_and_teardown_db):
    name: str = "Shaik Malik Basha delete_user"

    response = await client.post(
        "/api/v1/users/",
        json={"name": name},
    )

    user_id = response.json()["created_user"]["id"]

    response = await client.delete(f"/api/v1/users/{user_id}")

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json()["success"] is True
    assert response.json()["message"] == "User has been successfully deleted!"
    assert response.json()["ui_message"] == "User has been successfully deleted!"
    assert response.json()["is_deleted"] is True
