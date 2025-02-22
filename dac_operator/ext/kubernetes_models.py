from pydantic import BaseModel


class ConfigMap(BaseModel):
    api_version: str
    binary_data: dict[str, str] | None
    data: dict[str, str] | None
    immutable: bool | None
    kind: str
