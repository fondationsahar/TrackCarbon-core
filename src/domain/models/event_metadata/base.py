from abc import ABC, abstractmethod
from typing import Self
from pydantic import BaseModel


class BaseEventMetadata(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def from_dict(data: dict) -> Self:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass
