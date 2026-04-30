from typing import Callable
from uuid import uuid4

from events.adapters.repository import EventsAbstractRepo
from events.domain.event import Event
from events.domain.exceptions import UserDoesntExist, UserCantCreateEvents
from events.domain.services.event_overlap_checker import EventOverlapChecker
from events.domain.time_range_vo import EventTime
from events.schemas.events import EventCreate, EventResponse
from events.usecase.unit_of_work import AbstractUnitOfWork


class CreateEventUsecase:
    def __init__(self, uow: AbstractUnitOfWork,
                 overlap_checker_factory: Callable[[EventsAbstractRepo], EventOverlapChecker]):
        self.uow = uow
        self.overlap_checker_factory = overlap_checker_factory


    async def execute(self, create_event: EventCreate, user_id: uuid4) -> EventResponse:

        async with self.uow as uow:
            user = await self.uow.users_repo.get(user_id=user_id)
            if not user or not user.is_active:
                raise UserDoesntExist

            if not user.is_premium:
                raise UserCantCreateEvents

            new_event_time = EventTime(
                start_time=create_event.start_time,
                end_time=create_event.end_time
            )
            overlap_checker = self.overlap_checker_factory(uow.events_repo)
            await overlap_checker.check(user_id=user_id, new_event_time=new_event_time)
            event = Event.create(**create_event.model_dump(), author_id=user_id)
            event = await uow.events_repo.add(event)
            await uow.commit()

        return EventResponse.from_domain(event)