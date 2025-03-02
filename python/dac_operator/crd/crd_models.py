from typing import Any

from pydantic import BaseModel, ConfigDict


class MacroBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="allow", populate_by_name=True, from_attributes=True
    )


class MicrosoftSentinelMacroMetadata(MacroBaseModel):
    generation: int
    labels: dict[str, Any]
    name: str
    namespace: str


class MicrosoftSentinelMacroSpec(MacroBaseModel):
    content: str


class MicrosoftSentinelMacro(MacroBaseModel):
    spec: MicrosoftSentinelMacroSpec
    metadata: MicrosoftSentinelMacroMetadata
