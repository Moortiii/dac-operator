import httpx
from loguru import logger as default_loguru_logger

from dac_operator.splunk.splunk_models import SplunkDetectionRule


class SplunkRepository:
    def __init__(
        self,
        protocol: str,
        host: str,
        port: int,
        token: str,
        verify: bool,
        logger=default_loguru_logger,
    ):
        self._token = token
        self._logger = logger
        self._host = host
        self._port = port
        self._protocol = protocol
        self._verify = verify
        self._base_url = f"{self._protocol}://{self._host}:{self._port}"

    async def get_splunk_detection_rule(self, name: str) -> dict | None:
        async with httpx.AsyncClient(verify=self._verify) as client:
            try:
                res = await client.get(
                    f"{self._base_url}/services/saved/searches/{name}",  # noqa: E501
                    headers={"Authorization": f"Bearer {self._token}"},
                    params={"output_mode": "json"},
                )
                res.raise_for_status()
            except httpx.HTTPStatusError as err:
                if err.response.status_code == 404:
                    self._logger.info(
                        f"No Detection Rule with name '{name}' exists, creating!"
                    )
                    return None

                self._logger.exception(err)
                self._logger.error(
                    f"Status code: {err.response.status_code}. Response: "
                    f"{err.response.text}"
                )
                raise err
            except httpx.RequestError as err:
                self._logger.exception(err)
                raise err

        return res.json()

    async def create_splunk_detection_rule(self, detection_rule: SplunkDetectionRule):
        async with httpx.AsyncClient(verify=self._verify) as client:
            try:
                res = await client.post(
                    f"{self._base_url}/services/saved/searches",  # noqa: E501
                    data={
                        "name": detection_rule.name,
                        "description": detection_rule.description,
                        "search": detection_rule.search,
                    },
                    headers={"Authorization": f"Bearer {self._token}"},
                )
                res.raise_for_status()
            except httpx.HTTPStatusError as err:
                if err.response.status_code == 409:
                    self._logger.error(
                        f"Detection Rule with name {detection_rule.name} "
                        "already exists."
                    )
                    return

                self._logger.exception(err)
                self._logger.error(
                    f"Status code: {err.response.status_code}. Response: "
                    f"{err.response.text}"
                )
                raise err
            except httpx.RequestError as err:
                self._logger.exception(err)
                raise err
