
from events.adapters.repository import EventsAbstractRepo
from events.schemas.events import EventResponse
from events.usecase.signup_to_event import EventNotExist


class GetEventUsecase:
    def __init__(self, event_db_repo: EventsAbstractRepo):
        self.event_db_repo = event_db_repo


    async def execute(self, event_id: int) -> EventResponse:
        event = await self.event_db_repo.get(event_id)
        if not event:
            raise EventNotExist

        return EventResponse.from_domain(event)