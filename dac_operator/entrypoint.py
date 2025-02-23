from enum import StrEnum
from typing import Literal

import kopf
from kubernetes import client
from pydantic import BaseModel

from dac_operator import providers
from dac_operator.microsoft_sentinel import (
    microsoft_sentinel_exceptions,
    microsoft_sentinel_models,
)


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

    # Inject main query
    query = spec.get("query", "")
    result = await microsoft_sentinel_service.inject_macros(
        query=query, rule_name=rule_name
    )

    if not result.success:
        status.message = result.message
        return status.model_dump()

    query = result.query

    # Inject macros into query prefix
    query_prefix = spec.get("queryPrefix", "")
    result = await microsoft_sentinel_service.inject_macros(
        query=query_prefix, rule_name=rule_name
    )

    if not result.success:
        status.message = result.message
        return status.model_dump()

    query_prefix = result.query

    # Inject macros into query suffix
    query_suffix = spec.get("querySuffix", "")
    result = await microsoft_sentinel_service.inject_macros(
        query=query_suffix, rule_name=rule_name
    )

    if not result.success:
        status.message = result.message
        return status.model_dump()

    query_suffix = result.query

    try:
        await microsoft_sentinel_service.create_or_update(
            rule_name=kwargs["name"],
            payload=microsoft_sentinel_models.CreateScheduledAlertRule(
                properties=microsoft_sentinel_models.ScheduledAlertRuleProperties(  # type: ignore
                    displayName=spec["name"],
                    enabled=spec.get("enabled", True),
                    description=spec.get("description", ""),
                    query=query,
                    query_prefix=query_prefix,  # type: ignore
                    query_suffix=query_suffix,  # type: ignore
                    query_frequency=spec.get("queryFrequency", "PT1H"),  # type: ignore
                    query_period=spec.get("queryPeriod", "PT1H"),  # type: ignore
                    severity=spec.get("severity", "Informational"),
                    custom_details=spec.get("customDetails", {}),  # type: ignore
                    suppression_duration=spec.get("suppressionDuration", "PT1H"),  # type: ignore
                    suppression_enabled=spec.get("suppressionEnabled", False),  # type: ignore
                    alert_details_override=spec.get("alertDetailsOverride"),  # type: ignore
                    tactics=spec.get("tactics", []),
                    techniques=spec.get("techniques", []),
                    alert_rule_template_name=spec.get("alertRuleTemplateName"),  # type: ignore
                    event_grouping_settings=spec.get("eventGroupingSettings"),  # type: ignore
                    incident_configuration=spec.get("incidentConfiguration"),  # type: ignore
                    entity_mappings=spec.get("entityMappings", []),  # type: ignore
                    template_version=spec.get("templateVersion"),  # type: ignore
                    trigger_threshold=spec.get("triggerThreshold", 1),  # type: ignore
                    trigger_operator=spec.get("triggerOperator", "GreaterThan"),  # type: ignore
                ),
            ),
        )
    except Exception:
        status.message = ErrorMessages.create_error
        return status.model_dump()

    analytics_rule_status = await microsoft_sentinel_service.status(
        analytic_rule_id=microsoft_sentinel_service._compute_analytics_rule_id(
            rule_name=kwargs["name"]
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
        await microsoft_sentinel_service.remove(rule_name=kwargs["name"])
    except Exception:
        status.message = ErrorMessages.initialization_error
        return status.model_dump()

    status.deployed = "Deployed"
    return status.model_dump()


# microsoft_sentinel_models.IncidentConfiguration(
#     create_incident=spec.get("createIncident", True),
#     grouping_configuration=microsoft_sentinel_models.GroupingConfiguration(
#         group_by_alert_details=[],
#         group_by_custom_details=[],
#         group_by_entities=[],
#         enabled=True,
#         lookback_duration="P15H",
#         matching_method="AllEntities",
#         reopen_closed_incident=False,
#     ),
# ),
