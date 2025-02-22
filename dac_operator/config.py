from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    client_id: str
    client_secret: SecretStr


def get_settings() -> Settings:
    return Settings()  # type: ignore
