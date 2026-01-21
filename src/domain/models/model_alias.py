from enum import StrEnum


class ModelAlias(StrEnum):
    """
    Model alias for the models.
    """

    GPT_4O = "gpt-4o"
    GPT_5 = "gpt-5"
    MISTRAL_LARGE_2411 = "mistral-large-2411"
    CLAUDE_SONNET_4 = "claude-sonnet-4"
    GEMINI_1 = "gemini-1"
