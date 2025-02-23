import kopf
import kubernetes.client.exceptions
from kubernetes import client
from loguru import logger

from dac_operator import providers
from dac_operator.ext import kubernetes_models
from dac_operator.microsoft_sentinel import microsoft_sentinel_models


@kopf.timer("microsoftsentineldetectionrules", interval=30.0)  # type: ignore
async def create_detection_rule(spec, **kwargs):
    configmap_name = "microsoft-sentinel-configuration"

    v1 = client.CoreV1Api()

    try:
        configmap = kubernetes_models.ConfigMap.model_validate(
            v1.read_namespaced_config_map(
                name=configmap_name, namespace=kwargs["namespace"]
            ),
            from_attributes=True,
        )
    except kubernetes.client.exceptions.ApiException:
        logger.error(f"Config map '{configmap_name}' does not exist.")
        return

    if configmap.data is None:
        logger.error(f"No data in '{configmap_name}'.")
        return

    microsoft_sentinel_service = providers.get_microsoft_sentinel_service(
        tenant_id=configmap.data["azure_tenant_id"],
        workspace_id=configmap.data["azure_workspace_id"],
        subscription_id=configmap.data["azure_subscription_id"],
        resource_group_id=configmap.data["azure_resource_group_id"],
    )

    # TODO: Work out serialization / validation alias to prevent incorrect type errors
    await microsoft_sentinel_service.create_or_update(
        rule_name=kwargs["name"],
        payload=microsoft_sentinel_models.CreateScheduledAlertRule(
            properties=microsoft_sentinel_models.ScheduledAlertRuleProperties(  # type: ignore
                displayName=spec["name"],
                enabled=spec.get("enabled", True),
                description=spec.get("description", ""),
                query=spec["query"],
                query_prefix=spec.get("queryPrefix", ""),  # type: ignore
                query_suffix=spec.get("querySuffix", ""),  # type: ignore
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

    status = await microsoft_sentinel_service.status(
        analytic_rule_id=microsoft_sentinel_service._compute_analytics_rule_id(
            rule_name=kwargs["name"]
        )
    )

    return {
        "deployed": "Deployed" if status.deployed else "Not deployed",
        "enabled": "Enabled" if status.enabled else "Disabled",
        "rule_type": status.rule_type,
        "message": "This field will contain additional information",
    }


@kopf.on.delete("microsoftsentineldetectionrules")  # type: ignore
async def remove_detection_rule(spec, **kwargs):
    configmap_name = "microsoft-sentinel-configuration"

    v1 = client.CoreV1Api()

    try:
        configmap = kubernetes_models.ConfigMap.model_validate(
            v1.read_namespaced_config_map(
                name=configmap_name, namespace=kwargs["namespace"]
            ),
            from_attributes=True,
        )
    except kubernetes.client.exceptions.ApiException:
        logger.error(f"Config map '{configmap_name}' does not exist.")
        return

    if configmap.data is None:
        logger.error(f"No data in '{configmap_name}'.")
        return

    microsoft_sentinel_service = providers.get_microsoft_sentinel_service(
        tenant_id=configmap.data["azure_tenant_id"],
        workspace_id=configmap.data["azure_workspace_id"],
        subscription_id=configmap.data["azure_subscription_id"],
        resource_group_id=configmap.data["azure_resource_group_id"],
    )

    await microsoft_sentinel_service.remove(rule_name=kwargs["name"])


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
