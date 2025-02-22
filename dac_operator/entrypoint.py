import kopf

from dac_operator import providers
from dac_operator.microsoft_sentinel import microsoft_sentinel_models

microsoft_sentinel_service = providers.get_microsoft_sentinel_service()


@kopf.timer("microsoftsentineldetectionrules", interval=30.0)  # type: ignore
async def create_detection_rule(spec, **kwargs):
    await microsoft_sentinel_service.create_or_update(
        rule_name=kwargs["name"],
        payload=microsoft_sentinel_models.CreateScheduledAlertRule(
            properties=microsoft_sentinel_models.ScheduledAlertRuleProperties(
                displayName=spec["name"],
                enabled=spec.get("enabled", True),
                description=spec.get("description", ""),
                query=spec["query"],
                query_frequency=spec.get("queryFrequency", "PT1H"),
                query_period=spec.get("queryPeriod", "PT1H"),
                severity=spec.get("severity", "Informational"),
                custom_details=spec.get("customDetails", {}),
                suppression_duration=spec.get("suppressionDuration", "PT1H"),
                suppression_enabled=spec.get("suppressionEnabled", False),
                alert_details_override=spec.get("alertDetailsOverride"),
                tactics=spec.get("tactics", []),
                techniques=spec.get("techniques", []),
                alert_rule_template_name=spec.get("alertRuleTemplateName"),
                event_grouping_settings=spec.get("eventGroupingSettings"),
                incident_configuration=spec.get("incidentConfiguration"),
                entity_mappings=spec.get("entityMappings", []),
                template_version=spec.get("templateVersion"),
                trigger_threshold=spec.get("triggerThreshold", 1),
                trigger_operator=spec.get("triggerOperator", "GreaterThan"),
            ),
        ),
    )


@kopf.on.delete("microsoftsentineldetectionrules")
async def remove_detection_rule(spec, **kwargs):
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
