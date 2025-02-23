from pydantic import BaseModel


class ConfigMap(BaseModel):
    api_version: str
    data: dict[str, str]
    immutable: bool | None
    kind: str
