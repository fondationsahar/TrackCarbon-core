from datetime import datetime
from src.constants import DEFAULT_TIMEZONE
from src.domain.models.event import Event, EventWithEnergy
from src.domain.models.event_metadata import SupportedEventMetadata
from src.domain.models.event_metadata.ai import AIEventMetadata


def fake_events() -> list[Event]:
    return [
        Event(
            uid="0",
            type=SupportedEventMetadata.AI,
            timestamp=datetime(2023, 10, 1, 12, 0, tzinfo=DEFAULT_TIMEZONE),
            created_at=datetime(2023, 10, 1, 12, 0, tzinfo=DEFAULT_TIMEZONE),
            domain_alias="anthropic",
            model="claude-sonnet-4",
            event_metadata=AIEventMetadata(
                prompt="You there?",
                response="Hello - this is a test",
                latency=0.5,
                num_response_tokens=6,
                has_image=False,
                has_video=False,
            ),
        ),
        Event(
            uid="1",
            type=SupportedEventMetadata.AI,
            timestamp=datetime(2023, 10, 1, 12, 0, tzinfo=DEFAULT_TIMEZONE),
            created_at=datetime(2023, 10, 1, 12, 0, tzinfo=DEFAULT_TIMEZONE),
            domain_alias="openai",
            model="gpt-5",
            event_metadata=AIEventMetadata(
                prompt="You there?",
                response="Hello - this is a test",
                latency=0.5,
                num_response_tokens=6,
                has_image=False,
                has_video=False,
            ),
        ),
    ]


def fake_events_with_energy() -> list[EventWithEnergy]:
    return [
        EventWithEnergy(event=fake_events()[0], energy_consumed_kwh=1),
        EventWithEnergy(event=fake_events()[1], energy_consumed_kwh=1),
    ]
