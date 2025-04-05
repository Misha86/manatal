from pydantic import AnyHttpUrl, PostgresDsn, RedisDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    PROJECT_NAME: str = "Manatal APIs"
    API_PREFIX_V1: str = "/api/v1"
    ENVIRONMENT: str

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "manatallocal"

    SQLALCHEMY_DATABASE_URI: str | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
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

    REDIS_BASE_URL: str = "redis://localhost:6379"

    JINJA2_REDIS_CACHE_URL: str = f"{REDIS_BASE_URL}/0"
    JINJA2_TEMPLATES_FOLDER: str = "templates"
    JINJA2_CACHE_SIZE: int = 400
    JINJA2_CACHE_PREFIX: str = "jinja2:"
    JINJA2_CACHE_TIMEOUT: int = 3600

    REDIS_CACHE_URL: str = f"{REDIS_BASE_URL}/1"

    @field_validator("JINJA2_REDIS_CACHE_URL", "REDIS_CACHE_URL", mode="before")
    @classmethod
    def validate_redis_dsn(cls, value: str) -> str:
        if isinstance(value, str) and str(RedisDsn(value)):
            return value

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION_NAME: str = "us-east-1"
    AWS_S3_BUCKET_NAME: str = "jinja2-test"
    AWS_S3_CUSTOM_DOMAIN: str = f"{AWS_S3_BUCKET_NAME}.s3.{AWS_REGION_NAME}.amazonaws.com"

    JWT_VERIFYING_KEY: str = "local_verifying_key"
    JWT_ALGORITHM: str = "RS256"
    JWT_DISALLOW_SCOPES: list[str] = ["authentication"]
    JWT_ISSUER: str = "http://localhost:8000"

    @field_validator("BACKEND_CORS_ORIGINS", "JWT_DISALLOW_SCOPES", mode="before")
    @classmethod
    def assemble_cors_origins(cls, value: str | list[str]) -> list[str] | str:
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        elif isinstance(value, (list, str)):
            return value
        raise ValueError(value)
