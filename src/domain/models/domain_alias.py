from enum import StrEnum
from src.domain.models.area_mix import AreaMix, ElectricityMapsArea
from src.domain.models.model_alias import ModelAlias


class DomainAlias(StrEnum):
    """
    Domain alias for the domain.
    """

    OPENAI = "openai"
    MISTRAL = "mistral"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"

    def get_models_per_domain_alias(self) -> list[str]:
        """
        Returns the models associated with the domain alias.
        """
        return {
            DomainAlias.OPENAI: [ModelAlias.GPT_4O, ModelAlias.GPT_5],
            DomainAlias.MISTRAL: [ModelAlias.MISTRAL_LARGE_2411],
            DomainAlias.ANTHROPIC: [ModelAlias.CLAUDE_SONNET_4],
            DomainAlias.GOOGLE: [ModelAlias.GEMINI_1],
        }[self]

    def get_domain_alias_from_model(cls, model: ModelAlias) -> "DomainAlias":
        """
        Returns the domain alias for the given model.
        """
        for alias in DomainAlias:
            if model in alias.get_models_per_domain_alias():
                return alias
        raise ValueError(f"Model {model} does not belong to any known domain alias.")

    @staticmethod
    def list_all_available_models() -> list[ModelAlias]:
        return [
            model
            for alias in DomainAlias
            for model in alias.get_models_per_domain_alias()
        ]

    def to_area_mix(self) -> AreaMix:
        if self == DomainAlias.MISTRAL:
            return AreaMix(
                weights={
                    ElectricityMapsArea.FR: 1.0,
                    ElectricityMapsArea.MISO: 0.0,
                    ElectricityMapsArea.CAL: 0.0,
                    ElectricityMapsArea.TEX: 0.0,
                    ElectricityMapsArea.MIDA: 0.0,
                }
            )

        elif self == DomainAlias.OPENAI:
            return AreaMix(
                weights={
                    ElectricityMapsArea.FR: 0.0,
                    ElectricityMapsArea.MISO: 0.25,
                    ElectricityMapsArea.CAL: 0.25,
                    ElectricityMapsArea.TEX: 0.25,
                    ElectricityMapsArea.MIDA: 0.25,
                }
            )
        elif self == DomainAlias.ANTHROPIC:
            return AreaMix(
                weights={
                    ElectricityMapsArea.FR: 0.0,
                    ElectricityMapsArea.MISO: 0.25,
                    ElectricityMapsArea.CAL: 0.25,
                    ElectricityMapsArea.TEX: 0.25,
                    ElectricityMapsArea.MIDA: 0.25,
                }
            )
        elif self == DomainAlias.GOOGLE:
            return AreaMix(
                weights={
                    ElectricityMapsArea.FR: 0.0,
                    ElectricityMapsArea.MISO: 0.25,
                    ElectricityMapsArea.CAL: 0.25,
                    ElectricityMapsArea.TEX: 0.25,
                    ElectricityMapsArea.MIDA: 0.25,
                }
            )
