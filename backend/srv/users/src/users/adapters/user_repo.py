import uuid
from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from users.domain.users.user import User


class UsersAbstractRepo(ABC):
    @abstractmethod
    async def add(self, user: User) -> User: ...

    @abstractmethod
    async def get(self, user_id: uuid.UUID) -> Optional[User]: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    async def list(self, limit: int, offset: int) -> list[User]: ...

    @abstractmethod
    async def delete(self, user_id: uuid.UUID) -> bool: ...


class SQLAlchemyUsersRepo(UsersAbstractRepo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        return user

    async def get(self, user_id: uuid.UUID) -> Optional[User]:
        return await self.session.get(User, user_id)

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def list(self, limit: int, offset: int) -> list[User]:
        result = await self.session.execute(
            select(User).order_by(User.created_at).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def delete(self, user_id: uuid.UUID) -> bool:
        result = await self.session.execute(delete(User).where(User.id == user_id))
        return result.rowcount > 0
