from dac_operator.splunk import splunk_repository


class SplunkService:
    def __init__(self, repository: splunk_repository.SplunkRepository):
        self._repository = repository

    async def create_or_update_detection_rule(self):
        await self._repository.create_splunk_detection_rule()
