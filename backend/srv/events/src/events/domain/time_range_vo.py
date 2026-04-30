import datetime

class EventTime:
    def __init__(self, start_time: datetime.datetime, end_time: datetime.datetime):
        if start_time >= end_time:
            raise ValueError('End time should be later than start time')
        self.start_time = start_time
        self.end_time = end_time

    def __composite_values__(self):
        return self.start_time, self.end_time

    def __eq__(self, other):
        if not isinstance(other, EventTime):
            return NotImplemented
        return (self.start_time == other.start_time and
                self.end_time == other.end_time)

    def __ne__(self, other):
        return not self.__eq__(other)