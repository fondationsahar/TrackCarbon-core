from abc import abstractmethod, ABC
from src.domain.models.event import EventWithEnergy


class BaseEnergyToCarbonConvertor(ABC):
    @abstractmethod
    def to_carbon_emissions(events: list[EventWithEnergy]) -> float:
        """
        Returns the carbon emission factor used by the convertor in gCO2eq/MWh.
        """
        pass
