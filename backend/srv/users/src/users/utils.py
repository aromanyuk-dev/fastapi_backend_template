import datetime
from zoneinfo import ZoneInfo


def get_utc_now():
    return datetime.datetime.now(tz=ZoneInfo('UTC'))