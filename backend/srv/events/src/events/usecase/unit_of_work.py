from abc import ABC, abstractmethod

from events.adapters.repository import EventsAbstractRepo, SQLAlchemyEventsRepo
from events.adapters.user_repo import UsersAbstractRepo, SQLAlchemyUserRepo
from events.dependencies.session import async_session


class AbstractUnitOfWork(ABC):
    events_repo: EventsAbstractRepo
    users_repo: UsersAbstractRepo

    async def __aenter__(self) -> 'AbstractUnitOfWork':
        return self

    async def __aexit__(self, *args):
        """Rollback here to keep trancastion in a clean way"""
        await self.rollback()

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, async_session_factory=async_session):
        self.async_session_factory = async_session_factory

    async def __aenter__(self):
        print('Enter to the context')
        self.async_session = self.async_session_factory()
        self.events_repo = SQLAlchemyEventsRepo(self.async_session)
        self.users_repo = SQLAlchemyUserRepo(self.async_session)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        print('Exit from the context')
        await super().__aexit__(*args)
        await self.async_session.close()


    async def commit(self):
        print('commit')
        await self.async_session.commit()

    async def rollback(self):
        print('rollback')
        await self.async_session.rollback()