import httpx
from loguru import logger as default_loguru_logger
from pydantic import SecretStr

from dac_operator.microsoft_sentinel import microsoft_sentinel_models


class MicrosoftSentinelRepository:
    def __init__(
        self,
        tenant_id: str,
        client_id: str,
        subscription_id: str,
        resource_group_id: str,
        workspace_id: str,
        client_secret: str,
        http_client=httpx.AsyncClient(timeout=30),
        logger=default_loguru_logger,
    ):
        self._client_id = client_id
        self._client_secret = client_secret
        self._subscription_id = subscription_id
        self._resource_group_id = resource_group_id
        self._tenant_id = tenant_id
        self._logger = logger
        self._workspace_id = workspace_id
        self._http_client = http_client

    async def authenticate(self):
        try:
            response = await self._http_client.post(
                f"https://login.microsoftonline.com/{self._tenant_id}/oauth2/v2.0/token",
                data={
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                    "grant_type": "client_credentials",
                    "scope": "https://management.azure.com/.default",
                },
            )
            response.raise_for_status()
        except httpx.HTTPStatusError:
            self._logger.exception(
                "An error occured during authentication with Microsoft"
            )
            raise

        return response.json()["access_token"]

    async def get_analytics_rules(self) -> list[dict]:
        token = await self.authenticate()

        try:
            response = await self._http_client.get(
                f"https://management.azure.com/subscriptions/{self._subscription_id}/resourceGroups/{self._resource_group_id}/providers/Microsoft.OperationalInsights/workspaces/{self._workspace_id}/providers/Microsoft.SecurityInsights/alertRules?api-version=2024-09-01",
                headers={"Authorization": f"Bearer {token}"},
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            self._logger.exception(
                f"An error occured when fetching all Analytics Rules. Response: {err.response}"  # noqa: E501
            )
            raise

        return response.json()["value"]

    async def get_analytics_rule(self, analytic_rule_id: str) -> dict | None:
        token = await self.authenticate()

        try:
            response = await self._http_client.get(
                f"https://management.azure.com/subscriptions/{self._subscription_id}/resourceGroups/{self._resource_group_id}/providers/Microsoft.OperationalInsights/workspaces/{self._workspace_id}/providers/Microsoft.SecurityInsights/alertRules/{analytic_rule_id}?api-version=2024-09-01",
                headers={"Authorization": f"Bearer {token}"},
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            if err.response.status_code == 404:
                return None

            self._logger.exception(
                f"An error occured when fetching Analytic rule '{analytic_rule_id}'. Response: {err.response}"  # noqa: E501
            )
            raise

        return response.json()

    async def create_or_update_scheduled_alert_rule(
        self,
        payload: microsoft_sentinel_models.CreateScheduledAlertRule,
        analytic_rule_id: str,
    ):
        token = await self.authenticate()

        try:
            response = await self._http_client.put(
                f"https://management.azure.com/subscriptions/{self._subscription_id}/resourceGroups/{self._resource_group_id}/providers/Microsoft.OperationalInsights/workspaces/{self._workspace_id}/providers/Microsoft.SecurityInsights/alertRules/{analytic_rule_id}?api-version=2024-09-01",
                headers={"Authorization": f"Bearer {token}"},
                json=payload.model_dump(by_alias=True),
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            if err.response.status_code == 409:
                if "was recently deleted" in err.response.text:
                    self._logger.info(
                        f"'{payload.properties.displayName}' was deleted too recently, retrying later."  # noqa: E501
                    )
                elif "Etag does not match" in err.response.text:
                    self._logger.info(
                        f"'{payload.properties.displayName}' e-tag error, retrying later."  # noqa: E501
                    )
            else:
                self._logger.exception(
                    f"An error occured while creating Analytics rule: {err.response.text}"  # noqa: E501
                )
                raise err from None

    async def create_or_update_automation_rule(
        self,
        payload: dict,
        automation_rule_id: str,
    ):
        token = await self.authenticate()

        try:
            response = await self._http_client.put(
                f"https://management.azure.com/subscriptions/{self._subscription_id}/resourceGroups/{self._resource_group_id}/providers/Microsoft.OperationalInsights/workspaces/{self._workspace_id}/providers/Microsoft.SecurityInsights/automationRules/{automation_rule_id}?api-version=2024-09-01",
                headers={"Authorization": f"Bearer {token}"},
                json=payload,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            if err.response.status_code == 409:
                if "was recently deleted" in err.response.text:
                    self._logger.info(
                        f"'{payload['properties'].displayName}' was deleted too recently, retrying later."  # noqa: E501
                    )
                else:
                    self._logger.info("An unknown 409 error occured.")
            else:
                self._logger.exception(
                    f"An error occured while creating Automation rule: {err.response.text}"  # noqa: E501
                )
                raise err from None

    async def remove_scheduled_alert_rule(self, analytic_rule_id: str):
        token = await self.authenticate()

        try:
            response = await self._http_client.delete(
                f"https://management.azure.com/subscriptions/{self._subscription_id}/resourceGroups/{self._resource_group_id}/providers/Microsoft.OperationalInsights/workspaces/{self._workspace_id}/providers/Microsoft.SecurityInsights/alertRules/{analytic_rule_id}?api-version=2024-09-01",
                headers={"Authorization": f"Bearer {token}"},
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            self._logger.exception(
                f"An error occured while creating Analytics rule: {err.response.text}"  # noqa: E501
            )
            raise err from None
