from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from events.domain.event import Event
import pytest


def test_create_new_event_success():
    curr_dt = datetime.now(tz=ZoneInfo('UTC'))
    start_time = curr_dt +timedelta(days=30)
    end_time = start_time + timedelta(hours=2)
    event = Event.create(
        title='Meetup',
        description='Very useful',
        start_time = start_time,
        end_time = end_time,
        age_limitations = 18,
        max_quantity=50,
        author_id=111
    )
    assert isinstance(event, Event)

def test_create_new_event_time_in_past():
    curr_dt = datetime.now(tz=ZoneInfo('UTC'))
    start_time = curr_dt + timedelta(days=-30)
    end_time = start_time + timedelta(hours=2)

    with pytest.raises(ValueError, match="Cannot create an event in the past."):
        Event.create(
            title="Meetup",
            description="Very useful",
            start_time=start_time,
            end_time=end_time,
            age_limitations=18,
            max_quantity=50,
            author_id=111,
        )
