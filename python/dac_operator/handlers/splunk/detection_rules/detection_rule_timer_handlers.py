import kopf
from kubernetes import client as kubernetes_client

from dac_operator import providers
from dac_operator.splunk.splunk_models import SplunkDetectionRule

DETECTION_RULE_SYNC_INTERVAL = 500


@kopf.on.timer("splunkdetectionrules", interval=DETECTION_RULE_SYNC_INTERVAL)  # type: ignore
async def create_splunk_detection_rule(spec, **kwargs):
    namespace = kwargs["namespace"]

    splunk_service = providers.get_splunk_service(
        namespace=namespace,
        kubernetes_client=providers.get_kubernetes_client(
            core_api=kubernetes_client.CoreV1Api(),
            custom_objects_api=kubernetes_client.CustomObjectsApi(),
        ),
    )

    if splunk_service is None:
        return

    await splunk_service.create_or_update_detection_rule(
        SplunkDetectionRule.model_validate(spec)
    )
