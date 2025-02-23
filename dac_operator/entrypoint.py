import kopf
from kubernetes import client
from loguru import logger
from pydantic import BaseModel, model_serializer

from dac_operator import providers
from dac_operator.crd import crd_models
from dac_operator.ext import kubernetes_exceptions
from dac_operator.microsoft_sentinel import microsoft_sentinel_models
from dac_operator.microsoft_sentinel.microsoft_sentinel_macro_service import (
    MicrosoftSentinelMacroService,
)


class CreateDetectionRuleStatus(BaseModel):
    deployed: bool = False
    enabled: bool = False
    rule_type: str = "Unknown"
    message: str = ""

    @model_serializer
    def serialize(self):
        return {
            "deployed": "Deployed" if self.deployed else "Not deployed",
            "enabled": "Enabled" if self.enabled else "Disabled",
            "rule_type": self.rule_type,
            "message": self.message,
        }


@kopf.timer("microsoftsentineldetectionrules", interval=30.0)  # type: ignore
async def create_detection_rule(spec, **kwargs):
    status = CreateDetectionRuleStatus()

    namespace = kwargs["namespace"]

    kubernetes_client = providers.get_kubernetes_client(
        core_api=client.CoreV1Api(), custom_objects_api=client.CustomObjectsApi()
    )

    try:
        configmap = kubernetes_client.get_config_map(
            name="microsoft-sentinel-configuration", namespace=namespace
        )
    except kubernetes_exceptions.ResourceNotFoundException:
        status.message = "Unable to configure provider, see controller logs."
        return status.model_dump()

    microsoft_sentinel_service = providers.get_microsoft_sentinel_service(
        tenant_id=configmap.data["azure_tenant_id"],
        workspace_id=configmap.data["azure_workspace_id"],
        subscription_id=configmap.data["azure_subscription_id"],
        resource_group_id=configmap.data["azure_resource_group_id"],
    )

    query = spec["query"]
    macro_service = MicrosoftSentinelMacroService()
    for macro_name in macro_service.get_used_macros(query=query):
        try:
            macro = kubernetes_client.get_namespaced_custom_object(
                group="buildrlabs.io",
                version="v1",
                namespace=namespace,
                plural="microsoftsentinelmacros",
                name=macro_name,
                return_type=crd_models.MicrosoftSentinelMacro,
            )
            query = macro_service.replace_macro(
                text=query, macro_name=macro_name, replacement=macro.spec.content
            )
        except kubernetes_exceptions.ResourceNotFoundException:
            error_message = (
                f"The macro '{macro_name}' is referenced in '{kwargs['name']}', "
                "but is not deployed in the Tenant namespace."
            )
            logger.error(error_message)
            status.message = error_message
            return status.model_dump()

    # TODO: Work out serialization / validation alias to prevent incorrect type errors
    await microsoft_sentinel_service.create_or_update(
        rule_name=kwargs["name"],
        payload=microsoft_sentinel_models.CreateScheduledAlertRule(
            properties=microsoft_sentinel_models.ScheduledAlertRuleProperties(  # type: ignore
                displayName=spec["name"],
                enabled=spec.get("enabled", True),
                description=spec.get("description", ""),
                query=query,
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

    analytics_rule_status = await microsoft_sentinel_service.status(
        analytic_rule_id=microsoft_sentinel_service._compute_analytics_rule_id(
            rule_name=kwargs["name"]
        )
    )
    status.rule_type = analytics_rule_status.rule_type
    status.deployed = analytics_rule_status.deployed
    status.enabled = analytics_rule_status.enabled

    return status.model_dump()


@kopf.on.delete("microsoftsentineldetectionrules")  # type: ignore
async def remove_detection_rule(spec, **kwargs):
    kubernetes_client = providers.get_kubernetes_client(
        core_api=client.CoreV1Api(), custom_objects_api=client.CustomObjectsApi()
    )

    try:
        configmap = kubernetes_client.get_config_map(
            name="microsoft-sentinel-configuration", namespace=kwargs["namespace"]
        )
    except kubernetes_exceptions.ResourceNotFoundException:
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
