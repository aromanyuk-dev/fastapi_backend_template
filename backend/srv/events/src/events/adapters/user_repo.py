import uuid
from abc import ABC, abstractmethod
from typing import Optional

from events.domain.event import Event
from events.domain.users.users import User


class UsersAbstractRepo(ABC):

    @abstractmethod
    async def add(self, user: Event) -> Event:
        pass

    @abstractmethod
    async def get(self, user_id: uuid.UUID) -> Optional[User]:
        pass


class SQLAlchemyUserRepo(UsersAbstractRepo):
    def __init__(self, session):
        self.session = session

    async def add(self, user: User) -> User:
        self.session.add(user)

        await self.session.flush()

        return user

    async def get(self, user_id: uuid.uuid4) -> Optional[User]:
        result = await self.session.get(User, user_id)
        return result
