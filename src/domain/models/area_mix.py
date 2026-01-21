from enum import StrEnum

from pydantic import BaseModel, field_validator, model_validator


class ElectricityMapsArea(StrEnum):
    FR = "FR"
    MISO = "US-MIDW-MISO"
    CAL = "US-CAL-CISO"
    TEX = "US-TEX-ERCO"
    MIDA = "US-MIDA-PJM"


class AreaMix(BaseModel):
    weights: dict[ElectricityMapsArea, float]

    @field_validator("weights")
    @classmethod
    def values_between_0_and_1(
        cls, v: dict[ElectricityMapsArea, float]
    ) -> dict[ElectricityMapsArea, float]:
        for area, weight in v.items():
            if not 0.0 <= weight <= 1.0:
                raise ValueError(
                    f"Weight for area {area} must be between 0 and 1, got {weight}"
                )
        return v

    @model_validator(mode="after")
    def validate_distribution(self) -> "AreaMix":
        missing = set(ElectricityMapsArea) - set(self.weights)
        if missing:
            raise ValueError(f"Missing areas in distribution: {missing}")

        total = sum(self.weights.values())
        if not abs(total - 1.0) < 1e-6:
            raise ValueError(f"AreaMix weights must sum to 1, got {total}")

        return self
