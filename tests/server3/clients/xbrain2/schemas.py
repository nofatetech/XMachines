from pydantic import BaseModel
from typing import Optional

class MotorControl(BaseModel):
    left: int = 0    # -100 to 100
    right: int = 0

class LightsControl(BaseModel):
    lights_on: bool = False
    fog_lights_on: bool = False

class MachineStatus(BaseModel):
    uuid: str
    name: str
    is_online: bool
    motor_left_speed: int
    motor_right_speed: int
    lights_on: bool
    fog_lights_on: bool
    happiness: int
    hunger: int
    temperature: Optional[float] = None