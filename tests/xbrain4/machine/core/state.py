import time
from .lifecycle import Lifecycle

class MachineState:
    def __init__(self, machine_id: str):
        self.machine_id = machine_id
        self.lifecycle = Lifecycle.BOOT
        self.last_command_ts = 0.0
        self.mode = "manual"  # manual | autonomous
        self.telemetry = {}
        self.arm_state = {
            "joint1": 0, # Angle in degrees
            "joint2": 0, # Angle in degrees
            "clamp": 0   # 0=closed, 1=open
        }

    def update_command_timestamp(self):
        self.last_command_ts = time.time()
