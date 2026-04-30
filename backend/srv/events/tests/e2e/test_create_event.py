import uuid
from pprint import pprint

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio(loop_scope='session')
async def test_create_event(async_client: AsyncClient, truncate_tables):
    #preparations
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
    used_id = response.json()["id"]
    data = {
              "title": "string",
              "description": "string",
              "start_time": "2025-10-28T10:00:00.000Z",
              "end_time": "2025-10-28T14:00:00.000Z",
              "age_limitations": 18,
              "max_quantity": 20,
    }
    #execute test
    response = await async_client.post(
        f"/events/v1/events?user_id={used_id}",
        json=data
    )
    assert response.status_code == 201
    pprint(response.json())

    #overlap events
    data = {
              "title": "Cool event",
              "description": "string",
              "start_time": "2025-10-28T12:00:00.000Z",
              "end_time": "2025-10-28T13:00:00.000Z",
              "age_limitations": 18,
              "max_quantity": 20,
    }
    response = await async_client.post(
        f"/events/v1/events?user_id={used_id}",
        json=data
    )

    assert response.status_code == 400
    assert response.json() == {"msg": "You already have events which is overlapped"}

    data = {
              "title": "Python meetup",
              "description": "string",
              "start_time": "2025-10-28T16:00:00.000Z",
              "end_time": "2025-10-28T17:00:00.000Z",
              "age_limitations": 18,
              "max_quantity": 20,
    }
    response = await async_client.post(
        f"/events/v1/events?user_id={used_id}",
        json=data
    )
    assert response.status_code == 201

    # user doesn't exist
    response = await async_client.post(
        f"/events/v1/events?user_id={uuid.uuid4()}",
        json=data
    )
    assert response.status_code == 400
    assert response.json() == {"msg": "Bad Request"}


