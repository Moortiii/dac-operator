from pydantic import BaseModel, ConfigDict

class SplunkDetectionRule(BaseModel):
    name: str
    description: str
    search: str

    model_config = ConfigDict(extra="allow")