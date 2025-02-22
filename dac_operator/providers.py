from dac_operator.config import get_settings
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
