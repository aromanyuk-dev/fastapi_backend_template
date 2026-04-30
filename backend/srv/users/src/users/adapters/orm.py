import uuid

from sqlalchemy import Column, Date, DateTime, Enum, String, Table, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry

from users.domain.user_role import UserRole
from users.domain.users.user import User

mapper_registry = registry()
metadata = mapper_registry.metadata

users = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("name", String(255), nullable=False),
    Column("email", String(255), nullable=False),
    Column("birth_date", Date, nullable=False),
    Column("role", Enum(UserRole, name="user_role"), nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    ),
    UniqueConstraint("email", name="uq_users_email"),
)


_mappers_started = False


def start_mappers() -> None:
    global _mappers_started
    if _mappers_started:
        return
    mapper_registry.map_imperatively(User, users, eager_defaults=True)
    _mappers_started = True
