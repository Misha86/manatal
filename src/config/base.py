import secrets
from pathlib import Path
from typing import List, Union

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import (
    AnyHttpUrl,
    PostgresDsn,
    RedisDsn,
    ValidationInfo,
    field_validator,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

from src.core.cache.backends.redis import RedisBytecodeCache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    PROJECT_NAME: str = "Manatal APIs"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ENVIRONMENT: str

    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    TEMPLATE_DIRS: list[Path] = [BASE_DIR / "templates"]

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS")
    @classmethod
    def assemble_cors_origins(cls, value: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        elif isinstance(value, (list, str)):
            return value
        raise ValueError(value)

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "manatallocal"

    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI")
    @classmethod
    def assemble_db_connection(cls, value: str | None, info: ValidationInfo) -> str:
        if isinstance(value, str) and str(PostgresDsn(value)):
            return value

        env_data = info.data

        postgres_dsn = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=env_data["POSTGRES_USER"],
            password=env_data["POSTGRES_PASSWORD"],
            host=env_data["POSTGRES_HOST"],
            port=env_data["POSTGRES_PORT"],
            path=env_data["POSTGRES_DB"],
        )
        return str(postgres_dsn)

    JINJA2_REDIS_DSN: RedisDsn = "redis://localhost:6379/0"
    JINJA2_CACHE_SIZE: int = 400
    JINJA2_CACHE_PREFIX: str = "jinja2:"
    JINJA2_CACHE_TIMEOUT: int = 3600

    bytecode_cache: RedisBytecodeCache = RedisBytecodeCache(
        location=JINJA2_REDIS_DSN, key_prefix=JINJA2_CACHE_PREFIX, timeout=JINJA2_CACHE_TIMEOUT
    )

    JINJA2_ENV: Environment = Environment(
        loader=FileSystemLoader(TEMPLATE_DIRS),
        autoescape=select_autoescape(enabled_extensions=("html",)),
        cache_size=JINJA2_CACHE_SIZE,
        bytecode_cache=bytecode_cache,
        trim_blocks=True,
        lstrip_blocks=True,
        enable_async=True,
    )
