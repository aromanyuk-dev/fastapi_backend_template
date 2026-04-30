import datetime


class EventSignup:

    def __init__(self,
                 event_id: int,
                 user_id: int,
                 id: int = None,
                 created_at: datetime.datetime = None,
                 updated_at: datetime.datetime = None):
        self.id = id
        self.event_id = event_id
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at
