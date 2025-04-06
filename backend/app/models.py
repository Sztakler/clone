from pydantic import BaseModel, Field
from typing import Annotated
from enum import Enum
from dataclasses import dataclass

class RobotStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    OFFLINE = "offline"
    ERROR = "error"

class RobotAction(str, Enum):
    ON = "on"
    OFF = "off"
    RESET = "reset"

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
    fan_mode: FanMode
   
