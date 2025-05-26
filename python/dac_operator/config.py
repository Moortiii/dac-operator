import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    azure_client_id: str
    azure_client_secret: SecretStr


def get_settings() -> Settings:
    return Settings()  # type: ignore
