import datetime
from uuid import uuid4

from events.schemas.user_types import UserType


class User:
    def __init__(self,
                name: str,
                family_name: str,
                email: str,
                birth_date: datetime.datetime,
                role: UserType,
                can_create_event: bool,
                is_active: bool,
                is_premium: bool,
                id: uuid4 = None,
                created_at: datetime = None,
                updated_at: datetime = None):
        self.id = id
        self.name = name
        self.family_name = family_name
        self.birth_date = birth_date
        self.email = email
        self.role = role
        self.can_create_event = can_create_event
        self.is_active = is_active
        self.is_premium = is_premium
        self.created_at = created_at
        self.updated_at = updated_at


    @classmethod
    def create_user(cls, name: str, family_name: str, birth_date: datetime.datetime, email: str):
        return User(
            name=name,
            family_name=family_name,
            birth_date=birth_date,
            email=email,
            role=UserType.USER,
            can_create_event=False,
            is_active=True,
            is_premium=True
        )
