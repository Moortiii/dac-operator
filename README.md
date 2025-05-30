# Detection as Code operator

This repository contains the code for my Master thesis with the title:

> A novel approach for Detection Engineering using Kubernetes and GitOps principles

The general idea is to leverage Kubernetes operator with GitOps tooling in order to achieve seamless Continuous Deployment (CD) of a Detection Library, across multiple Tenants, environments and security products.

The operator uses `etcd` as a database, storing information in Custom Resource Definition objects and continuously synchronizing the content to relevant security products using relevant REST APIs or other means of programmatic interaction.

## Highlights:

- Fully automated continuous deployment of Detection Library using FluxCD

- Supports per-customer configuration for Sentinel Microsoft Workspace information using Confimaps

- Supports multiple environments per customer using Kustomize overlays

- Custom Admission Controller that validates resource creation and update requests against a JSON-schema

- Per-resource status information in `kubectl`, `k9s` or similar tooling

- Custom object support, e.g. `MicrosoftSentinelMacro` to support use-cases that are not provided by the SIEM

- Support for Microsoft Sentinel Alert Rules

- Support for Microsoft Sentinel Automation Rules

- Support for Microsoft Sentinel Workbooks

## Prerequisites

* [Kind](https://kind.sigs.k8s.io/)
* [Flux](https://fluxcd.io/)
* [Rust](https://www.rust-lang.org/)
* [Tilt](https://tilt.dev)

## Getting started

1. Create a cluster using `kind create cluster`
2. Follow the guide in [BOOTSTRAP.md](./docs/BOOTSTRAP.md) to bootstrap FluxCD
3. Create an App Registration in Microsoft
4. Create the necessary secrets given in `secret_ref` in `./deploy/tenants/<customer_id>/<environment>/configmap.yaml`

    ```
    # Microsoft Sentinel
    kubectl create secret generic azure-<tenant-id> --from-literal=azure_client_id=<client-id> --from-literal=azure_client_secret=<client-secret> -n <tenant-id>
    ```

    ```
    # Splunk
    kubectl create secret generic splunk-<tenant-id> --from-literal=token=<token> -n <tenant-id>
    ```

5. Run the application using `tilt up`

### TODO:

- [ ] Create CI pipeline that performs automated testing

- [ ] Showcase multi-product support for a single vendor by deploying Detection Rules to Microsoft Defender

- [ ] Showcase multi-vendor support by deploying Detection Rules to Splunk

- [ ] Create converter for Content Hub rules. It should be simple to import existing rules into the Detection library.

- [ ] Ingest externally sourced Analytic rules from Microsoft Sentinel, such as those installed from ContentHub.

- [ ] Facilitate automated testing of Detection Rules.

- [ ] Make it possible to verify changes before deploying to the live environment. Use a separate subscription to showcase this.

- [ ] Fetch MITRE Information from Detection rules to showcase how we can perform visualizations across multiple products / tenants using the Kubernetes API.

### Known issues:

#### "'Example 2' was deleted too recently, retrying later"

There is a built-in delay in Microsoft when deleting and re-creating Alert Rules. The exact duration of the delay is not known, but is suspected to be somewhere between 30m and 1h30m. This isn't usually a problem in production where Detection Rules are relatively static, and instead are toggled as enabled / disabled, which is a non-destructive operation.
