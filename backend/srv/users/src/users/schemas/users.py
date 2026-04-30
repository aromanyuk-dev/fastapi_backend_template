import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from users.domain.user_role import UserRole
from users.domain.users.user import User


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    birth_date: datetime.date
    role: UserRole = UserRole.USER


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    birth_date: Optional[datetime.date] = None
    role: Optional[UserRole] = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    email: EmailStr
    birth_date: datetime.date
    role: UserRole
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @classmethod
    def from_domain(cls, user: User) -> "UserResponse":
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            birth_date=user.birth_date,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
