from events.adapters.repository import EventsAbstractRepo
from events.schemas.events import EventResponse


class ListUserEventsUsecase:
    def __init__(self, event_db_repo: EventsAbstractRepo):
        self.event_db_repo = event_db_repo


    async def execute(self, user_id: int) -> list[EventResponse]:
        events = await self.event_db_repo.list(user_id)
        events_response = [EventResponse.from_domain(event) for event in events]
        return events_response
