from typing import Literal

from pydantic import BaseModel, Field

TriggerOn = Literal["Incidents", "Alerts"]
TriggerWhen = Literal["Created"]


class AddIncidentTaskActionProperties(BaseModel):
    description: str
    title: str


class AutomationRuleAddIncidentTaskAction(BaseModel):
    action_configuration: AddIncidentTaskActionProperties = Field(
        ..., alias="actionConfiguration"
    )
    action_type: Literal["Add Incident Task"] = "Add Incident Task"
    order: int


class AutomationRuleBooleanCondition(BaseModel): ...


class AutomationRuleConditions(BaseModel): ...


class AutomationRuleTriggeringLogic(BaseModel):
    enabled: bool = Field(..., alias="isEnabled")
    triggers_on: TriggerOn = Field(..., alias="triggersOn")
    triggers_when: TriggerWhen = Field(..., alias="triggersWhen")


class AutomationRuleProperties(BaseModel):
    display_name: str = Field(..., alias="displayName")
    order: int
    triggering_logic: AutomationRuleTriggeringLogic


class CreateAutomationRule(BaseModel):
    id: str
    name: str
    type: str
    properties: AutomationRuleProperties
