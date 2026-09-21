"""tests/test_config.py"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.core.config import Settings, get_settings


def test_settings_load_from_env(settings: Settings) -> None:
    assert settings.gemini.api_key.get_secret_value() == "test-api-key"
    assert settings.app.environment == "local"


def test_settings_missing_secret_falls_back_gracefully(monkeypatch: pytest.MonkeyPatch) -> None:
    """GEMINI_API_KEY defaults to empty string to permit alternate LLM providers or offline mode."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEYS", raising=False)
    get_settings.cache_clear()
    s = Settings()
    assert s.gemini.api_key.get_secret_value() == ""


def test_settings_defaults_applied(settings: Settings) -> None:
    assert settings.gemini.model_name in ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-flash-latest"]
    assert settings.gemini.max_json_retries == 2
    assert settings.database.pool_min_size == 1


def test_get_settings_is_cached(settings: Settings) -> None:
    assert get_settings() is get_settings()
