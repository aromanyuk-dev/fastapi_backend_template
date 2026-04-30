import datetime

from events.adapters.repository import SQLAlchemyEventsRepo
from events.domain.event import Event
import pytest

@pytest.mark.asyncio
async def test_repository_can_save_event(session):
    async for sess in session:
        repo = SQLAlchemyEventsRepo(sess)
        event = Event(
                      title="Concert",
                      description='Very interseting',
                      start_time=datetime.datetime(2025, 12, 10, 18),
                      end_time=datetime.datetime(2025, 12, 10, 20),
                      age_limitations=18,
                      max_quantity=100,
                      author_id=10
        )

        res = await repo.add(event)
        assert res.id == 1
        assert res.title == 'Concert'

@pytest.mark.asyncio
async def test_repository_get_event_by_id(session):
    async for sess in session:
        repo = SQLAlchemyEventsRepo(sess)
        event = Event(
                      title="Concert",
                      description='Very interseting',
                      start_time=datetime.datetime(2025, 12, 10, 18),
                      end_time=datetime.datetime(2025, 12, 10, 20),
                      age_limitations=18,
                      max_quantity=100,
                      author_id=10
        )
        await repo.add(event)

        res = await repo.get(1)
        assert res.id == 1
        assert res.title == 'Concert'


@pytest.mark.asyncio
async def test_repository_list_events(session):
    async for sess in session:
        repo = SQLAlchemyEventsRepo(sess)
        event_1 = Event(
                      title="Concert",
                      description='Very interseting',
                      start_time=datetime.datetime(2025, 12, 10, 18),
                      end_time=datetime.datetime(2025, 12, 10, 20),
                      age_limitations=18,
                      max_quantity=100,
                      author_id=10
        )
        event_2 = Event(
                      title="Bookclub",
                      description='For clever people',
                      start_time=datetime.datetime(2025, 12, 20, 18),
                      end_time=datetime.datetime(2025, 12, 20, 20),
                      age_limitations=6,
                      max_quantity=10,
                      author_id=10
        )
        await repo.add(event_1)
        await repo.add(event_2)

        res = await repo.list()
        assert len(res) == 2
        assert res[0].id == 1
        assert res[0].title == 'Concert'

        assert res[1].id == 2
        assert res[1].title == 'Bookclub'



