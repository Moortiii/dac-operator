use kube::CustomResourceExt;
use kube_derive::CustomResource;
use schemars::{schema_for, JsonSchema};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, HashMap};
use std::fs::File;
use std::io::Write;

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "lowercase")]
pub enum Kind {
    Shared,
    User,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct UserAssignedIdentity {
    client_id: String,
    principal_id: String,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, JsonSchema)]
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
    r#type: ManagedServiceIdentityType,
    user_assigned_identities: HashMap<String, UserAssignedIdentity>,
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
    version: Option<String>,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
struct MicrosoftSentinelWorkbookSpec {
    location: String,
    properties: WorkbookProperties,
    tags: Vec<String>,
    kind: Kind,
    identity: Identity,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
struct MicrosoftSentinelWorkbookStatus {
    message: String,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
enum CRDName {
    MicrosoftSentinelWorkbook,
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
struct MicrosoftSentinelWorkbookCRD {
    kind: CRDName,
    spec: MicrosoftSentinelWorkbookSpec,
    api_version: APIVersion,
    metadata: Metadata,
}

#[derive(CustomResource, Clone, Debug, Deserialize, Serialize, PartialEq, JsonSchema)]
#[kube(
    group = "buildrlabs.io",
    version = "v1",
    kind = "MicrosoftSentinelWorkbook",
    shortname = "msw",
    shortname = "msws",
    status = "MicrosoftSentinelWorkbookStatus",
    printcolumn = r#"{"name":"Message", "type":"string", "description":"Additional information about the deployment status", "jsonPath":".status.create_workbook.message"}"#,
    namespaced
)]
#[serde(rename_all = "camelCase")]
struct MicrosoftSentinelWorkbookCRDSpec {
    // For a pass-through CRD, we use a dynamic field structure with serde_json::Value
    #[schemars(schema_with = "preserve_unknown")]
    #[serde(flatten)]
    pub additional_fields: BTreeMap<String, serde_json::Value>,
}

/// Status for Microsoft Sentinel Automation Rule
#[derive(Serialize, Deserialize, Clone, Debug, JsonSchema)]
struct MicrosoftSentinelWorkbookCRDStatus {
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
    // Write MicrosoftSentinelWorkbook passthrough CRD
    let filename = "MicrosoftSentinelWorkbook";
    let crd_yaml = serde_yaml::to_string(&MicrosoftSentinelWorkbook::crd()).unwrap();
    let mut file = File::create(format!("./generated/crds/{}.yaml", filename)).unwrap();
    file.write_all(crd_yaml.as_bytes()).unwrap();
    println!("{filename} CRD-schema written to {filename}.yaml");

    // Write MicrosoftSentinelWorkbook validation JSON-schema
    let filename = "MicrosoftSentinelWorkbook";
    let schema = schema_for!(MicrosoftSentinelWorkbookSpec);
    let crd_json = serde_json::to_string_pretty(&schema).unwrap();
    let mut file = File::create(format!("./generated/jsonschema/{}.json", filename)).unwrap();
    file.write_all(crd_json.as_bytes()).unwrap();
    println!("{filename} JSON-schema written to {filename}.json");

    // Write MicrosoftSentinelWorkbook CRD JSON-schema
    let filename = "MicrosoftSentinelWorkbookCRD";
    let schema = schema_for!(MicrosoftSentinelWorkbookCRD);
    let crd_json = serde_json::to_string_pretty(&schema).unwrap();
    let mut file = File::create(format!("./generated/jsonschema/{}.json", filename)).unwrap();
    file.write_all(crd_json.as_bytes()).unwrap();
    println!("{filename} JSON-schema written to {filename}.json");
    Ok(())
}
