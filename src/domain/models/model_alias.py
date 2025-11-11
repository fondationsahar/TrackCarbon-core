from enum import StrEnum


class ModelAlias(StrEnum):
    """
    Model alias for the models.
    """

    OPENAI_MODEL = "openai_model"
    MISTRAL_MODEL = "mistral_model"
    ANTHROPIC_MODEL = "anthropic_model"
    GOOGLE_MODEL = "google_model"
