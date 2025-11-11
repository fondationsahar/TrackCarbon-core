from abc import abstractmethod, ABC
from src.domain.models.event import Event
from src.domain.models.energy_estimators import (
    SupportedEnergyConsumptionMethod,
)


class BaseEnergyEstimator(ABC):
    @abstractmethod
    def compute(events: list[Event]) -> float:
        pass

    @property
    @abstractmethod
    def method(self) -> SupportedEnergyConsumptionMethod:
        pass
