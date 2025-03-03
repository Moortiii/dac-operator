use kube::core::CustomResourceExt;
use kube_derive::CustomResource;
use schemars::{schema_for, JsonSchema};
use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::Write;

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "PascalCase")]
pub enum ExampleEnum {}

#[derive(Serialize, Deserialize, Debug, PartialEq, Clone, JsonSchema)]
#[serde(rename_all = "camelCase")]
struct ExampleStruct {}

#[derive(CustomResource, Clone, Debug, Deserialize, Serialize, PartialEq, JsonSchema)]
#[kube(
    group = "buildrlabs.io",
    version = "v1",
    kind = "MicrosoftSentinelMacro",
    shortname = "msmacro",
    shortname = "msmacros",
    namespaced
)]
#[serde(rename_all = "camelCase")]
struct MicrosoftSentinelMacroSpec {
    content: String,
}

pub fn write_crd() -> std::io::Result<()> {
    // Write MicrosoftSentinelMacro CRD
    let filename = "MicrosoftSentinelMacro";
    let crd_yaml = serde_yaml::to_string(&MicrosoftSentinelMacro::crd()).unwrap();
    let mut file = File::create(format!("./generated/crds/{}.yaml", filename)).unwrap();
    file.write_all(crd_yaml.as_bytes()).unwrap();
    println!("{filename} CRD-schema written to {filename}.yaml");

    // Write MicrosoftSentinelMacro Jsonschema
    let filename = "MicrosoftSentinelMacro";
    let schema = schema_for!(MicrosoftSentinelMacroSpec);
    let crd_json = serde_json::to_string_pretty(&schema).unwrap();
    let mut file = File::create(format!("./generated/jsonschema/{}.json", filename)).unwrap();
    file.write_all(crd_json.as_bytes()).unwrap();
    println!("{filename} JSON-schema written to {filename}.json");
    Ok(())
}
