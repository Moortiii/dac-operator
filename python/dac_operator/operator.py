import kopf

from dac_operator.handlers.microsoft_sentinel.analytic_rules import (
    analytic_rule_timers as analytic_rule_timers,
)
from dac_operator.handlers.microsoft_sentinel.automation_rules import (
    automation_rule_timers as automation_rule_timers,
)
from dac_operator.handlers.microsoft_sentinel.automation_rules import (
    automation_rule_validators as automation_rule_validators,
)


@kopf.on.startup()  # type: ignore
def configure(settings: kopf.OperatorSettings, **_):
    settings.admission.server = kopf.WebhookServer(
        addr="0.0.0.0",
        port=443,
        cafile="/certs/ca.crt",
        certfile="/certs/tls.crt",
        pkeyfile="/certs/tls.key",
    )
