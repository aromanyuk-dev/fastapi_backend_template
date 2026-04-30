from events.adapters.repository import  SQLAlchemyEventsRepo
from events.dependencies.session import get_db_session
from fastapi import Depends


def get_event_repo(session= Depends(get_db_session)):
    return SQLAlchemyEventsRepo(session=session)