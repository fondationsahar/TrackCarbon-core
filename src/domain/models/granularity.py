from enum import StrEnum


class Granularity(StrEnum):
    MINUTE = "minute"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"

    def to_pandas_freq(self) -> str:
        """Convert the granularity to pandas frequency string."""
        if self == Granularity.MINUTE:
            return "1min"
        if self == Granularity.HOURLY:
            return "1h"
        elif self == Granularity.DAILY:
            return "1d"
        elif self == Granularity.WEEKLY:
            return "1w"
        else:
            raise ValueError(f"Unsupported granularity: {self}")
