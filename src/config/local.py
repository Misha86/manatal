from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from pydantic import field_validator
from pydantic_settings import SettingsConfigDict

from .base import Settings


class LocalSettings(Settings):
    model_config = SettingsConfigDict(env_prefix="LOCAL_")

    JWT_PRIVATE_KEY: str

    @field_validator("JWT_PRIVATE_KEY")
    @classmethod
    def validate_jwt_private_key(cls, value: str) -> str:
        private_key = value.replace("\\n", "\n")

        if not (
            private_key.startswith("-----BEGIN PRIVATE KEY-----") or private_key.startswith("-----BEGIN RSA PRIVATE KEY-----")
        ) or not private_key.strip().endswith("-----END PRIVATE KEY-----"):
            raise ValueError("Invalid RS256 private key format.")

        try:
            serialization.load_pem_private_key(private_key.encode(), password=None, backend=default_backend())
        except Exception as err:
            raise ValueError(f"Invalid private key: {err}")

        return private_key
