from typing import Literal

from pydantic import BaseModel, Field

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


class GroupingConfiguration(BaseModel):
    enabled: bool
    group_by_alert_details: list[AlertDetail] = Field(
        ..., validation_alias="groupByAlertDetails"
    )
    group_by_custom_details: list[str] = Field(
        ..., validation_alias="groupByCustomDetails"
    )
    group_by_entities: list[EntityType] = Field(..., validation_alias="groupByEntities")
    lookback_duration: str = Field(..., validation_alias="lookbackDuration")
    matching_method: MatchingMethod = Field(..., validation_alias="matchingMethod")
    reopen_closed_incident: bool = Field(..., validation_alias="reopenClosedIncident")


class IncidentConfiguration(BaseModel):
    create_incident: bool = Field(..., validation_alias="createIncident")
    grouping_configuration: GroupingConfiguration = Field(
        ..., validation_alias="groupingConfiguration"
    )


class EventGroupingSettings(BaseModel):
    aggeregation_kind: AggregationKind = Field(..., validation_alias="aggregationKind")


class FieldMapping(BaseModel):
    column_name: str = Field(..., validation_alias="columnName")
    identifier: str


class EntityMapping(BaseModel):
    entity_type: EntityType = Field(..., validation_alias="entityType")
    field_mappings: list[FieldMapping] = Field(..., validation_alias="fieldMappings")


class AlertPropertyMapping(BaseModel):
    alert_property: AlertProperty = Field(..., validation_alias="alertProperty")
    value: str


class AlertDetailsOverride(BaseModel):
    alert_description_format: str = Field(
        ..., validation_alias="alertDescriptionFormat"
    )
    alert_display_name_format: str = Field(
        ..., validation_alias="alertDisplayNameFormat"
    )
    alert_dynamic_properties: list[AlertPropertyMapping] = Field(
        ..., validation_alias="alertDynamicProperties"
    )
    alert_severity_column_name: str = Field(
        ..., validation_alias="alertSeverityColumnName"
    )
    alert_tactics_column_name: str = Field(
        ..., validation_alias="alertTacticsColumnName"
    )


class ScheduledAlertRuleProperties(BaseModel):
    displayName: str
    enabled: bool
    query: str
    query_frequency: str = Field(..., validation_alias="queryFrequency")
    query_period: str = Field(..., validation_alias="queryPeriod")
    suppression_duration: str = Field(..., validation_alias="suppressionDuration")
    suppression_enabled: bool = Field(..., validation_alias="suppressionEnabled")
    trigger_operator: TriggerOperator = Field(..., validation_alias="triggerOperator")
    trigger_threshold: int = Field(..., validation_alias="suppressionEnabled")
    severity: AlertSeverity
    alert_details_override: AlertDetailsOverride = Field(
        ..., validation_alias="alertDetailsOverride"
    )
    alert_rule_template_name: str = Field(..., validation_alias="alertRuleTemplateName")
    custom_details: dict[str, str] = Field(..., validation_alias="customDetails")
    description: str
    entity_mappings: list[EntityMapping] = Field(..., validation_alias="entityMappings")
    event_grouping_settings: EventGroupingSettings = Field(
        ..., validation_alias="eventGroupingSettings"
    )
    incident_configuration: IncidentConfiguration = Field(
        ..., validation_alias="incidentConfiguration"
    )
    tactics: list[AttackTactic]
    techniques: list[str]
    template_version: str = Field(..., validation_alias="templateVersion")


class CreateScheduledAlertRule(BaseModel):
    kind: Literal["Scheduled"] = "Scheduled"
    etag: str
    properties: ScheduledAlertRuleProperties


class CreateScheduledAlertRuleCRDInput(BaseModel):
    displayName: str
    enabled: bool
    query: str
    query_frequency: str = Field(..., validation_alias="queryFrequency")
    query_period: str = Field(..., validation_alias="queryPeriod")
    suppression_duration: str = Field(..., validation_alias="suppressionDuration")
    suppression_enabled: bool = Field(..., validation_alias="suppressionEnabled")
    trigger_operator: TriggerOperator = Field(..., validation_alias="triggerOperator")
    trigger_threshold: int = Field(..., validation_alias="suppressionEnabled")
    severity: AlertSeverity
    alert_details_override: AlertDetailsOverride = Field(
        ..., validation_alias="alertDetailsOverride"
    )
    alert_rule_template_name: str = Field(..., validation_alias="alertRuleTemplateName")
    custom_details: dict[str, str] = Field(..., validation_alias="customDetails")
    description: str
    entity_mappings: list[EntityMapping] = Field(..., validation_alias="entityMappings")
    event_grouping_settings: EventGroupingSettings = Field(
        ..., validation_alias="eventGroupingSettings"
    )
    incident_configuration: IncidentConfiguration = Field(
        ..., validation_alias="incidentConfiguration"
    )
    tactics: list[AttackTactic]
    techniques: list[str]
    template_version: str = Field(..., validation_alias="templateVersion")
