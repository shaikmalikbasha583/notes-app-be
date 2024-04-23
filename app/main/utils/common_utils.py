from datetime import datetime, timezone


def get_timestamp_in_utc() -> datetime:
    return datetime.now(timezone.utc)
