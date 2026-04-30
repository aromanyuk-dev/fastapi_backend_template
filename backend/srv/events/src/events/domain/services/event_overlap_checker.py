from uuid import UUID

from events.adapters.repository import EventsAbstractRepo
from events.domain.exceptions import EventTimeConflictError
from events.domain.time_range_vo import EventTime


class EventOverlapChecker:
    def __init__(self, events_repo: EventsAbstractRepo):
        self.events_repo = events_repo

    async def check(self, user_id: UUID, new_event_time: EventTime) -> None:
        """
        Проверяет, есть ли у пользователя пересекающиеся по времени события.
        Выбрасывает EventTimeConflictError, если пересечение найдено.
        """
        user_events = await self.events_repo.get_by_user_id(user_id=user_id)

        for existing_event in user_events:

            has_overlap = (
                    new_event_time.start_time < existing_event.event_time.end_time and
                    new_event_time.end_time > existing_event.event_time.start_time
            )

            if has_overlap:
                raise EventTimeConflictError(
                    f"У вас уже есть событие '{existing_event.title}', "
                    f"которое пересекается с этим временным интервалом."
                )