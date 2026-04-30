from events.adapters.repository import EventsAbstractRepo
from events.domain.event import Event
from events.schemas.events import EventCreate, EventResponse, EventSignupRequestSchema

class EventNotExist(Exception):
    pass


class SignupToEventUsecase:
    def __init__(self, event_db_repo: EventsAbstractRepo):
        self.event_db_repo = event_db_repo


    async def execute(self, event_id: int, signup_request:EventSignupRequestSchema) -> EventResponse:
        event = await self.event_db_repo.get(event_id)
        if not event:
            raise EventNotExist
        event.add_signup(user_id=signup_request.user_id,
                         user_age=signup_request.age)
        await self.event_db_repo.save(event)
        return EventResponse.from_domain(event)