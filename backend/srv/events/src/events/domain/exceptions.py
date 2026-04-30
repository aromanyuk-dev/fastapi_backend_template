
class EventError(Exception):
    def __init__(self, message: str = 'Event error'):
        super().__init__(message)
        self.message = message


class AgeRestriction(EventError):
    pass


class LimitsExceeded(EventError):
    pass

class AlreadyRegistered(EventError):
    pass

class CannotRegister(EventError):
    pass

class EventTimeConflictError(EventError):
    """Выбрасывается, когда у пользователя уже есть событие в указанное время."""
    pass



class UserError(Exception):
    def __init__(self, message: str = 'User error'):
        super().__init__(message)
        self.message = message

class UserDoesntExist(UserError):
    pass


class UserCantCreateEvents(UserError):
    pass