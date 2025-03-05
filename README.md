# dac-operator

### Bootstrap flux

Flux is responsible for reconciling the Detection Rule state automatically, when new manifests are added to the repository. In order to do so, Flux installs itself into the cluster and pulls the Git repository on interval. As a result, it requires a bootstrapping procedure, which is detailed below.

By using a deploy key, we can avoid bootstrapping Flux with a Github PAT, which would have to be rotated fairly frequently. If you do not want to use an SSH key, it is also possible to bootstrap with a PAT or a Github App.

1.  Create an ssh-key using `ssh-keygen`

    Secure your key with a good passphrase.

2.  Save the private key to the root of this repository as `flux_bootstrap_key`, which is present in `.gitignore`.

3.  Save the private key passphrase to the root of this repository as `flux_bootstrap_key_passphrase`, which is present in `.gitignore`.

4.  Navigate to https://github.com/Moortiii/dac-operator/settings/keys and add the public key:

    Make sure to give it write-permissions to the repository, otherwise Flux won't have permission to push the sync manifests as it needs to.

5.  (optional) Export the passphrase to an environment variable, use a space at the beginning of the line to avoid storing the passphrase in your bash-history:

    ```bash
     export FLUX_PRIVATE_KEY_PASSPRHASE=<passphrase>
    ```

6.  Bootstrap Flux:

    ```bash
    # Set the correct context
    kubectl config use-context minikube

    # Perform the bootstrap process
    flux bootstrap git \
        --url=ssh://git@github.com/Moortiii/dac-operator \
        --branch=main \
        --private-key-file=./flux_bootstrap_key \
        --password=$FLUX_PRIVATE_KEY_PASSPRHASE \
        --path=clusters/production
    ```

#### Known errors:

'Example 2' was deleted too recently, retrying later.

There is a built-in delay in Microsoft when deleting and re-creating Detection Rules. The exact duration of the delay is not known, but is suspected to be somewhere between 30m and 1h30m.

This isn't usually a problem in production where Detection Rules are relatively static, and instead are toggled as enabled / disabled.

## Highlights:

- ✅ Supports per-customer configuration for Sentinel Microsoft Workspace information

- ✅ Custom Admission Controller that validates resource creation requests against API Schema

- ✅ Per-resource status information in `kubectl`, `k9s` or similar tooling

- ✅ Custom object support, e.g. `MicrosoftSentinelMacro` to support use-cases that are not provided by the SIEM

- ✅ Support for Microsoft Sentinel Analytic Rules

- ✅ Support for Microsoft Sentinel Automation Rules

#### TODO:

- [ ] Store sensitive operator configuration as Kubernetes Secrets, use SOPS-encryption for storing them in Git.

- [ ] Create converter for Content Hub rules. It should be siple to import existing rules into the Detection library.

- [ ] Add support for [Microsoft Sentinel Workbooks](https://learn.microsoft.com/en-us/azure/sentinel/monitor-your-data)

- [ ] Ingest externally sourced Analytic rules from Microsoft Sentinel, such as those installed from ContentHub.

- [ ] Facilitate automated testing of Detection Rules

- [ ] Make it possible to verify changes before deploying to the live environment. Use a separate subscription to showcase this.

- [ ] Fetch MITRE Information from Detection rules to showcase how we can perform visualizations across multiple products / tenants using the Kubernetes API
