from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal, Union, Dict, Any
from enum import Enum
import uuid
import datetime

class MachineState(str, Enum):
    OFFLINE = "OFFLINE"
    CONNECTING = "CONNECTING"
    IDLE = "IDLE"
    ACTIVE = "ACTIVE"
    ERROR = "ERROR"

class MessageEnvelope(BaseModel):
    type: Literal["state", "command", "event"]
    machine_id: str
    ts: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    seq: int
    payload: Dict[str, Any]

class CommandPayload(BaseModel):
    cmd_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    params: Dict[str, Any]

class StatePayload(BaseModel):
    status: MachineState
    battery_level: float | None = None
    speed: float | None = None
    position: Dict[str, float] | None = None

class EventPayload(BaseModel):
    event_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    severity: Literal["info", "warn", "error"]
    name: str
    details: Dict[str, Any]

class CommandMessage(MessageEnvelope):
    type: Literal["command"] = "command"
    payload: CommandPayload

class StateMessage(MessageEnvelope):
    type: Literal["state"] = "state"
    payload: StatePayload

class EventMessage(MessageEnvelope):
    type: Literal["event"] = "event"
    payload: EventPayload

Message = Union[CommandMessage, StateMessage, EventMessage]
