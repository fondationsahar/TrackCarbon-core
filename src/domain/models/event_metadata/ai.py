from typing import Self
from pydantic import Field
from src.utils import generate_hash
from src.domain.models.event_metadata.base import BaseEventMetadata


class AIEventMetadata(BaseEventMetadata):
    prompt: str = Field(..., description="Content of the prompt sent.")
    response: str = Field(..., description="Content of the response received.")
    latency: float = Field(..., description="Latency in receiving a response.")
    num_response_tokens: int = Field(
        ...,
        description="Number of tokens in the response.",
    )
    has_image: bool = Field(
        default=False,
        description="Indicates if the AI event contains an image.",
    )
    has_video: bool = Field(
        default=False,
        description="Indicates if the AI event contains a video.",
    )

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Create an AIMetadata instance from a dictionary."""
        return cls(
            prompt=data.get("prompt"),
            response=data.get("response"),
            latency=data.get("latency"),
            num_response_tokens=data.get("num_response_tokens"),
            has_image=data.get("has_image"),
            has_video=data.get("has_video"),
            estimated_emission_factor=data.get("estimated_emission_factor"),
        )

    def __str__(self):
        return f"AIMetadata(prompt_hash={generate_hash(self.prompt)}, has_image={self.has_image}, has_video={self.has_video})"
