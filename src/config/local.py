from pydantic_settings import SettingsConfigDict

from .base import Settings


class LocalSettings(Settings):
    model_config = SettingsConfigDict(env_prefix="LOCAL_")
