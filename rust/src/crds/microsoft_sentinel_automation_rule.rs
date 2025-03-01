use kube::core::CustomResourceExt;
use kube_derive::CustomResource;
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};
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
pub enum RunPlaybookActionType {
    #[serde(rename = "Run Playbook")]
    RunPlaybook,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
pub enum ModifyPropertiesActionType {
    #[serde(rename = "Modify Properties")]
    ModifyProperties,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
pub enum AddIncidentTaskActionType {
    #[serde(rename = "Add Incident Task")]
    AddIncidentTask,
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
    label_type: LabelType,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct IncidentPropertiesAction {
    classification: IncidentClassification,
    classification_comment: String,
    classification_reason: IncidentClassificationReason,
    labels: Vec<IncidentLabel>,
    owner: IncidentOwnerInfo,
    severity: IncidentSeverity,
    status: IncidentStatus,
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
pub struct TriggeringLogic {}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
pub enum Action {
    #[serde(rename_all = "camelCase")]
    ModifyPropertiesAction {
        action_type: ModifyPropertiesActionType,
        action_configuration: IncidentPropertiesAction,
        order: i64,
    },
    #[serde(rename_all = "camelCase")]
    AddIncidentTagAction {
        action_type: AddIncidentTaskActionType,
        action_configuration: AddIncidentTaskActionProperties,
        order: i64,
    },
    #[serde(rename_all = "camelCase")]
    RunPlaybookAction {
        action_type: RunPlaybookActionType,
        action_configuration: PlaybookActionProperties,
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

#[derive(CustomResource, Clone, Debug, Deserialize, Serialize, PartialEq, JsonSchema)]
#[kube(
    group = "buildrlabs.io",
    version = "v1",
    kind = "MicrosoftSentinelAutomationRule",
    shortname = "msar",
    status = "MicrosoftSentinelAutomationRuleStatus",
    shortname = "msars",
    printcolumn = r#"{"name":"Status", "type":"string", "description":"Checks if the Automation Rule is deployed to Microsoft Sentinel", "jsonPath":".status.create_automation_rule.deployed"}"#,
    printcolumn = r#"{"name":"Enabled", "type":"string", "description":"Checks if the Automation Rule is enabled in Microsoft Sentinel", "jsonPath":".status.create_automation_rule.enabled"}"#,
    printcolumn = r#"{"name":"Message", "type":"string", "description":"Additional information about the deployment status", "jsonPath":".status.create_automation_rule.message"}"#,
    namespaced
)]
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

pub fn write_crd() -> std::io::Result<()> {
    // Write MicrosoftSentinelAutomationRule CRD
    let filename = "MicrosoftSentinelAutomationRule";
    let crd_yaml = serde_yaml::to_string(&MicrosoftSentinelAutomationRule::crd()).unwrap();
    let mut file = File::create(format!("./generated/{}.yaml", filename)).unwrap();
    file.write_all(crd_yaml.as_bytes()).unwrap();
    println!("{filename} written to {filename}.yaml");
    Ok(())
}
