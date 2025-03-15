import kopf


@kopf.on.timer("splunkdetectionrules")  # type: ignore
async def create_splunk_detection_rule(spec, **kwargs):
    namespace = kwargs["namespace"]
    rule_name = kwargs["name"]
    print(spec)
