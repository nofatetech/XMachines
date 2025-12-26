import time
import threading
import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

load_dotenv()


from state import MachineState
from lifecycle import Lifecycle
from motor import SimulatedTankMotorController, GPIOTankMotorController, NullMotorController, AbstractMotorController
from udp_comm import UDPServer
from coordinator_client import send_heartbeat

def create_motor_controller(state: MachineState) -> AbstractMotorController:
    """Factory function to create the appropriate motor controller based on configuration."""
    controller_type = os.getenv("MOTOR_CONTROLLER", "simulation").lower()
    
    if controller_type == "simulation":
        print("[MAIN] Using SimulatedTankMotorController.")
        return SimulatedTankMotorController(state)
    elif controller_type == "gpio":
        print("[MAIN] Using GPIOTankMotorController.")
        return GPIOTankMotorController(state)
    elif controller_type == "none":
        print("[MAIN] Using NullMotorController.")
        return NullMotorController(state)
    else:
        raise ValueError(f"Invalid MOTOR_CONTROLLER type: {controller_type}")

# --- Initialization ---
machine_id = os.getenv("MACHINE_ID", "machine-001")
state = MachineState(machine_id=machine_id)
motor = create_motor_controller(state)
udp = UDPServer(state, motor)

app = FastAPI()

@app.get("/state")
def get_state():
    return {
        "id": state.machine_id,
        "lifecycle": state.lifecycle.value,
        "mode": state.mode,
    }

@app.post("/activate")
def activate():
    state.lifecycle = Lifecycle.ACTIVE
    return {"status": "activated"}

@app.post("/shutdown")
def shutdown():
    state.lifecycle = Lifecycle.SHUTDOWN
    return {"status": "shutdown"}

@app.post("/mode")
def set_mode(new_mode: dict):
    mode_value = new_mode.get("mode")
    if mode_value not in ["manual", "autonomous"]:
        return {"error": "Invalid mode. Must be 'manual' or 'autonomous'."}, 400
    state.mode = mode_value
    return {"status": f"mode set to {state.mode}"}

def udp_loop():
    while state.lifecycle != Lifecycle.SHUTDOWN:
        udp.poll()
        udp.watchdog()
        time.sleep(0.01)

def heartbeat_loop():
    while state.lifecycle != Lifecycle.SHUTDOWN:
        send_heartbeat(state.machine_id, state.lifecycle)
        time.sleep(1)

if __name__ == "__main__":
    state.lifecycle = Lifecycle.IDLE

    threading.Thread(target=udp_loop, daemon=True).start()
    threading.Thread(target=heartbeat_loop, daemon=True).start()

    api_host = os.getenv("MACHINE_API_HOST", "0.0.0.0")
    api_port = int(os.getenv("MACHINE_API_PORT", 8001))
    uvicorn.run(app, host=api_host, port=api_port)
