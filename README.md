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
        --path=clusters/main
    ```
