use kube::core::CustomResourceExt;
use kube_derive::CustomResource;
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::Write;

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
struct MicrosoftSentinelDetectionRuleSpec {
    query: String,
    query_suffix: Option<String>,
    query_prefix: Option<String>,
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
