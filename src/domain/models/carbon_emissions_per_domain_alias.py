from pydantic import BaseModel
from src.domain.models.domain_alias import DomainAlias


class CarbonEmissionsPerDomainAlias(BaseModel):
    domain_alias: DomainAlias
    value: float
    unit: str


class CarbonEmissions(BaseModel):
    value: float
    unit: str
