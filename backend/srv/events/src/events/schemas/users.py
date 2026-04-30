import datetime
import uuid

from pydantic import BaseModel

from events.schemas.user_types import UserType


class SignupUser(BaseModel):
    name: str
    family_name: str
    birth_date: datetime.date
    email: str


class UserResponse(SignupUser):
    id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    role: UserType
    can_create_event: bool
    is_active: bool
    is_premium: bool


    @classmethod
    def from_domain(cls, user: "User") -> "UserResponse":
        return cls(
            id=user.id,
            name=user.name,
            family_name=user.family_name,
            birth_date=user.birth_date,
            email=user.email,
            role=user.role,
            can_create_event=user.can_create_event,
            is_active=user.is_active,
            is_premium=user.is_premium,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )