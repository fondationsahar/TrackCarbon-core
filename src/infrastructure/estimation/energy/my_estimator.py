from src.domain.models.event import Event
from src.domain.ports.energy_estimator import BaseEnergyEstimator


class MyEstimator(BaseEnergyEstimator):
    def compute(self, events: list[Event]) -> float:
        return len(events)

    @property
    def method(self) -> str:
        return "my_method"
