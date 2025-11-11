from enum import StrEnum
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
            DomainAlias.OPENAI: [ModelAlias.OPENAI_MODEL],
            DomainAlias.MISTRAL: [ModelAlias.MISTRAL_MODEL],
            DomainAlias.ANTHROPIC: [ModelAlias.ANTHROPIC_MODEL],
            DomainAlias.GOOGLE: [ModelAlias.GOOGLE_MODEL],
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
