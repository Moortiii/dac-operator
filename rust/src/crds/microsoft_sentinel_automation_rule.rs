use kube::{CustomResource, CustomResourceExt};
use schemars::schema_for;
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
use std::collections::HashMap;
use std::fs::File;
use std::io::Write;

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
pub enum LabelType {
    AutoAssigned,
    User,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
pub enum IncidentClassification {
    BenignPositive,
    FalsePositive,
    TruePositive,
    Undetermined,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
pub enum IncidentSeverity {
    High,
    Medium,
    Low,
    Informational,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
pub enum IncidentStatus {
    Active,
    Closed,
    New,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
pub enum OwnerType {
    Group,
    Unknown,
    User,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
pub enum IncidentClassificationReason {
    InaccurateData,
    IncorrectAlertLogic,
    SuspiciousActivity,
    SuspiciousButExpected,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
pub enum TriggersOn {
    Incidents,
    Alerts,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
pub enum TriggersWhen {
    Created,
    Updated,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
pub enum BooleanConditionSupportedOperator {
    And,
    Or,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
pub enum PropertyArrayChangedConditionSupportedArrayType {
    Alerts,
    Comments,
    Labels,
    Tactics,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
pub enum PropertyArrayChangedConditionSupportedChangeType {
    Added,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
pub enum ArrayConditionSupportedArrayType {
    CustomDetailValues,
    CustomDetails,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
pub enum PropertyArrayConditionSupportedArrayConditionType {
    AnyItem,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
pub enum PropertyConditionSupportedProperty {
    AccountAadTenantId,
    AccountAadUserId,
    AccountNTDomain,
    AccountName,
    AccountObjectGuid,
    AccountPUID,
    AccountSid,
    AccountUPNSuffix,
    AlertAnalyticRuleIds,
    AlertProductNames,
    AzureResourceResourceId,
    AzureResourceSubscriptionId,
    CloudApplicationAppId,
    CloudApplicationAppName,
    DNSDomainName,
    FileDirectory,
    FileHashValue,
    FileName,
    HostAzureID,
    HostNTDomain,
    HostName,
    HostNetBiosName,
    HostOSVersion,
    IPAddress,
    IncidentCustomDetailsKey,
    IncidentCustomDetailsValue,
    IncidentDescription,
    IncidentLabel,
    IncidentProviderName,
    IncidentRelatedAnalyticRuleIds,
    IncidentSeverity,
    IncidentStatus,
    IncidentTactics,
    IncidentTitle,
    IncidentUpdatedBySource,
    IoTDeviceId,
    IoTDeviceModel,
    IoTDeviceName,
    IoTDeviceOperatingSystem,
    IoTDeviceType,
    IoTDeviceVendor,
    MailMessageDeliveryAction,
    MailMessageDeliveryLocation,
    MailMessageP1Sender,
    MailMessageP2Sender,
    MailMessageRecipient,
    MailMessageSenderIP,
    MailMessageSubject,
    MailboxDisplayName,
    MailboxPrimaryAddress,
    MailboxUPN,
    MalwareCategory,
    MalwareName,
    ProcessCommandLine,
    ProcessId,
    RegistryKey,
    RegistryValueData,
    Url,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(tag = "conditionType", rename_all = "camelCase")]
pub enum Condition {
    #[serde(rename = "Boolean", rename_all = "camelCase")]
    BooleanCondition {
        condition_properties: BooleanCondition,
    },
    #[serde(rename = "PropertyArrayChanged", rename_all = "camelCase")]
    PropertyArrayChangedCondition {
        condition_properties: PropertyArrayChangedCondition,
    },
    #[serde(rename = "PropertyChanged", rename_all = "camelCase")]
    PropertyChangedCondition {
        condition_properties: PropertyChangedCondition,
    },
    #[serde(rename = "PropertyArray", rename_all = "camelCase")]
    PropertyArrayCondition {
        condition_properties: PropertyArrayValuesCondition,
    },
    #[serde(rename = "Property", rename_all = "camelCase")]
    PropertyCondition {
        condition_properties: PropertyCondition,
    },
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct PropertyCondition {
    operator: PropertyConditionSupportedOperator,
    property_name: PropertyConditionSupportedProperty,
    property_values: Vec<String>,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct PropertyArrayValuesCondition {
    array_condition_type: PropertyArrayConditionSupportedArrayConditionType,
    array_type: ArrayConditionSupportedArrayType,
    item_conditions: Vec<Condition>,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct BooleanCondition {
    operator: BooleanConditionSupportedOperator,
    inner_conditions: Vec<Condition>,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct PropertyArrayChangedCondition {
    array_type: PropertyArrayChangedConditionSupportedArrayType,
    change_type: PropertyArrayChangedConditionSupportedChangeType,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
pub enum PropertyChangedConditionSupportedChangedType {
    ChangedFrom,
    ChangedTo,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
pub enum PropertyConditionSupportedOperator {
    Contains,
    EndsWith,
    Equals,
    NotContains,
    NotEndsWith,
    NotEquals,
    NotStartsWith,
    StartsWith,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
pub enum PropertyChangedConditionSupportedPropertyType {
    IncidentOwner,
    IncidentSeverity,
    IncidentStatus,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct PropertyChangedCondition {
    change_type: PropertyChangedConditionSupportedChangedType,
    propery_name: PropertyChangedConditionSupportedPropertyType,
    operator: PropertyConditionSupportedOperator,
    property_values: Vec<String>,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct IncidentOwnerInfo {
    assigned_to: String,
    email: String,
    object_id: String,
    owner_type: OwnerType,
    user_principal_name: String,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct IncidentLabel {
    label_name: String,
    label_type: Option<LabelType>,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct IncidentPropertiesActionProperties {
    classification: Option<IncidentClassification>,
    classification_comment: Option<String>,
    classification_reason: Option<IncidentClassificationReason>,
    labels: Option<Vec<IncidentLabel>>,
    owner: Option<IncidentOwnerInfo>,
    severity: Option<IncidentSeverity>,
    status: Option<IncidentStatus>,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct PlaybookActionProperties {
    logic_app_resource_id: String,
    tenant_id: String,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct AddIncidentTaskActionProperties {
    description: String,
    title: String,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct TriggeringLogic {
    conditions: Vec<Condition>,
    expiration_time_utc: String,
    is_enabled: bool,
    triggers_on: TriggersOn,
    triggers_when: TriggersWhen,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(tag = "actionType", rename_all = "camelCase")]
pub enum Action {
    #[serde(rename = "AddIncidentTask", rename_all = "camelCase")]
    AddIncidentTagAction {
        action_configuration: AddIncidentTaskActionProperties,
        order: i64,
    },
    #[serde(rename = "RunPlaybook", rename_all = "camelCase")]
    RunPlaybookAction {
        action_configuration: PlaybookActionProperties,
        order: i64,
    },
    #[serde(rename = "ModifyProperties", rename_all = "camelCase")]
    ModifyPropertiesAction {
        action_configuration: IncidentPropertiesActionProperties,
        order: i64,
    },
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
struct Properties {
    actions: Vec<Action>,
    display_name: String,
    order: i64,
    triggering_logic: TriggeringLogic,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
enum CRDName {
    MicrosoftSentinelAutomationRule,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
enum APIVersion {
    #[serde(rename = "buildrlabs.io/v1")]
    BuildrLabs,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
struct Metadata {
    name: String,
    namespace: Option<String>,
    #[serde(flatten)]
    additional_properties: HashMap<String, String>,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
struct MicrosoftSentinelAutomationRuleCRD {
    kind: CRDName,
    spec: MicrosoftSentinelAutomationRuleSpec,
    api_version: APIVersion,
    metadata: Metadata,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
struct MicrosoftSentinelAutomationRuleSpec {
    properties: Properties,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
struct MicrosoftSentinelAutomationRuleStatus {
    message: String,
    deployed: String,
    enabled: String,
}

/// Specification for Microsoft Sentinel Automation Rule
#[derive(CustomResource, Serialize, Deserialize, Clone, Debug, JsonSchema)]
#[kube(
    group = "buildrlabs.io",
    version = "v1",
    kind = "MicrosoftSentinelAutomationRule",
    status = "MicrosoftSentinelAutomationRuleStatus",
    shortname = "msautomation",
    shortname = "msautomations",
    shortname = "msautomationrule",
    shortname = "msautomationrules",
    printcolumn = r#"{"name":"Status", "type":"string", "description":"Checks if the Automation Rule is deployed to Microsoft Sentinel", "jsonPath":".status.create_automation_rule.deployed"}"#,
    printcolumn = r#"{"name":"Enabled", "type":"string", "description":"Checks if the Automation Rule is enabled in Microsoft Sentinel", "jsonPath":".status.create_automation_rule.enabled"}"#,
    printcolumn = r#"{"name":"Message", "type":"string", "description":"Additional information about the deployment status", "jsonPath":".status.create_automation_rule.message"}"#,
    namespaced
)]
struct MicrosoftSentinelAutomationRuleCRDSpec {
    // For a pass-through CRD, we use a dynamic field structure with serde_json::Value
    #[schemars(schema_with = "preserve_unknown")]
    #[serde(flatten)]
    pub additional_fields: BTreeMap<String, serde_json::Value>,
}

/// Status for Microsoft Sentinel Automation Rule
#[derive(Serialize, Deserialize, Clone, Debug, JsonSchema)]
struct MicrosoftSentinelAutomationRuleCRDStatus {
    #[schemars(schema_with = "preserve_unknown")]
    #[serde(flatten)]
    pub additional_fields: BTreeMap<String, serde_json::Value>,
}

// Helper function to mark a schema as accepting arbitrary properties
fn preserve_unknown(_: &mut schemars::gen::SchemaGenerator) -> schemars::schema::Schema {
    let mut schema = schemars::schema::SchemaObject::default();
    schema.extensions.insert(
        "x-kubernetes-preserve-unknown-fields".to_string(),
        serde_json::Value::Bool(true),
    );
    schemars::schema::Schema::Object(schema)
}

pub fn write_schemas() -> std::io::Result<()> {
    // Write MicrosoftSentinelAutomationRule passthrough CRD
    let filename = "MicrosoftSentinelAutomationRule";
    let crd_yaml = serde_yaml::to_string(&MicrosoftSentinelAutomationRule::crd()).unwrap();
    let mut file = File::create(format!("./generated/crds/{}.yaml", filename)).unwrap();
    file.write_all(crd_yaml.as_bytes()).unwrap();
    println!("{filename} CRD-schema written to {filename}.yaml");

    // Write MicrosoftSentinelAutomationRule validation JSON-schema
    let filename = "MicrosoftSentinelAutomationRule";
    let schema = schema_for!(MicrosoftSentinelAutomationRuleSpec);
    let crd_json = serde_json::to_string_pretty(&schema).unwrap();
    let mut file = File::create(format!("./generated/jsonschema/{}.json", filename)).unwrap();
    file.write_all(crd_json.as_bytes()).unwrap();
    println!("{filename} JSON-schema written to {filename}.json");

    // Write MicrosoftSentinelAutomationRule CRD JSON-schema
    let filename = "MicrosoftSentinelAutomationRuleCRD";
    let schema = schema_for!(MicrosoftSentinelAutomationRuleCRD);
    let crd_json = serde_json::to_string_pretty(&schema).unwrap();
    let mut file = File::create(format!("./generated/jsonschema/{}.json", filename)).unwrap();
    file.write_all(crd_json.as_bytes()).unwrap();
    println!("{filename} JSON-schema written to {filename}.json");
    Ok(())
}
