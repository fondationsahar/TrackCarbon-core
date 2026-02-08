from pydantic import BaseModel, Field
from pathlib import Path
from typing import Self
from src.domain.models.energy_estimators import SupportedEnergyConsumptionMethod
import yaml


class EstimatorConfig(BaseModel):
    method: SupportedEnergyConsumptionMethod = Field(..., description="")
    description: str = Field(
        default=..., description="Description of the estimator method"
    )
    parameters: dict = Field(
        ...,
        description="Parameters required for the energy estimation method",
    )


class ModelConfig(BaseModel):
    estimator_configs: list[EstimatorConfig] = Field(
        ...,
        description="List of estimator configuration.",
    )

    @classmethod
    def from_yaml(cls, path: Path) -> Self:
        with path.open("r") as file:
            data: dict = yaml.safe_load(file)
        return cls(estimator_configs=[EstimatorConfig(**i) for i in data])
