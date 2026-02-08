from src.domain.ports.energy_to_carbon_convertor import BaseEnergyToCarbonConvertor
from src.domain.models.event import EventWithEnergy


class MyConvertor(BaseEnergyToCarbonConvertor):
    def to_carbon_emissions(self, events: list[EventWithEnergy]) -> float:
        """
        Simple convertor that multiplies energy consumed by 2.
        """
        result = 0.0
        for event in events:
            result += event.energy_consumed_kwh * 2
        return result  # gCO2eq
