import time
import json
import socket
import logging
import os
import threading

from machine.core.node import AbstractNode
from machine.state import MachineState
from machine.nodes.tank_motor import AbstractTankMotorController
from machine.nodes.robotic_arm import AbstractRoboticArmController


class UDPServer(AbstractNode):
    def __init__(self, state: MachineState):
        super().__init__(state)
        self.log = logging.getLogger(self.__class__.__name__)
        self.command_handlers = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        port = int(os.getenv("MACHINE_UDP_PORT", 9999))
        self.sock.bind(("0.0.0.0", port))
        self.sock.setblocking(False)
        self.last_command_ts = 0.0
        self.watchdog_timeout = 1.0 # seconds
        self._running = False
        self._thread = None

    def register_command(self, command: str, handler):
        self.log.info(f"Registering command '{command}' to handler {handler.__name__}")
        self.command_handlers[command] = handler

    def _udp_loop(self):
        while self._running and self.state.lifecycle != self.state.lifecycle.SHUTDOWN:
            self._poll_and_watchdog()
            time.sleep(0.01) # Small sleep to prevent busy-waiting

    def start(self):
        if not self._running:
            self.log.info("UDP Server starting.")
            self._running = True
            self._thread = threading.Thread(target=self._udp_loop, daemon=True)
            self._thread.start()
        else:
            self.log.warning("UDP Server is already running.")

    def update(self):
        # The main update loop for a node.
        # For UDP server, its primary function (polling) runs in its own thread.
        # This method could be used for other periodic checks if needed, but for now,
        # the _udp_loop handles the continuous operation.
        pass

    def stop(self):
        if self._running:
            self.log.info("UDP Server stopping.")
            self._running = False
            if self._thread and self._thread.is_alive():
                self._thread.join(timeout=1.0) # Wait for thread to finish
            self.sock.close()
            self.log.info("UDP Server stopped.")
        else:
            self.log.warning("UDP Server is not running.")
    
    def _poll_and_watchdog(self):
        # Call the existing poll and watchdog logic
        self.poll()
        self.watchdog()

    def poll(self):
        """Poll for incoming UDP messages."""
        try:
            data, addr = self.sock.recvfrom(1024)
            self.log.debug(f"Received UDP message from {addr}: {data.decode()}")
            self.last_command_ts = time.time()
            message = json.loads(data.decode())
            
            for command, payload in message.items():
                if command in self.command_handlers:
                    self.command_handlers[command](**payload)
                else:
                    self.log.warning(f"Received unknown command: {command}")

        except BlockingIOError:
            # No data received
            pass
        except json.JSONDecodeError:
            logging.warning("Received invalid JSON in UDP message.")
        except Exception as e:
            logging.error(f"An unexpected error occurred in UDP poll: {e}")

    def watchdog(self, timeout=0.5):
        if time.time() - self.last_command_ts > timeout:
            if 'drive' in self.command_handlers:
                # Assuming the drive handler is a method of a node that has a stop method.
                # This is a bit of a hack, a better solution would be to have a more generic
                -                # way to stop all nodes.
                self.command_handlers['drive'].__self__.stop()
