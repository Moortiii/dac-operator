import base64

import kubernetes.client
from loguru import logger

from dac_operator.config import get_settings
from dac_operator.ext import kubernetes_exceptions
from dac_operator.ext.kubernetes_client import KubernetesClient
from dac_operator.microsoft_sentinel import (
    microsoft_sentinel_exceptions,
    microsoft_sentinel_repository,
    microsoft_sentinel_service,
)
from dac_operator.splunk import splunk_exceptions, splunk_repository, splunk_service

settings = get_settings()


def get_kubernetes_client(
    core_api: kubernetes.client.CoreV1Api,
    custom_objects_api: kubernetes.client.CustomObjectsApi,
):
    return KubernetesClient(custom_objects_api=custom_objects_api, core_api=core_api)


def get_splunk_service(
    namespace: str, kubernetes_client: KubernetesClient
) -> splunk_service.SplunkService | None:
    try:
        configmap = kubernetes_client.get_config_map(
            name="splunk-configuration", namespace=namespace
        )
    except kubernetes_exceptions.ResourceNotFoundException as err:
        logger.info(
            f"{namespace} has no configuration named "
            "'splunk-configuration', skipping..."
        )
        return None

    secret_name = configmap.data["secret_ref"]
    try:
        secret = kubernetes_client.get_secret(name=secret_name, namespace=namespace)
    except kubernetes_exceptions.ResourceNotFoundException as err:
        logger.exception(err)
        raise splunk_exceptions.ServiceConfigurationException

    return splunk_service.SplunkService(
        repository=splunk_repository.SplunkRepository(
            token=base64.b64decode(secret["token"]).decode(),
            host=configmap.data["host"],
            port=int(configmap.data["port"]),
            protocol=configmap.data["scheme"],
            verify=configmap.data["verify"] in [1, True, "true"],
        )
    )


def get_microsoft_sentinel_service(namespace: str, kubernetes_client: KubernetesClient):
    try:
        configmap = kubernetes_client.get_config_map(
            name="microsoft-sentinel-configuration", namespace=namespace
        )
    except kubernetes_exceptions.ResourceNotFoundException as err:
        logger.exception(err)
        raise microsoft_sentinel_exceptions.ServiceConfigurationException

    secret_name = configmap.data["secret_ref"]

    try:
        secret = kubernetes_client.get_secret(name=secret_name, namespace=namespace)
    except kubernetes_exceptions.ResourceNotFoundException as err:
        logger.exception(err)
        raise microsoft_sentinel_exceptions.ServiceConfigurationException

    return microsoft_sentinel_service.MicrosoftSentinelService(
        repository=microsoft_sentinel_repository.MicrosoftSentinelRepository(
            tenant_id=configmap.data["azure_tenant_id"],
            workspace_id=configmap.data["azure_workspace_id"],
            subscription_id=configmap.data["azure_subscription_id"],
            resource_group_id=configmap.data["azure_resource_group_id"],
            client_id=base64.b64decode(secret["azure_client_id"]).decode(),
            client_secret=base64.b64decode(secret["azure_client_secret"]).decode(),
        ),
        kubernetes_client=kubernetes_client,
        namespace=namespace,
    )
