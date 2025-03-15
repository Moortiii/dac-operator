import json
import os

import jsonschema
import kopf
from loguru import logger


@kopf.on.validate(
    "microsoftsentinelautomationrules",
    operations=["CREATE", "UPDATE"],
    id="validate-automation-rule",  # This becomes the exposed validation path!
)  # type: ignore
async def validate_automation_rule(spec, warnings, **_):
    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

    print(ROOT_PATH)
    with open(
        f"{ROOT_PATH}/../assets/jsonschema/MicrosoftSentinelAutomationRule.json"
    ) as f:
        schema = json.load(f)

    try:
        jsonschema.validate({"properties": spec["properties"]}, schema=schema)
    except jsonschema.SchemaError as err:
        logger.error(str(err))
        raise kopf.AdmissionError("The JSON-schema for Automation Rules is invalid")
    except jsonschema.ValidationError as err:
        logger.error(str(err))
        raise kopf.AdmissionError(
            f"Automation Rule specification did not pass validation:\n\n {err}"
        )
