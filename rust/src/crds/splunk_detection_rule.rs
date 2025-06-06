use kube::CustomResourceExt;
use kube_derive::CustomResource;
use schemars::{schema_for, JsonSchema};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::File;
use std::io::Write;

#[derive(CustomResource, Clone, Debug, Deserialize, Serialize, PartialEq, JsonSchema)]
#[kube(
    group = "buildrlabs.io",
    version = "v1",
    kind = "SplunkDetectionRule",
    shortname = "spldet",
    shortname = "spld",
    namespaced
)]
#[serde(rename_all = "camelCase")]
struct SplunkDetectionRuleSpec {
    description: String,
    name: String,
    search: String,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
enum CRDName {
    SplunkDetectionRule,
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
struct SplunkDetectionRuleCRD {
    kind: CRDName,
    spec: SplunkDetectionRuleSpec,
    api_version: APIVersion,
    metadata: Metadata,
}

pub fn write_schemas() -> std::io::Result<()> {
    // Write SplunkDetectionRule CRD
    let filename = "SplunkDetectionRule";
    let crd_yaml = serde_yaml::to_string(&SplunkDetectionRule::crd()).unwrap();
    let mut file = File::create(format!("./generated/crds/{}.yaml", filename)).unwrap();
    file.write_all(crd_yaml.as_bytes()).unwrap();
    println!("{filename} CRD-schema written to {filename}.yaml");

    // Write SplunkDetectionRule CRD JSON-schema
    let filename = "SplunkDetectionRuleCRD";
    let schema = schema_for!(SplunkDetectionRuleCRD);
    let crd_json = serde_json::to_string_pretty(&schema).unwrap();
    let mut file = File::create(format!("./generated/jsonschema/{}.json", filename)).unwrap();
    file.write_all(crd_json.as_bytes()).unwrap();
    println!("{filename} JSON-schema written to {filename}.json");
    Ok(())
}
