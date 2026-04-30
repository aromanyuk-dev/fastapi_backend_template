import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope='session')
async def test_create_user(async_client: AsyncClient, truncate_tables):
    response = await async_client.post(
        "/users/v1/users",
        json={
              "name": "Alexey",
              "family_name": "Romanyuk",
              "birth_date": "2000-02-16",
              "email": "56_lesha@mail.ru"
}
    )
    assert response.status_code == 201
