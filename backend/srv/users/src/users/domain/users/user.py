import datetime
import uuid
from typing import Optional

from users.domain.user_role import UserRole


class User:
    def __init__(
        self,
        name: str,
        email: str,
        birth_date: datetime.date,
        role: UserRole,
        id: Optional[uuid.UUID] = None,
        created_at: Optional[datetime.datetime] = None,
        updated_at: Optional[datetime.datetime] = None,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.birth_date = birth_date
        self.role = role
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create(
        cls,
        name: str,
        email: str,
        birth_date: datetime.date,
        role: UserRole = UserRole.USER,
    ) -> "User":
        return cls(
            id=uuid.uuid4(),
            name=name,
            email=email,
            birth_date=birth_date,
            role=role,
        )

    def update(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        birth_date: Optional[datetime.date] = None,
        role: Optional[UserRole] = None,
    ) -> None:
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if birth_date is not None:
            self.birth_date = birth_date
        if role is not None:
            self.role = role
