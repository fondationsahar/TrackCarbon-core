from src.domain.ports.carbon_intensity_repository import BaseCarbonIntensityRepository
from src.domain.ports.energy_to_carbon_convertor import BaseEnergyToCarbonConvertor
from src.domain.models.event import EventWithEnergy


class ElectricityMapsBasedConvertor(BaseEnergyToCarbonConvertor):
    def __init__(
        self,
        carbon_intensity_repository: BaseCarbonIntensityRepository,
    ) -> None:
        self.carbon_intensity_repository = carbon_intensity_repository

    def get_estimated_carbon_intensity_for_an_event(
        self, event: EventWithEnergy
    ) -> float:
        """
        This method is a wrapper around the "core" model to apply to
        a single event.
        """
        timestamp = event.event.timestamp
        domain_alias = event.event.domain_alias
        mix = domain_alias.to_area_mix()

        carbon_intensity = 0.0
        for area, weight in mix.weights.items():
            zone_ci = self.carbon_intensity_repository.get(
                timestamp=timestamp,
                zone=area.value,
            )
            carbon_intensity += weight * zone_ci

        return carbon_intensity  # gCO2eq / kWh

    def to_carbon_emissions(self, events: list[EventWithEnergy]) -> float:
        """
        This method is a wrapper around the "core" model to apply to
        a list of events.
        """
        result = 0.0
        for i in events:
            result += (
                i.energy_consumed_kwh
                * self.get_estimated_carbon_intensity_for_an_event(i)
            )
        return result  # gCo2eq
