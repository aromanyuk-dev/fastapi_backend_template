import uuid
from abc import ABC, abstractmethod

from events.domain.event import Event
from sqlalchemy import select

from events.domain.event_signup import EventSignup


class RepositoryError(Exception):
    pass


class DuplicatedError(RepositoryError):
    pass



class EventsAbstractRepo(ABC):

    @abstractmethod
    async def add(self, event: Event) -> Event:
        pass

    @abstractmethod
    async def get(self, id: int) -> Event:
        pass

    @abstractmethod
    async def list_all(self, user_id: int) -> list[Event]:
        pass

    @abstractmethod
    async def save(self, event: Event) -> Event:
        pass


    @abstractmethod
    async def get_by_user_id(self, user_id: uuid.UUID) -> list[Event]:
        pass


class SQLAlchemyEventsRepo(EventsAbstractRepo):
    def __init__(self, session):
        self.session = session

    async def add(self, event: Event) -> Event:
        self.session.add(event)

        await self.session.flush()

        return event

    async def get(self, id: int) -> Event:
        result = await self.session.execute(select(Event).where(Event.id == id))
        return result.unique().scalar_one_or_none()

    async def list_all(self, user_id: int) -> list[Event]:
        query = (
            select(Event)
            .join(Event.signups)
            .where(EventSignup.user_id == user_id)
        )
        result = await self.session.execute(query)
        return result.unique().scalars().all()

    async def save(self, event: Event) -> Event:
        self.session.add(event)
        await self.session.commit()
        return event


    async def get_by_user_id(self, user_id: uuid.UUID) -> list[Event]:
        """
        Находит и возвращает все события, созданные указанным пользователем.
        """
        # 1. Создаем запрос для выбора объектов Event
        query = select(Event).where(Event.author_id == user_id)

        # 2. Асинхронно выполняем запрос
        result = await self.session.execute(query)

        # 3. Извлекаем все результаты в виде списка объектов Event
        # .scalars() получает первый столбец из каждой строки (в нашем случае это и есть объект Event)
        # .all() собирает все результаты в список
        # .unique() гарантирует отсутствие дубликатов, если бы в запросе были JOIN'ы
        return result.unique().scalars().all()