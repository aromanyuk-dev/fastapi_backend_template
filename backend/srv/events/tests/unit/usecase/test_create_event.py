from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from events.adapters.repository import EventsAbstractRepo
from events.domain.event import Event
from events.schemas.events import EventCreate
from events.usecase.create_event import CreateEventUsecase
import pytest

curr_dt = datetime.now(tz=ZoneInfo('UTC'))
start_time = curr_dt + timedelta(days=30)
end_time = start_time + timedelta(hours=2)

class EventFakeRepo(EventsAbstractRepo):
    async def add(self, event: Event) -> Event:
        return Event(
            id=1,
            title='Meetup',
            description='Very useful',
            start_time = start_time,
            end_time = end_time,
            age_limitations = 18,
            max_quantity=50,
            author_id=111,
            created_at=datetime.now(tz=ZoneInfo('UTC')),
            updated_at=datetime.now(tz=ZoneInfo('UTC'))
        )

    async def get(self, id: int) -> Event:
        pass

    async def list(self, user_id: int) -> list[Event]:
        pass

    async def save(self, event: Event) -> Event:
        pass


@pytest.mark.asyncio
async def test_create_event_usecase():
    event_db_repo = EventFakeRepo()
    usecase = CreateEventUsecase(event_db_repo=event_db_repo)
    create_event = EventCreate( title='Meetup',
            description='Very useful',
            start_time = start_time,
            end_time = end_time,
            age_limitations = 18,
            max_quantity=50,
            author_id=111,)
    res = await usecase.execute(create_event)
    assert res.id == 1