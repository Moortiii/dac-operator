from uuid import uuid4

from dac_operator.microsoft_sentinel import (
    microsoft_sentinel_models,
    microsoft_sentinel_repository,
)


class MicrosoftSentinelService:
    def __init__(
        self, repository: microsoft_sentinel_repository.MicrosoftSentinelRepository
    ):
        self._repository = repository

    async def create(self, payload: microsoft_sentinel_models.CreateScheduledAlertRule):
        """
        Create a Detection Rule upstream

        Args:
            payload(CreateScheduledAlertRule): A valid ScheduledAlertRule object
        """
        # Generate a random uuid to use as the ID for the Analytic Rule
        analytic_rule_id = uuid4().hex

        await self._repository.create_or_update_scheduled_alert_rule(
            payload=payload, analytic_rule_id=analytic_rule_id
        )

    async def update(
        self,
        payload: microsoft_sentinel_models.CreateScheduledAlertRule,
        analytic_rule_id: str,
    ):
        """
        Update a Detection Rule upstream

        Args:
            payload(CreateScheduledAlertRule): A valid ScheduledAlertRule object
        """
        await self._repository.create_or_update_scheduled_alert_rule(
            payload=payload, analytic_rule_id=analytic_rule_id
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
        return rule is None
