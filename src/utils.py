import hashlib
from datetime import datetime, timezone, timedelta
from src.constants import DEFAULT_TIMEZONE, DATETIME_FORMAT
from src.domain.models.granularity import Granularity


def generate_hash(s: str) -> str:
    """Generate a hash from a string."""
    return hashlib.md5(s.encode()).hexdigest()


def parse_datetime(
    d: str, format: str = DATETIME_FORMAT, tz: timezone = DEFAULT_TIMEZONE
) -> datetime:
    try:
        parsed_datetime = datetime.strptime(d, format)
        if parsed_datetime.tzinfo is None or (
            parsed_datetime.utcoffset() != tz.utcoffset(parsed_datetime)
        ):
            raise ValueError(f"Timestamp '{d}' must be in UTC.")
        return parsed_datetime
    except ValueError as e:
        raise ValueError(
            f"Timestamp '{d}' is not in the correct format ({format}): {e}"
        )


def parse_datetime_to_str(
    d: datetime,
    format: str = DATETIME_FORMAT,
    tz: timezone = DEFAULT_TIMEZONE,
) -> str:
    """Send a datetime to str"""
    try:
        if d.tzinfo is None or d.utcoffset() != tz.utcoffset(d):
            raise ValueError(f"Timestamp {d} must be in UTC.")
        d_str = d.strftime(format=format)
    except Exception as e:
        raise ValueError(f"Can't parse to str as you have error: {e}")
    return d_str


def floor_datetime(dt: datetime, granularity: Granularity) -> datetime:
    if granularity == Granularity.MINUTE:
        return dt.replace(second=0, microsecond=0)
    elif granularity == Granularity.HOURLY:
        return dt.replace(minute=0, second=0, microsecond=0)
    elif granularity == Granularity.DAILY:
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    elif granularity == Granularity.WEEKLY:
        # Assuming weeks start on Monday
        start_of_week = dt - timedelta(days=dt.weekday())
        return start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        raise ValueError(f"Unsupported granularity: {granularity}")
