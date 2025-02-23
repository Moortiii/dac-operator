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
    kubectl config use-context kind-kind

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

#### TODO:

- [x] Fetch information about which workspace to use etc. in the kopf-controller from the customer configmap
- [x] Include a status column on the Detection Rule that indicates if it is deployed upstream or not
- [x] Include a status column on the Detection Rule that indicates if it is enabled upstream or not
- [ ] Add support for automation rules, analytics workbooks etc.
- [ ] Consider support for fetching third-party rules (e.g. those added via Content Hub, marking them as 'external' but generating Kubernetes resources for them)
- [ ] Add the option to include a query prefix, and query suffix, e.g. to support basic filter-macros for Tenants.
- [ ] Include a status column on the Detection Rule that describes _why_ it isn't deployed, if that is the case
- [ ] Store the expiry when authenticating to prevent authenticating again for each Detection Rule to deploy
- [ ] Make it possible to test Detection Rules prior to deployment
- [ ] Set up a "staging"-cluster in Kind that can be used to verify changes (different and more easily solvable than automated testing)
- [ ] Create a strict CRD manifest that can be used by Kubernetes to validate incoming resources that we want to create (use Kubebuilder or kube-rs and structure as monorepo?)
