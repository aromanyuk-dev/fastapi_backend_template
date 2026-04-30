class DomainError(Exception):
    """Base class for domain-level errors."""


class UserNotFound(DomainError):
    pass


class EmailAlreadyTaken(DomainError):
    pass
