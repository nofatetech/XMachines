import time
import json
import socket
import logging
from state import MachineState
from motor import AbstractMotorController
from arm import AbstractArmController

class UDPServer:
    def __init__(self, state: MachineState, motor_controller: AbstractMotorController, arm_controller: AbstractArmController):
        self.state = state
        self.motor = motor_controller
        self.arm = arm_controller
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        port = int(os.getenv("MACHINE_UDP_PORT", 9999))
        self.sock.bind(("0.0.0.0", port))
        self.sock.setblocking(False)
        self.last_command_ts = 0.0
        self.watchdog_timeout = 1.0 # seconds

    def poll(self):
        """Poll for incoming UDP messages."""
        try:
            data, addr = self.sock.recvfrom(1024)
            logging.info(f"Received UDP message from {addr}: {data.decode()}")
            self.last_command_ts = time.time()
            message = json.loads(data.decode())
            
            # Check for drive commands
            if "drive" in message:
                drive_cmd = message["drive"]
                if "linear" in drive_cmd and "angular" in drive_cmd:
                    self.motor.drive(drive_cmd["linear"], drive_cmd["angular"])

            # Check for arm commands
            if "arm_target" in message:
                arm_cmd = message["arm_target"]
                if "joint1" in arm_cmd and "joint2" in arm_cmd and "clamp" in arm_cmd:
                    self.arm.set_pose(arm_cmd["joint1"], arm_cmd["joint2"], arm_cmd["clamp"])

        except BlockingIOError:
            # No data received
            pass
        except json.JSONDecodeError:
            logging.warning("Received invalid JSON in UDP message.")
        except Exception as e:
            logging.error(f"An unexpected error occurred in UDP poll: {e}")

    def watchdog(self, timeout=0.5):
        if time.time() - self.state.last_command_ts > timeout:
            self.motor.drive(0.0, 0.0)
