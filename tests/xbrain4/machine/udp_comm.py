import socket
import json
import time

class UDPServer:
    def __init__(self, state, motor, port=9999):
        self.state = state
        self.motor = motor
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", port))
        self.sock.setblocking(False)

    def poll(self):
        try:
            data, _ = self.sock.recvfrom(1024)
            msg = json.loads(data.decode())

            linear = float(msg.get("linear", 0.0))
            angular = float(msg.get("angular", 0.0))

            self.state.update_command_timestamp()
            self.motor.drive(linear, angular)

        except BlockingIOError:
            pass

    def watchdog(self, timeout=0.5):
        if time.time() - self.state.last_command_ts > timeout:
            self.motor.drive(0.0, 0.0)
