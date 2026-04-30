from events.adapters.repository import EventsAbstractRepo
from events.dependencies.repos import get_event_repo
from events.dependencies.unit_of_work import get_sqlalchemy_uow
from events.domain.services.event_overlap_checker import EventOverlapChecker
from events.usecase.create_event import CreateEventUsecase
from fastapi import Depends

from events.usecase.get_event import GetEventUsecase
from events.usecase.list_user_events import ListUserEventsUsecase
from events.usecase.signup_to_event import SignupToEventUsecase
from events.usecase.unit_of_work import AbstractUnitOfWork

def get_overlap_checker(repo: EventsAbstractRepo) -> EventOverlapChecker:
    return EventOverlapChecker(events_repo=repo)

def get_create_event_usecase(uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow)):
    return CreateEventUsecase(uow=uow,
                              overlap_checker_factory=get_overlap_checker)


def get_signup_to_event_usecase(event_db_repo: EventsAbstractRepo = Depends(get_event_repo)):
    return SignupToEventUsecase(event_db_repo=event_db_repo)

def get_get_event_usecase(event_db_repo: EventsAbstractRepo = Depends(get_event_repo)):
    return GetEventUsecase(event_db_repo=event_db_repo)

def get_list_user_events_usecase(event_db_repo: EventsAbstractRepo = Depends(get_event_repo)):
    return ListUserEventsUsecase(event_db_repo)

