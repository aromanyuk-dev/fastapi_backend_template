from sqlalchemy import Table, Column, Integer, String, Text, DateTime, func, Boolean, Enum
from sqlalchemy.orm import registry, relationship, composite
from sqlalchemy.sql.schema import ForeignKey, UniqueConstraint

from events.domain.event import Event
from events.domain.event_signup import EventSignup
import uuid
from sqlalchemy.dialects.postgresql import UUID

from events.domain.time_range_vo import EventTime
from events.domain.users.users import User
from events.schemas.user_types import UserType

mapper_registry = registry()
metadata = mapper_registry.metadata

events = Table(
    "events",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), nullable=False),
    Column("description", Text, nullable=True),
    Column("start_time", DateTime(timezone=True), nullable=False),
    Column("end_time", DateTime(timezone=True), nullable=False),
    Column("age_limitations", Integer, nullable=True),
    Column("max_quantity", Integer, nullable=True),
    Column("author_id", UUID(as_uuid=True),nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
)

event_signups = Table(
    "event_signups",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("event_id", Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False),
    Column("user_id", Integer, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),

    UniqueConstraint('event_id', 'user_id', name='uq_event_user')
)

users = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("name", String, nullable=False),
    Column("family_name", String, nullable=False),
    Column("email", String, unique=True, nullable=False),
    Column("birth_date", DateTime(timezone=True), nullable=False),
    Column("role", Enum(UserType, name="user_role"), nullable=False),
    Column("can_create_event", Boolean, nullable=False, server_default="false"),
    Column("is_active", Boolean, nullable=False, server_default="true"),
    Column("is_premium", Boolean, nullable=False, server_default="false"),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),

    UniqueConstraint("email", name="uq_users_email"),
)

def start_mappers():
    print(">>> start_mappers called")

    mapper_registry.map_imperatively(EventSignup, event_signups)
    mapper_registry.map_imperatively(User, users)
    mapper_registry.map_imperatively(Event, events, properties={
        '_age_limitations': events.c.age_limitations,
        'event_time': composite(
            EventTime,
            events.c.start_time,
            events.c.end_time
        ),
        'signups': relationship(
            EventSignup,
            backref='event',
            lazy='joined',
            cascade="all, delete-orphan"
        )
    })

    print(">>> start_mappers finished")