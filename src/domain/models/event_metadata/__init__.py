from enum import StrEnum
from src.domain.models.event_metadata.ai import AIEventMetadata


class SupportedEventMetadata(StrEnum):
    AI = "ai"


__all__ = [
    "AIEventMetadata",
]

EventMetadataRegistry = {
    SupportedEventMetadata.AI: AIEventMetadata,
}
