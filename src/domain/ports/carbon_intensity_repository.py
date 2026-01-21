from abc import ABC, abstractmethod
from datetime import datetime


class BaseCarbonIntensityRepository(ABC):
    @abstractmethod
    def get(
        self,
        timestamp: datetime,
        area: str,
    ) -> float: ...
