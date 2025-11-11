from pydantic import BaseModel
from src.domain.models.energy_estimators import (
    SupportedEnergyConsumptionMethod,
)
from src.domain.models.domain_alias import DomainAlias


class EnergyConsumptionPerDomainAlias(BaseModel):
    domain_alias: DomainAlias
    method: SupportedEnergyConsumptionMethod
    value: float
    unit: str


class EnergyConsumption(BaseModel):
    value: float
    unit: str
    method: SupportedEnergyConsumptionMethod
