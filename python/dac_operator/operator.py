import kopf

from dac_operator.handlers import (
    microsoft_sentinel_timer_handlers,
    microsoft_sentinel_validation_handlers,
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
