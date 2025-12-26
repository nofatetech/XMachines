import socket
import json
import time
import os
import logging

class UDPServer:
    def __init__(self, state, motor, port=None):
        self.state = state
        self.motor = motor
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if port is None:
            port = int(os.getenv("MACHINE_UDP_PORT", 9999))
        self.sock.bind(("0.0.0.0", port))
        self.sock.setblocking(False)

    def poll(self):
        """Poll for incoming UDP messages."""
        try:
            data, addr = self.sock.recvfrom(1024)
            logging.info(f"Received UDP message from {addr}: {data.decode()}")
            self.last_command_ts = time.time()
            message = json.loads(data.decode())
            
            # Basic validation
            if "linear" in message and "angular" in message:
                self.motor.drive(message["linear"], message["angular"])

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
