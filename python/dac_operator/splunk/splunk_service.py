from dac_operator.splunk import splunk_repository
from dac_operator.splunk.splunk_models import SplunkDetectionRule


class SplunkService:
    def __init__(self, repository: splunk_repository.SplunkRepository):
        self._repository = repository

    async def create_or_update_detection_rule(
        self, detection_rule: SplunkDetectionRule
    ):
        detection_rule_from_api = await self._repository.get_splunk_detection_rule(
            name=detection_rule.name
        )

        if detection_rule_from_api is None:
            await self._repository.create_splunk_detection_rule(
                detection_rule=detection_rule
            )
