import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="session")
async def test_create_user(async_client: AsyncClient):
    response = await async_client.post(
        "/users/v1/users",
        json={
            "name": "Alexey",
            "email": "alexey@example.com",
            "birth_date": "2000-02-16",
            "role": "USER",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "alexey@example.com"
    assert body["name"] == "Alexey"
