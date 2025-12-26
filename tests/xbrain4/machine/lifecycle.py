from enum import Enum

class Lifecycle(Enum):
    BOOT = "boot"
    IDLE = "idle"
    ACTIVE = "active"
    ERROR = "error"
    SHUTDOWN = "shutdown"
