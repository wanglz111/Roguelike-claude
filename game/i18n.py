"""Internationalization support for the game."""

from typing import Dict, Union


class I18n:
    """Simple internationalization system supporting Chinese and English."""

    def __init__(self, language: str = "en"):
        """Initialize with default language.

        Args:
            language: "en" for English, "zh" for Chinese
        """
        self.language = language if language in {"en", "zh"} else "en"

    def set_language(self, language: str) -> None:
        """Change the current language."""
        if language in {"en", "zh"}:
            self.language = language

    def get(self, text: Union[str, Dict[str, str]]) -> str:
        """Get localized text.

        Args:
            text: Either a plain string or a dict with "en" and "zh" keys

        Returns:
            Localized string in current language
        """
        if isinstance(text, str):
            return text
        if isinstance(text, dict):
            return text.get(self.language, text.get("en", ""))
        return ""


# Global i18n instance
_i18n = I18n()


def get_i18n() -> I18n:
    """Get the global i18n instance."""
    return _i18n


def t(text: Union[str, Dict[str, str]]) -> str:
    """Shorthand for translating text."""
    return _i18n.get(text)
