import kubernetes.client

from dac_operator.config import get_settings
from dac_operator.ext.kubernetes_client import KubernetesClient
from dac_operator.microsoft_sentinel import (
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


def get_microsoft_sentinel_service(
    tenant_id: str, subscription_id: str, resource_group_id: str, workspace_id: str
):
    return microsoft_sentinel_service.MicrosoftSentinelService(
        repository=get_microsoft_sentinel_repository(
            tenant_id=tenant_id,
            resource_group_id=resource_group_id,
            workspace_id=workspace_id,
            subscription_id=subscription_id,
        )
    )
