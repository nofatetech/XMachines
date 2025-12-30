import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request
import uvicorn

from machine.core.service import AbstractService
from machine.core.state import MachineState
from machine.core.lifecycle import Lifecycle

# Load environment variables (ensure this is done at the application entry point, but keep here for standalone testing)
load_dotenv()

class APIService(AbstractService):
    def __init__(self, state: MachineState):
        super().__init__(state)
        self.app = FastAPI()
        self._configure_routes()
        self.server = None

    def _configure_routes(self):
        @self.app.get("/state")
        def get_state(request: Request):
            self.log.info(f"Received GET /state request from {request.client.host}")
            return {
                "id": self.state.machine_id,
                "lifecycle": self.state.lifecycle.value,
                "mode": self.state.mode,
            }

        @self.app.post("/activate")
        def activate(request: Request):
            self.log.info(f"Received POST /activate request from {request.client.host}")
            self.state.lifecycle = Lifecycle.ACTIVE
            return {"status": "activated"}

        @self.app.post("/shutdown")
        def shutdown(request: Request):
            self.log.info(f"Received POST /shutdown request from {request.client.host}")
            self.state.lifecycle = Lifecycle.SHUTDOWN
            return {"status": "shutdown"}

        @self.app.post("/mode")
        def set_mode(new_mode: dict, request: Request):
            self.log.info(f"Received POST /mode request from {request.client.host}")
            mode_value = new_mode.get("mode")
            if mode_value not in ["manual", "autonomous"]:
                self.log.warning(f"Invalid mode \'{mode_value}\' received from {request.client.host}")
                return {"error": "Invalid mode. Must be \'manual\' or \'autonomous\'."}, 400
            self.state.mode = mode_value
            self.log.info(f"Mode set to \'{self.state.mode}\'")
            return {"status": f"mode set to {self.state.mode}"}

    def _run(self):
        api_host = os.getenv("MACHINE_API_HOST", "0.0.0.0")
        api_port = int(os.getenv("MACHINE_API_PORT", 8001))
        self.log.info(f"API Service starting on {api_host}:{api_port}")
        
        # Uvicorn expects the app instance directly, not an instance of APIService
        # So we pass self.app, which is the FastAPI instance
        uvicorn_config = uvicorn.Config(self.app, host=api_host, port=api_port, log_level="warning")
        self.server = uvicorn.Server(uvicorn_config)
        
        # This call blocks until the server stops
        self.server.run()
        self.log.info("API Service shut down.")

    def stop(self):
        if self.server:
            self.log.info("Shutting down Uvicorn server...")
            # Uvicorn's shutdown is asynchronous, trigger it and then call super().stop()
            # to manage the thread state.
            self.server.should_exit = True
        super().stop()
