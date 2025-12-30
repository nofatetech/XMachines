import time
import os
import logging
from dotenv import load_dotenv

from machine.core.service import AbstractService
from machine.core.state import MachineState
from machine.core.lifecycle import Lifecycle
from machine.utils.coordinator_client import send_heartbeat

# Load environment variables (ensure this is done at the application entry point, but keep here for standalone testing)
load_dotenv()

class HeartbeatService(AbstractService):
    def __init__(self, state: MachineState):
        super().__init__(state)
        self.log = logging.getLogger(self.__class__.__name__)

    def _run(self):
        self.log.info("Heartbeat Service starting.")
        while self._running and self.state.lifecycle != Lifecycle.SHUTDOWN:
            send_heartbeat(self.state.machine_id, self.state.lifecycle.value)
            time.sleep(1) # Send heartbeat every second
        self.log.info("Heartbeat Service shut down.")
