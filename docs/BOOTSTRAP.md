### Prerequisites

Create the SSH key:

1.  Create an ssh-key using `ssh-keygen`

    Secure your key with a good passphrase.

2.  Save the private key to the root of this repository as `flux_bootstrap_key`, which is present in `.gitignore`.

3.  Save the private key passphrase to the root of this repository as `flux_bootstrap_key_passphrase`, which is present in `.gitignore`.

### Bootstrap flux (classic)

Flux is responsible for reconciling the Detection Rule state automatically, when new manifests are added to the repository. In order to do so, Flux installs itself into the cluster and pulls the Git repository on interval. As a result, it requires a bootstrapping procedure, which is detailed below.

By using a deploy key, we can avoid bootstrapping Flux with a Github PAT, which would have to be rotated fairly frequently. If you do not want to use an SSH key, it is also possible to bootstrap with a PAT or a Github App.

1.  Navigate to https://github.com/Moortiii/dac-operator/settings/keys and add the public key:

    Make sure to give it write-permissions to the repository, otherwise Flux won't have permission to push the sync manifests as it needs to.

2.  Bootstrap Flux:

    ```bash
    # Set the correct context
    kubectl config use-context minikube

    # Perform the bootstrap process
    flux bootstrap git \
        --url=ssh://git@github.com/Moortiii/dac-operator \
        --branch=main \
        --private-key-file=./flux_bootstrap_key \
        --password=$(cat ./flux_bootstrap_key_passphrase) \
        --path=clusters/production
    ```

### Bootstrap flux (operator)

1. Install the Flux operator using `kubectl apply -f https://github.com/controlplaneio-fluxcd/flux-operator/releases/latest/download/install.yaml`

2. Navigate to https://github.com/Moortiii/dac-operator/settings/keys and add the public key:

   In this case Flux does not need write-access to the repository.

3. Create the pullSecret:

```bash
flux create secret git flux-system \
  --url=ssh://git@github.com/Moortiii/dac-operator \
  --private-key-file=./flux_bootstrap_key \
  --password=$(cat ./flux_bootstrap_key_passphrase)
```

4. Bootstrap Flux, by applying the following manifest:

   ```yaml
   apiVersion: fluxcd.controlplane.io/v1
   kind: FluxInstance
   metadata:
     name: flux
     namespace: flux-system
   spec:
     distribution:
       version: "2.x"
       registry: "ghcr.io/fluxcd"
     components:
       - source-controller
       - kustomize-controller
       - helm-controller
       - notification-controller
     cluster:
       type: kubernetes
       multitenant: false
       networkPolicy: true
       domain: "cluster.local"
     sync:
       kind: GitRepository
       url: "ssh://git@github.com/moortiii/dac-operator.git"
       ref: "refs/heads/main"
       path: "clusters/production"
       pullSecret: "flux-system"
   ```
