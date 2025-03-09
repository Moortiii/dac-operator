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

settings = get_settings()


def get_microsoft_sentinel_repository(
    tenant_id: str, subscription_id: str, resource_group_id: str, workspace_id: str
):
    return microsoft_sentinel_repository.MicrosoftSentinelRepository(
        tenant_id=tenant_id,
        client_id=settings.client_id,
        client_secret=settings.client_secret,
        subscription_id=subscription_id,
        resource_group_id=resource_group_id,
        workspace_id=workspace_id,
    )


def get_kubernetes_client(
    core_api: kubernetes.client.CoreV1Api,
    custom_objects_api: kubernetes.client.CustomObjectsApi,
):
    return KubernetesClient(custom_objects_api=custom_objects_api, core_api=core_api)


def get_microsoft_sentinel_service(namespace: str, kubernetes_client: KubernetesClient):
    try:
        configmap = kubernetes_client.get_config_map(
            name="microsoft-sentinel-configuration", namespace=namespace
        )
    except kubernetes_exceptions.ResourceNotFoundException as err:
        logger.exception(err)
        raise microsoft_sentinel_exceptions.ServiceConfigurationException

    return microsoft_sentinel_service.MicrosoftSentinelService(
        repository=microsoft_sentinel_repository.MicrosoftSentinelRepository(
            tenant_id=configmap.data["azure_tenant_id"],
            workspace_id=configmap.data["azure_workspace_id"],
            subscription_id=configmap.data["azure_subscription_id"],
            resource_group_id=configmap.data["azure_resource_group_id"],
            client_id=settings.client_id,
            client_secret=settings.client_secret,
        ),
        kubernetes_client=kubernetes_client,
        namespace=namespace,
    )
