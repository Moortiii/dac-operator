from enum import StrEnum
from typing import Literal

import kopf
from kubernetes import client
from pydantic import BaseModel, ValidationError

from dac_operator import providers
from dac_operator.microsoft_sentinel import (
    microsoft_sentinel_exceptions,
    microsoft_sentinel_models,
)

ALLOWED_NAMESPACES = [
    "a1b2c3d4",
    "ce06ce71",
]

ALLOWED_RULE_NAMES = [
    "example-detection-rule-1",
    "example-detection-rule-2",
    "example-detection-rule-3",
]


class ErrorMessages(StrEnum):
    initialization_error = "Unable to configure provider, see controller logs."
    create_error = "Unable to create Detection Rule upstream."
    delete_error = "Unable to delete Detection Rule upstream."


class DetectionRuleStatus(BaseModel):
    deployed: Literal["Deployed", "Not deployed", "Unknown"] = "Unknown"
    enabled: Literal["Enabled", "Disabled", "Unknown"] = "Unknown"
    rule_type: str = "Unknown"
    message: str = ""


@kopf.timer("microsoftsentineldetectionrules", interval=30.0)  # type: ignore
async def create_detection_rule(spec, **kwargs):
    status = DetectionRuleStatus()
    namespace = kwargs["namespace"]
    rule_name = kwargs["name"]

    if rule_name not in ALLOWED_RULE_NAMES or namespace not in ALLOWED_NAMESPACES:
        print(f"Skipping {rule_name} for {namespace}")
        return

    try:
        microsoft_sentinel_service = providers.get_microsoft_sentinel_service(
            kubernetes_client=providers.get_kubernetes_client(
                core_api=client.CoreV1Api(),
                custom_objects_api=client.CustomObjectsApi(),
            ),
            namespace=namespace,
        )
    except microsoft_sentinel_exceptions.ServiceConfigurationException:
        status.message = ErrorMessages.initialization_error.value
        return status.model_dump()

    try:
        payload = microsoft_sentinel_models.CreateScheduledAlertRule.model_validate(
            spec
        )
    except ValidationError as err:
        status.message = str(err)
        return status.model_dump()

    properties = spec.get("properties", {})

    # TODO: Make it possible for the service to return a result so that we can
    # move this logic further down the stack
    # Inject main query
    result = await microsoft_sentinel_service.inject_macros(
        query=properties.get("query", ""), rule_name=rule_name
    )

    if not result.success:
        status.message = result.message
        return status.model_dump()

    payload.properties.query = result.query

    # Inject macros into query prefix
    result = await microsoft_sentinel_service.inject_macros(
        query=properties.get("queryPrefix", ""), rule_name=rule_name
    )

    if not result.success:
        status.message = result.message
        return status.model_dump()

    payload.properties.query_prefix = result.query

    # Inject macros into query suffix
    result = await microsoft_sentinel_service.inject_macros(
        query=properties.get("querySuffix", ""), rule_name=rule_name
    )

    if not result.success:
        status.message = result.message
        return status.model_dump()

    payload.properties.query_suffix = result.query

    try:
        await microsoft_sentinel_service.create_or_update_analytics_rule(
            rule_name=rule_name,
            payload=payload,
        )
    except Exception:
        status.message = ErrorMessages.create_error
        return status.model_dump()

    analytics_rule_status = await microsoft_sentinel_service.analytics_rule_status(
        analytic_rule_id=microsoft_sentinel_service._compute_analytics_rule_id(
            rule_name=rule_name
        )
    )
    status.rule_type = analytics_rule_status.rule_type
    status.deployed = "Deployed" if analytics_rule_status.deployed else "Not deployed"
    status.enabled = "Enabled" if analytics_rule_status.enabled else "Disabled"

    return status.model_dump()


@kopf.on.delete("microsoftsentineldetectionrules")  # type: ignore
async def remove_detection_rule(spec, **kwargs):
    status = DetectionRuleStatus(deployed="Deployed")

    try:
        microsoft_sentinel_service = providers.get_microsoft_sentinel_service(
            kubernetes_client=providers.get_kubernetes_client(
                core_api=client.CoreV1Api(),
                custom_objects_api=client.CustomObjectsApi(),
            ),
            namespace=kwargs["namespace"],
        )
    except microsoft_sentinel_exceptions.ServiceConfigurationException:
        status.message = ErrorMessages.initialization_error.value
        return status.model_dump()

    try:
        await microsoft_sentinel_service.remove_analytics_rule(rule_name=kwargs["name"])
    except Exception:
        status.message = ErrorMessages.initialization_error
        return status.model_dump()

    status.deployed = "Deployed"
    return status.model_dump()
