import pytest
from fastapi import status


# TestCase for getting the app info
@pytest.mark.asyncio
async def test_get_app_info(client):
    response = await client.get("/api/v1/actuator/info")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["app_name"] == "NOTES-APP"
    assert response.json()["app_code"] == "NA"
    assert response.json()["app_version"] == "v0.0.1"
