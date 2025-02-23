import hashlib

from dac_operator.microsoft_sentinel import (
    microsoft_sentinel_models,
    microsoft_sentinel_repository,
)


class MicrosoftSentinelService:
    def __init__(
        self, repository: microsoft_sentinel_repository.MicrosoftSentinelRepository
    ):
        self._repository = repository

    def _compute_analytics_rule_id(self, rule_name: str) -> str:
        return hashlib.sha1(rule_name.encode()).hexdigest()

    async def create_or_update(
        self,
        rule_name: str,
        payload: microsoft_sentinel_models.CreateScheduledAlertRule,
    ):
        """
        Create a Detection Rule upstream

        Args:
            payload(CreateScheduledAlertRule): A valid ScheduledAlertRule object
        """
        # Generate a random uuid to use as the ID for the Analytic Rule
        analytic_rule_id = self._compute_analytics_rule_id(rule_name=rule_name)

        await self._repository.create_or_update_scheduled_alert_rule(
            payload=payload, analytic_rule_id=analytic_rule_id
        )

    async def remove(self, rule_name: str):
        analytic_rule_id = self._compute_analytics_rule_id(rule_name=rule_name)
        await self._repository.remove_scheduled_alert_rule(
            analytic_rule_id=analytic_rule_id
        )

    async def is_deployed(self, analytic_rule_id: str) -> bool:
        """
        Check if a given Detection Rule is deployed remotely

        Args:
            rule_id(str): The ID of the upstream rule
        """
        rule = await self._repository.get_analytics_rule(
            analytic_rule_id=analytic_rule_id
        )
        return rule is not None
