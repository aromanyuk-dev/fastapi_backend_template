from abc import ABC, abstractmethod

from users.adapters.user_repo import SQLAlchemyUsersRepo, UsersAbstractRepo


class AbstractUnitOfWork(ABC):
    users_repo: UsersAbstractRepo

    async def __aenter__(self) -> "AbstractUnitOfWork":
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, async_session_factory):
        self.async_session_factory = async_session_factory

    async def __aenter__(self):
        self.session = self.async_session_factory()
        self.users_repo = SQLAlchemyUsersRepo(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
