from enum import StrEnum
from typing import Literal

import kopf
from kubernetes import client as kubernetes_client
from loguru import logger
from pydantic import BaseModel, ValidationError

from dac_operator import providers
from dac_operator.microsoft_sentinel import (
    microsoft_sentinel_exceptions,
    microsoft_sentinel_models,
)

AUTOMATION_RULE_SYNC_INTERVAL = 500
DETECTION_RULE_SYNC_INTERVAL = 500

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
    automation_rule_create_error = "Unable to create Automation Rule upstream."
    analytics_rule_create_error = "Unable to create Analytics Rule upstream."
    analytics_rule_delete_error = "Unable to delete Analytics Rule upstream."


class AutomationRuleStatus(BaseModel):
    deployed: Literal["Deployed", "Not deployed", "Unknown"] = "Unknown"
    enabled: Literal["Enabled", "Disabled", "Unknown"] = "Unknown"
    message: str = ""


class AnalyticsRuleStatus(BaseModel):
    deployed: Literal["Deployed", "Not deployed", "Unknown"] = "Unknown"
    enabled: Literal["Enabled", "Disabled", "Unknown"] = "Unknown"
    rule_type: str = "Unknown"
    message: str = ""


@kopf.timer("microsoftsentinelautomationrules", interval=AUTOMATION_RULE_SYNC_INTERVAL)  # type: ignore
async def create_automation_rule(spec, **kwargs):
    status = AutomationRuleStatus()

    namespace = kwargs["namespace"]
    rule_name = kwargs["name"]

    try:
        microsoft_sentinel_service = providers.get_microsoft_sentinel_service(
            kubernetes_client=providers.get_kubernetes_client(
                core_api=kubernetes_client.CoreV1Api(),
                custom_objects_api=kubernetes_client.CustomObjectsApi(),
            ),
            namespace=namespace,
        )
    except microsoft_sentinel_exceptions.ServiceConfigurationException:
        status.message = ErrorMessages.initialization_error.value
        return status.model_dump()

    try:
        await microsoft_sentinel_service.create_or_update_automation_rule(
            rule_name=rule_name,
            payload={"properties": spec["properties"]},
        )
    except Exception as err:
        logger.error(str(err))
        status.message = ErrorMessages.analytics_rule_create_error
        return status.model_dump()

    status.deployed = "Deployed"
    return status.model_dump()


@kopf.timer("microsoftsentineldetectionrules", interval=DETECTION_RULE_SYNC_INTERVAL)  # type: ignore
async def create_detection_rule(spec, **kwargs):
    status = AnalyticsRuleStatus()
    namespace = kwargs["namespace"]
    rule_name = kwargs["name"]

    if rule_name not in ALLOWED_RULE_NAMES or namespace not in ALLOWED_NAMESPACES:
        print(f"Skipping {rule_name} for {namespace}")
        return

    try:
        microsoft_sentinel_service = providers.get_microsoft_sentinel_service(
            kubernetes_client=providers.get_kubernetes_client(
                core_api=kubernetes_client.CoreV1Api(),
                custom_objects_api=kubernetes_client.CustomObjectsApi(),
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
    except Exception as err:
        logger.error(str(err))
        status.message = ErrorMessages.analytics_rule_create_error
        return status.model_dump()

    analytics_rule_status = await microsoft_sentinel_service.analytics_rule_status(  # noqa: E501
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
    status = AnalyticsRuleStatus(deployed="Deployed")

    try:
        microsoft_sentinel_service = providers.get_microsoft_sentinel_service(
            kubernetes_client=providers.get_kubernetes_client(
                core_api=kubernetes_client.CoreV1Api(),
                custom_objects_api=kubernetes_client.CustomObjectsApi(),
            ),
            namespace=kwargs["namespace"],
        )
    except microsoft_sentinel_exceptions.ServiceConfigurationException:
        status.message = ErrorMessages.initialization_error.value
        return status.model_dump()

    try:
        await microsoft_sentinel_service.remove_analytics_rule(rule_name=kwargs["name"])
    except Exception as err:
        logger.error(str(err))
        status.message = ErrorMessages.initialization_error
        return status.model_dump()

    status.deployed = "Deployed"
    return status.model_dump()
