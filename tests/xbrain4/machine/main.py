import time
import threading
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
import uvicorn
import logging

# Load environment variables first
load_dotenv()

# Setup logging before importing other modules that might log
from logging_config import setup_logging
setup_logging()

from state import MachineState
from lifecycle import Lifecycle
from motor import SimulatedTankMotorController, DCTankMotorController, StepperTankMotorController, NullMotorController, AbstractMotorController
from arm import SimulatedArmController, GPIOArmController, AbstractArmController as AbstractArmController
from udp_comm import UDPServer
from coordinator_client import send_heartbeat
# from tui import MachineTUI


def create_motor_controller(state: MachineState) -> AbstractMotorController:
    """Factory function to create the appropriate motor controller based on configuration."""
    # Default to 'simulation' for safety and ease of use.
    controller_type = os.getenv("MOTOR_CONTROLLER", "simulation").lower()
    
    if controller_type == "simulation":
        logging.info("🕹️  [MAIN] Using SimulatedTankMotorController.")
        return SimulatedTankMotorController(state)
    elif controller_type == "dc":
        logging.info("🤖 [MAIN] Using DC Motor Controller (via GPIO).")
        return DCTankMotorController(state)
    elif controller_type == "stepper":
        logging.info("⚙️ [MAIN] Using StepperTankMotorController.")
        return StepperTankMotorController(state)
    elif controller_type == "none":
        logging.info("💨 [MAIN] Using NullMotorController.")
        return NullMotorController(state)
    else:
        raise ValueError(f"Invalid MOTOR_CONTROLLER type: {controller_type}")

def create_arm_controller(state: MachineState) -> AbstractArmController:
    """Factory function to create the appropriate arm controller."""
    controller_type = os.getenv("ARM_CONTROLLER", "simulation").lower()

    if controller_type == "simulation":
        logging.info("🦾 [MAIN] Using SimulatedArmController.")
        return SimulatedArmController(state)
    elif controller_type == "gpio":
        logging.info("🦾 [MAIN] Using GPIOArmController.")
        return GPIOArmController(state)
    else:
        raise ValueError(f"Invalid ARM_CONTROLLER type: {controller_type}")

# --- API Setup ---
app = FastAPI()

@app.get("/state")
def get_state(request: Request):
    logging.info(f"Received GET /state request from {request.client.host}")
    # This needs to access the global state object
    return {
        "id": state.machine_id,
        "lifecycle": state.lifecycle.value,
        "mode": state.mode,
    }

@app.post("/activate")
def activate(request: Request):
    logging.info(f"Received POST /activate request from {request.client.host}")
    state.lifecycle = Lifecycle.ACTIVE
    return {"status": "activated"}

@app.post("/shutdown")
def shutdown(request: Request):
    logging.info(f"Received POST /shutdown request from {request.client.host}")
    state.lifecycle = Lifecycle.SHUTDOWN
    return {"status": "shutdown"}

@app.post("/mode")
def set_mode(new_mode: dict, request: Request):
    logging.info(f"Received POST /mode request from {request.client.host}")
    mode_value = new_mode.get("mode")
    if mode_value not in ["manual", "autonomous"]:
        logging.warning(f"Invalid mode '{mode_value}' received from {request.client.host}")
        return {"error": "Invalid mode. Must be 'manual' or 'autonomous'."}, 400
    state.mode = mode_value
    logging.info(f"Mode set to '{state.mode}'")
    return {"status": f"mode set to {state.mode}"}

# --- Background Tasks ---
def udp_loop():
    while state.lifecycle != Lifecycle.SHUTDOWN:
        udp.poll()
        udp.watchdog()
        time.sleep(0.01)

def heartbeat_loop():
    while state.lifecycle != Lifecycle.SHUTDOWN:
        send_heartbeat(state.machine_id, state.lifecycle)
        time.sleep(1)

# --- Main Execution ---
if __name__ == "__main__":
    # --- Initialization ---
    machine_id = os.getenv("MACHINE_ID", "machine-001")
    state = MachineState(machine_id=machine_id)
    motor = create_motor_controller(state)
    arm = create_arm_controller(state)
    udp = UDPServer(state, motor, arm)

    state.lifecycle = Lifecycle.IDLE

    # Start background threads
    threading.Thread(target=udp_loop, daemon=True).start()
    threading.Thread(target=heartbeat_loop, daemon=True).start()

    # Start Uvicorn in a background thread
    api_host = os.getenv("MACHINE_API_HOST", "0.0.0.0")
    api_port = int(os.getenv("MACHINE_API_PORT", 8001))
    
    uvicorn_config = uvicorn.Config(app, host=api_host, port=api_port)
    server = uvicorn.Server(uvicorn_config)
    threading.Thread(target=server.run, daemon=True).start()

    logging.info("Application started. Press Ctrl+C to shut down.")

    # Keep the main thread alive until shutdown
    try:
        while state.lifecycle != Lifecycle.SHUTDOWN:
            time.sleep(0.5)
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt received. Shutting down...")
    finally:
        state.lifecycle = Lifecycle.SHUTDOWN
        logging.info("Application shutting down.")
