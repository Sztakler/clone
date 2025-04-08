from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Annotated, Optional
from enum import Enum
from dataclasses import dataclass
from fastapi import HTTPException

class RobotStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    OFFLINE = "offline"
    ERROR = "error"

class RobotAction(str, Enum):
    ON = "on"
    OFF = "off"
    RESET = "reset"
    FAN = "fan"
    FAN_SPEED = "fan_speed"

class FanMode(str, Enum):
    PROPORTIONAL = "proportional"
    STATIC = "static"

class RobotState(BaseModel):
    temperature: Annotated[float, Field(ge=-100, le=500)]
    power: Annotated[float, Field(ge=0, le=100)] | None
    status: RobotStatus
    fan_speed: Annotated[int, Field(ge=0, le=100)]
    uptime: Annotated[int, Field(ge=0, le=2**32 - 1)]
    logs: list[str]

class RobotControlCommand(BaseModel):
    action: RobotAction
    fan_mode: Optional[FanMode] = None
    fan_speed: Optional[int] = None

    @model_validator(mode="after")
    def check_fan_mode_required(self):
        if self.action == RobotAction.FAN and self.fan_mode is None:
            raise HTTPException(status_code=422,
                                detail="fan_mode is required when action is FAN")
        if self.action == RobotAction.FAN_SPEED and self.fan_speed is None:
            raise HTTPException(status_code=422, detail="fan_speed is required when action is FAN_SPEED")
        return self
