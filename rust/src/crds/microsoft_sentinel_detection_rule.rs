use kube::core::CustomResourceExt;
use kube_derive::CustomResource;
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashMap;
use std::fs::File;
use std::io::Write;

fn scheduled() -> String {
    "Scheduled".into()
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "PascalCase")]
pub enum Severity {
    High,
    Informational,
    Low,
    Medium,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "PascalCase")]
pub enum TriggerOperator {
    Equal,
    GreaterThan,
    LessThan,
    NotEqual,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "PascalCase")]
pub enum AlertProperty {
    AlertLink,
    ConfidenceLevel,
    ConfidenceScore,
    ExtendedLinks,
    ProductComponentName,
    ProductName,
    ProviderName,
    RemediationSteps,
    Techniques,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "PascalCase")]
pub enum EntityType {
    Account,
    AzureResource,
    CloudApplication,
    DNS,
    File,
    FileHash,
    Host,
    IP,
    MailCluster,
    MailMessage,
    Mailbox,
    Malware,
    Process,
    RegistryKey,
    RegistryValue,
    SecurityGroup,
    SubmissionMail,
    URL,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "PascalCase")]
pub enum AggregationKind {
    AlertPerResult,
    SingleAlert,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "PascalCase")]
pub enum MatchingMethod {
    AllEntities,
    AnyAlert,
    Selected,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "PascalCase")]
pub enum AttackTactic {
    Collection,
    CommandAndControl,
    CredentialAccess,
    DefenseEvasion,
    Discovery,
    Execution,
    Exfiltration,
    Impact,
    ImpairProcessControl,
    InhibitResponseFunction,
    InitialAccess,
    LateralMovement,
    Persistence,
    PreAttack,
    PrivilegeEscalation,
    Reconnaissance,
    ResourceDevelopment,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
struct AlertPropertyMapping {
    alert_property: AlertProperty,
    value: String,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
struct AlertDetailsOverride {
    alert_description_format: Option<String>,
    alert_display_name_format: Option<String>,
    alert_severity_column_name: Option<String>,
    alert_tactics_column_name: Option<String>,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
struct FieldMapping {
    column_name: String,
    identifier: String,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
struct AlertDetail {
    display_name: String,
    severity: Severity,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
struct EntityMapping {
    entity_type: EntityType,
    field_mappings: Vec<FieldMapping>,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
struct EventGroupingSettings {
    aggregation_kind: AggregationKind,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
struct GroupingConfiguration {
    enabled: bool,
    group_by_alert_details: Vec<AlertDetail>,
    group_by_custom_details: Vec<String>,
    group_by_entities: Vec<EntityType>,
    lookback_duration: String,
    matching_method: MatchingMethod,
    reopen_closed_incident: bool,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
struct IncidentConfiguration {
    create_incident: bool,
    grouping_configuration: GroupingConfiguration,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
struct Properties {
    display_name: String,
    enabled: bool,
    query: String,
    query_frequency: String,
    query_period: String,
    severity: Severity,
    suppression_duration: String,
    suppression_enabled: bool,
    trigger_operator: TriggerOperator,
    trigger_threshold: i64,
    alert_details_override: Option<AlertDetailsOverride>,
    alert_rule_template_name: Option<String>,
    custom_details: Option<HashMap<String, Value>>,
    description: Option<String>,
    entity_mappings: Option<Vec<EntityMapping>>,
    event_grouping_settings: Option<EventGroupingSettings>,
    incident_configuration: Option<IncidentConfiguration>,
    tactics: Option<Vec<AttackTactic>>,
    techniques: Option<Vec<String>>,
    template_version: Option<String>,
}

#[derive(CustomResource, Clone, Debug, Deserialize, Serialize, PartialEq, JsonSchema)]
#[kube(
    group = "buildrlabs.io",
    version = "v1",
    kind = "MicrosoftSentinelDetectionRule",
    shortname = "msd",
    status = "MicrosoftSentinelDetectionRuleStatus",
    shortname = "msds",
    printcolumn = r#"{"name":"Status", "type":"string", "description":"Checks if the Detection Rule is deployed to Microsoft Sentinel", "jsonPath":".status.create_detection_rule.deployed"}"#,
    printcolumn = r#"{"name":"Enabled", "type":"string", "description":"Checks if the Detection Rule is enabled in Microsoft Sentinel", "jsonPath":".status.create_detection_rule.enabled"}"#,
    printcolumn = r#"{"name":"Message", "type":"string", "description":"Additional information about the deployment status", "jsonPath":".status.create_detection_rule.message"}"#,
    printcolumn = r#"{"name":"Rule type", "type":"string", "description":"The type of Microsoft Sentinel Detection Rule", "jsonPath":".status.create_detection_rule.rule_type"}"#,
    namespaced
)]
#[serde(rename_all = "camelCase")]
struct MicrosoftSentinelDetectionRuleSpec {
    properties: Properties,
    #[serde(default = "scheduled")]
    kind: String,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
struct MicrosoftSentinelDetectionRuleStatus {
    message: String,
    deployed: String,
    enabled: String,
    rule_type: String,
}

pub fn write_crd() -> std::io::Result<()> {
    // Write MicrosoftSentinelDetectionRule CRD
    let filename = "MicrosoftSentinelDetectionRule";
    let crd_yaml = serde_yaml::to_string(&MicrosoftSentinelDetectionRule::crd()).unwrap();
    let mut file = File::create(format!("./generated/{}.yaml", filename)).unwrap();
    file.write_all(crd_yaml.as_bytes()).unwrap();
    println!("{filename} written to {filename}.yaml");
    Ok(())
}
