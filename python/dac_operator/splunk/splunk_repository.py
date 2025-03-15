import splunklib.client


class SplunkRepository:
    def __init__(self, client: splunklib.client.Service):
        self._client = client

    async def create_splunk_app(self, app_name: str):
        app = self._client.apps.get(name=app_name)

    async def create_splunk_detection_rule(self):
        ...
        # self._client.saved_searches.create
