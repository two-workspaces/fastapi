"""Settings read from environment variables.

Every value has a default and a bad value falls back to it with a warning,
so a typo in a Railway variable never stops the app from booting.
"""
import os
from dataclasses import dataclass, field

# Problems found while reading variables; app.main logs them once logging is set up.
warnings: list[str] = []

LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


def _str(name: str, default: str) -> str:
    value = os.environ.get(name, "").strip()
    return value or default


def _bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name, "").strip().lower()
    if not raw:
        return default
    if raw in {"1", "true", "yes", "on"}:
        return True
    if raw in {"0", "false", "no", "off"}:
        return False
    warnings.append(f"{name}={raw!r} is not true/false; using {default}")
    return default


def _list(name: str) -> list[str]:
    raw = os.environ.get(name, "")
    return [item.strip() for item in raw.split(",") if item.strip()]


def _log_level() -> str:
    level = _str("LOG_LEVEL", "INFO").upper()
    if level not in LOG_LEVELS:
        warnings.append(f"LOG_LEVEL={level!r} is not one of {sorted(LOG_LEVELS)}; using INFO")
        return "INFO"
    return level


@dataclass(frozen=True)
class Settings:
    app_name: str = field(default_factory=lambda: _str("APP_NAME", "FastAPI"))
    log_level: str = field(default_factory=_log_level)
    # Comma-separated origins allowed to call the API from a browser, or "*".
    cors_origins: list[str] = field(default_factory=lambda: _list("CORS_ORIGINS"))
    # Set DOCS_ENABLED=false to hide /docs, /redoc and /openapi.json in production.
    docs_enabled: bool = field(default_factory=lambda: _bool("DOCS_ENABLED", True))
    # Railway sets these on every deploy; handy in /health and logs.
    environment: str = field(default_factory=lambda: _str("RAILWAY_ENVIRONMENT_NAME", "local"))
    commit: str = field(default_factory=lambda: _str("RAILWAY_GIT_COMMIT_SHA", "")[:7])


settings = Settings()
