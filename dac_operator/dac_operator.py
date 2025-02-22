import uuid

import kopf

from dac_operator import providers
from dac_operator.microsoft_sentinel import microsoft_sentinel_models

microsoft_sentinel_service = providers.get_microsoft_sentinel_service()


@kopf.timer("microsoftsentineldetectionrules", interval=5.0)
async def create_detection_rule(spec, **kwargs):
    await microsoft_sentinel_service.create(
        payload=microsoft_sentinel_models.CreateScheduledAlertRule(
            etag=uuid.uuid4().hex,
            properties=microsoft_sentinel_models.ScheduledAlertRuleProperties(
                displayName=spec["name"],
                enabled=spec.get("enabled", True),
                description=spec.get("description", ""),
                query=spec["query"],
                query_frequency=spec.get("queryFrequency", "P15H"),
                query_period=spec.get("queryPeriod", "P15H")
                severity=spec.get("severity", "Informational"),
                trigger_operator=spec["triggerOperator"],
                custom_details="",
            ),
        )
    )
    print(spec.get("name"))
    pass
