from typing import Self
from datetime import datetime
from src.constants import DEFAULT_TIMEZONE
from src.domain.models.event_metadata.base import BaseEventMetadata
from src.domain.models.event_metadata import SupportedEventMetadata
from src.domain.models.domain_alias import DomainAlias
from pydantic import BaseModel, Field, field_validator, model_validator
from src.utils import generate_hash


class Event(BaseModel):
    uid: str = Field(..., description="Unique identifier for the event.")
    type: SupportedEventMetadata = Field(
        ..., description="Type of the event, currently only 'ai' is supported."
    )
    timestamp: datetime = Field(
        ..., description="Timestamp when the event was intercepted."
    )
    created_at: datetime = Field(
        ..., description="Timestamp when the event was ingested."
    )
    domain_alias: DomainAlias = Field(
        ..., description="Domain with which the communication was made."
    )
    model: str = Field(..., description="Model used for the event, e.g., 'gpt-4o'.")
    event_metadata: BaseEventMetadata = Field(
        ..., description="Metadata associated with the event."
    )

    @field_validator("timestamp", "created_at")
    def validate_datetime_is_utc(cls, value: datetime) -> datetime:
        """Ensure that the datetime is in UTC."""
        if value.utcoffset() != DEFAULT_TIMEZONE.utcoffset(value):
            raise ValueError("Datetime must be in UTC.")
        return value

    @model_validator(mode="after")
    def validate_model_belongs_to_domain_models(self) -> Self:
        """Ensure that the model belongs to the domain alias."""
        if self.model not in self.domain_alias.get_models_per_domain_alias():
            raise ValueError(
                f"Model {self.model} does not belong to domain alias {self.domain_alias}."
            )
        return self

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Create a Prompt instance from a dictionary."""
        return cls(
            uid=generate_hash(
                s=f"{data['timestamp']}{data['model']}{data['domain_alias']}{data['event_metadata'].__str__()}"
            ),
            type=data.get("type"),
            timestamp=data.get("timestamp"),
            created_at=data.get("created_at"),
            domain_alias=data.get("domain_alias"),
            model=data.get("model"),
            event_metadata=data.get("event_metadata"),
        )


class EventWithEnergy(BaseModel):
    event: Event
    energy_consumed_kwh: float
