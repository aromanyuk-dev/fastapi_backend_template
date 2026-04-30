import datetime
import uuid

from pydantic import BaseModel, Field

from events.domain.event import Event


class EventCreate(BaseModel):
    title: str
    description: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    age_limitations: int
    max_quantity: int

class EventCreateUser(EventCreate):
    author_id: uuid.UUID


class EventResponse(EventCreateUser):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @classmethod
    def from_domain(cls, event: "Event") -> "EventResponse":
        return cls(
            id=event.id,
            title=event.title,
            description=event.description,
            start_time=event.event_time.start_time,
            end_time=event.event_time.end_time,
            age_limitations=event.age_limitations,
            max_quantity=event.max_quantity,
            author_id=event.author_id,
            created_at=event.created_at,
            updated_at=event.updated_at,
        )


class EventSignupRequestSchema(BaseModel):
    user_id: int
    age: int = Field(..., gt=0)