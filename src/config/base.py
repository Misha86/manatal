import secrets
from typing import List, Optional, Union

from pydantic import AnyHttpUrl, HttpUrl, PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    PROJECT_NAME: str = "My first project"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ENVIRONMENT: str

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, value: Union[str, List[str]]) -> Union[List[str], str]:  # noqa
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        elif isinstance(value, (list, str)):
            return value
        raise ValueError(value)

    SENTRY_DSN: HttpUrl | None = None

    @field_validator("SENTRY_DSN")
    def sentry_dsn_can_be_blank(cls, url: str) -> Optional[str]:  # noqa
        return None if url is None or not url else url

    SQLALCHEMY_DATABASE_URI: str | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI")
    def assemble_db_connection(cls, value: Optional[str], info: ValidationInfo) -> str:  # noqa
        if isinstance(value, str):
            return value

        env_data = info.data
        postgres_dsn = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=env_data.get("POSTGRES_USER", "postgres"),
            password=env_data.get("POSTGRES_PASSWORD", "postgres"),
            host=env_data.get("POSTGRES_HOST", "localhost"),
            port=env_data.get("POSTGRES_PORT", 5432),
            path=env_data.get("POSTGRES_DB", "manatallocal"),
        )
        return str(postgres_dsn)
