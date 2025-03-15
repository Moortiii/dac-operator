from enum import StrEnum
from typing import Literal

import kopf
from kubernetes import client as kubernetes_client
from loguru import logger
from pydantic import BaseModel

from dac_operator import providers
from dac_operator.microsoft_sentinel import (
    microsoft_sentinel_exceptions,
)

AUTOMATION_RULE_SYNC_INTERVAL = 500


class ErrorMessages(StrEnum):
    initialization_error = "Unable to configure provider, see controller logs."
    automation_rule_create_error = "Unable to create Automation Rule upstream."
    analytics_rule_create_error = "Unable to create Analytics Rule upstream."
    analytics_rule_delete_error = "Unable to delete Analytics Rule upstream."


class AutomationRuleStatus(BaseModel):
    deployed: Literal["Deployed", "Not deployed", "Unknown"] = "Unknown"
    enabled: Literal["Enabled", "Disabled", "Unknown"] = "Unknown"
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
