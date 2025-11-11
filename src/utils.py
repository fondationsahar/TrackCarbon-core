import hashlib
import json
import re
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


def parse_and_reconstruct_sse_from_openai(raw: bytes) -> str:
    """Parse raw SSE bytes and reconstruct the message content."""
    raw_str = raw.decode("utf-8")
    entries = raw_str.strip().split("\n\n")

    message = ""
    for entry in entries:
        lines = entry.strip().split("\n")
        evt = {"event": None, "data": ""}
        for line in lines:
            if line.startswith("event:"):
                evt["event"] = line[len("event:") :].strip()
            elif line.startswith("data:"):
                evt["data"] += line[len("data:") :].strip()

        if evt["event"] != "delta":
            continue

        try:
            data = json.loads(evt["data"])
        except json.JSONDecodeError:
            continue

        v = data.get("v")
        if isinstance(v, str):
            message += v
        elif isinstance(v, dict):
            content = v.get("message", {}).get("content", {})
            parts = content.get("parts", [])
            if parts:
                message = parts[0]
        elif isinstance(v, list):
            for patch in v:
                if patch["p"] == "/message/content/parts/0":
                    if patch["o"] == "append":
                        message += patch["v"]
                    elif patch["o"] == "replace":
                        message = patch["v"]

    return message


def reassemble_sse_content_from_mistral(raw_bytes: bytes) -> str:
    content = raw_bytes.decode("utf-8")
    lines = content.strip().split("\n")

    chunks = []
    for line in lines:
        if line.startswith("0:"):
            match = re.match(r'0:"(.*)"', line)
            if match:
                chunks.append(match.group(1))

    return "".join(chunks)


def reassemble_sse_text_stream_from_claude(raw_bytes: bytes) -> str:
    text_chunks = []
    content = raw_bytes.decode("utf-8")
    entries = content.strip().split("\n\n")

    for entry in entries:
        lines = entry.strip().split("\n")
        event_type = None
        data_payload = None

        for line in lines:
            if line.startswith("event:"):
                event_type = line[len("event:") :].strip()
            elif line.startswith("data:"):
                data_payload = line[len("data:") :].strip()

        if event_type == "content_block_delta" and data_payload:
            try:
                data = json.loads(data_payload)
                delta = data.get("delta", {})
                text = delta.get("text")
                if text:
                    text_chunks.append(text)
            except json.JSONDecodeError:
                pass  # skip bad JSON

    return "".join(text_chunks)
