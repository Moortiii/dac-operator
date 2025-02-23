# {
#     "apiVersion": "buildrlabs.io/v1",
#     "kind": "MicrosoftSentinelMacro",
#     "metadata": {
#         "creationTimestamp": "2025-02-23T13:29:38Z",
#         "generation": 1,
#         "labels": {
#             "kustomize.toolkit.fluxcd.io/name": "a1b2c3d4-detection-rules",
#             "kustomize.toolkit.fluxcd.io/namespace": "flux-system",
#         },
#         "managedFields": [
#             {
#                 "apiVersion": "buildrlabs.io/v1",
#                 "fieldsType": "FieldsV1",
#                 "fieldsV1": {
#                     "f:metadata": {
#                         "f:labels": {
#                             "f:kustomize.toolkit.fluxcd.io/name": {},
#                             "f:kustomize.toolkit.fluxcd.io/namespace": {},
#                         }
#                     },
#                     "f:spec": {"f:query": {}},
#                 },
#                 "manager": "kustomize-controller",
#                 "operation": "Apply",
#                 "time": "2025-02-23T13:29:38Z",
#             }
#         ],
#         "name": "example-macro-1",
#         "namespace": "a1b2c3d4",
#         "resourceVersion": "2170838",
#         "uid": "184faa17-c6b7-4472-b1b6-520a3b152456",
#     },
#     "spec": {"query": '| extend ExampleColumn = "This is a macro example"'},
# }

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class MicrosoftSentinelMacroMetadata(BaseModel):
    generation: int
    labels: dict[str, Any]
    name: str
    namespace: str


class MicrosoftSentinelMacroSpec(BaseModel):
    content: str


class MicrosoftSentinelMacro(BaseModel):
    api_version: str = Field(..., validation_alias="apiVersion")
    kind: Literal["MicrosoftSentinelMacro"] = "MicrosoftSentinelMacro"
    spec: MicrosoftSentinelMacroSpec
    metadata: MicrosoftSentinelMacroMetadata
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
