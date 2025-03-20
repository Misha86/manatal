from pydantic_settings import SettingsConfigDict

from .base import Settings


class LocalSettings(Settings):
    model_config = SettingsConfigDict(env_file=".env.local", env_file_encoding="utf-8", case_sensitive=True)
    ENVIRONMENT: str = "local"
