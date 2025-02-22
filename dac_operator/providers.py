from dac_operator.config import get_settings
from dac_operator.microsoft_sentinel import (
    microsoft_sentinel_repository,
    microsoft_sentinel_service,
)

settings = get_settings()


def get_microsoft_sentinel_repository():
    return microsoft_sentinel_repository.MicrosoftSentinelRepository(
        tenant_id=settings.azure_tenant_id,
        client_id=settings.client_id,
        client_secret=settings.client_secret,
        subscription_id=settings.azure_subscription_id,
        resource_group_id=settings.resource_group_id,
        workspace_id=settings.azure_workspace_id,
    )


def get_microsoft_sentinel_service():
    return microsoft_sentinel_service.MicrosoftSentinelService(
        repository=get_microsoft_sentinel_repository()
    )
