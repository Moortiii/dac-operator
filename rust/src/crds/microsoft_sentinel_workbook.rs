use kube::core::CustomResourceExt;
use kube_derive::CustomResource;
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::Write;

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "lowercase")]
pub enum Kind {
    Shared,
    User,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "PascalCase")]
pub enum ManagedServiceIdentityType {
    SystemAssigned,
    #[serde(rename = "SystemAssigned,UserAssigned")]
    SystemAssignedUserAssigned,
    UserAssigned,
    #[serde(rename = "None")]
    NoneIdentity,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
struct Identity {
    principal_id: String,
    tenant_id: String,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
struct WorkbookProperties {
    category: String,
    display_name: String,
    serialized_data: String,
    description: Option<String>,
    source_id: Option<String>,
    storage_uri: Option<String>,
    tags: Option<Vec<String>>,
    version: String,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
struct ExampleStruct {}

#[derive(CustomResource, Clone, Debug, Deserialize, Serialize, PartialEq, JsonSchema)]
#[kube(
    group = "buildrlabs.io",
    version = "v1",
    kind = "MicrosoftSentinelWorkbook",
    shortname = "msmacro",
    status = "MicrosoftSentinelWorkbookStatus",
    shortname = "msmacros",
    printcolumn = r#"{"name":"Message", "type":"string", "description":"Additional information about the deployment status", "jsonPath":".status.create_detection_rule.message"}"#,
    namespaced
)]
#[serde(rename_all = "camelCase")]
struct MicrosoftSentinelWorkbookSpec {
    location: String,
    tags: Vec<String>,
    kind: Kind,
    identity: Identity,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
struct MicrosoftSentinelWorkbookStatus {
    message: String,
}

pub fn write_crd() -> std::io::Result<()> {
    // Write MicrosoftSentinelWorkbook CRD
    let filename = "MicrosoftSentinelWorkbook";
    let crd_yaml = serde_yaml::to_string(&MicrosoftSentinelWorkbook::crd()).unwrap();
    let mut file = File::create(format!("./generated/{}.yaml", filename)).unwrap();
    file.write_all(crd_yaml.as_bytes()).unwrap();
    println!("{filename} written to {filename}.yaml");
    Ok(())
}
