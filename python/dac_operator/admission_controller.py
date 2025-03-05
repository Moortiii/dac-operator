import json
import os

import jsonschema
import kopf

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


@kopf.on.startup()  # type: ignore
def configure(settings: kopf.OperatorSettings, **_):
    # Assuming that the configuration is done manually:
    settings.admission.server = kopf.WebhookMinikubeServer()
    settings.admission.managed = "auto.kopf.dev"


@kopf.on.validate("microsoftsentinelautomationrules", operations=["CREATE", "UPDATE"])  # type: ignore
async def validate_automation_rule(spec, warnings, **_):
    def get_json_schema():
        with open(
            f"{ROOT_PATH}/assets/jsonschema/MicrosoftSentinelAutomationRule.json"
        ) as f:
            schema = json.load(f)

        return schema

    try:
        jsonschema.validate(
            {"properties": spec["properties"]}, schema=get_json_schema()
        )
    except jsonschema.SchemaError as err:
        print(f"Invalid JSON schema: {err}")
        raise kopf.AdmissionError("Schema for resource type is invalid")
    except jsonschema.ValidationError as err:
        print(f"Resource did not pass validation: {err}")
        raise kopf.AdmissionError("Resource does not comply with enforced schema.")
