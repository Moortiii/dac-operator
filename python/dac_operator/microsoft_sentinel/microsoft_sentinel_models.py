from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

EntityType = Literal[
    "Account",
    "AzureResource",
    "CloudApplication",
    "DNS",
    "File",
    "FileHash",
    "Host",
    "IP",
    "MailCluster",
    "MailMessage",
    "Mailbox",
    "Malware",
    "Process",
    "RegistryKey",
    "RegistryValue",
    "SecurityGroup",
    "SubmissionMail",
    "URL",
]

AlertProperty = Literal[
    "AlertLink",
    "ConfidenceLevel",
    "ConfidenceScore",
    "ExtendedLinks",
    "ProductComponentName",
    "ProductName",
    "RemediationSteps",
    "Techniques",
]

AttackTactic = Literal[
    "Collection",
    "CommandAndControl",
    "CredentialAccess",
    "DefenseEvasion",
    "Discovery",
    "Execution",
    "Exfiltration",
    "Impact",
    "ImpairProcessControl",
    "InhibitResponseFunction",
    "InitialAccess",
    "LateralMovement",
    "Persistence",
    "PreAttack",
    "PrivilegeEscalation",
    "Reconnaissance",
    "ResourceDevelopment",
]

AlertDetail = Literal["DisplayName", "Severity"]
AggregationKind = Literal["AlertPerResult", "SingleAlert"]
MatchingMethod = Literal["AllEntities", "AnyAlert", "Selected"]
TriggerOperator = Literal["Equal", "GreaterThan", "LessThan", "NotEqual"]
AlertSeverity = Literal["High", "Medium", "Low", "Informational"]
AnalyticRuleTypes = Literal[
    "Unknown", "MicrosoftSecurityIncidentCreation", "Fusion", "Scheduled"
]


class MacroInjectionResult(BaseModel):
    success: bool
    query: str
    message: str = ""


class AnalyticsRuleStatus(BaseModel):
    enabled: bool
    deployed: bool
    rule_type: AnalyticRuleTypes


class BaseModelWithConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, extra="allow"
    )


class GroupingConfiguration(BaseModelWithConfig):
    enabled: bool
    group_by_alert_details: list[AlertDetail] = Field(..., alias="groupByAlertDetails")
    group_by_custom_details: list[str] = Field(..., alias="groupByCustomDetails")
    group_by_entities: list[EntityType] = Field(..., alias="groupByEntities")
    lookback_duration: str = Field(..., alias="lookbackDuration")
    matching_method: MatchingMethod = Field(..., alias="matchingMethod")
    reopen_closed_incident: bool = Field(..., alias="reopenClosedIncident")


class IncidentConfiguration(BaseModelWithConfig):
    create_incident: bool = Field(..., alias="createIncident")
    grouping_configuration: GroupingConfiguration = Field(
        ..., alias="groupingConfiguration"
    )


class EventGroupingSettings(BaseModelWithConfig):
    aggeregation_kind: AggregationKind = Field(..., alias="aggregationKind")


class FieldMapping(BaseModelWithConfig):
    column_name: str = Field(..., alias="columnName")
    identifier: str


class EntityMapping(BaseModelWithConfig):
    entity_type: EntityType = Field(..., alias="entityType")
    field_mappings: list[FieldMapping] = Field(..., alias="fieldMappings")


class AlertPropertyMapping(BaseModelWithConfig):
    alert_property: AlertProperty = Field(..., alias="alertProperty")
    value: str


class AlertDetailsOverride(BaseModelWithConfig):
    alert_description_format: str = Field(..., alias="alertDescriptionFormat")
    alert_display_name_format: str = Field(..., alias="alertDisplayNameFormat")
    alert_dynamic_properties: list[AlertPropertyMapping] = Field(
        ..., alias="alertDynamicProperties"
    )
    alert_severity_column_name: str = Field(..., alias="alertSeverityColumnName")
    alert_tactics_column_name: str = Field(..., alias="alertTacticsColumnName")


class ScheduledAlertRuleProperties(BaseModelWithConfig):
    displayName: str
    enabled: bool
    query: str
    query_suffix: str = Field("", exclude=True, alias="queryPrefix")
    query_prefix: str = Field("", exclude=True, alias="querySuffix")
    query_frequency: str = Field("PT1H", alias="queryFrequency")
    query_period: str = Field("PT1H", alias="queryPeriod")
    suppression_duration: str = Field(..., alias="suppressionDuration")
    suppression_enabled: bool = Field(..., alias="suppressionEnabled")
    trigger_operator: TriggerOperator = Field(..., alias="triggerOperator")
    trigger_threshold: int = Field(..., alias="triggerThreshold")
    severity: AlertSeverity
    alert_details_override: AlertDetailsOverride | None = Field(
        None, alias="alertDetailsOverride"
    )
    alert_rule_template_name: str | None = Field(None, alias="alertRuleTemplateName")
    custom_details: dict[str, str] | None = Field(None, alias="customDetails")
    description: str | None = None
    entity_mappings: list[EntityMapping] = Field([], alias="entityMappings")
    event_grouping_settings: EventGroupingSettings | None = Field(
        None, alias="eventGroupingSettings"
    )
    incident_configuration: IncidentConfiguration | None = Field(
        None, alias="incidentConfiguration"
    )
    tactics: list[AttackTactic] = []
    techniques: list[str] = []
    template_version: str | None = Field(None, alias="templateVersion")


class CreateScheduledAlertRule(BaseModelWithConfig):
    kind: Literal["Scheduled"] = "Scheduled"
    properties: ScheduledAlertRuleProperties


class CreateScheduledAlertRuleCRDInput(BaseModelWithConfig):
    displayName: str
    enabled: bool
    query: str
    query_frequency: str = Field(..., alias="queryFrequency")
    query_period: str = Field(..., alias="queryPeriod")
    suppression_duration: str = Field(..., alias="suppressionDuration")
    suppression_enabled: bool = Field(..., alias="suppressionEnabled")
    trigger_operator: TriggerOperator = Field(..., alias="triggerOperator")
    trigger_threshold: int = Field(..., alias="suppressionEnabled")
    severity: AlertSeverity
    alert_details_override: AlertDetailsOverride = Field(
        ..., alias="alertDetailsOverride"
    )
    alert_rule_template_name: str = Field(..., alias="alertRuleTemplateName")
    custom_details: dict[str, str] = Field(..., alias="customDetails")
    description: str
    entity_mappings: list[EntityMapping] = Field(..., alias="entityMappings")
    event_grouping_settings: EventGroupingSettings = Field(
        ..., alias="eventGroupingSettings"
    )
    incident_configuration: IncidentConfiguration = Field(
        ..., alias="incidentConfiguration"
    )
    tactics: list[AttackTactic]
    techniques: list[str]
    template_version: str = Field(..., alias="templateVersion")
