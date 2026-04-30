import datetime
import uuid
from zoneinfo import ZoneInfo

from events.domain.event_signup import EventSignup
from events.domain.exceptions import AgeRestriction, LimitsExceeded, AlreadyRegistered, CannotRegister
from events.domain.time_range_vo import EventTime


class Event:
    def __init__(self,
                 title: str,
                 description: str,
                 event_time: EventTime,
                 age_limitations: int,
                 max_quantity: int,
                 author_id: uuid.uuid4,
                 id: int = None,
                 created_at: datetime = None,
                 updated_at: datetime = None,
                 signups: list[EventSignup] = None
                 ):
        self.id = id
        self.title = title
        self.description = description
        self.event_time = event_time #vo
        self.age_limitations = age_limitations
        self.max_quantity = max_quantity
        self.author_id = author_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.signups = signups or []



    @property
    def age_limitations(self) -> int:
        return self._age_limitations

    @age_limitations.setter
    def age_limitations(self, value: int) -> None:
        if value < 0 or value > 21:
            raise AgeRestriction
        self._age_limitations = value

    @property
    def remaining_places(self) -> int:
        return self.max_quantity - len(self.signups)

    @classmethod
    def create(cls, title: str,
                    description: str,
                   start_time: datetime.datetime,
                   end_time: datetime.datetime,
                   age_limitations: int,
                   max_quantity: int,
                   author_id: uuid.UUID
                        ) -> "Event":
        now_utc = datetime.datetime.now(tz=ZoneInfo('UTC'))
        if start_time < now_utc:
            raise ValueError('Cannot create an event in the past.')

        return cls(
            title=title,
            description=description,
            event_time = EventTime(start_time, end_time),
            age_limitations=age_limitations,
            max_quantity=max_quantity,
            author_id=author_id
        )


    def add_signup(self, user_id: int, user_age: int) -> None:
        if user_age < self.age_limitations:
            raise AgeRestriction(f"Age should be higher than {self.age_limitations}")

        if self.remaining_places <= 0:
            raise LimitsExceeded("No places left")

        if any(signup.user_id == user_id for signup in self.signups):
            raise AlreadyRegistered('You already registered for this event')

        curr_dt = datetime.datetime.now(tz=ZoneInfo('UTC'))
        if curr_dt > self.event_time.start_time:
            raise CannotRegister('Event already started')

        new_signup = EventSignup(
            event_id=self.id,
            user_id=user_id,
        )
        self.signups.append(new_signup)







