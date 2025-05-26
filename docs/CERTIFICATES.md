# Certificates

Kubernetes can only call validating and mutating admission webhooks over TLS. Most organizations will have their own mechanisms and routines for generating and renewing certificates. If you already have a certificate that you want to use, skip directly to [configuring webhook certificates](#configuring-webhook-certificates-manual).

## About certificates

We will use cert-manager in Kubernetes to operate as our own certificate authority.

A secure PKI chain usually consists of three elements:

1. A Root CA
2. An Intermediate CA (signed by the Root CA)
3. A Certificate (signed by the Intermediate CA)

The Root CA is installed in the system trust store and therefore trusted by the client. This makes it difficult to revoke a Root CA, since clients would have to update their CA-certificate store in order to stop trusting certificates that are signed by it.

This problem can be circumvented by using an intermediate CA. This certificate is _not_ installed in the system trust store, but is provided by the server directly during the initial handshake phase. This makes it possible to revoke an intermediate CA (and the certificates signed by it) without action being required on the part of the client.

For the sake of simplicity we will skip the intermediate certificates (at least for now) and sign certificates with a Root CA directly.

## Prerequisites

### Install cert-manager

```
helm repo add jetstack https://charts.jetstack.io
helm repo update

helm install \
    cert-manager jetstack/cert-manager \
    --namespace cert-manager \
    --create-namespace \
    --version v1.17.0 \
    --set installCRDs=true
```

### Configuring Webhook Certificates (cert-manager)

The `webhook-config.yaml` file contains the `ValidatingWebhookConfiguration` which describes which endpoint to use for validation when operating on various resources.

We are using the `cert-manager.io/inject-ca-from` annotation to automatically update the webhook configuration with the CA bundle from the generated cert. This tells the Kubernetes API server to use this CA bundle when validating the certificates provided by the admission webhook.

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: validate-automation-rules
  annotations:
    cert-manager.io/inject-ca-from: dac-system/admission-webhook
webhooks:
  - admissionReviewVersions:
      - v1
      - v1beta1
    clientConfig:
      service:
        name: {{ .Values.operator.name }}
        namespace: {{ .Release.Namespace }}
        path: /validate-automation-rule
        port: 443
    failurePolicy: Fail
    matchPolicy: Equivalent
    name: validate-automation-rules.buildrlabs.io
    namespaceSelector: {}
    objectSelector: {}
    rules:
      - apiGroups:
          - buildrlabs.io
        apiVersions:
          - v1
        operations:
          - CREATE
          - UPDATE
        resources:
          - microsoftsentinelautomationrules
        scope: "*"
    sideEffects: None
    timeoutSeconds: 30
```

### Configuring Webhook Certificates (manual)

In the event that you have a pre-generated certificate (that is not signed by a well-known CA), you need to provide the certificate bundle directly in the `caBundle` field. This tells the Kubernetes API server to use this CA bundle when validating the certificates provided by the admission webhook.

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: validate-automation-rules
  annotations:
    cert-manager.io/inject-ca-from: dac-system/admission-webhook
webhooks:
  - admissionReviewVersions:
      - v1
      - v1beta1
    clientConfig:
      caBundle: LS0t...LS0K # Provide your CA bundle here
      service:
        name: {{ .Values.operator.name }}
        namespace: {{ .Release.Namespace }}
        path: /validate-automation-rule
        port: 443
    failurePolicy: Fail
    matchPolicy: Equivalent
    name: validate-automation-rules.buildrlabs.io
    namespaceSelector: {}
    objectSelector: {}
    rules:
      - apiGroups:
          - buildrlabs.io
        apiVersions:
          - v1
        operations:
          - CREATE
          - UPDATE
        resources:
          - microsoftsentinelautomationrules
        scope: "*"
    sideEffects: None
    timeoutSeconds: 30
```
