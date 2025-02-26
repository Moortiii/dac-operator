import hashlib

from loguru import logger as default_loguru_logger

from dac_operator.crd import crd_models
from dac_operator.ext import kubernetes_exceptions
from dac_operator.ext.kubernetes_client import KubernetesClient
from dac_operator.microsoft_sentinel import (
    microsoft_sentinel_models,
    microsoft_sentinel_repository,
)
from dac_operator.microsoft_sentinel.microsoft_sentinel_macro_service import (
    MicrosoftSentinelMacroService,
)


class MicrosoftSentinelService:
    def __init__(
        self,
        repository: microsoft_sentinel_repository.MicrosoftSentinelRepository,
        kubernetes_client: KubernetesClient,
        namespace: str,
        logger=default_loguru_logger,
    ):
        self._repository = repository
        self._kubernetes_client = kubernetes_client
        self._logger = logger
        self._namespace = namespace

    def _compute_analytics_rule_id(self, rule_name: str) -> str:
        return hashlib.sha1(rule_name.encode()).hexdigest()

    def _compute_automation_rule_id(self, rule_name: str) -> str:
        return hashlib.sha1(rule_name.encode()).hexdigest()

    async def inject_macros(
        self, query: str, rule_name: str
    ) -> microsoft_sentinel_models.MacroInjectionResult:
        macro_service = MicrosoftSentinelMacroService()

        for macro_name in macro_service.get_used_macros(query=query):
            try:
                macro = self._kubernetes_client.get_namespaced_custom_object(
                    group="buildrlabs.io",
                    version="v1",
                    namespace=self._namespace,
                    plural="microsoftsentinelmacros",
                    name=macro_name,
                    return_type=crd_models.MicrosoftSentinelMacro,
                )
                query = macro_service.replace_macro(
                    text=query, macro_name=macro_name, replacement=macro.spec.content
                )
            except kubernetes_exceptions.ResourceNotFoundException:
                error_message = (
                    f"The macro '{macro_name}' is referenced in '{rule_name}', "
                    "but is not deployed in the Tenant namespace."
                )
                self._logger.error(error_message)
                return microsoft_sentinel_models.MacroInjectionResult(
                    success=False, query=query, message=error_message
                )

        return microsoft_sentinel_models.MacroInjectionResult(success=True, query=query)

    async def create_or_update_analytics_rule(
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

        # Support optional query prefix
        if payload.properties.query_prefix:
            payload.properties.query = (
                f"{payload.properties.query_prefix} {payload.properties.query}"
            )

        # Support optional query suffix
        if payload.properties.query_suffix:
            payload.properties.query = (
                f"{payload.properties.query} {payload.properties.query_suffix} "
            )

        await self._repository.create_or_update_scheduled_alert_rule(
            payload=payload, analytic_rule_id=analytic_rule_id
        )

    async def create_or_update_automation_rule(self, rule_name: str, payload: dict):
        """
        Create (or update) an automation rule upstream

        Args:
            payload(...): A valid ... object
        """
        automation_rule_id = self._compute_automation_rule_id(rule_name=rule_name)
        await self._repository.create_or_update_automation_rule(
            payload=payload, automation_rule_id=automation_rule_id
        )

    async def remove_analytics_rule(self, rule_name: str):
        analytic_rule_id = self._compute_analytics_rule_id(rule_name=rule_name)
        await self._repository.remove_scheduled_alert_rule(
            analytic_rule_id=analytic_rule_id
        )

    async def analytics_rule_status(
        self, analytic_rule_id: str
    ) -> microsoft_sentinel_models.AnalyticsRuleStatus:
        """
        Checks the status of a given Detection Rule upstream

        Args:
            rule_id(str): The ID of the upstream rule
        """
        rule = await self._repository.get_analytics_rule(
            analytic_rule_id=analytic_rule_id
        )
        deployed = rule is not None

        enabled = False
        if deployed:
            enabled = rule["properties"]["enabled"]

        rule_type = "Unknown"
        if deployed:
            rule_type = rule["kind"]

        return microsoft_sentinel_models.AnalyticsRuleStatus(
            deployed=deployed, enabled=enabled, rule_type=rule_type
        )
