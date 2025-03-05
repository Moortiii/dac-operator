# dac-operator

## Highlights:

- Fully automated continuous deployment of Detection Library using FluxCD

- Supports per-customer configuration for Sentinel Microsoft Workspace information

- Custom Admission Controller that validates resource creation requests against API Schema

- Per-resource status information in `kubectl`, `k9s` or similar tooling

- Custom object support, e.g. `MicrosoftSentinelMacro` to support use-cases that are not provided by the SIEM

- Support for Microsoft Sentinel Analytic Rules

- Support for Microsoft Sentinel Automation Rules

### TODO:

- [ ] Store sensitive operator configuration as Kubernetes Secrets, use SOPS-encryption for storing them in Git.

- [ ] Create converter for Content Hub rules. It should be siple to import existing rules into the Detection library.

- [ ] Add support for [Microsoft Sentinel Workbooks](https://learn.microsoft.com/en-us/azure/sentinel/monitor-your-data)

- [ ] Ingest externally sourced Analytic rules from Microsoft Sentinel, such as those installed from ContentHub.

- [ ] Facilitate automated testing of Detection Rules

- [ ] Make it possible to verify changes before deploying to the live environment. Use a separate subscription to showcase this.

- [ ] Fetch MITRE Information from Detection rules to showcase how we can perform visualizations across multiple products / tenants using the Kubernetes API

### Known errors:

#### 'Example 2' was deleted too recently, retrying later.

There is a built-in delay in Microsoft when deleting and re-creating Detection Rules. The exact duration of the delay is not known, but is suspected to be somewhere between 30m and 1h30m. This isn't usually a problem in production where Detection Rules are relatively static, and instead are toggled as enabled / disabled.
