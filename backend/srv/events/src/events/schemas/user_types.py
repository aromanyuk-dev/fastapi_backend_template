from enum import Enum


class UserType(str, Enum):
    USER = "USER"
    MODERATOR = "MODERATOR"
    SYSTEM = "SYSTEM"