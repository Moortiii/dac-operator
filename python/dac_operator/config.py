import os

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")



def get_settings() -> Settings:
    return Settings()  # type: ignore
