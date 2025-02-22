from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    azure_subscription_id: str
    azure_tenant_id: str
    azure_workspace_id: str
    azure_workspace_name: str
    resource_group_id: str
    client_id: str
    client_secret: SecretStr


def get_settings() -> Settings:
    return Settings()  # type: ignore
