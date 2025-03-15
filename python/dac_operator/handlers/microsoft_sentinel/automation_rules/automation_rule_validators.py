import json

import jsonschema
import kopf
from loguru import logger

from dac_operator.config import ROOT_PATH


@kopf.on.validate(
    "microsoftsentinelautomationrules",
    operations=["CREATE", "UPDATE"],
    id="validate-automation-rule",
)  # type: ignore
async def validate_automation_rule(spec, warnings, **_):
    with open(
        f"{ROOT_PATH}/assets/jsonschema/MicrosoftSentinelAutomationRule.json"
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
